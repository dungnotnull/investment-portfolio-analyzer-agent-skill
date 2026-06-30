# Finance-Insurance Cluster Integration

## Overview

This document defines the shared sub-skills, patterns, and cross-skill wiring for the `finance-insurance` cluster.

**Cluster**: `finance-insurance` (Finance, Investment & Insurance)
**Skills in Cluster**:
- `investment-portfolio-analyzer` (Idea #75) - Portfolio evaluation and optimization
- Additional skills to be integrated as cluster grows

**Cluster Coordinator**: This skill (`investment-portfolio-analyzer`) serves as the initial cluster anchor and pattern provider.

---

## Shared Sub-Skills Catalog

### Sub-Skill: profile-intake

**Purpose**: Capture user context, preferences, and constraints with domain-appropriate questions.

**Shared Pattern**:
```yaml
name: sub-profile-intake
description: Capture [domain-specific] context with educational disclaimer

Procedure:
  1. State educational disclaimer
  2. Parse user input/artifact
  3. Ask targeted intake questions (≤5)
  4. Normalize input to standard format
  5. Classify by domain categories
  6. Validate completeness
  7. Output structured profile

Quality Gates:
  - Disclaimer stated
  - Essential data points captured
  - Input normalized
  - Classification complete
```

**Domain Customizations**:
- Investment Portfolio: Holdings, risk tolerance, horizon, goals, contribution pattern
- Insurance: Coverage details, beneficiaries, risk factors, premium budget
- General Finance: Assets, liabilities, income, expenses, goals

**Shared Tools**: Read, Write, WebSearch (for classification verification)

**Implementation Location**: `skills/sub-profile-intake.md`

---

### Sub-Skill: risk-screener

**Purpose**: Systematically screen for critical risk issues before detailed analysis.

**Shared Pattern**:
```yaml
name: sub-risk-screener
description: Flag concentration, leverage, and risk-tolerance mismatches

Procedure:
  1. Select evaluation frameworks
  2. Assign dimension weights
  3. Screen for risk types (domain-specific)
  4. Assess horizon alignment
  5. Issue recommendation

Quality Gates:
  - Frameworks selected with rationale
  - Dimension weights sum to 100%
  - Risk screens completed
  - Recommendation issued
```

**Domain Customizations**:
- Investment Portfolio: Concentration (HHI), leverage, illiquidity, risk-tolerance mismatch
- Insurance: Coverage gaps, underinsurance, policy exclusions, beneficiary issues
- General Finance: Solvency risk, liquidity risk, leverage concentration

**Shared Tools**: Read, WebSearch (for risk threshold verification)

**Implementation Location**: `skills/sub-risk-screener.md`

---

### Sub-Skill: scoring-engine

**Purpose**: Quantitatively assess subject across dimensions using framework-grounded metrics.

**Shared Pattern**:
```yaml
name: sub-scoring-engine
description: Score across [N] dimensions using domain frameworks

Procedure:
  For each dimension:
    1. Calculate raw metrics
    2. Map to 0-5 score
    3. Apply framework citations
    4. Document justification
  5. Calculate overall score

Quality Gates:
  - All dimensions scored
  - Metrics shown
  - Frameworks cited
  - Overall score calculated
```

**Domain Customizations**:
- Investment Portfolio: 6 dimensions (diversification, risk-return, alignment, concentration, cost, liquidity)
- Insurance: 5 dimensions (coverage adequacy, cost efficiency, beneficiary alignment, exclusions, financial strength)
- General Finance: 4-6 dimensions (varies by use case)

**Shared Tools**: Read, WebSearch (for metric verification)

**Implementation Location**: `skills/sub-scoring-engine.md`

---

### Sub-Skill: improvement-roadmap

**Purpose**: Challenge analysis and provide prioritized, actionable recommendations.

**Shared Pattern**:
```yaml
name: sub-improvement-roadmap
description: Challenge findings, propose scenarios with trade-offs

Procedure:
  1. Generate challenges (≥3)
  2. For each: counterargument, evidence, impact, revision
  3. Generate recommendations (≥5)
  4. Develop rebalancing scenarios (≥3)
  5. Create implementation roadmap

Quality Gates:
  - ≥3 challenges documented
  - ≥5 recommendations with impact/effort
  - ≥3 scenarios with full analysis
  - Implementation roadmap provided
```

**Domain Customizations**:
- Investment Portfolio: Portfolio rebalancing scenarios, cost/tax analysis
- Insurance: Coverage adjustment scenarios, premium optimization
- General Finance: Action plans prioritized by impact/effort

**Shared Tools**: Read, Write

**Implementation Location**: `skills/sub-improvement-roadmap.md`

---

## Cluster-Level Patterns

### Pattern 1: Research-First Evidence Gathering

**Purpose**: Ensure all claims are grounded in current, authoritative evidence.

**Implementation**:
```python
# Shared across all cluster skills
def gather_evidence(queries):
    results = []
    for query in queries:
        # WebSearch for domain sources
        search_results = WebSearch(query)
        # WebFetch top authoritative hits
        sources = WebFetch(top_hits)
        # Grade by evidence tier
        graded = grade_by_tier(sources)
        results.append(graded)
    return results

# Fallback to knowledge base
if WebSearch unavailable:
    use_knowledge_base()
    label_degradation()
```

**Evidence Tiers (Shared)**:
- Tier 1: Systematic reviews, meta-analyses
- Tier 2: Academic studies, industry standards
- Tier 3: Expert consensus, reputable institutions
- Tier 4: General information, blogs

---

### Pattern 2: Educational Disclaimer

**Purpose**: Clearly state educational nature of analysis.

**Standard Disclaimer** (Shared):
```
DISCLAIMER: This analysis is for educational purposes only. It does not constitute
personalized [advice type], investment recommendations, or tax guidance. Consult
a qualified [professional type] for decisions specific to your situation.
```

**Domain Customizations**:
- Investment Portfolio: "financial advice, investment recommendations"
- Insurance: "insurance advice, coverage recommendations"
- General Finance: "financial advice, tax guidance"

---

### Pattern 3: Devil's Advocate Challenge

**Purpose**: Stress-test analysis before presenting conclusions.

**Implementation**:
```yaml
Challenge Types:
  - Score inflation challenge
  - Methodology challenge
  - Implementation challenge
  - Market/environment challenge
  - Goal conflict challenge

For Each Challenge:
  - Counterargument: What challenges the finding?
  - Evidence Required: What validates/refutes?
  - Impact if True: How does conclusion change?
  - Revision: Adjust score/recommendation if warranted
```

---

### Pattern 4: Impact/Effort Prioritization

**Purpose**: Rank recommendations by (Impact × Effort) matrix.

**Calculation** (Shared):
```python
def calculate_priority(recommendation):
    impact_values = {"High": 3, "Medium": 2, "Low": 1}
    effort_values = {"Low": 3, "Medium": 2, "High": 1}

    impact_score = impact_values[recommendation.impact]
    effort_score = effort_values[recommendation.effort]

    return (impact_score * 3) + effort_score
```

**Priority Matrix** (Shared):
```
High Impact, Low Effort     → Priority 1-2 (Do First)
High Impact, Medium Effort  → Priority 3-5
Medium Impact, Low Effort   → Priority 4-6
Low Impact, Low Effort      → Priority 7-8
High Impact, High Effort    → Priority 6-8 (Consider)
Low/Med Impact, High Effort → Priority 9+ (Defer)
```

---

## Cross-Skill Wiring

### Scenario: Portfolio → Insurance Recommendations

**Trigger**: User portfolio analysis reveals insurance gaps.

**Flow**:
```
investment-portfolio-analyzer
  → Detects: No disability insurance, insufficient life insurance
  → Flags in risk screener: "Insurance coverage gap identified"
  → In roadmap: "Review insurance coverage" recommendation
  → Cross-reference: "Use insurance-coverage-analyzer for detailed analysis"
```

**Implementation**:
```yaml
# In investment-portfolio-analyzer roadmap
Recommendation:
  title: "Review insurance coverage"
  impact: High
  effort: Medium
  framework: Risk Management
  cross_skill_reference: insurance-coverage-analyzer
  trigger_condition: "Life insurance < 10x income OR no disability insurance"
```

---

### Scenario: Insurance → Portfolio Recommendations

**Trigger**: Insurance analysis identifies assets that could be optimized.

**Flow**:
```
insurance-coverage-analyzer
  → Detects: High cash value life insurance, inefficient for current needs
  → Flags in scoring: "Asset allocation inefficiency"
  → In roadmap: "Review life insurance strategy vs investment alternatives"
  → Cross-reference: "Use investment-portfolio-analyzer for comparison"
```

**Implementation**:
```yaml
# In insurance-coverage-analyzer roadmap
Recommendation:
  title: "Optimize cash value life insurance strategy"
  impact: Medium
  effort: High
  framework: Asset Allocation
  cross_skill_reference: investment-portfolio-analyzer
  trigger_condition: "Cash value life insurance > 20% of investable assets"
```

---

### Scenario: Unified Financial Profile

**Trigger**: User wants comprehensive financial health assessment.

**Flow**:
```
coordinator-skill (cluster-level)
  → Run investment-portfolio-analyzer
  → Run insurance-coverage-analyzer
  → Run debt-management-analyzer (if applicable)
  → Aggregate scores across domains
  → Identify cross-domain issues (e.g., over-insured but under-invested)
  → Generate unified roadmap with cross-references
```

**Implementation**:
```yaml
# Cluster coordinator (future)
unified_assessment:
  skills_to_run:
    - investment-portfolio-analyzer
    - insurance-coverage-analyzer
    - debt-management-analyzer

  aggregation:
    overall_health_score: average(domain_scores)
    cross_domain_issues: identify_gaps()

  output:
    unified_report: true
    cross_references: true
    integrated_roadmap: true
```

---

## Knowledge Base Sharing

### Shared Knowledge Sources

The cluster shares knowledge sources across skills:

**ArXiv Categories** (Shared):
- `q-fin.PM` (Portfolio Management)
- `q-fin.RM` (Risk Management)

**Domain Sources** (Shared):
- CFA Institute curriculum & research
- Regulatory bodies (SEC, FINRA, state insurance commissioners)
- Industry research (Vanguard, BlackRock, major insurers)

**Knowledge Update Protocol** (Shared):
- Weekly crawl via `tools/knowledge_updater.py`
- Append to `SECOND-KNOWLEDGE-BRAIN.md`
- De-duplication by URL/DOI hash
- Relevance scoring by recency + domain keywords

---

## Cluster Standards

### Quality Gates (Cluster-Level)

All cluster skills must pass these gates before output:

1. **Educational disclaimer stated**
2. **Evidence-based analysis** (no unsupported claims)
3. **Framework-grounded** (use named methodologies)
4. **Challenge phase executed** (devil's advocate review)
5. **Actionable recommendations** (specific, measurable)
6. **Professional presentation** (clear, no contradictions)

---

### Output Format Standardization

All cluster skills follow similar report structure:

```markdown
# [Skill Name] — Evaluation Report

## 1. Executive Summary
- Overall score
- Top strengths
- Top priority fixes

## 2. Scoring Table
- Dimension scores
- Frameworks applied
- Evidence tiers

## 3. Detailed Findings
- Per-dimension analysis
- Metrics and justifications

## 4. Challenge / Devil's-Advocate Notes
- Counter-arguments
- Revisions

## 5. Prioritized Roadmap
- Impact/Effort matrix
- Implementation timeline

## 6. Sources & Evidence Grade
- Tiered citations
- Degradation labels (if applicable)
```

---

### Testing Standards

All cluster skills must have:

1. **Minimum 5 test scenarios** defined in `tests/test-scenarios.md`
2. **Test runner** implemented in `tests/test_suite.py`
3. **Regression checklist** for post-change validation
4. **Calibration framework** for threshold tuning
5. **Score reproducibility** within ±0.5

---

## Implementation Roadmap

### Phase 1: Foundation (Complete)
- ✅ Define shared sub-skill patterns
- ✅ Implement quality gates
- ✅ Standardize output format
- ✅ Create knowledge base sharing protocol

### Phase 2: Anchor Skill (Complete)
- ✅ Implement `investment-portfolio-analyzer` as cluster anchor
- ✅ Document patterns for reuse
- ✅ Create test infrastructure

### Phase 3: Cluster Expansion (Future)
- [ ] Add `insurance-coverage-analyzer` using shared patterns
- [ ] Add `debt-management-analyzer` using shared patterns
- [ ] Implement cluster coordinator for unified assessments
- [ ] Create cross-skill wiring for recommendations

### Phase 4: Optimization (Future)
- [ ] Refine shared sub-skills based on multi-skill usage
- [ ] Optimize knowledge base for cluster-wide needs
- [ ] Implement shared testing framework
- [ ] Create cluster-level calibration

---

## Usage Guidelines

### For Skill Developers

When creating a new skill in the cluster:

1. **Reuse shared sub-skills** where possible
2. **Follow cluster patterns** for evidence gathering, disclaimers, challenges
3. **Implement all quality gates**
4. **Use standardized output format**
5. **Create 5+ test scenarios**
6. **Document cross-skill references** in roadmap recommendations

### For Users

When using cluster skills:

1. **Each skill is independent** - can run separately
2. **Cross-skill references** provide guidance for related analysis
3. **Shared knowledge base** ensures consistent evidence quality
4. **Standardized output** enables comparison across domains

---

## Version History

- v1.0 (2026-06-30): Initial cluster integration document
- Patterns defined for shared sub-skills
- Cross-skill wiring documented
- Implementation roadmap established
