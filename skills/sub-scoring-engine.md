---
name: sub-scoring-engine
description: (investment-portfolio-analyzer) Score the portfolio across six dimensions using MPT metrics and correlation analysis.
---

# Sub-skill: scoring-engine

## Purpose
Score the portfolio across six dimensions using Modern Portfolio Theory metrics, correlation analysis, and framework-grounded calculations. Produce quantitative scores (0-5) for each dimension with explicit citations and justifications.

## When the Harness Calls This
Stage matching `sub-scoring-engine` in the `investment-portfolio-analyzer` main workflow. Runs after research stage, using selected frameworks from risk screener.

## Inputs
- Normalized portfolio from Stage 1
- Risk screening results from Stage 2
- Selected frameworks and dimension weights
- Research evidence from WebSearch/WebFetch
- Investor profile (risk tolerance, horizon, goals)

## Scoring Framework

### Scoring Scale (0-5)
| Score | Descriptor | Meaning |
|-------|------------|---------|
| 5 | Excellent | Best practice or near-optimal for this profile |
| 4 | Good | Above average, minor improvements possible |
| 3 | Adequate | Meets minimum standards, room for improvement |
| 2 | Fair | Below average, notable issues present |
| 1 | Poor | Significant problems requiring attention |
| 0 | Critical | Major risks or misalignment |

### Scoring Formula
For each dimension, calculate a raw score (0-100), then map to 0-5 scale:

```
Raw_Score = (metric_value - min_threshold) / (max_threshold - min_threshold) * 100
Final_Score = floor(Raw_Score / 20)  # Maps 0-100 to 0-5

Special cases:
- If metric < min_critical: Score = 0
- If metric >= excellent_threshold: Score = 5
```

## Dimension 1: Diversification & Correlation

### Metrics Calculated

#### 1.1 Herfindahl-Hirschman Index (HHI)
```python
HHI = sum(weight_i^2 for all positions) * 10000

Score mapping:
- HHI <= 800: Score 5 (Excellent diversification)
- HHI 801-1200: Score 4 (Good)
- HHI 1201-1800: Score 3 (Adequate)
- HHI 1801-2500: Score 2 (Fair - concentration present)
- HHI 2501-3500: Score 1 (Poor - high concentration)
- HHI > 3500: Score 0 (Critical - severe concentration)
```

#### 1.2 Correlation Matrix Analysis
```python
# Calculate average pairwise correlation for equity holdings
avg_correlation = mean(corr(i, j) for all equity pairs i, j)

Score mapping:
- avg_corr <= 0.3: Score 5 (Excellent - low correlation)
- avg_corr 0.31-0.5: Score 4 (Good)
- avg_corr 0.51-0.7: Score 3 (Adequate)
- avg_corr 0.71-0.8: Score 2 (Fair - high correlation)
- avg_corr > 0.8: Score 1 (Poor - very high correlation)
```

#### 1.3 Asset Class Count
```python
asset_class_count = len(unique_asset_classes)

Score mapping:
- >= 6 asset classes: +1 bonus
- 4-5 asset classes: 0
- 2-3 asset classes: -1 penalty
- 1 asset class: -2 penalty
```

#### 1.4 Geographic Diversification
```python
geographic_score = 0
regions = [domestic, developed_intl, emerging, frontier]

regions_present = len([r for r in regions if allocation[r] > 5%])
if regions_present >= 4: geographic_score = +1
elif regions_present >= 3: geographic_score = 0
elif regions_present == 2: geographic_score = -1
else: geographic_score = -2
```

### Combined Score Calculation
```python
def calculate_diversification_score(hhi, avg_corr, asset_classes, geographic):
    base_score = 0

    # HHI component (40% weight)
    if hhi <= 800: base_score += 2.0
    elif hhi <= 1200: base_score += 1.6
    elif hhi <= 1800: base_score += 1.2
    elif hhi <= 2500: base_score += 0.8
    elif hhi <= 3500: base_score += 0.4

    # Correlation component (30% weight)
    if avg_corr <= 0.3: base_score += 1.5
    elif avg_corr <= 0.5: base_score += 1.2
    elif avg_corr <= 0.7: base_score += 0.9
    elif avg_corr <= 0.8: base_score += 0.6
    else: base_score += 0.3

    # Asset class component (15% weight)
    base_score += max(-1, min(1, (asset_classes - 4) * 0.5)) * 0.75

    # Geographic component (15% weight)
    base_score += max(-1, min(1, geographic)) * 0.75

    # Clamp to 0-5
    return max(0, min(5, round(base_score)))
```

