# Final Consistency Matrix

**Date**: 2026-04-14  
**Scope**: Canonical thesis chapters after the revised-hypothesis restructuring  
**Evidence sources**: `processed_data/all_processed_data.csv`, `processed_data/data_quality_report.md`, `revised_hypothesis_analysis/summary.json`, `revised_hypothesis_analysis/analysis_report.md`

## Core Facts

| Fact | Evidence Baseline | Abstract | Ch1 Intro | Ch3 Methods | Ch4 Results | Ch5 Discussion | Ch6 Conclusion | PASS? |
|:---|:---|:---|:---|:---|:---|:---|:---|:---|
| Total comments | 142,426 | 142,426 | 142,426 | 142,426 | 142,426 | 142,426 | 142,426 | Yes |
| Insecurity-related comments | 1,679 | 1,679 | 1,679 | 1,679 | 1,679 | 1,679 | 1,679 | Yes |
| Insecurity-related ratio | 1.18% | 1.18% | 1.18% | 1.18% | 1.18% | 1.18% | 1.18% | Yes |
| Platform count | 4 | 4 | 4 | 4 | 4 | 4 | 4 | Yes |
| Core inference platforms | 知乎 + 哔哩哔哩 | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Descriptive-only platforms | 微博 + 小红书 | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Full-sample date range | 2024-10-12 to 2026-04-13 | 2024.10-2026.04 | 2024.10-2026.04 | 2024-10-12 to 2026-04-13 | 2024-10-12 to 2026-04-13 | 2024-10-12 to 2026-04-13 | 2024-10-12 to 2026-04-13 | Yes |
| Unique observation dates | 380 | 380 | 380 | 380 | 380 | 380 | 380 | Yes |
| Main trend sample | 哔哩哔哩 366 days | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Main trend range | 2024-10-12 to 2026-03-30 | No explicit value | Yes | Yes | Yes | Yes | No explicit value | Yes |

## Hypotheses

| Item | Evidence Baseline | Abstract | Ch1 Intro | Ch3 Methods | Ch4 Results | Ch5 Discussion | Ch6 Conclusion | PASS? |
|:---|:---|:---|:---|:---|:---|:---|:---|:---|
| H1 statement | 平台异质性 | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| H1 main comparison | 知乎 vs 哔哩哔哩 | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| H1 zhihu rate | 2.19% | 2.19% | 2.19% | 2.19% | 2.19% | 2.19% | 2.19% | Yes |
| H1 bili rate | 0.86% | 0.86% | 0.86% | 0.86% | 0.86% | 0.86% | 0.86% | Yes |
| H1 z statistic | 19.833 | 19.833 | 19.833 | 19.833 | 19.833 | 19.833 | 19.833 | Yes |
| H1 significance | p < 0.001 | p < 0.001 | p < 0.001 | p < 0.001 | p = 1.54 × 10^-87 | p < 0.001 | p = 1.54 × 10^-87 | Yes |
| H2 statement | 议题异质性 | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| H2 eligible queries | 11 | No explicit value | Yes | Yes | 11 | No explicit value | No explicit value | Yes |
| H2 chi-square | 113.456 | 113.456 | 113.456 | 113.456 | 113.456 | 113.456 | 113.456 | Yes |
| H2 Monte Carlo p | 0.0002 | 0.0002 | 0.0002 | 0.0002 | 0.0002 | 0.0002 | 0.0002 | Yes |
| H3 statement | 时间动态 | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| H3 main platform | 哔哩哔哩 | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| H3 main slope | 0.00002293 | 0.00002293 | 0.00002293 | 0.00002293 | 0.00002293 | 0.00002293 | 0.00002293 | Yes |
| H3 main p | 0.0002 | 0.0002 | 0.0002 | 0.0002 | 0.0002 | 0.0002 | 0.0002 | Yes |
| H3 full-sample slope | 0.00003852 | No explicit value | 0.00003852 | 0.00003852 | 0.00003852 | No explicit value | 0.00003852 | Yes |
| Event analysis status | Exploratory only | Yes | Yes | Yes | Yes | Yes | Yes | Yes |

## Terminology Audit

| Phrase / Claim | Required Status | Result |
|:---|:---|:---|
| `影响` as headline causal framing | Absent from core claims | Pass |
| `导致` as causal interpretation of findings | Absent from findings sections | Pass |
| `验证因果` | Absent | Pass |
| `构念水平变化` | Absent as direct interpretation | Pass |
| “事件主效应是核心贡献” | Absent | Pass |
| “恢复时间是主假设” | Absent | Pass |

## Structural Audit

| Rule | Status |
|:---|:---|
| Title switched from event-effect framing to heterogeneity and dynamics framing | Pass |
| Abstract centers H1, H2, H3 rather than event effects | Pass |
| Methods chapter distinguishes theoretical object and observable proxy | Pass |
| Results chapter reports formal tests for H1 and H2 | Pass |
| Trend analysis limited to reliable timestamp sample as main result | Pass |
| Weibo and Xiaohongshu retained as descriptive supplements only | Pass |
| Event window analysis downgraded to exploratory status | Pass |

## Residual Risks

- `citations_extracted.txt` may still reflect the old chapter set and should not be treated as the current citation baseline.
- The Word build script carries separately maintained abstract text and must remain synchronized with the canonical abstract.
- If later data cleaning changes the query threshold or timestamp coverage, H2 and H3 statistics must be refreshed together across all chapters.
