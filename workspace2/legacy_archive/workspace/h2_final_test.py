import glob
from datetime import timedelta

import numpy as np
import pandas as pd
from scipy import stats

print("=" * 70)
print("H2 重新检验 - 事件类型调节效应分析")
print("=" * 70)

# 读取事件数据
csv_file = glob.glob("E:/Project/论文/workspace/eventdatabase/*.CSV")[0]
events_df = pd.read_csv(csv_file, encoding="gbk", skiprows=3)

# 读取日度数据
daily_df = pd.read_parquet(
    "E:/Project/论文/workspace/paper-revision/processed_data/daily_data.parquet"
)
daily_df["date"] = pd.to_datetime(daily_df["date"])

print("\n【数据概况】")
print(f"事件总数：{len(events_df)}")
print(f"日度数据：{len(daily_df)} 天")
print(f"时间范围：{daily_df['date'].min().date()} 至 {daily_df['date'].max().date()}")

# 分类事件
tech_events = events_df[events_df["event_type"] == "tech_positive"]
job_events = events_df[events_df["event_type"] == "job_negative"]

print("\n【事件分类】")
print(f"技术突破事件：{len(tech_events)} 个")
print(f"失业裁员事件：{len(job_events)} 个")


# 计算每个事件后 7 天的效应
def calculate_event_effect(event_date, daily_df, window=7):
    """计算事件后 window 天相对于事件前 window 天的效应"""
    event_date = pd.to_datetime(event_date)
    post_window = daily_df[
        (daily_df["date"] > event_date)
        & (daily_df["date"] <= event_date + timedelta(days=window))
    ]
    pre_window = daily_df[
        (daily_df["date"] > event_date - timedelta(days=window))
        & (daily_df["date"] <= event_date)
    ]

    if len(post_window) > 0 and len(pre_window) > 0:
        effect = (
            post_window["insecurity_count"].mean()
            - pre_window["insecurity_count"].mean()
        )
        return effect
    return None


# 计算技术事件效应
tech_effects = []
for _, event in tech_events.iterrows():
    effect = calculate_event_effect(event["event_date"], daily_df)
    if effect is not None:
        tech_effects.append(effect)

# 计算负面事件效应
job_effects = []
for _, event in job_events.iterrows():
    effect = calculate_event_effect(event["event_date"], daily_df)
    if effect is not None:
        job_effects.append(effect)

print("\n【效应量统计】")
print(
    f"技术事件平均效应：{np.mean(tech_effects):.3f} (SD={np.std(tech_effects):.3f}, n={len(tech_effects)})"
)
print(
    f"负面事件平均效应：{np.mean(job_effects):.3f} (SD={np.std(job_effects):.3f}, n={len(job_effects)})"
)

# 效应量比值
if len(tech_effects) > 0 and len(job_effects) > 0:
    ratio = (
        np.mean(job_effects) / np.mean(tech_effects)
        if np.mean(tech_effects) != 0
        else float("inf")
    )
    print(f"效应量比值 (负面/技术): {ratio:.2f} 倍")

# t 检验
print("\n【H2 假设检验】")
if len(tech_effects) > 0 and len(job_effects) > 0:
    t_stat, p_value = stats.ttest_ind(job_effects, tech_effects, equal_var=False)
    print(f"t 统计量：{t_stat:.3f}")
    print(f"p 值：{p_value:.4f}")

    if p_value < 0.05:
        print(f"\n✅ H2 获得支持！负面事件效应显著强于技术事件 (p={p_value:.4f})")
    else:
        print(f"\n⚠️ H2 未获支持 (p={p_value:.4f} > 0.05)")

    # 效应量 Cohen's d
    pooled_std = np.sqrt((np.std(tech_effects) ** 2 + np.std(job_effects) ** 2) / 2)
    cohens_d = (np.mean(job_effects) - np.mean(tech_effects)) / pooled_std
    print(f"Cohen's d: {cohens_d:.3f}")

    if abs(cohens_d) >= 0.8:
        print("效应强度：大效应")
    elif abs(cohens_d) >= 0.5:
        print("效应强度：中等效应")
    else:
        print("效应强度：小效应")
else:
    print("⚠️ 数据不足，无法进行 t 检验")

# 保存结果
results = {
    "H2_test": {
        "tech_events_n": len(tech_effects),
        "job_events_n": len(job_effects),
        "tech_mean_effect": float(np.mean(tech_effects)),
        "job_mean_effect": float(np.mean(job_effects)),
        "effect_ratio": float(ratio),
        "t_statistic": float(t_stat),
        "p_value": float(p_value),
        "cohens_d": float(cohens_d),
        "supported": p_value < 0.05,
    }
}

import json

with open(
    "E:/Project/论文/workspace/paper-revision/event_analysis/h2_retest_results.json",
    "w",
    encoding="utf-8",
) as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print("\n【结果已保存】")
print(
    "文件：E:/Project/论文/workspace/paper-revision/event_analysis/h2_retest_results.json"
)
print("=" * 70)
