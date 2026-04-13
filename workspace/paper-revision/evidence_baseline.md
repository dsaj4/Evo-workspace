# Evidence Baseline (Canonical Facts)

**Generated**: 2026-04-10  
**Source**: Direct inspection of processed data files  
**Status**: These are the ONLY numbers the manuscript may quote.

---

## 1. Raw Data Scope

| Metric | Value | Source File |
|:---|---:|:---|
| Total comments | **114,915** | `all_processed_data.csv` (shape: 114,915 rows) |
| Platforms | **3** (bili, xhs, zhihu) | `all_processed_data.csv`, column `platform` |
| Unique calendar dates | **361** | `daily_data.parquet`, column `date` (nunique) |
| Date range | 2024-10-12 to 2026-03-30 | `daily_data.parquet` |
| Panel rows (platform-date) | **800** | `daily_data.parquet` (shape[0]) |
| Events | **33** | `event_database.csv` |

### 1.1 Platform Distribution

| Platform | Code | Notes |
|:---|:---|:---|
| Bilibili | bili | Present |
| Xiaohongshu | xhs | Present |
| Zhihu | zhihu | Present |
| Weibo | weibo | **NOT PRESENT** - must not be mentioned |

### 1.2 Key Insecurity Metrics

| Metric | Value | Notes |
|:---|---:|:---|
| Total insecurity comments | **2,484** | Sum of `insecurity_count` in daily parquet |
| Mean daily insecurity ratio | **0.00557** (0.557%) | Mean of `insecurity_ratio` |

### 1.3 Event Distribution

| Event Type | Count |
|:---|---:|
| tech_positive | 26 |
| job_negative | 4 |
| policy | 2 |
| report | 1 |
| **Total** | **33** |

---

## 2. Canonical Study Scope (DECISIONS)

| Parameter | Canonical Value | Notes |
|:---|:---|:---|
| Comment count | 114,915 | From all_processed_data.csv |
| Platform count | 3 | bili, xhs, zhihu. No weibo. |
| Unique calendar days | 361 | Date range: 2024-10-12 to 2026-03-30 |
| Panel rows | 800 | Platform-date rows (NOT calendar days) |
| Event count | 33 | 26 tech_positive, 4 job_negative, 2 policy, 1 report |

---

## 3. Forbidden Claims

These claims must NOT appear in any chapter:

- **4 platforms** - Only 3 exist in data
- **Weibo / 微博** - Not in data
- **800 days / 800 天** as calendar days - 800 is panel rows, 361 is unique dates
- **355 days** - Not the correct date range
- **~540 days** - Not verifiable
- **R analysis / Stata analysis** - Not used
- **LDA topic modeling** - Not implemented
- **OSF preregistration** - Not done
- **GitHub repository** - Not created
- **Ethics approval with specific number** - Not obtained
- **H2 or H5 as contributions** - Both deleted
- **Causal mechanism claims** - Observational data only

---

## 4. Canonical Hypotheses

| Hypothesis | Content |
|:---|:---|
| **H1** | AI tech events increase insecurity expression (IRR > 1, 7-day window) |
| **H3** | Effect decays rapidly; returns to baseline within 7-10 days |
| **H4** | Platform-level differences exist among the 3 platforms |
| **H6** | Upward time trend in baseline insecurity expression |

---

**This file is the single source of truth. All chapters must align with these facts.**
