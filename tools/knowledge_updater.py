#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
knowledge_updater.py — self-improving knowledge pipeline for `investment-portfolio-analyzer` (idea #75).

Crawls authoritative Finance, Investment & Insurance sources with ArXiv API + web search integration,
scores entries by recency and domain relevance, and appends new, de-duplicated entries to
SECOND-KNOWLEDGE-BRAIN.md.

Schedule: weekly (cron). Cluster: finance-insurance.

Usage:
    python tools/knowledge_updater.py [--dry-run] [--max-results N]
"""

import os
import re
import json
import hashlib
import datetime
import argparse
import urllib.request
import urllib.parse
import time
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from pathlib import Path

# Configuration
BRAIN_FILE = Path(__file__).parent.parent / "SECOND-KNOWLEDGE-BRAIN.md"
ARXIV_CATEGORIES = ['q-fin.PM', 'q-fin.RM']
SEARCH_QUERIES = [
    'portfolio optimization risk parity',
    'asset allocation diversification',
    'sharpe ratio risk management',
    'modern portfolio theory markowitz',
    'capm systematic risk',
    'monte carlo portfolio simulation',
    'fama french factors',
    'correlation matrix portfolio'
]
DOMAIN_SOURCES = [
    'CFA Institute curriculum & research',
    'Morningstar methodology',
    'arXiv q-fin (portfolio, risk)',
    'SSRN finance working papers',
    'Vanguard asset-allocation research',
    'BlackRock investment research'
]
DOMAIN_KEYWORDS = [
    'portfolio', 'asset', 'sharpe', 'sortino', 'alpha', 'beta',
    'correlation', 'covariance', 'variance', 'volatility',
    'allocation', 'diversification', 'concentration',
    'risk', 'return', 'performance', 'benchmark'
]
ARXIV_BASE_URL = "http://export.arxiv.org/api/query?"

# Evidence tier weights for scoring
EVIDENCE_TIERS = {
    'systematic_review': 3.0,
    'meta_analysis': 2.8,
    'rct': 2.5,
    'cohort_study': 2.0,
    'expert_consensus': 1.5,
    'industry_standard': 1.8,
    'academic': 2.2,
    'blog': 0.5,
    'news': 0.8
}


@dataclass
class KnowledgeEntry:
    """Structured knowledge entry with metadata."""
    title: str
    authors: str
    year: str
    venue: str
    url: str
    abstract: str = ""
    key_finding: str = ""
    evidence_tier: str = ""
    relevance_score: float = 0.0
    entry_hash: str = ""

    def __post_init__(self):
        if not self.entry_hash:
            self.entry_hash = self._compute_hash()

    def _compute_hash(self) -> str:
        """Compute hash for deduplication."""
        content = f"{self.url}|{self.title}".lower().strip()
        return hashlib.sha256(content.encode()).hexdigest()[:12]

    def to_markdown_row(self) -> str:
        """Format as markdown table row."""
        title_truncated = self.title[:80]
        authors_truncated = self.authors[:40]
        return (f"| {title_truncated} | {authors_truncated} | {self.year} "
                f"| {self.venue} | {self.url} | Score: {self.relevance_score:.1f} "
                f"| <!--h:{self.entry_hash}-->")

    def to_markdown_detail(self) -> str:
        """Format as detailed entry."""
        return f"""
### {self.title}
**Authors**: {self.authors}
**Year**: {self.year}
**Venue**: {self.venue}
**URL**: {self.url}
**Relevance Score**: {self.relevance_score:.1f}
**Entry Hash**: {self.entry_hash}

**Key Finding**: {self.key_finding or self.abstract[:200]}

**Evidence Tier**: {self.evidence_tier}

---
"""


class ArXivFetcher:
    """Fetch papers from ArXiv API."""

    def __init__(self, categories: List[str], max_results: int = 25):
        self.categories = categories
        self.max_results = max_results
        self.entries: List[KnowledgeEntry] = []

    def fetch(self) -> List[KnowledgeEntry]:
        """Fetch papers from all configured categories."""
        all_entries = []

        for category in self.categories:
            try:
                entries = self._fetch_category(category)
                all_entries.extend(entries)
                time.sleep(1)  # Rate limiting
            except Exception as e:
                print(f"[ArXiv] Failed to fetch {category}: {e}")

        self.entries = all_entries
        return all_entries

    def _fetch_category(self, category: str) -> List[KnowledgeEntry]:
        """Fetch papers from a single ArXiv category."""
        params = urllib.parse.urlencode({
            "search_query": f"cat:{category}",
            "sortBy": "submittedDate",
            "sortOrder": "descending",
            "max_results": self.max_results,
        })
        url = f"{ARXIV_BASE_URL}{params}"

        try:
            with urllib.request.urlopen(url, timeout=30) as response:
                raw = response.read().decode("utf-8", "ignore")
        except Exception as e:
            print(f"[ArXiv] HTTP error for {category}: {e}")
            return []

        return self._parse_arxiv_response(raw, category)

    def _parse_arxiv_response(self, raw: str, category: str) -> List[KnowledgeEntry]:
        """Parse ArXiv API response into KnowledgeEntry objects."""
        entries = []

        for match in re.finditer(r"<entry>(.*?)</entry>", raw, re.DOTALL):
            entry_block = match.group(1)

            def extract_tag(tag_name: str) -> str:
                tag_match = re.search(rf"<{tag_name}>(.*?)</{tag_name}>", entry_block, re.DOTALL)
                if tag_match:
                    return re.sub(r"\s+", " ", tag_match.group(1)).strip()
                return ""

            title = extract_tag("title")
            authors = extract_tag("name")
            published = extract_tag("published")
            year = published[:4] if published else "Unknown"
            url = extract_tag("id")
            abstract = extract_tag("summary")

            if not title or not url:
                continue

            entry = KnowledgeEntry(
                title=title,
                authors=authors,
                year=year,
                venue=f"arXiv:{category}",
                url=url,
                abstract=abstract,
                key_finding=abstract[:300] if abstract else "",
                evidence_tier="academic"
            )
            entries.append(entry)

        return entries


class WebSearchSimulator:
    """
    Simulate web search results for integration with Claude Code WebSearch.

    In production within Claude Code, this would be replaced by actual WebSearch tool calls.
    For standalone execution, we provide a placeholder that can be extended.
    """

    def __init__(self, queries: List[str]):
        self.queries = queries

    def search(self) -> List[Dict[str, Any]]:
        """
        Simulate web search results.

        Returns list of search result dictionaries with keys:
        - title, url, snippet, source, date
        """
        results = []

        for query in self.queries:
            print(f"[WebSearch] Searching for: {query}")

            # Placeholder: In Claude Code, this would call WebSearch tool
            # For now, return empty to indicate integration point
            # Real implementation would:
            # 1. Call WebSearch with query
            # 2. Parse results
            # 3. Extract metadata (title, url, snippet, source)
            # 4. Return structured data

            print(f"[WebSearch] Integration point: Would call WebSearch for '{query}'")

        return results

    def results_to_entries(self, results: List[Dict[str, Any]]) -> List[KnowledgeEntry]:
        """Convert web search results to KnowledgeEntry objects."""
        entries = []

        for result in results:
            entry = KnowledgeEntry(
                title=result.get('title', ''),
                authors=result.get('source', 'Unknown Author'),
                year=str(result.get('date', {}).get('year', '2026')),
                venue='Web Source',
                url=result.get('url', ''),
                abstract=result.get('snippet', ''),
                key_finding=result.get('snippet', ''),
                evidence_tier=self._classify_evidence_tier(result)
            )
            entries.append(entry)

        return entries

    def _classify_evidence_tier(self, result: Dict[str, Any]) -> str:
        """Classify evidence tier based on source domain."""
        url = result.get('url', '').lower()
        source = result.get('source', '').lower()

        # High-quality sources
        if any(domain in url for domain in ['cfainstitute.org', 'morningstar.com', 'ssrn.com']):
            return 'industry_standard'
        if any(domain in url for domain in ['vanguard.com', 'blackrock.com']):
            return 'industry_standard'
        if 'arxiv.org' in url or 'ssrn.com' in url:
            return 'academic'

        # Medium quality
        if any(domain in url for domain in ['investopedia.com', 'morningstar.com']):
            return 'expert_consensus'

        # Lower quality
        return 'blog'


class EntryScorer:
    """Score knowledge entries by relevance and recency."""

    def __init__(self, domain_keywords: List[str], current_year: int = None):
        self.domain_keywords = [k.lower() for k in domain_keywords]
        self.current_year = current_year or datetime.date.today().year

    def score_entry(self, entry: KnowledgeEntry) -> float:
        """Calculate relevance score for an entry."""
        score = 0.0

        # Recency component (max 2.0 points)
        try:
            year_int = int(entry.year) if entry.year.isdigit() else self.current_year
            years_old = self.current_year - year_int
            if years_old < 0:
                years_old = 0

            # Newer papers get higher scores
            if years_old <= 1:
                score += 2.0
            elif years_old <= 3:
                score += 1.5
            elif years_old <= 5:
                score += 1.0
            elif years_old <= 10:
                score += 0.5
        except (ValueError, AttributeError):
            pass

        # Domain keyword relevance (max 3.0 points)
        text = (entry.title + " " + entry.abstract + " " + entry.key_finding).lower()
        keyword_hits = sum(2.0 for keyword in self.domain_keywords if keyword in text)
        score += min(keyword_hits, 3.0)

        # Evidence tier boost (max 1.0 point)
        tier_score = EVIDENCE_TIERS.get(entry.evidence_tier, 0.0)
        score += min(tier_score, 1.0)

        # Venue quality boost
        if 'arxiv' in entry.venue.lower():
            score += 0.5
        if any(domain in entry.venue.lower() for domain in ['cfa', 'morningstar', 'vanguard', 'blackrock']):
            score += 0.3

        entry.relevance_score = score
        return score


class KnowledgeBase:
    """Manage the SECOND-KNOWLEDGE-BRAIN.md file."""

    def __init__(self, brain_path: Path):
        self.brain_path = brain_path
        self.content = ""
        self.existing_hashes = set()

        if brain_path.exists():
            self._load()

    def _load(self):
        """Load existing brain content and extract entry hashes."""
        with open(self.brain_path, 'r', encoding='utf-8') as f:
            self.content = f.read()

        # Extract existing hashes for deduplication
        self.existing_hashes = set(re.findall(r'<!--h:([0-9a-f]{12})-->', self.content))

    def append_entries(self, entries: List[KnowledgeEntry], dry_run: bool = False) -> int:
        """Append new entries to the knowledge base."""
        new_entries = [e for e in entries if e.entry_hash not in self.existing_hashes]

        if not new_entries:
            print("[KnowledgeBase] No new entries to append.")
            return 0

        # Sort by relevance score
        new_entries.sort(key=lambda e: e.relevance_score, reverse=True)

        # Generate markdown content
        today = datetime.date.today().isoformat()
        markdown_lines = [
            f"\n- **{today}** — Auto-crawl appended {len(new_entries)} new entries.\n",
            "| Title | Authors | Year | Venue | URL/DOI | Relevance |",
            "|-------|---------|------|-------|---------|-----------|"
        ]

        for entry in new_entries:
            markdown_lines.append(entry.to_markdown_row())

        markdown_content = "\n".join(markdown_lines) + "\n"

        if dry_run:
            print("[KnowledgeBase] DRY RUN - Would append:")
            print(markdown_content)
            return len(new_entries)

        # Append to file
        with open(self.brain_path, 'a', encoding='utf-8') as f:
            f.write(markdown_content)

        print(f"[KnowledgeBase] Appended {len(new_entries)} new entries to {self.brain_path}")

        # Update in-memory state
        self.existing_hashes.update(e.entry_hash for e in new_entries)

        return len(new_entries)

    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about the knowledge base."""
        total_entries = len(self.existing_hashes)

        # Count entries by evidence tier
        tier_counts = {}
        tier_pattern = r'\|(?:.*?)\|(?:.*?)\|(?:.*?)\|(?:.*?)\|(?:.*?)\|(?:.*?)\|'
        for match in re.finditer(tier_pattern, self.content):
            # Extract venue to infer tier
            venue_match = re.search(r'\|(?:.*?)\|(?:.*?)\|(?:.*?)\|([^|]+)\|', match.group(0))
            if venue_match:
                venue = venue_match.group(1).strip()
                if 'arxiv' in venue.lower():
                    tier_counts['academic'] = tier_counts.get('academic', 0) + 1
                elif any(org in venue.lower() for org in ['cfa', 'vanguard', 'blackrock']):
                    tier_counts['industry_standard'] = tier_counts.get('industry_standard', 0) + 1

        return {
            'total_entries': total_entries,
            'tier_distribution': tier_counts,
            'file_size': self.brain_path.stat().st_size if self.brain_path.exists() else 0,
            'last_modified': datetime.datetime.fromtimestamp(self.brain_path.stat().st_mtime).isoformat()
        } if self.brain_path.exists() else {}


def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(
        description='Update investment portfolio analyzer knowledge base'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be added without modifying files'
    )
    parser.add_argument(
        '--max-results',
        type=int,
        default=25,
        help='Maximum results per category (default: 25)'
    )
    parser.add_argument(
        '--categories',
        nargs='+',
        default=ARXIV_CATEGORIES,
        help='ArXiv categories to search'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose output'
    )

    args = parser.parse_args()

    print("=" * 70)
    print("Investment Portfolio Analyzer - Knowledge Updater")
    print("=" * 70)
    print(f"Timestamp: {datetime.datetime.now().isoformat()}")
    print(f"Brain file: {BRAIN_FILE}")
    print(f"ArXiv categories: {args.categories}")
    print(f"Max results per category: {args.max_results}")
    print(f"Dry run: {args.dry_run}")
    print("=" * 70)
    print()

    # Initialize components
    knowledge_base = KnowledgeBase(BRAIN_FILE)
    arxiv_fetcher = ArXivFetcher(args.categories, args.max_results)
    web_search = WebSearchSimulator(SEARCH_QUERIES)
    scorer = EntryScorer(DOMAIN_KEYWORDS)

    all_entries = []

    # Fetch from ArXiv
    print("[Step 1] Fetching from ArXiv...")
    arxiv_entries = arxiv_fetcher.fetch()
    print(f"  Retrieved {len(arxiv_entries)} papers from ArXiv")
    all_entries.extend(arxiv_entries)

    # Simulate web search (integration point)
    print("\n[Step 2] Web search integration...")
    web_results = web_search.search()
    if web_results:
        web_entries = web_search.results_to_entries(web_results)
        print(f"  Retrieved {len(web_entries)} entries from web search")
        all_entries.extend(web_entries)
    else:
        print("  No web search results (integration point for Claude Code WebSearch)")

    # Score all entries
    print(f"\n[Step 3] Scoring {len(all_entries)} entries...")
    for entry in all_entries:
        scorer.score_entry(entry)

    # Sort and show top entries
    all_entries.sort(key=lambda e: e.relevance_score, reverse=True)
    if args.verbose and all_entries:
        print("\n  Top 5 entries by relevance score:")
        for i, entry in enumerate(all_entries[:5], 1):
            print(f"    {i}. [{entry.relevance_score:.1f}] {entry.title[:60]}...")

    # Append to knowledge base
    print(f"\n[Step 4] Appending new entries to knowledge base...")
    appended = knowledge_base.append_entries(all_entries, dry_run=args.dry_run)

    # Show statistics
    print(f"\n[Step 5] Knowledge base statistics:")
    stats = knowledge_base.get_stats()
    print(f"  Total entries: {stats.get('total_entries', 0)}")
    print(f"  File size: {stats.get('file_size', 0):,} bytes")
    if stats.get('tier_distribution'):
        print(f"  Tier distribution: {stats['tier_distribution']}")
    print(f"  Last modified: {stats.get('last_modified', 'Unknown')}")

    print("\n" + "=" * 70)
    print(f"Complete! Added {appended} new entries.")
    print("=" * 70)

    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
