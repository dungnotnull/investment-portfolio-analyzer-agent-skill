# Test Scenarios — Investment Portfolio Analyzer (stocks/funds/crypto)

Skill: `investment-portfolio-analyzer` · idea #75 · cluster `finance-insurance`
Minimum 5 scenarios; each lists Setup → Expected Behavior → Pass Criteria.

## Test Framework

This document defines 5 test scenarios that validate the skill's functionality across different use cases. Each scenario includes:
- **Setup**: Input conditions and portfolio state
- **Expected Behavior**: What the skill should do
- **Pass Criteria**: Specific validation checkpoints
- **Test Data**: Representative portfolio data
- **Expected Outputs**: Sample responses for comparison

---

## Scenario 1: Happy-Path Full Evaluation

### Purpose
Validate end-to-end execution with complete, well-formed input.

### Setup
**Input**: Representative finance, investment & insurance portfolio with all required data.

**Test Portfolio**:
```markdown
Portfolio Value: $478,350

Holdings:
| Ticker | Asset Class | Quantity | Current Value | Weight |
|--------|-------------|----------|---------------|--------|
| VTI    | ETF Equity  | 200      | $48,600       | 10.2%  |
| BND    | ETF Bond    | 500      | $45,200       | 9.5%   |
| AAPL   | Stock       | 150      | $28,500       | 6.0%   |
| MSFT   | Stock       | 80       | $31,200       | 6.5%   |
| SCHD   | ETF Equity  | 120      | $29,400       | 6.1%   |
| VXUS   | ETF Equity  | 150      | $24,450       | 5.1%   |
| JEPI   | ETF Equity  | 200      | $31,600       | 6.6%   |
| BTC-USD| Crypto      | 0.5      | $27,500       | 5.7%   |
| SHV    | ETF Cash    | 300      | $30,090       | 6.3%   |
| BSV    | ETF Bond    | 200      | $20,000       | 4.2%   |

Investor Profile:
- Risk Tolerance: Moderate
- Investment Horizon: 10+ years
- Primary Goal: Growth for retirement
- Secondary Goal: Some income generation
- Pattern: Accumulating (+$2,000/month)
```

### Expected Behavior

1. **Stage 1 (Intake)**: Acknowledge complete input, normalize portfolio
2. **Stage 2 (Risk Screener)**: Select frameworks, assign dimension weights, screen risks
3. **Stage 3 (Research)**: Execute WebSearch queries, fetch evidence
4. **Stage 4 (Scoring)**: Score all 6 dimensions with metrics and citations
5. **Stage 5 (Challenge)**: Generate counter-arguments, revise if needed
6. **Stage 6 (Synthesis)**: Assemble final report

### Pass Criteria

✅ **All 6 dimensions scored** (0-5 range with metrics shown)
✅ **Scoring table present** with overall score calculated
✅ **At least 3 frameworks cited** with evidence tiers
✅ **Challenge section present** with ≥3 counter-arguments
✅ **Roadmap provided** with impact/effort ratings
✅ **Evidence sources graded** by tier (Tier 1-4)
✅ **Executive summary** with top 3 strengths and priority fixes

### Expected Output Structure

```markdown
# Investment Portfolio Analyzer — Evaluation Report

## 1. Executive Summary
**Overall Score**: 3.6 / 5
**Top 3 Strengths**: [List]
**Top 3 Priority Fixes**: [List]

## 2. Scoring Table
| Dimension | Score | Weight | Weighted Score | Framework |
|-----------|-------|--------|----------------|-----------|
| Diversification & Correlation | 4.0 | 18% | 0.72 | MPT, Correlation Analysis |
| Risk-Adjusted Return | 3.0 | 18% | 0.54 | Sharpe/Sortino, CAPM |
| Allocation vs Risk Tolerance | 4.0 | 18% | 0.72 | Risk Parity |
| Concentration Risk | 3.0 | 18% | 0.54 | CAPM, Concentration Analysis |
| Cost & Tax Efficiency | 4.0 | 14% | 0.56 | Industry Benchmarks |
| Liquidity & Horizon Fit | 4.0 | 14% | 0.56 | Monte Carlo |
| **OVERALL** | **3.6** | **100%** | **3.64** | — |

## 3. Detailed Findings
[Per-dimension analysis with metrics, justifications, evidence]

## 4. Challenge / Devil's-Advocate Notes
[≥3 counter-arguments with evidence requirements and revisions]

## 5. Prioritized Improvement Roadmap
| # | Recommendation | Impact | Effort | Priority |
|---|----------------|--------|--------|----------|
[Minimum 5 recommendations with ratings]

## 6. Sources & Evidence Grade
[Tier 1-4 citations with relevance]
```

