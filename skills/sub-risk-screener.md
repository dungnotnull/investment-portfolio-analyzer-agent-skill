---
name: sub-risk-screener
description: (investment-portfolio-analyzer) Flag concentration, leverage, illiquidity and risk-tolerance mismatches before scoring.
---

# Sub-skill: risk-screener

## Purpose
Systematically screen the portfolio for critical risk issues before detailed scoring. Flag concentration, leverage, illiquidity, and risk-tolerance mismatches. Select and weight the evaluation frameworks appropriate for this portfolio's characteristics.

## When the Harness Calls This
Stage matching `sub-risk-screener` in the `investment-portfolio-analyzer` main workflow. Runs after profile intake, before research and scoring.

## Inputs
- Normalized portfolio from Stage 1 (sub-profile-intake)
- Investor profile (risk tolerance, horizon, goals, pattern)
- Early-stage flags from intake

## Procedure

### Step 1: Framework Selection and Weighting
Select which evaluation frameworks to apply and assign dimension weights based on portfolio characteristics.

#### Available Frameworks (from catalog):
1. **Modern Portfolio Theory (Markowitz)** — Mean-variance optimization, efficient frontier
2. **Capital Asset Pricing Model (CAPM)** — Systematic vs idiosyncratic risk
3. **Sharpe / Sortino Ratios** — Risk-adjusted return measurement
4. **Risk Parity & Strategic Asset Allocation** — Risk budgeting across asset classes
5. **Diversification & Correlation Analysis** — Correlation matrices, concentration metrics
6. **Fama-French Factors** — Size, value, profitability factors
7. **Monte Carlo Risk Simulation** — Probabilistic scenario analysis

#### Framework Selection Logic:

```python
# Framework activation based on portfolio characteristics

if portfolio.has_multiple_asset_classes:
    apply_framework("Modern Portfolio Theory (Markowitz)")
    apply_framework("Risk Parity & Strategic Asset Allocation")

if portfolio.has_equities:
    apply_framework("Capital Asset Pricing Model (CAPM)")
    apply_framework("Fama-French Factors")

if portfolio.has_complex_instruments or leverage:
    apply_framework("Monte Carlo Risk Simulation")

# Always apply core frameworks
apply_framework("Sharpe / Sortino Ratios")
apply_framework("Diversification & Correlation Analysis")
```

#### Dimension Weight Assignment:

Adjust scoring dimension weights based on investor profile:

| Investor Profile | Diversification | Risk-Return | Risk-Tolerance | Concentration | Cost-Efficiency | Liquidity |
|------------------|------------------|-------------|----------------|----------------|-----------------|-----------|
| Conservative     | 20%              | 15%         | 20%            | 15%            | 10%             | 20%       |
| Moderate         | 18%              | 18%         | 18%            | 18%            | 14%             | 14%       |
| Growth           | 15%              | 20%         | 15%            | 20%            | 15%             | 15%       |
| Aggressive       | 12%              | 22%         | 12%            | 22%            | 16%             | 16%       |

### Step 2: Concentration Risk Screening
Calculate concentration metrics and flag excess concentration.

#### Concentration Metrics:

1. **Herfindahl-Hirschman Index (HHI)**:
```
HHI = sum(weight_i^2 for all positions) * 10000

Interpretation:
- < 1000: Low concentration
- 1000-1800: Moderate concentration
- > 1800: High concentration
```

2. **Largest Position Weight**:
```
Flag if > 20% of portfolio (single position risk)
Critical if > 40% (severe concentration)
```

3. **Sector Concentration**:
```
Flag if any sector > 25% of equity holdings
Critical if > 40% of total portfolio
```

4. **Geographic Concentration**:
```
Flag if home country > 80% (home bias)
Critical if > 95% (extreme home bias)
```

5. **Asset Class Concentration**:
```
Flag if any asset class deviates > 15% from strategic allocation
Critical if single asset class > 70%
```

#### Concentration Risk Categories:
- **CRITICAL (Red Flag)**: Single position > 40% OR HHI > 2500
- **HIGH (Orange Flag)**: Single position > 20% OR HHI > 1800
- **MODERATE (Yellow Flag)**: Single position > 10% OR HHI > 1000
- **ACCEPTABLE (Green)**: All metrics below thresholds

### Step 3: Leverage Risk Screening
Detect and flag leverage across all position types.