### Example Output
```markdown
### Dimension 1: Diversification & Correlation - Score: 4/5

**Metrics:**
- HHI: 1,247 (Moderate concentration)
- Average Equity Correlation: 0.42 (Good diversification)
- Asset Classes: 5 (Stocks, ETFs, Bonds, Crypto, Cash)
- Geographic Regions: 3 (US, Developed Intl, Emerging)

**Analysis:**
Portfolio demonstrates good diversification across asset classes with five distinct categories represented. The HHI of 1,247 indicates moderate concentration, primarily driven by ETF allocations which themselves provide internal diversification. Correlation analysis shows equity holdings have average pairwise correlation of 0.42, suggesting reasonable diversification benefits. Geographic exposure includes three regions but emerging markets allocation is minimal (1.4%).

**Strengths:**
- Multiple asset classes reduce systematic risk
- Core ETF positions provide broad market exposure
- Low correlation between bonds and equities

**Areas for Improvement:**
- Increase emerging markets exposure to 5-10%
- Consider adding alternatives (REITs, commodities) to 5-10%
- Reduce HHI below 1000 through broader security selection

**Framework Application:**
Modern Portfolio Theory (Markowitz) suggests the portfolio lies on the efficient frontier for its risk level, but could improve through:
1. Increased international diversification (reduce home bias from 76.8% to ~60%)
2. Slight increase in alternatives for correlation benefits

**Evidence:**
[1] CFA Institute, "Portfolio Diversification: Theory and Practice" (2024) - recommends HHI < 1000 for optimal diversification
[2] Vanguard, "Global Allocation Recommendations" (2023) - suggests 20-35% international for US investors
```

## Dimension 2: Risk-Adjusted Return

### Metrics Calculated

#### 2.1 Sharpe Ratio (Estimated)
```python
def estimate_sharpe_ratio(portfolio):
    # Use historical returns based on asset allocation
    # Risk-free rate: current 10-year Treasury yield
    rf_rate = get_current_risk_free_rate()  # Approx 4.5% in 2026

    # Expected returns by asset class (based on historical + forward estimates)
    expected_returns = {
        'us_equities': 0.085,  # 8.5%
        'intl_equities': 0.075,
        'bonds': 0.045,
        'crypto': 0.15,  # High volatility adjusted
        'cash': 0.045,
    }

    # Portfolio expected return
    expected_return = sum(weight * expected_returns[asset_class]
                          for position in portfolio)

    # Portfolio volatility (estimated by asset class)
    volatilities = {
        'us_equities': 0.18,
        'intl_equities': 0.20,
        'bonds': 0.08,
        'crypto': 0.80,
        'cash': 0.01,
    }

    portfolio_volatility = calculate_portfolio_volatility(
        weights, volatilities, correlation_matrix
    )

    sharpe = (expected_return - rf_rate) / portfolio_volatility
    return sharpe

Score mapping:
- Sharpe >= 1.5: Score 5 (Excellent risk-adjusted returns)
- Sharpe 1.0-1.49: Score 4 (Good)
- Sharpe 0.5-0.99: Score 3 (Adequate)
- Sharpe 0.25-0.49: Score 2 (Fair)
- Sharpe 0-0.24: Score 1 (Poor)
- Sharpe < 0: Score 0 (Critical - underperforming risk-free)
```

#### 2.2 Sortino Ratio (Downside Risk)
```python
def calculate_sortino_ratio(portfolio, target_return=rf_rate):
    # Focus on downside volatility only
    downside_returns = [r for r in portfolio_returns if r < target_return]
    downside_deviation = std(downside_returns)

    expected_return = calculate_expected_return(portfolio)
    sortino = (expected_return - target_return) / downside_deviation

    return sortino

Score mapping (similar to Sharpe):
- Sortino >= 2.0: Score 5 (Excellent downside protection)
- Sortino 1.5-1.99: Score 4 (Good)
- Sortino 1.0-1.49: Score 3 (Adequate)
- Sortino 0.5-0.99: Score 2 (Fair)
- Sortino 0.25-0.49: Score 1 (Poor)
- Sortino < 0.25: Score 0 (Critical)
```

#### 2.3 Information Ratio (vs Benchmark)
```python
# Compare to appropriate benchmark (e.g., 60/40 portfolio)
benchmark_returns = get_benchmark_returns("60_40_portfolio")
active_returns = portfolio_returns - benchmark_returns
tracking_error = std(active_returns)
information_ratio = mean(active_returns) / tracking_error

Score mapping:
- IR >= 1.0: Score 5 (Outperforming benchmark significantly)
- IR 0.5-0.99: Score 4 (Moderately outperforming)
- IR 0.25-0.49: Score 3 (Matching benchmark)
- IR 0-0.24: Score 2 (Slightly underperforming)
- IR -0.24 to -0.49: Score 1 (Underperforming)
- IR < -0.5: Score 0 (Significantly underperforming)
```

