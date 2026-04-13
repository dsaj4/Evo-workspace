# Paper Revision Remediation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Turn the current thesis draft into a defensible submission by rebuilding one reproducible evidence chain from data to analysis to prose.

**Architecture:** Do not revise prose first. First freeze one canonical dataset specification, one canonical event database, and one canonical analysis pipeline. Only after all core numbers are regenerated should the abstract, methods, results, discussion, and conclusion be rewritten against those regenerated outputs.

**Tech Stack:** Python, pandas, statsmodels, Markdown, CSV, Parquet

---

## Non-Negotiable Rules

- Do not keep any number in the manuscript unless it can be traced to a file in `workspace/paper-revision/`.
- Do not use both "800 days" and "361 days" again. One must be the natural-day count, the other must be renamed as platform-day rows if retained at all.
- Do not mention four platforms unless raw data and preprocessing code actually include Weibo.
- Do not keep H2 or H5 as headline contributions.
- Do not claim ethics approval, OSF preregistration, GitHub release, R analysis, or Stata analysis unless evidence files exist.
- Do not keep any 2023-2025 citation that has not been manually verified.
- Do not edit `05_discussion_final.md` or `06_conclusion_FINAL.md` before `03_methodology_FINAL.md` and `04_results_revised.md` are rebuilt.

---

### Task 1: Freeze the Canonical Study Scope

**Files:**
- Inspect: `workspace/paper-revision/processed_data/all_processed_data.csv`
- Inspect: `workspace/paper-revision/processed_data/daily_data.parquet`
- Inspect: `workspace/paper-revision/event_analysis/event_database.csv`
- Modify: `workspace/draft_chapters/00_abstract_FINAL.md`
- Modify: `workspace/draft_chapters/01_introduction_revised_v2.md`
- Modify: `workspace/draft_chapters/02_literature_review_FINAL.md`
- Modify: `workspace/draft_chapters/03_methodology_FINAL.md`
- Modify: `workspace/draft_chapters/04_results_revised.md`
- Modify: `workspace/draft_chapters/05_discussion_final.md`
- Modify: `workspace/draft_chapters/06_conclusion_FINAL.md`

**Checklist:**
- Confirm the canonical comment count, platform count, unique-date count, event count, and platform names from processed data.
- Choose the canonical scope. Recommended: `114,915 comments`, `3 platforms`, `361 unique dates`, `33 events`.
- Replace every occurrence of `4 platforms`, `Weibo`, `800 days` as a natural-day claim, `355 days`, and `~540 days` if unsupported by the chosen scope.
- Add one sentence in methods clarifying that `800` in `daily_data.parquet` is a panel row count, not the number of unique calendar days, if this table is retained for modeling.

**Done Criteria:**
- All seven chapter files state the same platform count, study period, event count, and sample size.
- No chapter still claims Weibo data if Weibo is absent from preprocessing and raw data directories.

---

### Task 2: Create One Evidence Baseline Table

**Files:**
- Create: `workspace/paper-revision/evidence_baseline.md`
- Inspect: `workspace/preprocess_data.py`
- Inspect: `workspace/paper-revision/processed_data/data_quality_report.md`

**Checklist:**
- Build a one-page evidence table with the exact values that the manuscript is allowed to quote.
- Include: total comments, platform names, comments by platform, unique dates, panel rows, insecurity comments, insecurity ratio, event counts by type, and raw-data directory coverage.
- Add a "forbidden claims" block listing unsupported claims that must not reappear.

**Done Criteria:**
- The team can answer every basic "how many?" question from one file without re-reading scripts.
- Every quoted global number in the manuscript appears in this baseline file.

---

### Task 3: Separate Natural-Day Data from Platform-Day Panel Data

**Files:**
- Modify: `workspace/preprocess_data.py`
- Create: `workspace/paper-revision/processed_data/daily_total.parquet`
- Create: `workspace/paper-revision/processed_data/daily_platform_panel.parquet`
- Modify: `workspace/paper-revision/processed_data/data_quality_report.md`

**Checklist:**
- Stop overloading one file for two statistical units.
- Save a natural-day series with one row per date.
- Save a platform-day panel with one row per platform-date.
- Remove the pseudo-platform `all` from any dataset used for platform comparison.
- Update the data quality report so it explicitly distinguishes `unique dates` from `panel rows`.

**Done Criteria:**
- A reader can tell which analyses use dates and which use platform-date rows.
- No downstream script needs to infer the statistical unit from context.

---

### Task 4: Rebuild a Single Canonical Analysis Pipeline

