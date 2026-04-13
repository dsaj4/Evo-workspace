# Sparse Platform Evidence Handling Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 在不伪造数据、不掩盖样本不足的前提下，把当前三平台数据重构为“证据强弱分层”的分析与写作方案，产出可送审的稳健解释框架。

**Architecture:** 以 `bili` 作为强证据主样本，`zhihu` 作为有限覆盖下的补充比较样本，`xhs` 作为仅描述不推断的弱证据样本。核心思路不是“假装数据足够”，而是把结论拆成主结论、补充结论、边界结论，并用重叠窗口分析、情景界限分析、留一平台稳健性分析来增强解释稳定性。

**Tech Stack:** Python, pandas, statsmodels, manuscript markdown files in `workspace/canonical_chapters`, processed data in `workspace/paper-revision/processed_data`

---

### Task 1: Freeze an evidence-tier framework

**Files:**
- Modify: `workspace/canonical_chapters/00_abstract.md`
- Modify: `workspace/canonical_chapters/01_introduction.md`
- Modify: `workspace/canonical_chapters/03_methodology.md`
- Modify: `workspace/canonical_chapters/04_results.md`
- Modify: `workspace/canonical_chapters/05_discussion.md`
- Modify: `workspace/canonical_chapters/06_conclusion.md`
- Create: `workspace/paper-revision/canonical_results/evidence_tiers.md`

**Step 1: Write the evidence-tier table**

Create a table with three rows:
- `Strong evidence`: bili only, long time series, can support trend/event analyses
- `Moderate evidence`: zhihu, limited coverage, can support bounded platform comparison and overlap-window comparison
- `Weak evidence`: xhs, descriptive only, no inferential use

**Step 2: Save the table**

Write it to `workspace/paper-revision/canonical_results/evidence_tiers.md`.

**Step 3: Rewrite scope sentences**

Update chapter-level framing so the paper no longer implies all three platforms equally support all analyses.

Use language like:

```text
本研究采用分层证据策略：哔哩哔哩用于主分析，知乎用于有限覆盖下的补充比较，小红书仅用于描述性呈现。
```

**Step 4: Verify wording consistency**

Search for and remove claims implying:
- all platforms support all hypotheses
- all platforms have comparable time coverage
- xhs supports formal inference

**Step 5: Commit**

```bash
git add workspace/canonical_chapters workspace/paper-revision/canonical_results/evidence_tiers.md
git commit -m "docs: define evidence tiers for sparse platform data"
```

### Task 2: Redefine the paper’s claim hierarchy

**Files:**
- Modify: `workspace/canonical_chapters/00_abstract.md`
- Modify: `workspace/canonical_chapters/04_results.md`
- Modify: `workspace/canonical_chapters/05_discussion.md`
- Modify: `workspace/canonical_chapters/06_conclusion.md`

**Step 1: Define the primary claim**

Primary claim should be:

```text
在主样本平台（哔哩哔哩）及自然日总量口径下，职业不安全感表达呈长期上升趋势；事件主效应未显示稳定显著增加。
```

**Step 2: Define the secondary claim**

Secondary claim should be:

```text
在有限覆盖条件下，知乎观测到更高的不安全感表达率；这一差异提示平台社群结构可能重要，但其外推应保持谨慎。
```

**Step 3: Define the boundary claim**

Boundary claim should be:

```text
小红书样本当前仅提供存在性与方向性描述，不支持统计推断。
```

**Step 4: Remove overstated synthesis**

Cut or downgrade sentences that imply:
- “中国公众整体” level claims
- stable cross-platform generalization
- platform comparison as already fully established population fact

**Step 5: Commit**

```bash
git add workspace/canonical_chapters
git commit -m "docs: separate primary secondary and boundary claims"
```

### Task 3: Add overlap-window comparison for bili vs zhihu

**Files:**
- Create: `workspace/analysis_scripts/overlap_window_platform_compare.py`
- Create: `workspace/paper-revision/canonical_results/overlap_window_platform_compare.md`
- Modify: `workspace/canonical_chapters/03_methodology.md`
- Modify: `workspace/canonical_chapters/04_results.md`
- Test: `workspace/analysis_scripts/overlap_window_platform_compare.py`

**Step 1: Write the comparison script**

Build a script that:
- reads `daily_data.parquet`
- keeps `bili` and `zhihu`
- restricts analysis to dates where `zhihu` has data
- reports platform-level totals, insecurity counts, ratios
- runs a formal proportion test or chi-square test on the overlap window only

**Step 2: Run the script**

Run:

```bash
cd workspace
..\.venv\Scripts\python.exe analysis_scripts/overlap_window_platform_compare.py
```

Expected:
- markdown summary file created
- overlap-window ratio comparison produced
- formal p-value reported

**Step 3: Add method text**

Add one sentence to methods:

```text
为避免平台时间覆盖不一致导致的比较偏差，本文进一步在知乎实际覆盖日期内，对哔哩哔哩与知乎进行重叠窗口比较。
```

**Step 4: Add result text**

Add one short subsection under H4:
- full-sample descriptive comparison
- overlap-window inferential comparison
- note whether conclusion direction stays the same

**Step 5: Commit**

```bash
git add workspace/analysis_scripts/overlap_window_platform_compare.py workspace/paper-revision/canonical_results/overlap_window_platform_compare.md workspace/canonical_chapters
git commit -m "feat: add overlap-window comparison for bili and zhihu"
```

### Task 4: Add coverage-sensitivity bounds instead of pretending missing days do not matter