### Validation Checklist

- [ ] Report includes all 6 numbered sections
- [ ] Scoring table has 7 rows (6 dimensions + overall)
- [ ] Each dimension score between 0-5
- [ ] Overall score between 0-5
- [ ] Challenge section has ≥3 distinct counter-arguments
- [ ] Roadmap has ≥5 recommendations
- [ ] Each recommendation has impact/effort rating
- [ ] Evidence section has ≥3 sources with tiers
- [ ] No placeholder text (e.g., "[TODO]", "[fill in]")
- [ ] No contradictions within report

---

## Scenario 2: Ambiguous / Incomplete Input

### Purpose
Validate that skill detects missing data and asks clarifying questions instead of fabricating.

### Setup
**Input**: Partial portfolio with gaps.

**Test Portfolio**:
```markdown
Portfolio Value: [Unknown]

Holdings:
| Ticker | Asset Class | Quantity | Current Value | Weight |
|--------|-------------|----------|---------------|--------|
| VTI    | ETF Equity  | [Unknown]| [Unknown]     | [Unknown] |
| AAPL   | Stock       | 100      | [Unknown]     | [Unknown] |
| [Some Crypto] | [Unknown] | [Unknown] | [Unknown] | [Unknown] |

Investor Profile:
- Risk Tolerance: [Not specified]
- Investment Horizon: [Not specified]
- Goals: [Not specified]
- Pattern: [Not specified]
```

### Expected Behavior

1. **Stage 1 (Intake)**: Detect gaps, ask targeted questions
2. **No scoring** until gaps filled
3. **No fabrication** of missing values

### Pass Criteria

✅ **Asks ≤5 focused questions** (not 10+ generic questions)
✅ **Does not proceed to scoring** with incomplete data
✅ **Does not fabricate** missing values
✅ **Questions are specific** (not "tell me everything about your portfolio")

### Expected Questions

Expected clarifying questions:
1. "What is the approximate current market value of your VTI holding?"
2. "What is your risk tolerance: Conservative, Moderate, Growth, or Aggressive?"
3. "What is your investment time horizon (years until you need the money)?"
4. "What is the primary goal of this portfolio: Income, Growth, Preservation, or Speculation?"
5. "Do you make regular contributions, withdrawals, or mostly hold steady?"

### Validation Checklist

- [ ] Skill asks exactly 3-5 questions
- [ ] Questions are specific and targeted
- [ ] No scoring output produced
- [ ] No fabricated values in any output
- [ ] Response clearly states what information is needed
- [ ] Response does not make assumptions about missing data

---

## Scenario 3: Offline / Degraded Research Mode

### Purpose
Validate graceful degradation when WebSearch/WebFetch unavailable.

### Setup
**Input**: Complete portfolio but simulate WebSearch/WebFetch failure.

**Test Portfolio**:
```markdown
Portfolio Value: $100,000

Holdings:
| Ticker | Asset Class | Quantity | Current Value | Weight |
|--------|-------------|----------|---------------|--------|
| VTI    | ETF Equity  | 50       | $25,000       | 25%    |
| BND    | ETF Bond    | 250      | $25,000       | 25%    |
| AAPL   | Stock       | 50       | $25,000       | 25%    |
| Cash   | Cash        | —        | $25,000       | 25%    |

Investor Profile:
- Risk Tolerance: Moderate
- Investment Horizon: 10 years
- Goal: Growth
- Pattern: Static

**Environment**: WebSearch/WebFetch unavailable (simulate error or timeout)
```

### Expected Behavior

1. **Stage 3 (Research)**: Detect WebSearch failure
2. **Fallback**: Use SECOND-KNOWLEDGE-BRAIN.md
3. **Label**: Clearly state degradation in output
4. **Complete**: Still produce full report

### Pass Criteria

✅ **Output contains degradation label** (explicit statement about fallback mode)
✅ **Full report still produced** (all sections present)
✅ **Scoring completed** using knowledge base
✅ **Evidence sources labeled** as from knowledge base
✅ **No crash or error** in execution

### Expected Degradation Label

Expected label formats (any of these acceptable):
- "⚠️ Analysis degraded - using knowledge base only"
- "Note: WebSearch unavailable - some claims rely on knowledge base without current verification"
- "Degraded Mode: Analysis based on SECOND-KNOWLEDGE-BRAIN.md"

### Validation Checklist

- [ ] Degradation label present in report
- [ ] Label is prominent (not buried in footnotes)
- [ ] All 6 dimensions still scored
- [ ] Overall score calculated
- [ ] Roadmap still provided
- [ ] Evidence sources cite knowledge base
- [ ] No error messages or crashes
- [ ] Report structure identical to happy-path