**Files:**
- Create: `workspace/run_canonical_analysis.py`
- Modify or retire: `workspace/event_analysis.py`
- Modify or retire: `workspace/test_all_hypotheses.py`
- Modify or retire: `workspace/test_hypotheses_updated.py`
- Modify or retire: `workspace/h2_final_test.py`
- Modify or retire: `workspace/h2_retest_updated.py`

**Checklist:**
- Replace the current multi-script patchwork with one script that produces all manuscript-facing results.
- Make this script read exactly one processed dataset and exactly one event database.
- Make it output one machine-readable results file and one human-readable summary file.
- Remove or clearly mark legacy scripts so future numbers cannot be copied from obsolete outputs.

**Done Criteria:**
- H1, H3, H4, and H6 all come from one executable pipeline.
- No chapter depends on numbers from deprecated scripts.

---

### Task 5: Repair H1, H3, H4, and H6 Definitions Before Re-estimation

**Files:**
- Modify: `workspace/run_canonical_analysis.py`
- Modify: `workspace/draft_chapters/03_methodology_FINAL.md`

**Checklist:**
- Define the exact statistical unit for each hypothesis.
- Lock the event window. If H1 uses `7-day window`, methods and results must both say `7-day window`.
- Rewrite H3 so "days" refers to actual calendar days, not panel rows.
- Redefine H4 to compare real platforms only, never including `all`.
- Redefine H6 so time trend is estimated on the intended unit and with clear controls.
- Explicitly document whether H1 is Poisson, Negative Binomial, or something else. The prose must match the implemented model.

**Done Criteria:**
- Methods section matches the code line-for-line in model family, window length, controls, and unit of analysis.
- No hypothesis definition is ambiguous about what a "day" or "platform effect" means.

---

### Task 6: Fix Sign Interpretation, Placebo Logic, and Serialization Failures

**Files:**
- Modify: `workspace/robustness_checks.py`
- Modify: `workspace/heterogeneity_analysis.py`
- Modify: `workspace/test_hypotheses_updated.py`
- Modify: `workspace/paper-revision/robustness_checks/robustness_report_FINAL.md`
- Modify: `workspace/paper-revision/heterogeneity_analysis/heterogeneity_report_FINAL.md`

**Checklist:**
- Correct every place where `IRR < 1` is described as an increase.
- Recompute and reinterpret placebo statistics with the correct tail logic.
- Remove any causal language justified only by the placebo test.
- Fix numpy/pandas boolean serialization so JSON outputs complete successfully.
- Regenerate results files after code fixes and delete truncated artifacts.

**Done Criteria:**
- No report describes a ratio below 1 as a positive increase.
- `all_results_updated.json`, `robustness_results.json`, and `heterogeneity_results.json` save successfully and parse as valid JSON.

---

### Task 7: Apply Minimum Evidentiary Thresholds to Supplementary Analyses

**Files:**
- Modify: `workspace/heterogeneity_analysis.py`
- Modify: `workspace/case_studies_analysis.py`
- Modify: `workspace/draft_chapters/04_results_revised.md`
- Modify: `workspace/paper-revision/case_studies/case_studies_report_FINAL.md`

**Checklist:**
- Add minimum sample rules for subgroup analysis.
- Do not report a platform-specific estimate when the platform has only trivial coverage.
- Do not elevate a single dramatic case like `E031` into general evidence if its inferential test is not significant.
- Move fragile case studies to appendix or exploratory analysis if they cannot support chapter-level claims.

**Done Criteria:**
- Every supplementary result is labeled as `confirmatory`, `robustness`, or `exploratory`.
- No exploratory case study is used as if it validates the main theory.

---

### Task 8: Rewrite the Methods Chapter from Actual Practice, Not Intended Practice

**Files:**
- Modify: `workspace/draft_chapters/03_methodology_FINAL.md`

**Checklist:**
- Remove unsupported claims about Weibo, 800 natural days, and unavailable software pipelines.
- Remove unimplemented elements such as LDA, artificial theme coding, R workflows, and Stata workflows unless they are genuinely executed and archived.
- Replace placeholder ethics, OSF, and repository claims with verified statements only.
- Separate "what was planned" from "what was actually done"; keep only the latter in the final chapter.

**Done Criteria:**
- A reviewer can follow the chapter and reproduce the study without guessing.
- No sentence in methods requires a file or approval number that does not exist.

---

### Task 9: Rewrite the Results Chapter from Regenerated Outputs

**Files:**
- Modify: `workspace/draft_chapters/04_results_revised.md`
- Inspect: `workspace/paper-revision/event_analysis/*.json`
- Inspect: `workspace/paper-revision/robustness_checks/*.json`
- Inspect: `workspace/paper-revision/heterogeneity_analysis/*.json`
- Inspect: `workspace/paper-revision/figures/*.pdf`

