# PROJECT-detail.md — Investment Portfolio Analyzer (stocks/funds/crypto)

## Executive Summary
`investment-portfolio-analyzer` is a Claude Skill in the **Finance, Investment & Insurance** cluster (idea #75). It acts as an investment analyst and portfolio strategist who evaluates allocation, diversification and risk against modern portfolio theory (educational, not personalized financial advice). It runs a research-first, evidence-graded harness that profiles the input, selects named world-renowned frameworks, scores the subject across 6 dimensions, challenges its own conclusions, and emits a professional deliverable with a prioritized improvement roadmap.

## Problem Statement
Retail portfolios are often concentrated, mis-diversified and misaligned with risk tolerance. This skill scores allocation quality and risk, and proposes rebalancing options.

Domain context: practitioners in finance, investment & insurance need decisions grounded in citable, current methodology rather than ad-hoc opinion. This skill enforces the evidence hierarchy (Systematic Review > Meta-Analysis > RCT > Cohort > Expert Opinion > Blog) and keeps its knowledge current through a weekly crawl.

## Target Users & Use Cases
- **Trigger example A:** User says *"Evaluate / score / optimize my investment portfolio analyzer"* → skill runs the full harness and returns a scored report + roadmap.
- **Trigger example B:** User provides an artifact (document, dataset, design, plan) → skill audits it against the frameworks below.
- **Trigger example C:** User asks *"What should I improve first?"* → skill returns the impact/effort-ranked roadmap section only.

## Harness Architecture
```
USER INPUT
   |
   v
[Stage 1] sub-profile-intake  --> scoped profile / context
   |
   v
[Stage 2] sub-risk-screener  --> selected frameworks (Modern Portfolio Theory (Markowitz), ...)
   |
   v
[Stage 3] RESEARCH (WebSearch/WebFetch) --> evidence pack  (fallback: SECOND-KNOWLEDGE-BRAIN.md)
   |
   v
[Stage 4] sub-scoring-engine  --> 6-dimension score
   |
   v
[Stage 5] sub-improvement-roadmap  --> challenge / validation
   |
   v
[Stage 6] MAIN HARNESS --> final deliverable (score table + prioritized roadmap)
```

## Full Sub-Skill Catalog

### sub-profile-intake
- **Purpose:** Capture holdings, risk tolerance, horizon and goals with a clear educational disclaimer.
- **Inputs:** scoped context from prior stage + user artifact
- **Outputs:** structured findings passed to the next stage
- **Tools used:** Read, WebSearch, WebFetch, Write
- **Quality gate:** output must be evidence-linked and complete before the harness advances

### sub-risk-screener
- **Purpose:** Flag concentration, leverage, illiquidity and risk-tolerance mismatches before scoring.
- **Inputs:** scoped context from prior stage + user artifact
- **Outputs:** structured findings passed to the next stage
- **Tools used:** Read, WebSearch, WebFetch, Write
- **Quality gate:** output must be evidence-linked and complete before the harness advances

### sub-scoring-engine
- **Purpose:** Score the portfolio across six dimensions using MPT metrics and correlation analysis.
- **Inputs:** scoped context from prior stage + user artifact
- **Outputs:** structured findings passed to the next stage
- **Tools used:** Read, WebSearch, WebFetch, Write
- **Quality gate:** output must be evidence-linked and complete before the harness advances

### sub-improvement-roadmap
- **Purpose:** Propose rebalancing scenarios with risk/return trade-offs and cost/tax notes.
- **Inputs:** scoped context from prior stage + user artifact
- **Outputs:** structured findings passed to the next stage
- **Tools used:** Read, WebSearch, WebFetch, Write
- **Quality gate:** output must be evidence-linked and complete before the harness advances

## Skill File Format Specification
Frontmatter schema (all skill files):
```yaml
---
name: investment-portfolio-analyzer            # or sub-<name>
description: <one-line summary shown in /help>
---
```
Required sections in `main.md`: Role & Persona, Workflow (Harness Flow), Sub-skills Available, Tools, Output Format, Quality Gates.

## E2E Execution Flow
1. Parse user request and artifact; if ambiguous, ask targeted intake questions.
2. Run `sub-profile-intake` to build the scoped profile.
3. Run `sub-risk-screener` to lock frameworks: Modern Portfolio Theory (Markowitz), Capital Asset Pricing Model (CAPM), Sharpe / Sortino ratios, Risk-parity & strategic asset allocation....
4. Research: issue WebSearch queries (portfolio optimization risk parity; asset allocation diversification; sharpe ratio risk management); WebFetch top authoritative hits; grade evidence. On failure, fall back to SECOND-KNOWLEDGE-BRAIN.md and label the degradation.
5. Run `sub-scoring-engine` to score the 6 dimensions.
6. Run `sub-improvement-roadmap` challenge pass.


8. Synthesize the final deliverable.

## Scoring Dimensions
1. Diversification & correlation
2. Risk-adjusted return (Sharpe/Sortino)
3. Allocation vs. risk tolerance
4. Concentration risk
5. Cost & tax efficiency
6. Liquidity & horizon fit

Each dimension is scored 0–5 with an evidence citation and a one-line justification; the overall score is the weighted mean (weights set by `sub-risk-screener`).

## SECOND-KNOWLEDGE-BRAIN Integration
- **Sources:** ArXiv (q-fin.PM, q-fin.RM); CFA Institute curriculum & research, Morningstar methodology, arXiv q-fin (portfolio, risk), SSRN finance working papers, Vanguard/BlackRock asset-allocation research.
- **Crawl config:** weekly cron via `tools/knowledge_updater.py` (crawl4ai).
- **Append format:** scored entries (title, authors, year, DOI/URL, key finding, relevance) added to the Knowledge Update Log with a date stamp and dedup by URL/DOI hash.

## Supporting Tools Spec
`tools/knowledge_updater.py`:
- **Inputs:** search queries (above), ArXiv categories, last-run timestamp.
- **Outputs:** appended entries in `SECOND-KNOWLEDGE-BRAIN.md`.
- **Schedule:** weekly.

## Quality Gates (must all be TRUE before final output)
- Every dimension scored with a cited source or explicit fallback label.
- At least one framework from the catalog explicitly applied.
- Challenge phase documented (≥3 counter-arguments considered).


- Roadmap items carry impact + effort ratings.

## Test Scenarios (summary; full set in tests/)
1. Happy-path full audit of a typical finance, investment & insurance artifact.
2. Ambiguous/incomplete input → intake clarification path.
3. Offline/degraded mode → graceful fallback to knowledge brain.
4. Edge artifact stress test (adversarial input).
5. Roadmap-only request → returns prioritized recommendations.

## Key Design Decisions
1. Framework-grounded scoring only — no ad-hoc criteria.
2. Research-first with explicit graceful degradation.
3. Mandatory challenge phase before synthesis.
4. Impact/effort roadmap is always the final artifact.
5. Self-improving knowledge base via weekly crawl.