---

## Scenario 4: Challenge Phase Changes Verdict

### Purpose
Validate that devil's-advocate phase can revise initial scoring.

### Setup
**Input**: Portfolio with concentration that should trigger challenge.

**Test Portfolio**:
```markdown
Portfolio Value: $500,000

Holdings:
| Ticker | Asset Class | Quantity | Current Value | Weight |
|--------|-------------|----------|---------------|--------|
| TSLA   | Stock       | 2,000    | $400,000      | 80%    |
| BND    | ETF Bond    | 200      | $20,000       | 4%     |
| Cash   | Cash        | —        | $80,000       | 16%    |

Investor Profile:
- Risk Tolerance: Moderate
- Investment Horizon: 5 years
- Goal: Growth
- Pattern: Static

**Trigger**: Single stock concentration (80% TSLA) with moderate risk tolerance → should generate challenge
```

### Expected Behavior

1. **Stage 4 (Scoring)**: Initial scoring may give moderate scores (diversification poor but other dimensions okay)
2. **Stage 5 (Challenge)**: Detect over-optimism on risk-tolerance alignment or concentration
3. **Revision**: At least one dimension score revised downward
4. **Documentation**: Challenge section explains revision rationale

### Pass Criteria

✅ **Challenge section present** with ≥3 counter-arguments
✅ **At least one score revised** (documented before/after)
✅ **Revision rationale explained** (why change was made)
✅ **Evidence required** stated for validating/refuting challenge

### Expected Challenge Structure

```markdown
## 4. Challenge / Devil's-Advocate Notes

### Challenge 1: Risk-Tolerance Mismatch
**Counterargument**: Initial scoring rated allocation vs risk tolerance as 3/5 (Adequate),
but 80% single-stock concentration with moderate tolerance represents severe mismatch.
**Evidence Required**: Stress test showing 40% drawdown impact on moderate investor
**Impact if True**: Dimension 3 score revised from 3 to 1
**Revision Applied**: Dimension 3 (Allocation vs Risk Tolerance): 3 → 1

[2 additional challenges...]
```

### Validation Checklist

- [ ] Challenge section has ≥3 distinct counter-arguments
- [ ] At least one score shows "X → Y" revision
- [ ] Each challenge has counterargument stated
- [ ] Each challenge has evidence requirement
- [ ] Each challenge has impact if true
- [ ] Revisions are logically justified
- [ ] No contradictions in revision rationale

---

## Scenario 5: Roadmap-Only Request

### Purpose
Validate that skill can provide targeted roadmap without full analysis.

### Setup
**Input**: User asks "What should I fix first?" with portfolio context.

**Test Portfolio**:
```markdown
Portfolio Value: $200,000

Holdings:
| Ticker | Asset Class | Quantity | Current Value | Weight |
|--------|-------------|----------|---------------|--------|
| VTI    | ETF Equity  | 100      | $100,000      | 50%    |
| AAPL   | Stock       | 200      | $50,000       | 25%    |
| MSFT   | Stock       | 100      | $50,000       | 25%    |

Investor Profile:
- Risk Tolerance: Growth
- Investment Horizon: 15+ years
- Goal: Growth
- Pattern: Accumulating

**User Query**: "What should I improve first in my portfolio?"
```

### Expected Behavior

1. **Stage 1 (Intake)**: Parse portfolio and question
2. **Stage 2-5**: Execute analysis but **focus output on roadmap**
3. **Output**: Prioritized roadmap table (not full report)

### Pass Criteria

✅ **Output is roadmap table** (not full report)
✅ **Roadmap ranked by impact/effort** (priority column present)
✅ **Framework basis present** (each recommendation links to framework)
✅ **Full ranking** (1-N, not just top 3)
✅ **Actionable recommendations** (specific, not vague)

### Expected Output

```markdown
# Prioritized Improvement Roadmap

| # | Recommendation | Impact | Effort | Priority | Framework Basis | Expected Improvement |
|---|----------------|--------|--------|----------|----------------|---------------------|
| 1 | Increase international diversification from 0% to 20% | High | Medium | 1 | MPT, Correlation Analysis | Diversification: 2 → 4 |
| 2 | Reduce technology concentration from 100% to 25% of equities | High | Low | 2 | Concentration Analysis | Concentration: 1 → 3 |
| 3 | Add fixed income allocation (10-20%) for risk management | Medium | Low | 3 | Risk Parity, Strategic Allocation | Risk-Return: 3 → 4 |
| 4 | Implement tax-loss harvesting annually | Medium | Low | 4 | Industry Best Practices | Cost Efficiency: 3 → 5 |
| 5 | Add small-cap value exposure (5-10%) | Low | Medium | 5 | Fama-French Factors | Diversification: 2 → 3 |

**Top Priority**: #1 - Increase international diversification
**Quick Wins**: #2, #4 (Low effort, High/Medium impact)
**Long-term Considerations**: #3, #5 (strategic improvements)
```