### Combined Score Calculation
```python
def calculate_risk_adjusted_return_score(sharpe, sortino, ir):
    # Weighted combination
    # Sharpe: 50%, Sortino: 30%, IR: 20%

    def normalize_to_5(value, thresholds):
        if value >= thresholds[0]: return 5
        if value >= thresholds[1]: return 4
        if value >= thresholds[2]: return 3
        if value >= thresholds[3]: return 2
        if value >= thresholds[4]: return 1
        return 0

    sharpe_score = normalize_to_5(sharpe, [1.5, 1.0, 0.5, 0.25, 0])
    sortino_score = normalize_to_5(sortino, [2.0, 1.5, 1.0, 0.5, 0.25])
    ir_score = normalize_to_5(ir, [1.0, 0.5, 0.25, 0, -0.24])

    final_score = (sharpe_score * 0.5 + sortino_score * 0.3 + ir_score * 0.2)
    return round(final_score)
```

### Example Output
```markdown
### Dimension 2: Risk-Adjusted Return - Score: 3/5

**Metrics:**
- Estimated Sharpe Ratio: 0.68 (Moderate)
- Estimated Sortino Ratio: 0.92 (Adequate downside protection)
- Information Ratio (vs 60/40 benchmark): 0.18 (Slightly underperforming)

**Analysis:**
Portfolio exhibits moderate risk-adjusted returns. The estimated Sharpe ratio of 0.68 indicates adequate compensation for volatility taken, though below the 1.0+ threshold for "good" risk-adjusted performance. The Sortino ratio of 0.92 suggests better downside protection than overall volatility implies, due to the bond allocation cushioning equity drawdowns.

**Decomposition:**
- Expected annual return: 7.2% (pre-tax)
- Expected volatility: 15.8%
- Risk-free rate: 4.5% (current 10-year Treasury)
- Excess return: 2.7%

**Strengths:**
- Bond allocation (23.4%) provides downside cushion
- Dividend-focused ETFs (SCHD, JEPI) offer income stability
- Cash buffer (12.5%) reduces drawdown risk

**Areas for Improvement:**
- Crypto allocation (7.6%) adds volatility without commensurate returns for moderate profile
- Consider reducing tech concentration to lower portfolio beta
- International diversification could improve risk-adjusted returns

**Framework Application:**
CAPM analysis indicates the portfolio has a beta of approximately 1.05, suggesting slightly higher systematic risk than the market. Given the moderate risk tolerance, consider reducing beta toward 0.95-1.0 through:
1. Slight increase in bond allocation to 25-28%
2. Reduction in high-beta tech names
3. Maintaining quality dividend growers

**Evidence:**
[3] Sharpe, W. "The Sharpe Ratio" (Journal of Portfolio Management, 1994) - methodology foundation
[4] Morningstar, "Risk-Adjusted Return Methodologies" (2025) - classification standards
```

## Dimension 3: Allocation vs Risk Tolerance

### Metrics Calculated

#### 3.1 Risk Capacity Analysis
```python
def calculate_risk_capacity(portfolio, investor_profile):
    # Risk capacity: ability to withstand losses
    capacity_score = 0

    # Time horizon factor
    if investor_profile.horizon >= 10: capacity_score += 2
    elif investor_profile.horizon >= 5: capacity_score += 1
    else: capacity_score += 0

    # Wealth factor (relative to portfolio value)
    if investor_profile.net_worth / portfolio_value >= 5: capacity_score += 2
    elif investor_profile.net_worth / portfolio_value >= 2: capacity_score += 1
    else: capacity_score += 0

    # Income stability factor
    if investor_profile.income_stability == "High": capacity_score += 1
    elif investor_profile.income_stability == "Medium": capacity_score += 0.5

    return capacity_score
```

#### 3.2 Risk Required Analysis
```python
def calculate_risk_required(goals, current_value, target_value, time_horizon):
    # Required return to achieve goals
    required_return = (target_value / current_value) ** (1 / time_horizon) - 1

    # Risk level needed for that return
    if required_return <= 0.03: risk_required = "Low"
    elif required_return <= 0.06: risk_required = "Moderate"
    elif required_return <= 0.09: risk_required = "Growth"
    else: risk_required = "Aggressive"

    return risk_required, required_return
```

#### 3.3 Risk Tolerance Alignment Score
```python
def calculate_risk_tolerance_alignment(
    portfolio_risk_score,
    risk_capacity,
    risk_required,
    stated_tolerance
):
    # Calculate alignment between all three risk dimensions
    alignment_score = 5

    # Portfolio risk vs capacity
    if portfolio_risk_score > risk_capacity + 1:
        alignment_score -= 2  # Taking more risk than capacity allows
    elif portfolio_risk_score < risk_capacity - 1:
        alignment_score -= 1  # Under-deployed relative to capacity

    # Portfolio risk vs required
    risk_map = {"Low": 1, "Moderate": 2, "Growth": 3, "Aggressive": 4}
    portfolio_level = risk_map[calculate_portfolio_risk_level(portfolio)]
    required_level = risk_map[risk_required]

    if abs(portfolio_level - required_level) > 1:
        alignment_score -= 1

    # Portfolio risk vs stated tolerance
    stated_level = risk_map[stated_tolerance]
    if abs(portfolio_level - stated_level) > 1:
        alignment_score -= 1

    return max(0, min(5, alignment_score))
```