**Files:**
- Create: `workspace/analysis_scripts/platform_coverage_sensitivity.py`
- Create: `workspace/paper-revision/canonical_results/platform_coverage_sensitivity.md`
- Modify: `workspace/canonical_chapters/03_methodology.md`
- Modify: `workspace/canonical_chapters/04_results.md`
- Modify: `workspace/canonical_chapters/05_discussion.md`

**Step 1: Define sensitivity scenarios**

For zhihu and xhs, calculate platform-level ratio bounds under transparent scenarios:
- Scenario A: missing days have zero insecurity comments
- Scenario B: missing days have same ratio as observed days
- Scenario C: missing days have same ratio as bili

**Step 2: Write and run the script**

Run:

```bash
cd workspace
..\.venv\Scripts\python.exe analysis_scripts/platform_coverage_sensitivity.py
```

Expected:
- each platform gets a bounded plausible ratio range
- markdown summary explains the assumptions

**Step 3: Integrate into methods**

Add language like:

```text
针对平台覆盖不完整问题，本文使用情景界限分析评估关键结论对未观测日期的敏感性。
```

**Step 4: Integrate into results/discussion**

Use the output to write:
- whether zhihu > bili remains true across scenarios
- whether xhs remains uninterpretable even under optimistic assumptions

**Step 5: Commit**

```bash
git add workspace/analysis_scripts/platform_coverage_sensitivity.py workspace/paper-revision/canonical_results/platform_coverage_sensitivity.md workspace/canonical_chapters
git commit -m "feat: add platform coverage sensitivity analysis"
```

### Task 5: Add leave-one-platform-out narrative robustness

**Files:**
- Modify: `workspace/canonical_chapters/04_results.md`
- Modify: `workspace/canonical_chapters/05_discussion.md`
- Create: `workspace/paper-revision/canonical_results/platform_leave_one_out.md`

**Step 1: Write the logic note**

Document:
- main trend/event conclusions come from natural-day total or bili-dominant sample
- removing xhs should not matter materially
- platform comparison conclusion depends mainly on bili vs zhihu

**Step 2: Save the note**

Write a short markdown note that explicitly says which conclusions survive removal of each platform.

**Step 3: Use bounded wording**

Recommended wording:

```text
平台覆盖不均衡不会改变主结论的方向，但会影响跨平台比较结论的解释强度。
```

**Step 4: Commit**

```bash
git add workspace/canonical_chapters workspace/paper-revision/canonical_results/platform_leave_one_out.md
git commit -m "docs: add leave-one-platform-out robustness narrative"
```

### Task 6: Rewrite explanation logic so it stays within evidence

**Files:**
- Modify: `workspace/canonical_chapters/04_results.md`
- Modify: `workspace/canonical_chapters/05_discussion.md`
- Modify: `workspace/canonical_chapters/06_conclusion.md`

**Step 1: Replace overclaiming phrases**

Replace:
- `中国公众`
- `平台间存在显著差异` when no formal test is shown in that exact subsection
- `恢复至基线`
- `结构性担忧`
- `高知焦虑`

with more bounded alternatives such as:

```text
在当前观测样本中
在可比平台与可比日期范围内
回落至观测均值附近
提示可能存在持续关注上升
与平台用户结构差异相一致
```

**Step 2: Separate result from explanation**

In results:
- keep only numerical findings
- label interpretation as `可能解释`

In discussion:
- present 2-3 explanations as hypotheses, not conclusions

**Step 3: Add a “what we can and cannot infer” paragraph**

Insert a short paragraph in discussion and conclusion:

```text
本文能够识别公开表达模式及其平台/时间差异，但不能直接识别总体人群心理水平、个体因果机制或最优干预策略。
```

**Step 4: Commit**

```bash
git add workspace/canonical_chapters
git commit -m "docs: bound explanations to observed evidence"
```

### Task 7: Add a reviewer-facing robustness paragraph

**Files:**
- Modify: `workspace/canonical_chapters/00_abstract.md`
- Modify: `workspace/canonical_chapters/04_results.md`
- Modify: `workspace/canonical_chapters/06_conclusion.md`

**Step 1: Add one compact paragraph**

Use wording like:

```text
考虑到平台时间覆盖不均衡，本文采用主样本分析、重叠窗口比较与情景界限分析三种策略交叉验证关键结论。结果显示，主结论方向在不同处理下保持一致，但跨平台比较的证据强度存在层级差异。
```

**Step 2: Keep it short**

Do not expand into a full appendix inside the abstract or conclusion.

**Step 3: Commit**

```bash
git add workspace/canonical_chapters
git commit -m "docs: add reviewer-facing robustness summary"
```

### Task 8: Prepare fallback wording for submission if zhihu/xhs still remain sparse

**Files:**
- Create: `workspace/paper-revision/canonical_results/fallback_claims.md`
- Modify: `workspace/canonical_chapters/00_abstract.md`
- Modify: `workspace/canonical_chapters/05_discussion.md`
- Modify: `workspace/canonical_chapters/06_conclusion.md`

**Step 1: Write fallback claims**

Create a short note with three blocks:
- `Safe to claim`
- `Only with qualifier`
- `Do not claim`

Suggested content:

```text
Safe to claim:
- bili-dominant sample shows upward trend
- event main effect is not robustly positive
- zhihu observed ratio exceeds bili in available sample

Only with qualifier:
- platform heterogeneity as a broader social fact
- recovery to baseline
- policy implications beyond observed platforms

Do not claim:
- xhs platform effect
- full-population inference
- causal impact of AI events
```

**Step 2: Use this note to trim conclusion**

Make the conclusion shorter and less ambitious if new data is still unavailable at submission time.

**Step 3: Commit**

```bash
git add workspace/paper-revision/canonical_results/fallback_claims.md workspace/canonical_chapters
git commit -m "docs: add fallback claims for sparse-platform submission"
```