### Validation Checklist

- [ ] Output is roadmap table (not full report)
- [ ] Roadmap has ≥5 recommendations
- [ ] Each recommendation has impact rating
- [ ] Each recommendation has effort rating
- [ ] Each recommendation has priority score (1-N)
- [ ] Each recommendation links to framework
- [ ] Recommendations are specific (not "diversify more")
- [ ] Recommendations include expected improvement

---

## Regression Testing

### Regression Checklist
Run after any code changes to ensure no functionality breaks.

- [ ] All 6 dimensions appear in scoring table
- [ ] At least one named framework cited per run
- [ ] Evidence tiers labeled on every external claim
- [ ] Roadmap items ranked by impact × effort
- [ ] Challenge phase executes (≥3 counter-arguments)
- [ ] Educational disclaimer present
- [ ] No placeholder text in any output
- [ ] No contradictory statements
- [ ] All scores within 0-5 range
- [ ] Overall score calculated correctly

### Score Reproducibility Test

Run same portfolio twice, compare scores:
- **Threshold**: Scores must be within ±0.5
- **Variance tracking**: Log any dimension with >0.3 variance
- **Formula validation**: Ensure scoring formulas produce consistent results

### Evidence Quality Test

Validate evidence sources:
- **Tier distribution**: At least one Tier 1 or Tier 2 source
- **Source diversity**: Sources from ≥2 different domains
- **Recency check**: At least one source from last 3 years
- **Relevance check**: Sources actually support claims made

---

## Calibration Notes

### Calibration History

Record scoring adjustments and rationale:

| Date | Dimension | Old Threshold | New Threshold | Rationale |
|------|-----------|---------------|---------------|-----------|
| 2026-06-30 | Diversification HHI | Excellent: < 500 | Excellent: < 800 | Adjusted for typical ETF-heavy portfolios |
| 2026-06-30 | Risk-Return Sharpe | Good: ≥ 1.0 | Good: ≥ 0.8 | Relaxed for moderate risk profiles |
| [Future entries...] |

### Calibration Triggers

Recalibrate when:
- Score reproducibility fails (>0.5 variance)
- User feedback indicates scores misaligned with intuition
- Market regime changes invalidate historical thresholds
- New frameworks added to catalog

### Calibration Process

1. **Collect data**: Run test suite, capture score variances
2. **Analyze patterns**: Identify consistent over/under-scoring
3. **Adjust thresholds**: Modify scoring formulas
4. **Re-test**: Validate new thresholds produce expected results
5. **Document**: Record changes in calibration history

---

## Test Execution

### Running Tests

```bash
# Run all scenarios
python tests/test_suite.py

# Run specific scenario
python tests/test_suite.py --scenario 1

# Verbose output
python tests/test_suite.py --verbose

# Run with calibration
python tests/test_suite.py --calibrate
```

### Expected Test Results

```
Test Suite Results:
==================
Scenario 1: Happy-path full evaluation
  [✓] PASS (2.34s)
  All required components present in report. Scoring is reproducible within ±0.5

Scenario 2: Ambiguous / incomplete input
  [✓] PASS (0.89s)
  Passed: Asked 4 targeted questions. Questions: risk tolerance, horizon, goals, values

Scenario 3: Offline / degraded research mode
  [✓] PASS (1.45s)
  Passed: Degraded mode labeled and complete report produced

Scenario 4: Challenge phase changes verdict
  [✓] PASS (1.92s)
  Passed: 3 counter-arguments with score revision documented

Scenario 5: Roadmap-only request
  [✓] PASS (1.12s)
  Passed: Roadmap present, correctly ranked, framework-linked

==================
Test Summary
==================
Total: 5
Passed: 5 (100.0%)
Failed: 0
Errored: 0
Skipped: 0
Total Time: 7.72s
==================

Results saved to: tests/test_results.json
```

### Failure Handling

If test fails:
1. **Review error message** in test output
2. **Check test data** for correctness
3. **Validate skill logic** against expected behavior
4. **Update test** if expected behavior changed
5. **Document change** in calibration history

---

## Version History

- v1.0 (2026-06-18): Initial test scenarios defined
- v1.1 (2026-06-30): Enhanced with test data, expected outputs, validation checklists