### Score Mapping
```python
def score_allocation_vs_tolerance(alignment_score, capacity_utilization):
    # alignment_score: 0-5 from above
    # capacity_utilization: % of risk capacity being used

    base_score = alignment_score

    # Adjust for capacity utilization
    if 80% <= capacity_utilization <= 100%:
        base_score = min(5, base_score + 0.5)
    elif capacity_utilization < 60%:
        base_score = max(0, base_score - 0.5)  # Under-deployed

    return round(base_score)
```

### Example Output
```markdown
### Dimension 3: Allocation vs Risk Tolerance - Score: 4/5

**Metrics:**
- Risk Capacity: High (10+ year horizon, regular contributions)
- Risk Required: Moderate-Growth (7.2% expected return meets goals)
- Portfolio Risk Level: Moderate-Growth (Score: 2.6/4)
- Stated Tolerance: Moderate
- Capacity Utilization: 78%

**Analysis:**
Portfolio allocation aligns well with stated risk tolerance. The moderate-growth risk profile matches both the investor's capacity (high, due to long horizon and accumulation pattern) and requirements (7.2% expected return sufficient for retirement goals). Slight variance exists as portfolio leans toward growth due to tech concentration and crypto allocation.

**Risk Decomposition:**
- Capacity: HIGH (10+ year horizon, +$2,000/mo contributions, age-appropriate)
- Required: MODERATE (Goals achievable with 6-8% returns)
- Deployed: MODERATE-GROWTH (Portfolio volatility: 15.8%)
- Stated: MODERATE (Questionnaire result)

**Alignment Assessment:**
- ✅ Capacity matches required (sufficient runway for growth)
- ✅ Deployed risk matches capacity (not over-extending)
- ⚠️ Deployed risk slightly exceeds stated (2.6 vs 2.0)
- ✅ Capacity utilization healthy (78% - room for flexibility)

**Strengths:**
- Long horizon allows growth orientation without excessive risk
- Regular contributions reduce sequence-of-returns risk
- Emergency fund represented in cash allocation

**Areas for Improvement:**
- Reduce crypto allocation to align with stated moderate tolerance
- Slight increase in bonds would better match stated profile
- Consider segregating high-risk assets in "risk bucket"

**Framework Application:**
Risk Parity analysis suggests the portfolio risk contribution is approximately:
- Equities: 75% of total risk
- Bonds: 15% of total risk
- Crypto: 8% of total risk
- Cash: 2% of total risk

For moderate tolerance, target risk contributions should be closer to:
- Equities: 65%
- Bonds: 25%
- Alternatives: 10%

**Evidence:**
[5] CFA Institute, "Risk Tolerance Assessment Frameworks" (2024)
[6] Vanguard, "Risk Capacity vs Risk Tolerance" (Investment Philosophy, 2025)
```

## Dimension 4: Concentration Risk

### Metrics Calculated

#### 4.1 Single Position Concentration
```python
max_position_weight = max(position.weight for position in portfolio)

concentration_penalty = 0
if max_position_weight > 0.40: concentration_penalty = 3  # Critical
elif max_position_weight > 0.25: concentration_penalty = 2  # High
elif max_position_weight > 0.15: concentration_penalty = 1  # Moderate
elif max_position_weight > 0.10: concentration_penalty = 0.5  # Slight
```

#### 4.2 Sector Concentration
```python
def calculate_sector_concentration(portfolio):
    sector_weights = aggregate_by_sector(portfolio)
    max_sector = max(sector_weights.values())
    concentration_count = len([w for w in sector_weights.values() if w > 0.10])

    score_impact = 0
    if max_sector > 0.40: score_impact = 2
    elif max_sector > 0.30: score_impact = 1.5
    elif max_sector > 0.25: score_impact = 1
    elif max_sector > 0.20: score_impact = 0.5

    # Additional penalty for multiple concentrated sectors
    if concentration_count > 2:
        score_impact += 0.5

    return score_impact
```

#### 4.3 Geographic Concentration
```python
def calculate_geographic_concentration(portfolio, home_country):
    home_weight = portfolio.allocation[home_country]

    if home_weight > 0.90: return 1.5  # Severe home bias
    elif home_weight > 0.80: return 1.0  # Moderate home bias
    elif home_weight > 0.70: return 0.5  # Slight home bias
    else: return 0  # Good international diversification
```

#### 4.4 Asset Class Concentration
```python
def calculate_asset_class_concentration(portfolio):
    asset_class_weights = aggregate_by_asset_class(portfolio)
    max_asset_class = max(asset_class_weights.values())

    if max_asset_class > 0.80: return 2  # Critical imbalance
    elif max_asset_class > 0.70: return 1.5
    elif max_asset_class > 0.60: return 1
    else: return 0  # Balanced
```

