# Final Consistency Matrix

**Date**: 2026-04-10
**Scope**: All canonical chapters verified against evidence baseline

## Core Facts — Consistency Check

| Fact | Evidence Baseline | Abstract | Ch1 Intro | Ch2 Lit Rev | Ch3 Methods | Ch4 Results | Ch5 Discussion | Ch6 Conclusion | PASS? |
|------|-------------------|----------|-----------|-------------|-------------|-------------|----------------|----------------|-------|
| **Total comments** | 114,915 | 114,915 | 114,915 | — | 114,915 | 114,915 | — | 114,915 | ✅ |
| **Insecurity comments** | 1,242 | 1,242 | — | — | 1,242 | 1,242 | 1,242 | 1,242 | ✅ |
| **Insecurity ratio** | 1.08% | 1.08% | — | — | 1.08% | 1.08% | 1.08% | 1.08% | ✅ |
| **Platforms** | 3 (bili, xhs, zhihu) | 3 | 3 | — | 3 | 3 (xhs excluded from inference) | 3 | 3 | ✅ |
| **Unique dates** | 361 | 361 | 361 | — | 361 | 361 | — | 361 | ✅ |
| **Date range** | 2024-10-12 to 2026-03-30 | 2024.10–2026.03 | 2024.10–2026.03 | — | 2024-10-12–2026-03-30 | 2024-10-12–2026-03-30 | — | 2024-10-12–2026-03-30 | ✅ |
| **Events** | 33 | 33 | 33 | — | 33 | 33 | 33 | 33 | ✅ |
| **Panel rows** | 439 | — | — | — | 439 | — | — | — | ✅ |

## Hypotheses — Consistency Check

| Item | Evidence Baseline | Abstract | Ch1 Intro | Ch3 Methods | Ch4 Results | Ch5 Discussion | Ch6 Conclusion | PASS? |
|------|-------------------|----------|-----------|-------------|-------------|----------------|----------------|-------|
| **H1 IRR** | 0.6533 | 0.653 | 0.653 | — | 0.653 | 0.653 | 0.653 | ✅ |
| **H1 p-value** | 0.083 | 0.083 | — | — | 0.083 | — | — | ✅ |
| **H1 supported?** | No (p>0.05) | 不显著 | 不显著 | — | 不显著 | 不显著 | 不显著 | ✅ |
| **H3 recovery** | 3 days | 3 天 | 3 天 | — | 3 天 | 3 天 | 3 天 | ✅ |
| **H4 zhihu** | 2.80% | 2.80% | 2.80% | — | 2.80% | 2.80% | 2.80% | ✅ |
| **H4 bili** | 0.86% | 0.86% | 0.86% | — | 0.86% | 0.86% | 0.86% | ✅ |
| **H4 xhs** | 0.70% (3 dates, excluded) | excluded | excluded | — | excluded from inference | excluded | excluded | ✅ |
| **H6 IRR** | 1.030 | 1.030 | 1.030 | — | 1.030 | 1.030 | 1.030 | ✅ |
| **H6 p-value** | <0.001 | <0.001 | — | — | <0.001 | — | — | ✅ |

## Risk Phrase Audit

| Risk Phrase | Abstract | Ch1 | Ch2 | Ch3 | Ch4 | Ch5 | Ch6 | Status |
|-------------|----------|-----|-----|-----|-----|-----|-----|--------|
| `微博` / Weibo | ❌ absent | ❌ absent | ❌ absent | ❌ absent | ❌ absent | ❌ absent | ❌ absent | ✅ Clean |
| `4 个平台` | ❌ absent | ❌ absent | ❌ absent | ❌ absent | ❌ absent | ❌ absent | ❌ absent | ✅ Clean |
| `800 天` | ❌ absent | ❌ absent | ❌ absent | ❌ absent | ❌ absent | ❌ absent | ❌ absent | ✅ Clean |
| `355 天` | ❌ absent | ❌ absent | ❌ absent | ❌ absent | ❌ absent | ❌ absent | ❌ absent | ✅ Clean |
| `540 天` | ❌ absent | ❌ absent | ❌ absent | ❌ absent | ❌ absent | ❌ absent | ❌ absent | ✅ Clean |
| `TODO` | ❌ absent | ❌ absent | ❌ absent | ❌ absent | ❌ absent | ❌ absent | ❌ absent | ✅ Clean |
| `待填写` | ❌ absent | ❌ absent | ❌ absent | ❌ absent | ❌ absent | ❌ absent | ❌ absent | ✅ Clean |
| `支持因果推断` | ❌ absent | ❌ absent | ❌ absent | ❌ absent | ❌ absent | ❌ absent | ❌ absent | ✅ Clean |

## Citation Status

- Canonical chapters: **0 parenthetical citations** (intentionally citation-light to avoid fabrication risk)
- Reference verification log: **36 citations audited** → 7 deleted, 3 years fixed
- A separate BibTeX bibliography can be generated from the verified reference list

## Remediation Plan Compliance

| Rule | Status |
|------|--------|
| No number without traceable file | ✅ All numbers from `canonical_results/` or `evidence_baseline.md` |
| No "800 days" or "361 days" conflict | ✅ 361 unique dates used consistently; 439 panel rows documented separately |
| No Weibo claim | ✅ Only 3 platforms throughout |
| No H2 or H5 as headline contributions | ✅ H2/H5 not mentioned as contributions |
| No fake ethics/OSF/GitHub claims | ✅ No such claims in canonical chapters |
| Methods chapter matches actual practice | ✅ Only executed methods described |
| Results chapter has no TODOs | ✅ Zero TODO lines |
| No causal language from observational data | ✅ "关联" not "影响"; "描述性" framing |
| Discussion never overclaims | ✅ Limitations sharper than contributions |

---

*Generated from canonical evidence baseline. All values traceable to `run_canonical_analysis.py` output.*
