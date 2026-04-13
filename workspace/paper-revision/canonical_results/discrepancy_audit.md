# Critical Discrepancy Audit

**Date**: 2026-04-10

## Canonical Results vs Paper Claims

| Metric | Paper Claim | Canonical Result | Status |
|--------|-------------|-----------------|--------|
| **Platforms** | 4 (微博, 知乎, B站, 小红书) | 3 (bili, xhs, zhihu) | MISMATCH |
| **Weibo** | Yes | Absent from data | FABRICATION |
| **Unique dates** | 800 | 361 | MISMATCH (800 = panel rows, not dates) |
| **H1 IRR** | 1.45 (p<0.001, +45%) | 0.6533 (p=0.083, -34.7%) | CRITICAL MISMATCH |
| **H1 Supported** | YES | NO (p=0.083 > 0.05) | CRITICAL |
| **H3 Half-life** | 1.36 days | 0 days | MISMATCH |
| **H3 Recovery** | 7-10 days | Day 3 | MISMATCH |
| **H4 Zhihu** | 2.80% | 2.80% | MATCH |
| **H4 Bili** | 0.86% | 0.86% | MATCH |
| **H4 Xiaohongshu** | 0.70% (361 days) | 0.70% (3 days only) | CRITICAL - insufficient data |
| **H6 Trend** | p<0.001 upward | IRR=1.03, p<0.001 | CONSISTENT |
| **Total comments** | 114,915 | 114,915 | MATCH |
| **Insecurity comments** | 1,242 | 1,242 | MATCH |
| **Events** | 33 | 33 | MATCH |

## Root Cause Analysis: H1 Discrepancy

The paper claims IRR=1.45 (p<0.001). The canonical pipeline gives IRR=0.6533 (p=0.083).

### Possible Explanations

1. **Statistical Unit**: The previous analysis may have used the platform-day panel (800 rows, including "all" pseudo-platform) instead of natural-day totals (361 rows). Using more rows can inflate significance.

2. **Event Window Construction**: The event dummy might have been applied differently (e.g., before/after instead of a window, or including different events).

3. **Controls**: Different control variables (or no controls) could dramatically change the coefficient.

4. **Model Family**: Previous analysis might have used OLS or a different family instead of Negative Binomial.

### Investigation Needed

- Re-run the analysis on the platform-day panel to see if IRR=1.45 appears
- Check if the "all" pseudo-platform was included in previous analysis
- Verify the exact event window construction in the original test_all_hypotheses.py

## Implications

If H1 is truly NOT supported (p=0.083):
- The paper's central claim is weakened
- H1 must be reframed as "marginal" or "not supported at conventional levels"
- The discussion must acknowledge this limitation prominently
- The contribution shifts from "AI events increase insecurity" to "no strong evidence of systematic increase, but notable platform differences"

## Immediate Actions Required

1. Do NOT claim H1 is supported until the discrepancy is resolved
2. Mark all H1-related claims as "pending verification"
3. Update the evidence baseline with the canonical results
4. Investigate the source of the IRR=1.45 claim