#### Leverage Detection:
```python
leverage_sources = []

# Check for:
# 1. Margin debt
if portfolio.has_margin_debt:
    leverage_sources.append("Margin debt")

# 2. Options/futures
if portfolio.has_derivatives:
    leverage_sources.append("Derivatives (options/futures)")

# 3. Leveraged ETFs (2x, 3x, inverse)
if position.symbol.startswith(("PRO", "SSO", "UBT", "UGL", "TQQQ", "UPRO")):
    leverage_sources.append(f"Leveraged ETF: {position.symbol}")

# 4. Crypto leverage (futures, perpetuals)
if position.is_crypto_perpetual_or_future:
    leverage_sources.append(f"Crypto leverage: {position.symbol}")

# 5. Portfolio margin
if account.type == "Portfolio Margin":
    leverage_sources.append("Portfolio margin account")
```

#### Leverage Risk Calculation:
```
Gross Exposure = (Long positions + Short positions absolute) / Portfolio Value
Net Exposure = (Long positions - Short positions) / Portfolio Value

Leverage Ratio = Gross Exposure

Risk levels:
- < 1.2: Minimal leverage
- 1.2-1.5: Low leverage
- 1.5-2.0: Moderate leverage (FLAG)
- > 2.0: High leverage (CRITICAL FLAG)
```

#### Leverage Risk Categories:
- **CRITICAL**: Gross exposure > 2.5x OR short derivatives > 50% of portfolio
- **HIGH**: Gross exposure > 2.0x OR leverage from multiple sources
- **MODERATE**: Gross exposure 1.5-2.0x OR single leverage source
- **LOW**: Gross exposure < 1.5x OR no leverage detected

### Step 4: Illiquidity Risk Screening
Identify positions that may be difficult to sell quickly without significant price impact.

#### Illiquidity Metrics:
1. **Trading Volume** (for stocks/ETFs):
```
Daily volume < $1M: Highly illiquid (FLAG)
Daily volume < $10M: Moderately illiquid
Daily volume >= $10M: Generally liquid
```

2. **Asset Class Liquidity**:
```
High liquidity: Major stock ETFs (VTI, VOO, etc.), Treasuries
Medium liquidity: Individual stocks > $1B market cap, major bond ETFs
Low liquidity: Small cap stocks, municipal bonds, corporate bonds
Very low: Crypto altcoins, microcaps, private placements, alternatives
```

3. **Position Size vs Volume**:
```
If position_value > 10% of avg_daily_volume: CRITICAL
If position_value > 5% of avg_daily_volume: FLAG
```

4. **Bid-Ask Spread**:
```
Spread > 2%: Highly illiquid (CRITICAL)
Spread 1-2%: Moderately illiquid (FLAG)
Spread < 1%: Acceptable for most assets
Spread < 0.1%: Highly liquid
```

#### Illiquidity Risk Categories:
- **CRITICAL**: Position > 10% of daily volume OR spread > 2%
- **HIGH**: Position > 5% of daily volume OR spread > 1% OR > 20% in alternatives
- **MODERATE**: 10-20% in alternatives OR some microcaps
- **LOW**: Mostly liquid assets with minimal illiquid exposure

### Step 5: Risk-Tolerance Mismatch Analysis
Compare portfolio risk profile to stated investor risk tolerance.

#### Risk Profile Calculation:

```python
# Portfolio risk score (0-100)
portfolio_risk_score = (
    equity_allocation * 0.3 +
    crypto_allocation * 0.5 +
    alternatives_allocation * 0.2 +
    volatility_measure * 0.2 +
    concentration_penalty * 0.1 +
    leverage_penalty * 0.2 +
    (1 - liquidity_ratio) * 0.1
)

# Map to tolerance categories:
# 0-30: Conservative
# 31-50: Moderate
# 51-70: Growth
# 71-100: Aggressive
```

#### Tolerance Mismatch Detection:
```
IF stated_tolerance != calculated_tolerance_category:
    mismatch_severity = abs(stated_score - calculated_score) / 25

    IF mismatch_severity > 1.0: CRITICAL MISMATCH
    ELIF mismatch_severity > 0.5: HIGH MISMATCH
    ELIF mismatch_severity > 0.25: MODERATE MISMATCH
```

#### Specific Mismatch Patterns:
- **Conservative investor + Crypto > 10%**: HIGH mismatch
- **Conservative investor + Single stock > 20%**: HIGH mismatch
- **Conservative investor + Options/leverage**: CRITICAL mismatch
- **Moderate investor + Crypto > 20%**: MODERATE mismatch
- **Moderate investor + Leverage > 1.5x**: MODERATE mismatch
- **Aggressive investor + 100% cash**: HIGH mismatch (under-deployment)

### Step 6: Horizon Alignment Check
Verify portfolio structure aligns with investment time horizon.