### Combined Score Calculation
```python
def calculate_concentration_score(
    max_position, sector_conc, geo_conc, asset_conc
):
    base_score = 5.0

    base_score -= max_position
    base_score -= sector_conc
    base_score -= geo_conc
    base_score -= asset_conc

    # Bonus for good diversification
    if max_position <= 0.10: base_score += 0.5
    if sector_conc == 0: base_score += 0.5
    if geo_conc == 0: base_score += 0.5

    return max(0, min(5, round(base_score)))
```

### Example Output
```markdown
### Dimension 4: Concentration Risk - Score: 3/5

**Metrics:**
- Maximum Single Position: 10.2% (VTI) - Acceptable
- Maximum Sector Weight: 28.4% (Technology) - Moderate concentration
- Home Country Bias: 76.8% (US) - Slight concentration
- Maximum Asset Class: 55.2% (Equities) - Balanced

**Analysis:**
Portfolio demonstrates moderate concentration risk. While no single position exceeds 10% threshold (good), sector concentration in technology (+3.4% to +8.4% above typical) and home country bias (76.8% vs 60-70% recommended) elevate concentration risk. Asset class allocation is balanced with no single class exceeding 60%.

**Concentration Breakdown:**
| Type | Current | Recommended | Variance | Risk Level |
|------|---------|-------------|----------|------------|
| Single Position | 10.2% (VTI) | < 10-15% | Within range | 🟢 Acceptable |
| Sector (Tech) | 28.4% | 20-25% | +3.4% to +8.4% | 🟡 Moderate |
| Geographic (US) | 76.8% | 60-70% | +6.8% to +16.8% | 🟡 Moderate |
| Asset Class (Equities) | 55.2% | 50-70% | Within range | 🟢 Acceptable |

**Specific Concentrations:**
- Technology: 28.4% (AAPL, MSFT, GOOGL, AMZN, NVDA, semiconductors)
- United States: 76.8% (home bias for US investor)
- Large-cap growth: Bias through VTI, SCHD, JEPI

**Strengths:**
- No single stock concentration (max individual stock: 6.5%)
- ETF positions provide internal diversification
- Multiple sectors represented (6+ sectors > 5% each)

**Areas for Improvement:**
- Reduce technology allocation to 20-25%
- Increase international allocation to 20-30%
- Consider small-cap or value factor exposure to diversify away from large-cap growth

**Framework Application:**
CAPM indicates that concentration in technology increases portfolio beta to approximately 1.15, making the portfolio more volatile than the market. Diversification benefits can be achieved through:
1. Adding value factor exposure (e.g., VTV, VBR)
2. Increasing small-cap allocation (e.g., VB, VWO)
3. Expanding international developed markets (e.g., VEA, VGK)

**Evidence:**
[7] Morningstar, "Sector Concentration Guidelines" (2025)
[8] CFA Institute, "International Diversification Benefits" (2024)
```

## Dimension 5: Cost & Tax Efficiency

### Metrics Calculated

#### 5.1 Expense Ratio Analysis
```python
def calculate_total_expense_ratio(portfolio):
    total_expense_ratio = sum(
        position.weight * position.expense_ratio
        for position in portfolio
    )

    # Score based on portfolio value
    if total_expense_ratio <= 0.05: score = 5  # Excellent (< 0.05%)
    elif total_expense_ratio <= 0.10: score = 4  # Good
    elif total_expense_ratio <= 0.20: score = 3  # Adequate
    elif total_expense_ratio <= 0.50: score = 2  # Fair
    elif total_expense_ratio <= 1.0: score = 1  # Poor
    else: score = 0  # Critical (> 1%)

    return total_expense_ratio, score
```

#### 5.2 Turnover & Trading Costs
```python
def estimate_annual_trading_cost(portfolio, turnover_rate):
    # Assume trading costs: 0.10% per trade (modern low-cost brokers)
    trading_cost = portfolio_value * turnover_rate * 0.001

    if turnover_rate <= 0.05: cost_score = 5  # Low turnover
    elif turnover_rate <= 0.25: cost_score = 4
    elif turnover_rate <= 0.50: cost_score = 3
    elif turnover_rate <= 0.75: cost_score = 2
    elif turnover_rate <= 1.0: cost_score = 1
    else: cost_score = 0  # High turnover (> 100% annually)

    return trading_cost, cost_score
```

#### 5.3 Tax Efficiency Analysis
```python
def calculate_tax_efficiency(portfolio, tax_status, investor_tax_bracket):
    tax_inefficiency_score = 0

    # Check for tax-inefficient holdings in taxable accounts
    for position in portfolio:
        if position.account_type == "Taxable":
            if position.asset_class in ["High-Yield Bond", "REIT", "Bond"]:
                # Interest income taxed at ordinary income rates
                tax_inefficiency_score += position.weight * 0.5
            elif position.type in ["Short-Term Capital Gains", "High Turnover"]:
                tax_inefficiency_score += position.weight * 0.3

    # Tax-efficient assets get credit
    if position.type in ["Municipal Bond", "ETF (Tax-Efficient)", "Index Fund"]:
        tax_inefficiency_score -= position.weight * 0.1

    tax_efficiency_score = 5 - tax_inefficiency_score
    return max(0, min(5, round(tax_efficiency_score)))
```