**Checklist:**
- Delete the duplicated 4.6/4.7 block and keep one clean narrative.
- Remove every TODO line from the chapter.
- Replace all tables with values copied from regenerated outputs only.
- Rewrite robustness and heterogeneity subsections so direction, magnitude, and uncertainty are interpreted correctly.
- Downgrade any result that fails rerun verification from "main result" to "exploratory note" or delete it.

**Done Criteria:**
- The results chapter contains no TODOs, no duplicated sections, and no numbers without a backing artifact.
- Every table and figure caption points to a real generated artifact.

---

### Task 10: Rewrite Discussion and Conclusion Conservatively

**Files:**
- Modify: `workspace/draft_chapters/05_discussion_final.md`
- Modify: `workspace/draft_chapters/06_conclusion_FINAL.md`

**Checklist:**
- Rewrite all theoretical claims to match the surviving evidence only.
- Remove any sentence that infers causal mechanism from observational social media data.
- Stop using H2 and H5 as disguised contributions.
- Reframe contributions as descriptive, associational, and methodological unless stronger identification is actually demonstrated.
- Keep limitations sharper than contributions; do not bury the structural weaknesses.

**Done Criteria:**
- The discussion never overclaims beyond the re-estimated models.
- The conclusion no longer states internally inconsistent dataset facts.

---

### Task 11: Audit References and Remove Fabrication Risk

**Files:**
- Modify: `workspace/draft_chapters/01_introduction_revised_v2.md`
- Modify: `workspace/draft_chapters/02_literature_review_FINAL.md`
- Modify: `workspace/draft_chapters/05_discussion_final.md`
- Modify: `workspace/draft_chapters/06_conclusion_FINAL.md`
- Create: `workspace/reference_verification_log.md`

**Checklist:**
- Verify every 2023-2025 citation manually against a real source.
- Delete any citation that cannot be located exactly.
- Remove the sentence admitting that some recent references were "reasonable inference".
- Mark every retained reference in a verification log with status: `verified`, `replace`, or `delete`.

**Done Criteria:**
- No fabricated or placeholder citation remains in the manuscript.
- The literature review no longer contains self-incriminating disclaimers.

---

### Task 12: Final Cross-Chapter Consistency Pass

**Files:**
- Modify: `workspace/draft_chapters/00_abstract_FINAL.md`
- Modify: `workspace/draft_chapters/01_introduction_revised_v2.md`
- Modify: `workspace/draft_chapters/02_literature_review_FINAL.md`
- Modify: `workspace/draft_chapters/03_methodology_FINAL.md`
- Modify: `workspace/draft_chapters/04_results_revised.md`
- Modify: `workspace/draft_chapters/05_discussion_final.md`
- Modify: `workspace/draft_chapters/06_conclusion_FINAL.md`
- Create: `workspace/final_consistency_matrix.md`

**Checklist:**
- Build a final matrix for sample size, platform count, date count, event count, hypothesis set, main coefficients, and key qualitative claims.
- Check that abstract, introduction, methods, results, discussion, and conclusion all use the same values.
- Run a search for these risk phrases and delete or fix every hit: `微博`, `4 个平台`, `800 天`, `355 天`, `540 天`, `TODO`, `待填写`, `合理推断`, `支持因果推断`.

**Done Criteria:**
- One matrix row per core fact, one identical value across all chapters.
- No placeholder, unsupported, or contradictory statement remains.

---

## Recommended Execution Order

1. Task 1
2. Task 2
3. Task 3
4. Task 4
5. Task 5
6. Task 6
7. Task 7
8. Task 8
9. Task 9
10. Task 10
11. Task 11
12. Task 12

---

## Stoplight Priorities

### Red: Must Fix Before Any Submission
- Task 1
- Task 3
- Task 4
- Task 5
- Task 6
- Task 8
- Task 9
- Task 11
- Task 12

### Yellow: Fix Before Claiming Theoretical Contribution
- Task 7
- Task 10

### Green: Final Packaging
- Abstract shortening
- Figure caption polish
- Style and formatting cleanup

---

## Definition of "Ready to Send"

The paper is ready for external review only if all of the following are true:

- One canonical analysis script regenerates all core numbers.
- One canonical evidence table matches every chapter.
- No unsupported platform, date, software, ethics, or preregistration claim remains.
- No result direction is misinterpreted.
- No reference remains unverified.
- Results chapter contains zero TODOs and zero duplicated sections.
