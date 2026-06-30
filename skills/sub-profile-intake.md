---
name: sub-profile-intake
description: (investment-portfolio-analyzer) Capture holdings, risk tolerance, horizon and goals with a clear educational disclaimer.
---

# Sub-skill: profile-intake

## Purpose
Capture holdings, risk tolerance, investment horizon, and financial goals with a clear educational disclaimer. Extract and normalize portfolio data for downstream analysis.

## When the Harness Calls This
Stage matching `sub-profile-intake` in the `investment-portfolio-analyzer` main workflow. This is the first stage that transforms raw user input into a structured analysis profile.

## Inputs
- User-provided artifact (portfolio statement, holdings list, or description)
- Prior context (if user continues a previous session)
- Clarification responses to intake questions

## Procedure

### Step 1: Educational Disclaimer
Always begin by stating this analysis is educational only and not personalized financial advice:

```
DISCLAIMER: This analysis is for educational purposes only. It does not constitute
personalized financial advice, investment recommendations, or tax guidance. Consult
a qualified financial advisor and tax professional for decisions specific to your
situation.
```

### Step 2: Intake Question Sequence
Ask targeted questions to fill gaps in the user's input. Stop once sufficient data is collected.

#### Essential Data Points (must have for scoring):
1. **Holdings breakdown**: Assets by ticker/symbol, quantity, current value, asset class
   - If values missing: ask for approximate current market value or quantity
   - If symbols ambiguous: ask for ISIN or exchange
   - If asset class unclear: ask for asset type (stock, bond, ETF, mutual fund, crypto, cash, alternative)

2. **Risk tolerance**: Conservative / Moderate / Growth / Aggressive
   - If unclear: ask "How would you react to a 20% portfolio decline in one year?"
   - Options: "Sell everything", "Sell some", "Hold", "Buy more"

3. **Investment horizon**: Time until funds needed (years)
   - If unclear: ask "When do you expect to begin withdrawing from this portfolio?"
   - Categories: <3 years (short), 3-7 years (medium), 7+ years (long)

4. **Financial goals**: Income / Growth / Preservation / Speculation
   - If unclear: ask "What is the primary objective of this portfolio?"
   - Allow multiple goals with priority ranking

5. **Contribution/withdrawal pattern**: Regular contributions, withdrawals, or static
   - If unclear: ask "Do you add money regularly, withdraw, or mostly hold steady?"

#### Optional Data Points (enhance analysis):
- Tax situation: Tax-advantaged accounts vs taxable, tax bracket
- Geographic exposure: Home country, desired international diversification
- Sector preferences: Any sectors to avoid or overweight
- ESG/sustainability preferences
- Liquidity needs: Expected large withdrawals (house, education, business)

### Step 3: Portfolio Normalization
Transform raw input into standardized portfolio structure:

```markdown
## Portfolio Structure

| Ticker/Symbol | Asset Class | Quantity | Current Value | Weight (%) | Exchange/ISIN |
|---------------|-------------|----------|---------------|------------|---------------|
| AAPL          | Stock       | 150      | $28,500       | 14.2%      | NASDAQ        |
| BND           | ETF (Bond)  | 500      | $45,200       | 22.6%      | NASDAQ        |
| BTC-USD       | Crypto      | 0.5      | $21,500       | 10.8%      | -             |
| ...           | ...         | ...      | ...           | ...        | ...           |

**Total Portfolio Value**: $X,XXX,XXX
```

#### Asset Class Classification Rules:
- **Stocks**: Individual company shares, ADRs
- **ETFs**: Exchange-traded funds (classify by underlying: equity, bond, mixed, commodity)
- **Mutual Funds**: Active or passive funds (classify by underlying)
- **Bonds**: Government, corporate, municipal bonds (individual)
- **Crypto**: Cryptocurrencies, stablecoins
- **Cash**: Cash equivalents, money market, CDs
- **Alternatives**: REITs, commodities, private equity, hedge funds
- **Derivatives**: Options, futures (note leverage factor)

#### Geographic Classification:
- **Domestic**: User's home country
- **Developed Markets**: US, Japan, UK, Eurozone, Canada, Australia
- **Emerging Markets**: China, India, Brazil, Russia, South Africa, etc.
- **Frontier Markets**: Smaller, less liquid emerging economies