#### 5.4 Tax-Location Optimization
```python
def assess_tax_location(portfolio):
    # Check if assets are optimally located across account types
    optimal_placement = {
        "Taxable": ["ETFs", "Stocks", "Municipal Bonds", "Tax-Managed Funds"],
        "Tax-Deferred": ["Bonds", "REITs", "High-Yield", "High Turnover"],
        "Tax-Free": ["Growth", "High Tax Bracket Assets"]
    }

    misalignment_score = 0
    for position in portfolio:
        if position.asset_class not in optimal_placement[position.account_type]:
            misalignment_score += position.weight * 0.2

    return 5 - misalignment_score
```

### Combined Score Calculation
```python
def calculate_cost_tax_efficiency_score(
    expense_score, turnover_score, tax_eff_score, tax_loc_score
):
    # Weighted combination
    # Expense ratio: 35%, Turnover: 15%, Tax efficiency: 30%, Tax location: 20%

    final_score = (
        expense_score * 0.35 +
        turnover_score * 0.15 +
        tax_eff_score * 0.30 +
        tax_loc_score * 0.20
    )

    return round(final_score)
```

### Example Output
```markdown
### Dimension 5: Cost & Tax Efficiency - Score: 4/5

**Metrics:**
- Total Expense Ratio: 0.08% - Excellent
- Estimated Turnover: 8% (buy-and-hold) - Excellent
- Tax Efficiency: Good (mostly index ETFs, minimal short-term gains)
- Tax Location: Assumed optimal (mixed account types)

**Cost Breakdown:**
| Position | Weight | Expense Ratio | Weighted Cost |
|----------|--------|---------------|---------------|
| VTI | 10.2% | 0.03% | 0.003% |
| BND | 9.5% | 0.03% | 0.003% |
| VXUS | 5.1% | 0.08% | 0.004% |
| SCHD | 6.1% | 0.06% | 0.004% |
| JEPI | 6.6% | 0.68% | 0.045% |
| Individual Stocks | 17.7% | 0% | 0% |
| Crypto | 7.6% | Trading fees ~0.1% | 0.008% |
| **TOTAL** | **100%** | — | **0.08%** |

**Comparison:**
- Portfolio cost: 0.08% ($383/year on $478,350)
- Industry average: 0.50-1.00% ($2,391-$4,784/year)
- Savings: $2,008-$4,401/year vs average

**Tax Analysis:**
- **Tax-Efficient**: Index ETFs (VTI, VXUS), municipal positions, long-term holdings
- **Moderate Efficiency**: Dividend ETFs (SCHD, JEPI) - qualified dividends taxed at 15%
- **Considerations**: Crypto transactions may trigger capital gains, bond interest taxed as ordinary income

**Assumptions:**
- Mixed account structure (taxable + tax-advantaged) allows optimal placement
- Long-term buy-and-hold strategy minimizes turnover
- Tax-loss harvesting opportunities available in individual stock positions

**Strengths:**
- Very low expense ratio (0.08% vs 0.50% industry average)
- Index-based strategy minimizes turnover costs
- Tax-efficient fund selection (VTI, VXUS, SCHD)
- Individual stocks provide tax-loss harvesting opportunities

**Areas for Improvement:**
- JEPI (0.68% expense) represents 45% of total cost; consider alternatives if performance doesn't justify fee
- Consider tax-loss harvesting on positions with losses
- Optimal account placement if not already implemented

**Framework Application:**
Strategic Asset Allocation principles emphasize cost efficiency as a key determinant of long-term returns. The portfolio's 0.08% expense ratio adds approximately 0.42% annually vs average-cost funds, compounding to significant wealth accumulation over 10+ year horizons.

**Tax Optimization Recommendations:**
1. Place high-yield assets (JEPI, bonds) in tax-advantaged accounts
2. Use tax-loss harvesting on individual stock positions annually
3. Consider municipal bond allocation for taxable accounts if in high tax bracket
4. Hold international funds in taxable accounts to utilize foreign tax credit

**Evidence:**
[9] Vanguard, "The Impact of Fees on Investment Returns" (2024) - 0.42% annual advantage from low fees
[10] CFA Institute, "Tax-Efficient Investing Strategies" (2025)
```

## Dimension 6: Liquidity & Horizon Fit

### Metrics Calculated

#### 6.1 Liquidity Ratio Analysis
```python
def calculate_liquidity_ratio(portfolio):
    # Categorize positions by liquidity
    liquid_assets = sum(
        p.value for p in portfolio
        if p.liquidity_category in ["Cash", "Highly Liquid ETF", "Major Crypto"]
    )
    moderately_liquid = sum(
        p.value for p in portfolio
        if p.liquidity_category == "Moderately Liquid"
    )
    illiquid = sum(
        p.value for p in portfolio
        if p.liquidity_category in ["Illiquid", "Time-Locked"]
    )

    liquidity_ratio = liquid_assets / portfolio.total_value

    # Score based on liquidity needs
    if liquidity_ratio >= 0.80: score = 5
    elif liquidity_ratio >= 0.60: score = 4
    elif liquidity_ratio >= 0.40: score = 3
    elif liquidity_ratio >= 0.20: score = 2
    else: score = 1

    return liquidity_ratio, score, {
        "liquid": liquid_assets,
        "moderate": moderately_liquid,
        "illiquid": illiquid
    }
```

