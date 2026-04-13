# Thesis Major Revision Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Preserve the current topic and usable data, but rebuild the thesis argument so that the paper becomes internally consistent, methodologically defensible, and submission-ready under a strict academic review standard.

**Architecture:** This is a salvage-through-major-revision plan, not a full research restart. The work proceeds in three passes: first stop credibility loss by fixing hard contradictions and invalid citations; then rebuild the methods-results chain so every claim has matching evidence; finally compress the paper into a cautious descriptive study with no overclaiming.

**Tech Stack:** Markdown chapter files in `workspace/canonical_chapters/`, reference audit file, consistency matrix, and the final formatted thesis document.

---

### Task 1: Freeze the Thesis Positioning

**Files:**
- Modify: `workspace/canonical_chapters/00_abstract.md`
- Modify: `workspace/canonical_chapters/01_introduction.md`
- Modify: `workspace/canonical_chapters/02_literature_review.md`
- Modify: `workspace/canonical_chapters/05_discussion.md`
- Modify: `workspace/canonical_chapters/06_conclusion.md`

- [ ] **Step 1: Replace the study identity everywhere with one unified sentence**

Use this positioning across all chapters:

`本研究是一项基于公开社交媒体评论的描述性、关联性研究，分析的是职业不安全感相关表达，而非通过标准化量表直接测量职业不安全感构念本身。`

- [ ] **Step 2: Delete or downgrade all claims that imply strong theory testing**

Delete or rewrite phrases such as:

- `检验西方理论的跨文化适用性`
- `验证社交媒体数据在职业心理研究中的适用性`
- `为政策制定提供依据`
- `核心假设`

Replace them with weaker, defensible phrasing such as:

- `为后续理论检验提供描述性线索`
- `展示一种可供后续研究进一步验证的数据路径`
- `为风险监测与议题识别提供参考`

- [ ] **Step 3: Reframe the paper as a narrower contribution**

Keep only three contribution types:

- descriptive contribution
- measurement/process contribution
- context-specific exploratory contribution

Do not claim causal contribution, general population inference, or theory confirmation.

### Task 2: Fix Hard Consistency Errors First

**Files:**
- Modify: `workspace/canonical_chapters/00_abstract.md`
- Modify: `workspace/canonical_chapters/01_introduction.md`
- Modify: `workspace/canonical_chapters/03_methodology.md`
- Modify: `workspace/canonical_chapters/04_results.md`
- Modify: `workspace/canonical_chapters/05_discussion.md`
- Modify: `workspace/canonical_chapters/06_conclusion.md`
- Modify: `workspace/canonical_chapters/final_consistency_matrix.md`

- [ ] **Step 1: Resolve the date-range contradiction before any other revision**

The current pair of claims cannot coexist:

- `2024-10-12 至 2026-03-30`
- `361 个自然日`

Decide which is true from the underlying analysis output, then propagate the corrected version everywhere. If the real analytic period is 361 observed date points rather than 361 calendar days, write that explicitly.

- [ ] **Step 2: Standardize four quantities and use only one version of each**

Lock and propagate these values:

- total comments
- number of flagged insecurity comments
- number of platforms included in inference
- number of dates or panel rows

Any quantity that differs by chapter must be explained, not silently switched.

- [ ] **Step 3: Add one sentence wherever unequal platform coverage matters**

Use a sentence with this logic:

`由于平台日期覆盖显著不均衡，跨平台比较反映的是在当前采样覆盖下的表达差异，而非严格可比的总体平台差异。`

### Task 3: Rebuild the Citation System

**Files:**
- Modify: `workspace/canonical_chapters/01_introduction.md`
- Modify: `workspace/canonical_chapters/02_literature_review.md`
- Modify: `workspace/canonical_chapters/05_discussion.md`
- Modify: `workspace/canonical_chapters/references.md`
- Review: `workspace/canonical_chapters/citations_extracted.txt`

- [ ] **Step 1: Remove every citation already marked invalid or deleted**

Remove or replace all occurrences of:

- `Brough & Rudd, 2022`
- `Nam, 2019`
- `Liu et al., 2023`
- `Probst et al., 2017`
- `Zhang et al., 2021`
- incorrect-year variants such as `Arntz et al., 2017` and `Asur & Huberman, 2011`

