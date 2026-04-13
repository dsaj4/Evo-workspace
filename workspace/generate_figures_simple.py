#!/usr/bin/env python
# -*- coding: utf-8 -*-
r"""
Figure 1-6 图表生成脚本（简化版）
使用：E:\Project\论文\.venv\Scripts\python.exe generate_figures_simple.py
"""

import pandas as pd
import numpy as np
from pathlib import Path
import sys


def _get_series(df, primary, fallback=None):
    """Return a numeric series from *df*, supporting legacy/fallback names."""
    if primary in df.columns:
        return pd.to_numeric(df[primary], errors="coerce")
    if fallback and fallback in df.columns:
        return pd.to_numeric(df[fallback], errors="coerce")
    raise KeyError(f"Missing column: {primary}" + (f" or {fallback}" if fallback else ""))


def _as_percent(series):
    """Normalize a rate-like series to percent units for plotting."""
    numeric = pd.to_numeric(series, errors="coerce")
    max_abs = numeric.abs().max(skipna=True)
    if pd.notna(max_abs) and max_abs <= 1.0:
        return numeric * 100
    return numeric

# 尝试导入 matplotlib
try:
    import matplotlib
    matplotlib.use('Agg')  # 非交互式后端
    import matplotlib.pyplot as plt
    import seaborn as sns
    HAS_MATPLOTLIB = True
    print("[OK] matplotlib 和 seaborn 已加载")
except ImportError as e:
    HAS_MATPLOTLIB = False
    print(f"[ERROR] matplotlib/seaborn 不可用：{e}")
    print("将仅导出数据文件，请手动绘制图表")

# 设置中文字体
if HAS_MATPLOTLIB:
    plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
    plt.rcParams['axes.unicode_minus'] = False

DATA_DIR = Path("E:/Project/论文/workspace/paper-revision/figures_data")
OUTPUT_DIR = Path("E:/Project/论文/workspace/paper-revision/figures")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print("=" * 80)
print("Figure 1-6 图表生成")
print("=" * 80)

if not HAS_MATPLOTLIB:
    print("\nmatplotlib 未安装，仅导出数据文件。")
    print("\n请使用以下命令安装:")
    print("  E:\\Project\\论文\\.venv\\Scripts\\python.exe -m pip install matplotlib seaborn")
    print("\n或使用 Excel 手动绘制（参考 EXCEL_PLOTTING_GUIDE.md）")
    sys.exit(0)

# ============================================================================
# Figure 1: 时间序列图
# ============================================================================
print("\n[1/6] 生成 Figure 1: 时间序列图...")

fig1_data = pd.read_csv(DATA_DIR / "fig1_timeseries.csv")
fig1_data['date'] = pd.to_datetime(fig1_data['date'])
fig1_rate = _as_percent(_get_series(fig1_data, 'insecurity_rate', 'insecurity_ratio'))
fig1_ma7 = _as_percent(_get_series(fig1_data, 'rate_ma7'))

fig, ax = plt.subplots(figsize=(14, 8))

# 绘制日度数据（面积图）
ax.fill_between(fig1_data['date'], fig1_rate,
                alpha=0.3, color='#2E86AB', label='日度表达率')

# 绘制 7 天移动平均（折线图）
ax.plot(fig1_data['date'], fig1_ma7,
        color='#A23B72', linewidth=2.5, label='7 天移动平均')

# 添加主要事件标注
major_events = [
    ('2025-02-05', 'Gemini 2.0'),
    ('2025-05-23', 'Claude 4'),
    ('2025-08-08', 'GPT-5'),
    ('2025-09-30', 'Claude 4.5'),
    ('2025-12-23', 'GLM-4.7'),
]

for event_date, event_name in major_events:
    ax.axvline(pd.to_datetime(event_date), color='red', linestyle='--', 
               linewidth=1, alpha=0.7)
    ax.text(pd.to_datetime(event_date), fig1_ma7.max()*0.95,
            event_name, rotation=90, fontsize=9, ha='right', va='top')

ax.set_xlabel('日期', fontsize=12)
ax.set_ylabel('不安全感表达率 (%)', fontsize=12)
ax.set_title('Figure 1 职业不安全感表达的时间序列（2024.10-2026.03）', fontsize=14)
ax.legend(loc='upper right')
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(OUTPUT_DIR / "figure1_timeseries.png", dpi=300, bbox_inches='tight')
plt.savefig(OUTPUT_DIR / "figure1_timeseries.pdf", bbox_inches='tight')
plt.close()

print(f"  [OK] 已保存：figure1_timeseries.png/pdf")

# ============================================================================
# Figure 2: 森林图
# ============================================================================
print("\n[2/6] 生成 Figure 2: 森林图...")

fig2_data = pd.read_csv(DATA_DIR / "fig2_forest.csv")