#### 6.2 Horizon Matching
```python
def assess_horizon_match(portfolio, goals):
    mismatch_score = 0

    for goal in goals:
        goal_horizon = goal.time_until_needed
        goal_amount = goal.amount

        # Find assets allocated to this goal
        allocated_assets = find_assets_for_goal(portfolio, goal)

        # Check if asset duration matches goal horizon
        if goal_horizon <= 3:  # Short-term goal
            # Should be in cash + short-term bonds
            equity_ratio = calculate_equity_ratio(allocated_assets)
            if equity_ratio > 0.40:
                mismatch_score += (equity_ratio - 0.40) * 2

        elif goal_horizon <= 7:  # Medium-term goal
            # Should be balanced
            if equity_ratio > 0.70 or equity_ratio < 0.50:
                mismatch_score += abs(equity_ratio - 0.60) * 1

        else:  # Long-term goal
            # Can be growth-oriented
            if equity_ratio < 0.70:
                mismatch_score += (0.70 - equity_ratio) * 1

    return max(0, 5 - mismatch_score)
```

#### 6.3 Emergency Fund Adequacy
```python
def assess_emergency_fund(portfolio, monthly_expenses):
    cash_and_equivalents = sum(
        p.value for p in portfolio
        if p.asset_class in ["Cash", "Cash Equivalents", "Money Market"]
    )

    emergency_months = cash_and_equivalents / monthly_expenses

    if emergency_months >= 6: score = 5  # Excellent
    elif emergency_months >= 4: score = 4  # Good
    elif emergency_months >= 3: score = 3  # Adequate
    elif emergency_months >= 2: score = 2  # Fair
    elif emergency_months >= 1: score = 1  # Poor
    else: score = 0  # Critical

    return emergency_months, score
```

#### 6.4 RMD & Required Withdrawal Capacity
```python
def assess_rmd_capacity(portfolio, investor_age):
    # If near or in retirement, check RMD capacity
    if investor_age < 70:
        return 5  # Not applicable, score neutral

    # Calculate expected RMD
    expected_rmd = calculate_required_minimum_distribution(
        portfolio.tax_deferred_value,
        investor_age
    )

    # Check if portfolio has sufficient liquid assets for RMDs
    liquid_for_rmd = portfolio.liquid_assets / expected_rmd

    if liquid_for_rmd >= 2: return 5  # Can cover 2+ years of RMDs
    elif liquid_for_rmd >= 1.5: return 4
    elif liquid_for_rmd >= 1: return 3  # Can cover current year
    elif liquid_for_rmd >= 0.5: return 2
    else: return 1  # May need to sell illiquid assets
```

### Combined Score Calculation
```python
def calculate_liquidity_horizon_score(
    liquidity_score, horizon_score, emergency_score, rmd_score
):
    # Weighted combination based on life stage
    if investor.age < 50:
        # Pre-retirement: focus on horizon matching
        weights = [0.25, 0.40, 0.35, 0]
    elif investor.age < 70:
        # Near retirement: balance all factors
        weights = [0.30, 0.30, 0.25, 0.15]
    else:
        # Post-RMD: RMD capacity important
        weights = [0.30, 0.25, 0.20, 0.25]

    final_score = sum(
        score * weight
        for score, weight in zip(
            [liquidity_score, horizon_score, emergency_score, rmd_score],
            weights
        )
    )

    return round(final_score)
```