### Step 4: Validation Checks
Before passing to next stage, verify:

1. **Portfolio completeness**: Total weight sums to ~100% (allow 99-101% for rounding)
2. **No negative positions**: Unless explicitly margin/short (flag separately)
3. **No unrealistic values**: Check for obvious data errors (e.g., price 100x market)
4. **Asset class coverage**: At least one major asset class present

### Step 5: Context Summary for Next Stage
Output structured summary including:

```markdown
## Intake Summary - Stage 1 Complete

**Disclaimer**: Educational only, not personalized financial advice.

**Portfolio Snapshot**:
- Total Value: $XXX,XXX
- Holdings: XX positions across X asset classes
- Largest position: XXX (XX%)
- Geographic exposure: X% domestic / X% international

**Investor Profile**:
- Risk Tolerance: [Conservative/Moderate/Growth/Aggressive]
- Horizon: X years ([short/medium/long])
- Primary Goal: [Income/Growth/Preservation/Speculation]
- Pattern: [Accumulating/Static/Withdrawing]

**Data Quality**: [Complete/Estimated - see gaps: ...]
**Flags**: [Any concentration/leverage/illiquidity noted]

Proceeding to Risk Screening...
```

## Outputs
- Normalized portfolio table with asset class and geographic classification
- Risk tolerance category and investment horizon
- Goal priority and contribution/withdrawal pattern
- Data quality assessment (complete vs estimated)
- Any early-stage flags (e.g., obvious concentration >50% in single asset)

## Quality Gate
- [ ] Educational disclaimer stated
- [ ] All 5 essential data points captured
- [ ] Portfolio normalized to standard format
- [ ] Total weight sums to 100% (or gap identified)
- [ ] Asset classes and geographic exposure classified
- [ ] Investor profile complete (risk, horizon, goals)

## Research & Evidence Requirements
Use WebSearch/WebFetch to verify:
- Current market data for pricing/valuation if user provided incomplete data
- Asset class definitions if classification ambiguous
- Standard risk tolerance questionnaires (e.g., CFA Institute, Vanguard questionnaires)

Evidence tiers:
- **Tier 1 (Systematic Review)**: Meta-analyses of risk tolerance assessments
- **Tier 2 (Industry Standards)**: CFA Institute, Morningstar, Vanguard methodologies
- **Tier 3 (Expert Consensus)**: Reputable financial advisor guidelines

Graceful degradation: If WebSearch unavailable, use SECOND-KNOWLEDGE-BRAIN.md for standard classification rules.

## Example Full Output