# 颜色映射
color_map = {
    'tech_positive': '#2E86AB',
    'job_negative': '#A23B72',
    'policy': '#F18F01',
    'report': '#C73E1D'
}

fig, ax = plt.subplots(figsize=(10, 8))

# 绘制森林图
y_pos = np.arange(len(fig2_data))

for i, (_, row) in enumerate(fig2_data.iterrows()):
    color = color_map.get(row['event_type'], '#333333')
    ax.errorbar(row['irr'], i, xerr=[[row['irr'] - row['ci_low']], 
                [row['ci_high'] - row['irr']]], fmt='o', color=color, 
                ecolor='gray', capsize=5, markersize=8, label=row['event_type'] if i==0 else "")

# 添加参考线 x=1
ax.axvline(x=1, color='red', linestyle='--', linewidth=2, alpha=0.7)

ax.set_xlabel('发生率比 (IRR)', fontsize=12)
ax.set_ylabel('事件', fontsize=12)
ax.set_title('Figure 2 各事件后职业不安全感表达效应的森林图', fontsize=14)
ax.set_yticks(y_pos)
ax.set_yticklabels(fig2_data['event_id'], fontsize=9)
ax.grid(True, alpha=0.3, axis='x')

# 自定义图例
from matplotlib.lines import Line2D
legend_elements = [
    Line2D([0], [0], marker='o', color='w', markerfacecolor='#2E86AB', markersize=10, label='tech_positive'),
    Line2D([0], [0], marker='o', color='w', markerfacecolor='#A23B72', markersize=10, label='job_negative'),
    Line2D([0], [0], marker='o', color='w', markerfacecolor='#F18F01', markersize=10, label='policy'),
]
ax.legend(handles=legend_elements, loc='upper right')

plt.tight_layout()
plt.savefig(OUTPUT_DIR / "figure2_forest.png", dpi=300, bbox_inches='tight')
plt.savefig(OUTPUT_DIR / "figure2_forest.pdf", bbox_inches='tight')
plt.close()

print(f"  [OK] 已保存：figure2_forest.png/pdf")

# ============================================================================
# Figure 3: 动态衰减曲线
# ============================================================================
print("\n[3/6] 生成 Figure 3: 动态衰减曲线...")

fig3_data = pd.read_csv(DATA_DIR / "fig3_decay.csv")

fig, ax = plt.subplots(figsize=(10, 7))

# 绘制观测值（带误差线）
ax.errorbar(fig3_data['day'], fig3_data['mean_effect'], 
            yerr=fig3_data['std_effect'], fmt='o', color='#2E86AB', 
            ecolor='gray', capsize=4, markersize=6, label='观测值')

# 绘制拟合曲线
ax.plot(fig3_data['day'], fig3_data['fitted'], '-', color='#A23B72', 
        linewidth=2.5, label='指数拟合')

# 添加参考线
ax.axhline(y=0, color='green', linestyle='--', linewidth=1.5, alpha=0.7, label='基线')
ax.axhline(y=5, color='gray', linestyle=':', linewidth=1.5, alpha=0.7, label='+5% 阈值')