- [ ] **Step 2: Do not let a citation survive unless it appears in the verified reference list**

Apply this rule:

`正文出现的每一条作者-年份引文，必须能在 references.md 中找到一一对应的真实条目。`

- [ ] **Step 3: Cut unsupported literature claims instead of inventing replacements**

If a claim currently depends on an invalid citation and you cannot immediately replace it with a verified source, delete the claim. This is especially important for:

- `公众对 AI 持乐观态度`
- `专业社区用户情绪表达更强烈`
- `中国用户更关注经济影响`

### Task 4: Rewrite the Research Questions and Hypothesis Layer

**Files:**
- Modify: `workspace/canonical_chapters/01_introduction.md`
- Modify: `workspace/canonical_chapters/03_methodology.md`
- Modify: `workspace/canonical_chapters/04_results.md`

- [ ] **Step 1: Shrink the paper from “large theory test” to “four descriptive analytic questions”**

Recommended structure:

- `RQ1：不同平台上的职业不安全感相关表达率如何分布？`
- `RQ2：样本期内该类表达是否呈现时间趋势？`
- `RQ3：AI 事件窗口与该类表达是否存在统计关联？`
- `RQ4：事件后的表达变化是否呈现短期恢复模式？`

- [ ] **Step 2: Decide whether to keep H-labels**

Recommended option: remove `H1/H3/H4/H6` entirely and use `RQ1-RQ4`.

Why: the current study is too descriptive for a heavy hypothesis architecture, and the numbering gap already exposes revision scars.

- [ ] **Step 3: If H-labels are retained, weaken them**

Do not write directional or confirmatory wording unless the model truly supports it. Use:

`本研究探索是否存在统计关联`

instead of:

`本研究检验事件是否显著影响`

### Task 5: Rebuild Chapter 3 as a Real Methods Chapter

**Files:**
- Modify: `workspace/canonical_chapters/03_methodology.md`

- [ ] **Step 1: Make the sampling logic transparent**

Explicitly report:

- search keywords used for crawling
- whether comments were collected around event topics only or across general AI discussion
- whether the keyword set overlaps with the insecurity dictionary
- why this overlap may bias prevalence estimates

- [ ] **Step 2: Rewrite the construct section with a defensive tone**

Add a paragraph stating:

- the dictionary captures explicit lexical signals
- the measure likely misses implicit, ironic, and contextual expressions
- the output is best interpreted as `职业不安全感相关表达`
- the measure should not be equated with a validated scale score

- [ ] **Step 3: Delete unused or unreported method elements**

Delete any method element that is not later used in results, especially:

- vague `职业身份识别` if there is no corresponding table or model
- any implied causal identification language
- any claim of mixed methods if no qualitative coding exists

- [ ] **Step 4: Rewrite the main model so the denominator problem is acknowledged**

At minimum, add a sentence like:

`由于事件窗口内总评论量可能同步波动，基于绝对计数的模型结果应理解为对表达数量变化的关联分析，而非对表达率变化的直接估计。`

If you have a rate-based or offset model in the real analysis, then report that instead and demote the current count model to robustness.

- [ ] **Step 5: Match every method subsection to a result subsection**

No subsection in Chapter 3 should remain unless Chapter 4 reports:

- the statistic
- the uncertainty
- the interpretation limit

### Task 6: Rebuild Chapter 4 from Reported Evidence Only

**Files:**
- Modify: `workspace/canonical_chapters/04_results.md`

- [ ] **Step 1: Keep only results that can be numerically reported**

Every subsection must contain actual reported quantities. No prose-only claims such as `存在显著差异` without the test statistic.

- [ ] **Step 2: Rewrite the platform comparison subsection**

Minimum reporting standard:

- exact numerator and denominator by platform
- whether the comparison is descriptive only or inferential
- if inferential, report `χ²`, `df`, `p`, and preferably an effect size
- an explicit warning that coverage is temporally unbalanced

- [ ] **Step 3: Rewrite the trend subsection**

Do not leave the sentence `每天增加约 3.0%` unless the time unit is unquestionably daily and substantively interpretable. If the coefficient is based on a coarser or transformed time index, explain that precisely. If not, downgrade to:

`时间项系数为正，表明样本期内相关表达存在上升关联。`

- [ ] **Step 4: Rewrite the event-effect subsection**

Keep:

- coefficient
- SE
- IRR
- confidence interval
- p-value

Add:

- what exactly the model can and cannot say
- why the denominator issue limits interpretation

- [ ] **Step 5: Rewrite the dynamic subsection or cut it**

Keep H3-style findings only if you can report:

- baseline definition
- event-day value
- recovery-day criterion
- uncertainty or at least a clearly described operational rule

If these cannot be reported cleanly, cut the subsection and mention it as future work or exploratory appendix material.

- [ ] **Step 6: Remove all placeholders and fake completeness**

Delete or complete every unfinished element, especially:

- `[位置]`
- `[比较结果]`
- any robustness section without actual coefficients or summary table

### Task 7: Rewrite Chapters 5 and 6 as Cautious Interpretation

**Files:**
- Modify: `workspace/canonical_chapters/05_discussion.md`
- Modify: `workspace/canonical_chapters/06_conclusion.md`

- [ ] **Step 1: Ban speculative inflation**

Delete or soften phrases such as:

- `高知焦虑`
- `温水煮青蛙`
- `结构性担忧`
- `公众逐渐将 AI 事件常态化`

unless they are explicitly labeled as tentative interpretations.

- [ ] **Step 2: Make every interpretation subordinate to evidence quality**

Use a three-part sentence pattern:

- observed result
- narrow interpretation
- limitation clause

Example:

`样本中知乎评论的相关表达率高于哔哩哔哩，但由于平台覆盖期和用户构成不均衡，这一差异更适合作为后续研究线索，而非总体平台差异结论。`

- [ ] **Step 3: Rewrite practical implications downward**

Current ceiling for implication claims:

- monitoring
- issue awareness
- communication sensitivity

Not acceptable:

- strong policy design guidance
- intervention prescriptions that imply causal evidence

- [ ] **Step 4: Strengthen the limitations section**

The limitations chapter should explicitly include:

- sampling-selection bias
- keyword-screening and dictionary overlap risk
- platform coverage imbalance
- construct validity weakness
- observational non-causal design
- unfinished generalizability

### Task 8: Run the Final Consistency Audit

**Files:**
- Modify: `workspace/canonical_chapters/final_consistency_matrix.md`
- Review: `workspace/canonical_chapters/00_abstract.md`
- Review: `workspace/canonical_chapters/01_introduction.md`
- Review: `workspace/canonical_chapters/02_literature_review.md`
- Review: `workspace/canonical_chapters/03_methodology.md`
- Review: `workspace/canonical_chapters/04_results.md`
- Review: `workspace/canonical_chapters/05_discussion.md`
- Review: `workspace/canonical_chapters/06_conclusion.md`
- Review: `workspace/canonical_chapters/references.md`

- [ ] **Step 1: Audit the fixed vocabulary**

Standardize these terms across all chapters:

- `职业不安全感`
- `职业不安全感相关表达`
- `描述性研究`
- `关联分析`
- `观察性数据`

- [ ] **Step 2: Audit all quantitative facts**

Create a final locked list for:

- date range
- number of observed dates
- panel rows
- event count
- platform-level counts
- flagged-comment count

- [ ] **Step 3: Audit all citations**

Run a last pass with the simple rule:

`正文任何作者-年份组合，如果在 references.md 中找不到，就必须删除或修正。`

- [ ] **Step 4: Make the abstract the last chapter you touch**

Only after all six chapters are stable should the abstract be rewritten, because right now it is overconfident relative to the body.

### Decision Rule: When to Stop Revising and Restart Instead

If any of the following turns out to be true, stop the salvage plan and redesign the research:

- the raw analysis cannot reproduce the reported core numbers
- the real sampling period and reported sampling period cannot be reconciled
- the keyword-retrieval pipeline makes the insecurity measure fundamentally circular and irreparable
- the event analysis cannot be reported with complete model outputs
- the remaining valid literature base is too thin to support the current framing

If none of these red lines is triggered, the thesis should be treated as a **major revision project**, not a full restart.