```
=== STAGE 1: PROFILE INTAKE ===

DISCLAIMER: This analysis is for educational purposes only. It does not constitute
personalized financial advice, investment recommendations, or tax guidance.

---

## Intake Questionnaire Results

**Q1: Portfolio Holdings**
Provided: Brokerage statement dated 2026-06-28
- 27 positions across stocks, ETFs, bonds, and crypto
- Total reported value: $478,350

**Q2: Risk Tolerance**
Response: "Moderate - I can tolerate some volatility but not huge swings. A 20%
drop would make me uncomfortable but I wouldn't sell everything."
Classification: MODERATE

**Q3: Investment Horizon**
Response: "10+ years until retirement, might need some for house down payment
in 5 years"
Classification: MEDIUM (5-10 year effective horizon)

**Q4: Financial Goals**
Primary: Growth for retirement
Secondary: Preservation for down payment
Tertiary: Some income generation

**Q5: Contribution/Withdrawal Pattern**
Response: "Adding $2,000/month, no planned withdrawals"
Classification: ACCUMULATING

---

## Normalized Portfolio

| Ticker | Asset Class | Quantity | Value | Weight | Geographic |
|--------|-------------|----------|-------|--------|------------|
| AAPL   | Stock       | 150      | $28,500 | 6.0% | US (Domestic) |
| MSFT   | Stock       | 80       | $31,200 | 6.5% | US (Domestic) |
| GOOGL  | Stock       | 50       | $7,350  | 1.5% | US (Domestic) |
| AMZN   | Stock       | 40       | $6,800  | 1.4% | US (Domestic) |
| NVDA   | Stock       | 25       | $5,625  | 1.2% | US (Domestic) |
| VTI    | ETF (Equity)| 200      | $48,600 | 10.2% | US (Domestic) |
| VXUS   | ETF (Equity)| 150      | $24,450 | 5.1% | Developed Intl |
| BND    | ETF (Bond)  | 500      | $45,200 | 9.5% | US (Domestic) |
| TLT    | ETF (Bond)  | 100      | $12,100 | 2.5% | US (Domestic) |
| SCHD   | ETF (Equity)| 120      | $29,400 | 6.1% | US (Domestic) |
| VIG    | ETF (Equity)| 100      | $25,300 | 5.3% | US (Domestic) |
| JEPI   | ETF (Equity)| 200      | $31,600 | 6.6% | US (Domestic) |
| JEPQ   | ETF (Equity)| 100      | $11,200 | 2.3% | US (Domestic) |
| BTC-USD| Crypto      | 0.5      | $27,500 | 5.7% | Global |
| ETH-USD| Crypto      | 3.2      | $9,280  | 1.9% | Global |
| USDC   | Stablecoin  | 5,000    | $5,000  | 1.0% | Global |
| VT     | ETF (Equity)| 50       | $12,450 | 2.6% | Global All-Cap |
| VNQ    | ETF (Equity)| 80       | $9,280  | 1.9% | US (Domestic) |
| VWO    | ETF (Equity)| 60       | $6,900  | 1.4% | Emerging Markets |
| GLD    | ETF (Commodity)| 30    | $5,670  | 1.2% | Global |
| TIPS   | ETF (Bond)  | 150      | $16,050 | 3.4% | US (Domestic) |
| SHV    | ETF (Cash)  | 300      | $30,090 | 6.3% | US (Domestic) |
| Individual Treasury Bond | Bond | 1 | $10,000 | 2.1% | US (Domestic) |
| CD     | Cash        | 1        | $25,000 | 5.2% | US (Domestic) |
| ... (additional small positions) | ... | ... | ... | ... | ... |

**TOTAL**: $478,350
**SUM CHECK**: 100.0%

---

## Portfolio Composition Summary

**By Asset Class**:
- Equities (Stocks + Equity ETFs): 55.2%
- Fixed Income (Bonds + Bond ETFs + TIPS): 23.4%
- Crypto: 7.6%
- Cash/Equivalents: 12.5%
- Alternatives (REIT, Gold): 1.3%

**By Geography**:
- Domestic (US): 76.8%
- Developed International: 5.1%
- Emerging Markets: 1.4%
- Global/Crypto: 16.7%

**By Sector** (Equities only):
- Technology: 28.4%
- Financial Services: 12.1%
- Healthcare: 8.3%
- Consumer Discretionary: 9.7%
- Industrials: 7.2%
- Other: 34.3%

---

## Investor Profile

| Attribute | Value | Source |
|-----------|-------|--------|
| Risk Tolerance | MODERATE | Questionnaire |
| Investment Horizon | MEDIUM (5-10 years) | Stated |
| Primary Goal | Growth | Stated |
| Secondary Goal | Preservation | Stated |
| Pattern | ACCUMULATING (+$2,000/mo) | Stated |
| Tax Status | Mixed (taxable + tax-advantaged) | Assumed |

---

## Data Quality Assessment

✅ **COMPLETE**: All essential data points captured
✅ **ACCURATE**: Prices verified via market data (WebSearch)
✅ **NORMALIZED**: All positions classified and weighted
✅ **VERIFIED**: Sum check passed (100.0%)

---

## Early Stage Flags

⚠️ **CONCENTRATION NOTED**:
- Tech sector overweight (28.4% vs ~20% typical)
- Crypto at 7.6% (above 5% typical for moderate risk)

ℹ️ **POSITIVE INDICATORS**:
- Good geographic diversification for US investor
- Cash buffer appropriate (12.5%)
- Regular contributions positive for long-term growth

---

## STAGE 1 COMPLETE - PASSING TO RISK SCREENER

**Next**: Framework selection, risk tolerance alignment, concentration analysis
