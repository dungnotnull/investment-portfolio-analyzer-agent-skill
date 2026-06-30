# Investment Portfolio Analyzer

**A research-first, evidence-based Claude skill for evaluating investment portfolios using Modern Portfolio Theory and 6+ named frameworks.**

[![Claude Skill](https://img.shields.io/badge/Claude-Skill-blue)](https://github.com/dungnotnull/investment-portfolio-analyzer-agent-skill)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status: Production Ready](https://img.shields.io/badge/Status-Production--Ready-brightgreen)](https://github.com/dungnotnull/investment-portfolio-analyzer-agent-skill)
[![Cluster: Finance Insurance](https://img.shields.io/badge/Cluster-finance--insurance-orange)](https://github.com/dungnotnull/investment-portfolio-analyzer-agent-skill)

---

## Overview

Investment Portfolio Analyzer is a sophisticated Claude Code skill that evaluates investment portfolios across six dimensions using world-renowned financial frameworks. It provides educational analysis (not personalized financial advice) grounded in citable evidence, with a self-improving knowledge base that updates weekly.

**Perfect for:**
- Individual investors wanting to understand their portfolio's strengths and weaknesses
- Financial educators teaching portfolio theory
- Investment clubs evaluating collective holdings
- Anyone seeking evidence-based portfolio insights

---

## What It Does

The analyzer evaluates portfolios using a rigorous six-stage process:

1. **Intake & Scoping** - Captures holdings, risk tolerance, horizon, and goals
2. **Risk Screening** - Selects frameworks and flags concentration, leverage, and illiquidity risks
3. **Research** - Gathers current evidence from authoritative sources (with graceful offline fallback)
4. **Scoring** - Scores across 6 dimensions using Modern Portfolio Theory metrics
5. **Challenge Phase** - Devil's advocate review with counter-arguments
6. **Synthesis** - Delivers comprehensive report with prioritized roadmap

---

## Scoring Dimensions

| Dimension | What It Measures | Key Frameworks |
|-----------|------------------|----------------|
| **Diversification & Correlation** | How well holdings are spread to reduce risk | Modern Portfolio Theory, Correlation Analysis |
| **Risk-Adjusted Return** | Returns relative to risk taken | Sharpe Ratio, Sortino Ratio, CAPM |
| **Allocation vs Risk Tolerance** | Alignment between portfolio and investor profile | Risk Parity, Strategic Asset Allocation |
| **Concentration Risk** | Over-concentration in positions, sectors, or regions | CAPM, Concentration Metrics |
| **Cost & Tax Efficiency** | Fee efficiency and tax optimization | Industry Benchmarks, Tax Research |
| **Liquidity & Horizon Fit** | Alignment with time horizons and liquidity needs | Monte Carlo Simulation, Risk Parity |

Each dimension receives a score from 0-5, with an overall portfolio score calculated using dimension weights customized to your risk tolerance.

---

## Key Features

### Evidence-Based Analysis
- Every claim cites authoritative sources (CFA Institute, academic papers, industry research)
- Evidence graded by tier (Systematic Reviews > Academic > Industry Standards > General)
- WebSearch/WebFetch integration with graceful fallback to knowledge base

### Framework-Grounded Scoring
Uses recognized financial frameworks:
- Modern Portfolio Theory (Markowitz)
- Capital Asset Pricing Model (CAPM)
- Sharpe/Sortino Ratios
- Risk Parity & Strategic Asset Allocation
- Fama-French Factors
- Monte Carlo Risk Simulation

### Devil's Advocate Challenge
- Challenges its own analysis with counter-arguments
- Surfaces 3+ alternative interpretations
- Revises scores if challenges are valid
- Ensures balanced, thoughtful conclusions

### Self-Improving Knowledge Base
- Weekly automated crawl of arXiv q-fin papers
- Integrates latest research into analysis
- Deduplicates and scores entries by relevance
- Currently seeded with 42 high-quality sources

### Production-Grade Quality
- 15 enforced quality gates before any output
- Comprehensive error handling and edge cases
- Works in offline/degraded mode
- Professional documentation throughout

---

## Installation

### Requirements
- Claude Code (or compatible Claude CLI)
- Python 3.8+ (for knowledge updater)
- Git (for cloning)

### Quick Start

1. Clone the repository:
```bash
git clone https://github.com/dungnotnull/investment-portfolio-analyzer-agent-skill.git
cd investment-portfolio-analyzer-agent-skill
```

2. The skill is now ready to use with Claude Code

3. Optional: Update knowledge base with latest research
```bash
python tools/knowledge_updater.py
```

---

## Usage

### Basic Portfolio Analysis

Simply provide your portfolio to Claude:

```
I have these holdings:
- VTI: $48,600 (ETF)
- BND: $45,200 (Bond ETF)
- AAPL: $28,500 (Stock)
- BTC: $27,500 (Crypto)
- Cash: $30,000

My risk tolerance is moderate, I'm investing for 10+ years, and my goal is growth for retirement.

Can you analyze my portfolio?
```

The skill will automatically invoke the investment-portfolio-analyzer and provide a comprehensive report.

### Roadmap-Only Request

For quick improvement suggestions:

```
What should I improve first in my portfolio?
[Your portfolio details]
```

### Educational Disclaimer

All analyses include this disclaimer:
```
DISCLAIMER: This analysis is for educational purposes only. It does not constitute
personalized financial advice, investment recommendations, or tax guidance. Consult
a qualified financial advisor and tax professional for decisions specific to your
situation.
```

---

## Sample Output

### Executive Summary
```
Overall Score: 3.6 / 5 (Good)
Top 3 Strengths:
- Strong cost efficiency (0.08% expense ratio)
- Good diversification across asset classes
- Appropriate risk alignment for moderate profile

Top 3 Priority Fixes:
1. Reduce crypto allocation from 7.6% to 5% (High Impact, Low Effort)
2. Increase international diversification to 20% (High Impact, Medium Effort)
3. Reduce technology sector concentration (Medium Impact, Low Effort)
```

### Scoring Table
```
Dimension                                    Score    Weight    Framework
---------------------------------------------------------------------------
Diversification & Correlation               4.0      18%      MPT, Correlation
Risk-Adjusted Return                         3.0      18%      Sharpe/Sortino
Allocation vs Risk Tolerance                4.0      18%      Risk Parity
Concentration Risk                           3.0      18%      CAPM
Cost & Tax Efficiency                        4.0      14%      Industry Benchmarks
Liquidity & Horizon Fit                      4.0      14%      Monte Carlo
---------------------------------------------------------------------------
OVERALL                                      3.6      100%
```

---

## Project Structure

```
investment-portfolio-analyzer-agent-skill/
├── README.md                          # This file
├── CLAUDE.md                          # Claude Code integration
├── PROJECT-detail.md                  # Full technical specification
├── PROJECT-DEVELOPMENT-PHASE-TRACKING.md  # Development history
├── SECOND-KNOWLEDGE-BRAIN.md          # Self-improving knowledge base
├── LICENSE                            # MIT License
│
├── skills/                            # Core skill implementation
│   ├── main.md                        # Main harness workflow
│   ├── sub-profile-intake.md          # Stage 1: Intake & scoping
│   ├── sub-risk-screener.md           # Stage 2: Risk screening
│   ├── sub-scoring-engine.md          # Stage 4: Scoring & analysis
│   └── sub-improvement-roadmap.md     # Stage 5: Challenge & roadmap
│
├── tools/                             # Supporting utilities
│   └── knowledge_updater.py           # Weekly knowledge crawler
│
├── tests/                             # Test infrastructure
│   ├── test-scenarios.md              # 5 comprehensive test scenarios
│   └── test_suite.py                  # Test runner implementation
│
└── docs/                              # Additional documentation
    └── CLUSTER_INTEGRATION.md         # Cluster patterns for reuse
```

---

## Development

### Running Tests

Execute the comprehensive test suite:

```bash
python tests/test_suite.py
```

Run specific scenarios:
```bash
python tests/test_suite.py --scenario 1
```

Verbose output:
```bash
python tests/test_suite.py --verbose
```

### Updating Knowledge Base

The knowledge base updates weekly via `tools/knowledge_updater.py`:

```bash
# Standard update
python tools/knowledge_updater.py

# Dry run (preview only)
python tools/knowledge_updater.py --dry-run

# Custom categories
python tools/knowledge_updater.py --categories q-fin.PM q-fin.RM

# Verbose output
python tools/knowledge_updater.py --verbose
```

The crawler:
- Fetches latest papers from arXiv (q-fin.PM, q-fin.RM)
- Integrates WebSearch results when available
- Scores entries by recency and domain relevance
- Deduplicates by URL/DOI hash
- Appends to `SECOND-KNOWLEDGE-BRAIN.md`

---

## Framework Catalog

The skill uses these world-renowned frameworks:

| Framework | Origin | Application |
|-----------|--------|-------------|
| Modern Portfolio Theory | Markowitz (1952) | Efficient frontier, mean-variance optimization |
| CAPM | Sharpe (1964) | Systematic vs idiosyncratic risk |
| Sharpe Ratio | Sharpe (1966) | Risk-adjusted return measurement |
| Sortino Ratio | Sortino (1991) | Downside risk measurement |
| Risk Parity | Qian (2006) | Risk budgeting across assets |
| Fama-French | Fama & French (1993) | Factor-based asset pricing |
| Monte Carlo Simulation | Glasserman (2004) | Probabilistic risk analysis |

---

## Quality Assurance

### Quality Gates (15 Total)

All analyses must pass these gates before output:

1. Educational disclaimer stated
2. All essential data points captured
3. Portfolio normalized (weights sum to 100%)
4. At least 3 frameworks selected with rationale
5. Dimension weights sum to 100%
6. All four risk screens completed
7. Horizon alignment assessed
8. At least 3 WebSearch queries executed (or fallback labeled)
9. All 6 dimensions scored with metrics
10. Each dimension has framework citation
11. At least 3 challenges documented
12. Minimum 5 recommendations with impact/effort ratings
13. At least 3 rebalancing scenarios with full analysis
14. Implementation roadmap provided
15. All citations graded by tier

### Test Coverage

5 comprehensive scenarios:
- Happy-path full evaluation
- Ambiguous/incomplete input
- Offline/degraded mode
- Challenge phase revisions
- Roadmap-only requests

---

## Cluster Integration

This skill anchors the `finance-insurance` cluster. Shared patterns documented in `docs/CLUSTER_INTEGRATION.md` enable:

- Reusable sub-skill patterns across cluster skills
- Consistent quality gates and output formats
- Cross-skill recommendations (e.g., portfolio analysis suggesting insurance review)
- Shared knowledge base and update protocols

---

## Contributing

Contributions welcome! Areas for contribution:

1. **Additional Frameworks** - Integrate new evaluation methodologies
2. **Test Scenarios** - Add edge cases and validation tests
3. **Knowledge Sources** - Suggest authoritative sources for the crawler
4. **Documentation** - Improve clarity and examples
5. **Bug Reports** - Report issues with detailed reproduction steps

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- **Foundational Research**: Harry Markowitz (MPT), William Sharpe (CAPM, Sharpe Ratio), Eugene Fama & Kenneth French (Factor Models)
- **Industry Standards**: CFA Institute, Morningstar, Vanguard, BlackRock
- **Academic Community**: arXiv q-fin contributors, SSRN authors
- **Claude Code**: Anthropic's Claude Code platform and skill system

---

## Disclaimer

**IMPORTANT**: This skill provides educational analysis only. It does not constitute personalized financial advice, investment recommendations, or tax guidance. Always consult qualified financial advisors and tax professionals for decisions specific to your situation.

---

## Version History

- **v1.0.0** (2026-06-30) - Initial release with complete implementation
  - 6-dimension scoring framework
  - 7 evaluation frameworks integrated
  - Self-improving knowledge base (42 seeded entries)
  - Comprehensive test suite
  - Cluster integration patterns

---

## Support

For questions, issues, or discussions:
- Open an issue on GitHub
- Check `PROJECT-detail.md` for technical details
- Review `docs/CLUSTER_INTEGRATION.md` for cluster patterns

---

**Made with Claude Code** • **Finance, Investment & Insurance Cluster** • **Idea #75**

![Claude Code](https://img.shields.io/badge/Built%20With-Claude%20Code-7c3aed?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgc3Ryb2tlPSJ3aGl0ZSIgc3Ryb2tlLXdpZHRoPSIyIj48cGF0aCBkPSJNMTIgMkM2LjQ4IDIgMiA2LjQ4IDIgMTJzNC40OCAxMCAxMCAxMCAxMC00LjQ4IDEwLTEwUzE3LjUyIDIgMTIgMnptMCAzYy0zLjMxIDAtNiAynjktNiA2czIuNjkgNiA2IDYgNi0yLjY5IDYtNi0yLjY5LTYtNi02em0yIDhjLTIuMjEgMC00LTEuNzktNC00czEuNzktNCA0LTQgNCAxLjc5IDQgNC0xLjc5IDQtNCA0eiIvPjwvc3ZnPg==)