#### Horizon-Asset Alignment Rules:
```
Short Horizon (< 3 years):
- Recommended: Cash + short-term bonds (≥70%)
- Flags if: Equities > 40% OR Bonds duration > 5 years
- Critical if: Crypto, alternatives, or long bonds > 20%

Medium Horizon (3-7 years):
- Recommended: Balanced 60/40 or 70/30 stocks/bonds
- Flags if: Cash > 40% OR Crypto > 15%
- Critical if: Single stock > 30% OR Leverage > 1.5x

Long Horizon (> 7 years):
- Recommended: Growth-oriented (80%+ equities)
- Flags if: Cash > 30% (under-deployment)
- Critical if: High-risk leverage > 2.0x without capacity
```

### Step 7: Output Risk Screening Report
Compile all flags into structured output for the scoring stage.

```markdown
## Risk Screening Report - Stage 2

### Framework Selection
Frameworks Applied: [list with rationale]
Dimension Weights: [table with weights per dimension]

### Risk Flags Summary
- CRITICAL: X issues
- HIGH: X issues
- MODERATE: X issues
- LOW: X issues

### Detailed Findings
[Per-risk-category detailed analysis]

### Framework-Scoring Alignment
[Which frameworks will be applied to which scoring dimensions]

### Proceed/Proceed with Caution/Hold Recommendation
[Based on overall risk profile]
```

## Outputs
- Selected evaluation frameworks with justification
- Dimension weights for scoring stage
- Comprehensive risk flag report (concentration, leverage, illiquidity)
- Risk-tolerance mismatch assessment
- Horizon alignment analysis
- Proceed/proceed with caution/hold recommendation

## Quality Gate
- [ ] At least 3 frameworks selected with clear rationale
- [ ] Dimension weights sum to 100%
- [ ] All four risk screens completed (concentration, leverage, illiquidity, tolerance)
- [ ] Critical flags identified and explained
- [ ] Horizon alignment assessed
- [ ] Output structured and ready for research stage

## Research & Evidence Requirements
Use WebSearch/WebFetch to verify:
- Current leverage ratios and norms for comparison
- Volume and spread data for illiquid positions
- Industry-standard concentration thresholds
- Risk tolerance assessment methodologies

Evidence tiers:
- **Tier 1**: Academic research on portfolio risk metrics
- **Tier 2**: Industry standards (CFA Institute, Morningstar)
- **Tier 3**: Regulatory guidance (FINRA, SEC concentration limits)

## Example Full Output