# 添加半衰期标注
ax.annotate('半衰期 = 1.36 天', xy=(5, 20), fontsize=11, 
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

ax.set_xlabel('事件后天数', fontsize=12)
ax.set_ylabel('相对基线变化 (%)', fontsize=12)
ax.set_title('Figure 3 事件后职业不安全感表达的动态衰减曲线', fontsize=14)
ax.legend(loc='upper right')
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(OUTPUT_DIR / "figure3_decay.png", dpi=300, bbox_inches='tight')
plt.savefig(OUTPUT_DIR / "figure3_decay.pdf", bbox_inches='tight')
plt.close()

print(f"  [OK] 已保存：figure3_decay.png/pdf")

# ============================================================================
# Figure 4: 箱线图
# ============================================================================
print("\n[4/6] 生成 Figure 4: 箱线图...")

fig4_data = pd.read_csv(DATA_DIR / "fig4_boxplot.csv")
fig4_data['plot_rate'] = _as_percent(
    _get_series(fig4_data, 'insecurity_rate', 'insecurity_ratio')
)

# 按平台分组
platforms = ['zhihu', 'bili', 'xhs', 'all']
platform_names = {'zhihu': '知乎', 'bili': 'B 站', 'xhs': '小红书', 'all': '全平台'}
colors = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D']

fig, ax = plt.subplots(figsize=(10, 7))

data_to_plot = [fig4_data[fig4_data['platform'] == p]['plot_rate'].values
                for p in platforms]

bp = ax.boxplot(
    data_to_plot,
    patch_artist=True,
    tick_labels=[platform_names[p] for p in platforms],
)

# 设置箱体颜色
for patch, color in zip(bp['boxes'], colors):
    patch.set_facecolor(color)
    patch.set_alpha(0.7)

# 添加均值点
means = [fig4_data[fig4_data['platform'] == p]['plot_rate'].mean() for p in platforms]
ax.plot(range(1, len(platforms)+1), means, 'D', color='red', markersize=12, label='均值')

ax.set_xlabel('平台', fontsize=12)
ax.set_ylabel('不安全感表达率 (%)', fontsize=12)
ax.set_title('Figure 4 分平台职业不安全感表达率箱线图', fontsize=14)
ax.legend(loc='upper right')
ax.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig(OUTPUT_DIR / "figure4_boxplot.png", dpi=300, bbox_inches='tight')
plt.savefig(OUTPUT_DIR / "figure4_boxplot.pdf", bbox_inches='tight')
plt.close()

print(f"  [OK] 已保存：figure4_boxplot.png/pdf")

# ============================================================================
# Figure 5: 时间趋势图
# ============================================================================
print("\n[5/6] 生成 Figure 5: 时间趋势图...")

fig5_data = pd.read_csv(DATA_DIR / "fig5_trend.csv")
fig5_data['date'] = pd.to_datetime(fig5_data['date'])
fig5_residual = _as_percent(_get_series(fig5_data, 'residual_rate', 'insecurity_ratio'))
fig5_loess = _as_percent(_get_series(fig5_data, 'loess'))
fig5_trend = _as_percent(_get_series(fig5_data, 'trend'))

fig, ax = plt.subplots(figsize=(14, 8))

# 绘制残差序列
ax.plot(fig5_data['date'], fig5_residual,
        color='#2E86AB', linewidth=0.8, alpha=0.5, label='残差序列')

# 绘制 LOESS 平滑
ax.plot(fig5_data['date'], fig5_loess,
        color='#A23B72', linewidth=2.5, label='LOESS 平滑')

# 绘制线性趋势
ax.plot(fig5_data['date'], fig5_trend,
        color='#F18F01', linewidth=2, linestyle='--', label='线性趋势')

ax.set_xlabel('日期', fontsize=12)
ax.set_ylabel('不安全感表达率 (%)', fontsize=12)
ax.set_title('Figure 5 去趋势化后职业不安全感表达的时间趋势', fontsize=14)
ax.legend(loc='upper left')
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(OUTPUT_DIR / "figure5_trend.png", dpi=300, bbox_inches='tight')
plt.savefig(OUTPUT_DIR / "figure5_trend.pdf", bbox_inches='tight')
plt.close()

print(f"  [OK] 已保存：figure5_trend.png/pdf")

# ============================================================================
# Figure 6: 安慰剂检验
# ============================================================================
print("\n[6/6] 生成 Figure 6: 安慰剂检验...")

fig6_data = pd.read_csv(DATA_DIR / "fig6_placebo.csv")

fig, ax = plt.subplots(figsize=(10, 7))

# 绘制直方图
ax.hist(fig6_data['coef'], bins=20, color='#2E86AB', alpha=0.7, 
        edgecolor='black', linewidth=1.5)

# 添加真实效应量
true_effect = 0.1574
ax.axvline(x=true_effect, color='red', linestyle='--', linewidth=2.5, 
           label=f'真实效应量 ({true_effect:.4f})')

# 添加安慰剂均值
placebo_mean = fig6_data['coef'].mean()
ax.axvline(x=placebo_mean, color='green', linestyle=':', linewidth=2.5, 
           label=f'安慰剂均值 ({placebo_mean:.4f})')

ax.set_xlabel('效应量', fontsize=12)
ax.set_ylabel('频数', fontsize=12)
ax.set_title('Figure 6 安慰剂检验系数分布（100 次模拟）', fontsize=14)
ax.legend(loc='upper right')
ax.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig(OUTPUT_DIR / "figure6_placebo.png", dpi=300, bbox_inches='tight')
plt.savefig(OUTPUT_DIR / "figure6_placebo.pdf", bbox_inches='tight')
plt.close()

print(f"  [OK] 已保存：figure6_placebo.png/pdf")

# ============================================================================
# 完成
# ============================================================================
print("\n" + "=" * 80)
print("Figure 1-6 图表生成完成！")
print("=" * 80)
print(f"\n输出目录：{OUTPUT_DIR}")
print("\n生成的文件:")
for i in range(1, 7):
    fig_names = {
        1: 'timeseries', 2: 'forest', 3: 'decay',
        4: 'boxplot', 5: 'trend', 6: 'placebo'
    }
    print(f"  Figure {i}: figure{i}_{fig_names[i]}.png/pdf")

print("\n下一步:")
print("  1. 检查生成的图表文件")
print("  2. 将图表插入论文第 4 章相应位置")
print("  3. 添加图注（参考第 4 章草稿）")