### Example Output
```markdown
### Dimension 6: Liquidity & Horizon Fit - Score: 4/5

**Metrics:**
- Liquidity Ratio: 82.3% (Highly Liquid) - Excellent
- Horizon Match: Good (goals aligned with asset duration)
- Emergency Fund: 4.2 months of expenses - Good
- RMD Capacity: N/A (pre-retirement)

**Liquidity Analysis:**
| Liquidity Category | Value | Portfolio % | Risk Level |
|--------------------|-------|-------------|------------|
| Highly Liquid | $393,000 | 82.3% | 🟢 Excellent |
| Moderately Liquid | $25,000 | 5.2% | 🟢 Acceptable |
| Illiquid / Time-Locked | $60,350 | 12.5% | 🟡 Monitor |

**Highly Liquid Assets ($393,000):**
- Major ETFs (VTI, VXUS, BND, SCHD, etc.): $295,000
- Major crypto (BTC, ETH): $36,780
- Cash equivalents (SHV): $30,090
- Stablecoins (USDC): $5,000
- Liquid Treasuries: $26,130

**Moderately Liquid Assets ($25,000):**
- Certificate of Deposit (CD): $25,000 (time-locked with penalty)

**Illiquid / Time-Locked Assets ($60,350):**
- Individual Treasury Bond: $10,000 (sell-through broker required)
- Alternative positions: $1,300 (REIT, gold - moderately liquid)
- Small-cap / micro positions: $49,050 (assume small positions have spread costs)

**Liquidity Assessment:**
- Primary liquidity is excellent (82.3%)
- ETF positions can be converted to cash within 1-2 days
- Crypto positions have 24/7 liquidity
- CD represents 5.2% and aligns with 5-year down payment goal

**Horizon Analysis:**
| Goal | Time Horizon | Amount | Allocated Assets | Match | Risk Level |
|------|--------------|--------|------------------|-------|------------|
| House Down Payment | 5 years | $50,000 | CD ($25k) + Cash + Bonds | ✅ Good | 🟢 Acceptable |
| Retirement (Growth) | 10+ years | $400,000 | Equities + Crypto | ✅ Excellent | 🟢 Appropriate |
| Emergency Fund | Ongoing | $30,000 | Cash + Equivalents | ⚠️ Slight | 🟡 Good (4.2 months) |

**Emergency Fund Assessment:**
- Current: $30,090 (SHV) + $5,000 (USDC) = $35,090
- Monthly expenses (estimated): $8,400
- Coverage: 4.2 months
- Status: Good (6 months recommended, 3-6 months acceptable)

**Recommendations:**
1. Increase emergency fund to 6 months ($50,400) in highly liquid cash
2. CD allocation ($25,000) appropriate for 5-year down payment goal
3. Consider additional $25,000 for down payment in short-term bonds

**Strengths:**
- Majority of portfolio (82.3%) highly liquid
- ETF positions trade on major exchanges with tight spreads
- Crypto provides 24/7 liquidity (albeit with volatility)
- Cash buffer appropriate for moderate risk tolerance

**Areas for Improvement:**
- Emergency fund slightly below 6-month target (4.2 vs 6.0 months)
- Consider segregating down payment funds into dedicated account
- Small positions may have spread costs on liquidation; consider consolidating

**Framework Application:**
Monte Carlo simulation (1,000 scenarios, 10-year horizon) indicates:
- 95% confidence interval: Portfolio value between $380K-$1.2M
- Liquidity stress test: Portfolio can handle $50,000 withdrawal without material impact
- Sequence-of-returns risk: Moderate (mitigated by regular contributions)

**Horizon-Specific Recommendations:**
1. **5-year down payment**: Protect $50,000 in conservative allocation (60% short-term bonds, 40% cash)
2. **10-year retirement**: Current equity allocation appropriate for growth phase
3. **Emergency**: Increase to 6 months cash cushion

**Evidence:**
[11] CFA Institute, "Liquidity Risk Management" (2025)
[12] Vanguard, "Emergency Fund Guidelines" (Investment Philosophy, 2024)
```

## Overall Score Calculation

### Weighted Score Formula
```python
def calculate_overall_score(dimension_scores, dimension_weights):
    """
    dimension_scores: dict of {dimension_name: score_0_to_5}
    dimension_weights: dict of {dimension_name: weight_percentage}
    """
    overall_score = sum(
        dimension_scores[dim] * (dimension_weights[dim] / 100)
        for dim in dimension_scores
    )
    return round(overall_score, 1)
```

### Score Interpretation
| Overall Score | Interpretation |
|---------------|----------------|
| 4.5-5.0 | Excellent - Portfolio well-optimized for profile |
| 4.0-4.4 | Very Good - Minor improvements possible |
| 3.5-3.9 | Good - Adequate with room for enhancement |
| 3.0-3.4 | Satisfactory - Meets minimum standards |
| 2.0-2.9 | Fair - Notable issues present |
| 1.0-1.9 | Poor - Significant problems |
| 0.0-0.9 | Critical - Major risks/misalignment |

## Outputs
- Six dimension scores (0-5) with metrics and justifications
- Framework citations for each dimension
- Overall portfolio score (0-5)
- Score interpretation and confidence level
- Identification of strengths and weaknesses by dimension

## Quality Gate
- [ ] All 6 dimensions scored (no missing dimensions)
- [ ] Each score has explicit calculation/metrics shown
- [ ] Framework cited for each dimension
- [ ] Evidence sources graded by tier
- [ ] Overall score calculated using approved weights
- [ ] Interpretation provided with confidence interval

## Research & Evidence Requirements
Use WebSearch/WebFetch for:
- Current risk-free rate for Sharpe ratio
- Historical returns by asset class
- Volatility and correlation data
- Industry benchmarks for comparison

Evidence tiers:
- **Tier 1**: Academic studies on scoring methodology
- **Tier 2**: Industry standards (CFA, Morningstar)
- **Tier 3**: Reputable financial institutions (Vanguard, BlackRock)
