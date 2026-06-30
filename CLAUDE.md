# CLAUDE.md — Investment Portfolio Analyzer (stocks/funds/crypto)

**Skill name:** `investment-portfolio-analyzer`
**Tagline:** Investment Portfolio Analyzer (stocks/funds/crypto)
**Source idea:** #75  |  **Cluster:** `finance-insurance` (Finance, Investment & Insurance)
**Current phase:** Phase 2 complete (core sub-skills + harness + quality gates). Phase 3 knowledge pipeline scaffolded.

## Problem This Skill Solves
Retail portfolios are often concentrated, mis-diversified and misaligned with risk tolerance. This skill scores allocation quality and risk, and proposes rebalancing options.

## Harness Flow Summary
1. **Intake / scoping** → `sub-profile-intake.md` gathers context and constraints.
2. **Framework selection** → `sub-risk-screener.md` chooses the named evaluation frameworks for this case.
3. **Research / evidence** → WebSearch + WebFetch pull authoritative sources; fall back to SECOND-KNOWLEDGE-BRAIN.md if offline.
4. **Scoring / analysis** → `sub-scoring-engine.md` scores across the 6 dimensions.
5. **Challenge phase** → devil's-advocate review (`sub-improvement-roadmap.md`).
6. **Synthesis** → main harness assembles the final professional deliverable (score + prioritized roadmap).

Standard quality gates apply (see Quality Gates below).

## Sub-skills
- `skills/sub-profile-intake.md` — Capture holdings, risk tolerance, horizon and goals with a clear educational disclaimer.
- `skills/sub-risk-screener.md` — Flag concentration, leverage, illiquidity and risk-tolerance mismatches before scoring.
- `skills/sub-scoring-engine.md` — Score the portfolio across six dimensions using MPT metrics and correlation analysis.
- `skills/sub-improvement-roadmap.md` — Propose rebalancing scenarios with risk/return trade-offs and cost/tax notes.

## Tools Required
- WebSearch, WebFetch (research-first evidence gathering)
- Read, Write (deliverable assembly)
- Bash / Python (run `tools/knowledge_updater.py`)

## Knowledge Sources
- ArXiv categories: q-fin.PM, q-fin.RM
- Domain sources: CFA Institute curriculum & research, Morningstar methodology, arXiv q-fin (portfolio, risk), SSRN finance working papers, Vanguard/BlackRock asset-allocation research

## Supporting Python Tools
- `tools/knowledge_updater.py` — crawl4ai pipeline that refreshes `SECOND-KNOWLEDGE-BRAIN.md` weekly.

## Active Development Tasks
- [x] Scaffold folder + 8 required deliverables
- [x] Define 7 named evaluation frameworks
- [x] Implement 4 sub-skills (min 3)
- [ ] Wire shared cluster sub-skills across `finance-insurance`
- [ ] First live crawl to seed SECOND-KNOWLEDGE-BRAIN knowledge log

## Reference Docs
- `PROJECT-detail.md` — full technical spec
- `PROJECT-DEVELOPMENT-PHASE-TRACKING.md` — phase roadmap
- `SECOND-KNOWLEDGE-BRAIN.md` — self-improving knowledge base