```
=== STAGE 2: RISK SCREENER ===

## Framework Selection

### Frameworks Applied for This Portfolio:

| Framework | Rationale | Application |
|-----------|-----------|-------------|
| Modern Portfolio Theory (Markowitz) | Multi-asset class portfolio with correlation opportunities | Diversification, allocation optimization |
| Capital Asset Pricing Model (CAPM) | Significant equity exposure requiring systematic risk evaluation | Risk-return, concentration analysis |
| Sharpe / Sortino Ratios | Need risk-adjusted return measurement for balanced portfolio | Risk-return scoring |
| Risk Parity & Strategic Asset Allocation | Multiple asset classes with different risk profiles | Allocation, risk-tolerance alignment |
| Diversification & Correlation Analysis | Concentration risk detected in tech sector | Concentration, correlation scoring |
| Monte Carlo Risk Simulation | Moderate risk tolerance with goal-based horizon | Risk-tolerance, liquidity scoring |

### Dimension Weights (Based on MODERATE Risk Profile):

| Dimension | Weight | Rationale |
|-----------|--------|-----------|
| Diversification & Correlation | 18% | Multi-asset portfolio, tech concentration noted |
| Risk-Adjusted Return | 18% | Core metric for performance evaluation |
| Allocation vs Risk Tolerance | 18% | Critical for moderate profile alignment |
| Concentration Risk | 18% | Tech and crypto concentration flagged |
| Cost & Tax Efficiency | 14% | Standard importance for moderate investor |
| Liquidity & Horizon Fit | 14% | Medium horizon with some goals at 5 years |

**SUM CHECK**: 100%

---

## Risk Flags Summary

🔴 **CRITICAL**: 0 issues
🟠 **HIGH**: 3 issues
🟡 **MODERATE**: 2 issues
🟢 **LOW**: 1 issue

---

## Detailed Risk Screening

### 1. Concentration Risk 🟠 HIGH

#### Herfindahl-Hirschman Index (HHI):
- **Calculated HHI**: 1,247
- **Interpretation**: Moderate concentration
- **Benchmark**: Diversified portfolio typically < 1,000

#### Largest Position Analysis:
| Position | Weight | Risk Level | Action |
|----------|--------|------------|--------|
| VTI | 10.2% | 🟢 Acceptable | Monitor |
| BND | 9.5% | 🟢 Acceptable | Acceptable |
| AAPL | 6.0% | 🟢 Acceptable | Acceptable |
| MSFT | 6.5% | 🟢 Acceptable | Acceptable |
| JEPI | 6.6% | 🟢 Acceptable | Acceptable |
| BTC | 5.7% | 🟡 Moderate | Monitor |

**Summary**: No single position exceeds 10% threshold. Largest positions are diversified ETFs.

#### Sector Concentration:
| Sector | Portfolio Weight | Typical Weight | Deviation | Risk Level |
|--------|------------------|----------------|-----------|------------|
| Technology | 28.4% | 20-25% | +3.4% to +8.4% | 🟡 Moderate |
| Financial Services | 12.1% | 12-15% | Within range | 🟢 Acceptable |
| Healthcare | 8.3% | 8-12% | Within range | 🟢 Acceptable |
| Real Estate (REITs) | 1.9% | 3-5% | -1.1% to -3.1% | 🟢 Acceptable |

**Flag**: Technology sector overweight by 3.4-8.4% vs typical allocation. Recommend monitoring.

#### Geographic Concentration:
| Region | Weight | Home Bias Threshold | Risk Level |
|--------|--------|---------------------|------------|
| United States (Domestic) | 76.8% | < 80% | 🟢 Acceptable |
| Developed International | 5.1% | 15-25% recommended | 🟡 Underweight |
| Emerging Markets | 1.4% | 5-10% recommended | 🟡 Underweight |
| Global/Crypto | 16.7% | — | 🟡 Moderate |

**Flag**: Moderate home bias. International diversification below recommendations.

#### Asset Class Concentration:
| Asset Class | Weight | Strategic Target | Deviation | Risk Level |
|-------------|--------|-------------------|-----------|------------|
| Equities | 55.2% | 60-70% | -4.8% to -14.8% | 🟢 Acceptable |
| Fixed Income | 23.4% | 20-30% | Within range | 🟢 Acceptable |
| Crypto | 7.6% | 0-5% | +2.6% to +7.6% | 🟠 HIGH |
| Cash | 12.5% | 5-15% | Within range | 🟢 Acceptable |
| Alternatives | 1.3% | 5-10% | -3.7% to -8.7% | 🟢 Acceptable |

**Flag**: Crypto allocation above recommended range for moderate risk tolerance.

### 2. Leverage Risk 🟢 LOW

#### Leverage Detection Results:
- ✅ No margin debt detected
- ✅ No options/futures positions
- ✅ No leveraged ETFs (2x, 3x, inverse)
- ✅ No crypto leverage or perpetuals
- ✅ Standard margin account type

#### Leverage Calculation:
- **Gross Exposure**: 1.0x (no leverage)
- **Net Exposure**: 1.0x (fully invested)
- **Leverage Ratio**: 1.0x

**Assessment**: Minimal leverage risk. No flags.

### 3. Illiquidity Risk 🟠 HIGH

#### Liquidity Analysis by Asset Class:

| Asset Class | Daily Volume (Est.) | Position Size | % of Volume | Risk Level |
|-------------|---------------------|----------------|-------------|------------|
| VTI | $2.5B | $48,600 | 0.002% | 🟢 Liquid |
| BND | $800M | $45,200 | 0.006% | 🟢 Liquid |
| BTC | $2B | $27,500 | 0.001% | 🟢 Liquid |
| ETH | $1B | $9,280 | 0.001% | 🟢 Liquid |
| USDC (Stablecoin) | $5B | $5,000 | 0.0001% | 🟢 Liquid |
| Individual Treasury Bond | — | $10,000 | — | 🟢 Liquid (Treasuries) |
| CD | — | $25,000 | — | 🟡 Illiquid (time lock) |

#### Illiquidity Flags:
- 🟠 **HIGH**: CD position of $25,000 (5.2% of portfolio) may have early withdrawal penalties
- 🟡 **MODERATE**: Individual Treasury bond requires selling via broker, may have spread costs
- 🟢 **LOW**: All ETF and crypto positions trade on liquid markets with sub-1% spreads

#### Overall Liquidity Assessment:
- **Highly Liquid**: 82.3% (ETFs, major crypto, Treasuries)
- **Moderately Liquid**: 5.2% (CD - with time lock)
- **Liquid with constraints**: 12.5% (Cash equivalents)

**Recommendation**: Most portfolio is liquid. CD should be considered for 5-year down payment goal.

### 4. Risk-Tolerance Mismatch 🟡 MODERATE

#### Stated vs Calculated Risk Profile:

| Attribute | Stated | Calculated | Match |
|-----------|--------|------------|-------|
| Risk Category | Moderate | Moderate-Growth | ✅ Aligned |
| Risk Score | 45/100 | 52/100 | ⚠️ Slight variance |

#### Variance Sources:
- Crypto allocation (7.6%) pushes toward Growth profile
- Tech concentration (28.4%) adds volatility
- Cash buffer (12.5%) provides stability for Moderate profile

#### Specific Tolerance Checks:
| Check | Result | Risk Level |
|-------|--------|------------|
| Conservative + Crypto > 10%? | N/A (Moderate profile) | ✅ N/A |
| Moderate + Crypto > 20%? | 7.6% < 20% | ✅ Pass |
| Moderate + Single stock > 20%? | Max 6.5% | ✅ Pass |
| Moderate + Leverage > 1.5x? | 1.0x | ✅ Pass |
| Moderate + Concentration > 30% single asset? | Max 10.2% | ✅ Pass |

**Assessment**: 🟡 **MODERATE MISMATCH** - Slightly more aggressive than stated due to tech concentration and crypto, but within acceptable variance. Recommend reviewing risk tolerance if market volatility increases.

### 5. Horizon Alignment 🟡 MODERATE

#### Stated Horizon Analysis:
- **Primary Horizon**: 10+ years (retirement)
- **Secondary Horizon**: 5 years (house down payment)
- **Effective Horizon**: Medium-term (5-10 years)

#### Alignment with Portfolio Structure:

| Horizon Check | Portfolio Reality | Recommendation | Risk Level |
|---------------|-------------------|----------------|------------|
| Medium horizon allocation | 55.2% equity / 23.4% fixed | ✅ Appropriate | 🟢 Good |
| Down payment protection | 12.5% cash + 5.2% CD + 3.4% TIPS | ✅ Adequate for 5-year goal | 🟢 Good |
| Growth for retirement | 55.2% equity + 7.6% crypto | ✅ Growth-oriented | 🟢 Good |
| Liquidity for goals | Cash + CD + TIPS = 21.1% | ✅ Sufficient liquidity | 🟢 Good |

#### Horizon-Specific Recommendations:
- **5-year down payment**: Consider separating $40,000-50,000 into conservative allocation (60% short-term bonds, 40% cash)
- **10-year retirement**: Current allocation appropriate for growth phase

**Assessment**: 🟡 **MODERATE ALIGNMENT** - Portfolio structure supports stated horizons, but consider segregating down payment funds.

---

## Risk Screening Summary

### Critical Issues Requiring Immediate Attention:
None detected.

### High-Priority Issues:
1. **Crypto allocation above moderate profile** (7.6% vs 0-5% recommended)
2. **International underweight** (6.5% total vs 20-35% recommended)
3. **CD illiquidity** for potential early withdrawal needs

### Moderate-Priority Issues:
1. **Technology sector concentration** (+3.4% to +8.4% overweight)
2. **Slight risk-tolerance variance** (calculated 52 vs stated 45)
3. **Horizon goal fund segregation** recommended for down payment

### Low-Priority Issues:
1. **Emerging markets underweight** (1.4% vs 5-10%)

---

## Recommendation

✅ **PROCEED WITH CAUTION**

Portfolio is suitable for detailed analysis with the following caveats:
- Address high-priority issues in improvement roadmap
- Monitor tech concentration and crypto allocation
- Consider international diversification improvements
- Evaluate goal-based account segregation

Risk level is acceptable for MODERATE risk tolerance profile but slightly aggressive. Proceeding to scoring stage with selected frameworks and dimension weights.

---

## Framework-to-Dimension Mapping

| Dimension | Primary Framework(s) | Secondary Framework(s) |
|-----------|---------------------|------------------------|
| Diversification & Correlation | Diversification & Correlation Analysis | MPT, Risk Parity |
| Risk-Adjusted Return | Sharpe / Sortino Ratios | CAPM, Fama-French |
| Allocation vs Risk Tolerance | Risk Parity & Strategic Asset Allocation | MPT, Monte Carlo |
| Concentration Risk | Diversification & Correlation Analysis | CAPM, HHI metrics |
| Cost & Tax Efficiency | Strategic Asset Allocation | Industry benchmarks |
| Liquidity & Horizon Fit | Monte Carlo Risk Simulation | Risk Parity |

---

## STAGE 2 COMPLETE - PASSING TO RESEARCH STAGE

**Next**: Evidence gathering for framework application, then scoring analysis
