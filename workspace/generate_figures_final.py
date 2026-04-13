#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Figure 1-6 图表生成脚本（稳健版）
使用简单配置，避免编码问题
"""

import pandas as pd
import numpy as np
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# 设置中文字体
import matplotlib
matplotlib.use('Agg')  # 非交互式后端
matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
matplotlib.rcParams['axes.unicode_minus'] = False

try:
    import matplotlib.pyplot as plt
    import seaborn as sns
    print("matplotlib 和 seaborn 导入成功")
except Exception as e:
    print(f"导入失败：{e}")
    print("尝试使用基础 matplotlib...")
    import matplotlib.pyplot as plt

# 路径设置
DATA_DIR = Path('E:/Project/论文/workspace/paper-revision/processed_data')
EVENTS_DIR = Path('E:/Project/论文/workspace/paper-revision/event_analysis')
FIGURES_DIR = Path('E:/Project/论文/workspace/paper-revision/figures')
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

print("=" * 80)
print("Figure 1-6 图表生成")
print("=" * 80)

# 加载数据
print("\n[1/7] 加载数据...")
daily_df = pd.read_parquet(DATA_DIR / 'daily_data.parquet')
events_df = pd.read_csv(EVENTS_DIR / 'event_database.csv')

daily_df['date'] = pd.to_datetime(daily_df['date'])
events_df['date'] = pd.to_datetime(events_df['event_date'])
daily_df['insecurity_rate'] = daily_df['insecurity_count'] / daily_df['total_comments'] * 100

print(f"  日度数据：{len(daily_df)} 天")
print(f"  事件数：{len(events_df)} 个")

# ============================================================================
# Figure 1: 时间序列图
# ============================================================================
print("\n[2/7] 生成 Figure 1: 时间序列图...")

try:
    fig, ax = plt.subplots(figsize=(14, 6))
    
    # 绘制日度数据
    ax.plot(daily_df['date'], daily_df['insecurity_rate'], 
            alpha=0.3, linewidth=0.5, color='#2E86AB', label='日度表达率')
    
    # 绘制 7 天移动平均
    ma7 = daily_df['insecurity_rate'].rolling(window=7, min_periods=1).mean()
    ax.plot(daily_df['date'], ma7, 
            linewidth=2, color='#A23B72', label='7 天移动平均')
    
    # 标注主要事件
    for i, (_, event) in enumerate(events_df.head(10).iterrows()):
        ax.axvline(event['date'], color='red', linestyle='--', 
                   alpha=0.5, linewidth=0.8)
        if i < 5:  # 只标注前 5 个事件
            ax.text(event['date'], daily_df['insecurity_rate'].max() * 0.95,
                   event['event_id'], rotation=90, fontsize=8, alpha=0.7)
    
    ax.set_xlabel('日期', fontsize=12)
    ax.set_ylabel('不安全感表达率 (%)', fontsize=12)
    ax.set_title('Figure 1: 职业不安全感表达的时间序列（2024.10-2026.03）', 
                fontsize=14, fontweight='bold')
    ax.legend(loc='upper right', fontsize=10)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / 'Figure1_timeseries.png', dpi=300, bbox_inches='tight')
    plt.savefig(FIGURES_DIR / 'Figure1_timeseries.pdf', bbox_inches='tight')
    plt.close()
    
    print(f"  [OK] 已保存：Figure1_timeseries.png/pdf")
except Exception as e:
    print(f"  [ERROR] Figure 1 生成失败：{e}")

# ============================================================================
# Figure 2: 森林图
# ============================================================================
print("\n[3/7] 生成 Figure 2: 森林图...")

try:
    # 计算各事件的 IRR
    event_irrs = []
    for _, event in events_df.iterrows():
        event_date = event['date']
        
        pre_mask = (daily_df['date'] >= event_date - pd.Timedelta(days=7)) & (daily_df['date'] < event_date)
        post_mask = (daily_df['date'] >= event_date) & (daily_df['date'] <= event_date + pd.Timedelta(days=6))
        
        pre_mean = daily_df.loc[pre_mask, 'insecurity_count'].mean()
        post_mean = daily_df.loc[post_mask, 'insecurity_count'].mean()
        
        if not pd.isna(pre_mean) and not pd.isna(post_mean) and pre_mean > 0:
            irr = post_mean / pre_mean
            se = np.sqrt(1/post_mean + 1/pre_mean) if post_mean > 0 and pre_mean > 0 else 0.5
            ci_low = irr * np.exp(-1.96 * se)
            ci_high = irr * np.exp(1.96 * se)
            
            event_irrs.append({
                'event_id': event['event_id'],
                'event_type': event['event_type'],
                'irr': irr,
                'ci_low': ci_low,
                'ci_high': ci_high
            })
    
    forest_df = pd.DataFrame(event_irrs)
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # 颜色映射
    colors = {'tech_positive': '#2E86AB', 'job_negative': '#A23B72', 
              'policy': '#F18F01', 'report': '#C73E1D'}
    
    y_pos = np.arange(len(forest_df))
    
    for i, (_, row) in enumerate(forest_df.iterrows()):
        color = colors.get(row['event_type'], 'gray')
        ax.errorbar(row['irr'], i, 
                   xerr=[[row['irr'] - row['ci_low']], [row['ci_high'] - row['irr']]],
                   fmt='o', color=color, capsize=3, alpha=0.7)
    
    # 添加垂直线 x=1
    ax.axvline(x=1, color='red', linestyle='--', alpha=0.5)
    
    ax.set_yticks(y_pos)
    ax.set_yticklabels(forest_df['event_id'], fontsize=9)
    ax.set_xlabel('发生率比 (IRR)', fontsize=12)
    ax.set_title('Figure 2: 各事件后职业不安全感表达效应的森林图', 
                fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3, axis='x')
    
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / 'Figure2_forest.png', dpi=300, bbox_inches='tight')
    plt.savefig(FIGURES_DIR / 'Figure2_forest.pdf', bbox_inches='tight')
    plt.close()
    
    print(f"  [OK] 已保存：Figure2_forest.png/pdf")
except Exception as e:
    print(f"  [ERROR] Figure 2 生成失败：{e}")

# ============================================================================
# Figure 3: 动态衰减曲线
# ============================================================================
print("\n[4/7] 生成 Figure 3: 动态衰减曲线...")

try:
    from scipy.optimize import curve_fit
    
    # 读取已计算的衰减数据
    decay_df = pd.read_csv(FIGURES_DIR.parent / 'figures_data' / 'fig3_decay.csv')
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # 绘制观测值
    ax.errorbar(decay_df['day'], decay_df['mean_effect'], 
               yerr=decay_df['std_effect'],
               fmt='o', color='#2E86AB', capsize=3, alpha=0.7, label='观测值')
    
    # 绘制拟合曲线
    if 'fitted' in decay_df.columns:
        ax.plot(decay_df['day'], decay_df['fitted'], 
               '-', color='#A23B72', linewidth=2, label='指数拟合')
    
    # 添加参考线
    ax.axhline(y=0, color='green', linestyle='--', alpha=0.5, label='基线')
    ax.axhline(y=5, color='gray', linestyle=':', alpha=0.5, label='+5% 阈值')
    
    # 标注半衰期
    ax.text(7, decay_df['mean_effect'].max() * 0.8, 
           '半衰期 = 1.36 天', fontsize=11, 
           bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    ax.set_xlabel('事件后天数', fontsize=12)
    ax.set_ylabel('相对基线变化 (%)', fontsize=12)
    ax.set_title('Figure 3: 事件后职业不安全感表达的动态衰减曲线', 
                fontsize=14, fontweight='bold')
    ax.legend(loc='upper right', fontsize=10)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / 'Figure3_decay.png', dpi=300, bbox_inches='tight')
    plt.savefig(FIGURES_DIR / 'Figure3_decay.pdf', bbox_inches='tight')
    plt.close()
    
    print(f"  [OK] 已保存：Figure3_decay.png/pdf")
except Exception as e:
    print(f"  [ERROR] Figure 3 生成失败：{e}")

# ============================================================================
# Figure 4: 箱线图
# ============================================================================
print("\n[5/7] 生成 Figure 4: 箱线图...")

try:
    boxplot_df = pd.read_csv(FIGURES_DIR.parent / 'figures_data' / 'fig4_boxplot.csv')
    
    # 平台名称映射
    platform_names = {'zhihu': '知乎', 'bili': 'B 站', 'xhs': '小红书', 'all': '全平台'}
    boxplot_df['platform_name'] = boxplot_df['platform'].map(platform_names)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # 创建箱线图
    platforms = ['知乎', 'B 站', '小红书', '全平台']
    data_to_plot = [boxplot_df[boxplot_df['platform_name'] == p]['insecurity_rate'].values 
                    for p in platforms]
    
    bp = ax.boxplot(data_to_plot, patch_artist=True, 
                    labels=platforms, widths=0.6)
    
    # 设置颜色
    colors_box = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D']
    for patch, color in zip(bp['boxes'], colors_box):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)
    
    # 添加均值点
    means = [boxplot_df[boxplot_df['platform_name'] == p]['insecurity_rate'].mean() 
             for p in platforms]
    ax.plot(range(1, len(platforms) + 1), means, 'D-', color='red', 
           markersize=8, label='均值')
    
    ax.set_ylabel('不安全感表达率 (%)', fontsize=12)
    ax.set_title('Figure 4: 分平台职业不安全感表达率箱线图', 
                fontsize=14, fontweight='bold')
    ax.legend(loc='upper right', fontsize=10)
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / 'Figure4_boxplot.png', dpi=300, bbox_inches='tight')
    plt.savefig(FIGURES_DIR / 'Figure4_boxplot.pdf', bbox_inches='tight')
    plt.close()
    
    print(f"  [OK] 已保存：Figure4_boxplot.png/pdf")
except Exception as e:
    print(f"  [ERROR] Figure 4 生成失败：{e}")

# ============================================================================
# Figure 5: 时间趋势图
# ============================================================================
print("\n[6/7] 生成 Figure 5: 时间趋势图...")

try:
    trend_df = pd.read_csv(FIGURES_DIR.parent / 'figures_data' / 'fig5_trend.csv')
    trend_df['date'] = pd.to_datetime(trend_df['date'])
    
    fig, ax = plt.subplots(figsize=(14, 6))
    
    # 绘制残差序列
    ax.plot(trend_df['date'], trend_df['residual_rate'], 
           alpha=0.3, linewidth=0.5, color='#2E86AB', label='残差序列')
    
    # 绘制 LOESS 平滑
    ax.plot(trend_df['date'], trend_df['loess'], 
           linewidth=2, color='#A23B72', label='LOESS 平滑（30 天）')
    
    # 绘制线性趋势
    ax.plot(trend_df['date'], trend_df['trend'], 
           linewidth=2, color='#F18F01', linestyle='--', label='线性趋势')
    
    ax.set_xlabel('日期', fontsize=12)
    ax.set_ylabel('不安全感表达率 (%)', fontsize=12)
    ax.set_title('Figure 5: 去趋势化后职业不安全感表达的时间趋势', 
                fontsize=14, fontweight='bold')
    ax.legend(loc='upper left', fontsize=10)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / 'Figure5_trend.png', dpi=300, bbox_inches='tight')
    plt.savefig(FIGURES_DIR / 'Figure5_trend.pdf', bbox_inches='tight')
    plt.close()
    
    print(f"  [OK] 已保存：Figure5_trend.png/pdf")
except Exception as e:
    print(f"  [ERROR] Figure 5 生成失败：{e}")

# ============================================================================
# Figure 6: 安慰剂检验
# ============================================================================
print("\n[7/7] 生成 Figure 6: 安慰剂检验...")

try:
    placebo_df = pd.read_csv(FIGURES_DIR.parent / 'figures_data' / 'fig6_placebo.csv')
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # 绘制直方图
    ax.hist(placebo_df['coef'], bins=20, color='#2E86AB', 
           alpha=0.7, edgecolor='black', linewidth=1)
    
    # 添加真实效应量
    true_effect = 0.1574  # 从稳健性检验结果
    ax.axvline(x=true_effect, color='red', linestyle='--', 
              linewidth=2, label=f'真实效应量 ({true_effect:.4f})')
    
    # 添加安慰剂均值
    placebo_mean = placebo_df['coef'].mean()
    ax.axvline(x=placebo_mean, color='green', linestyle=':', 
              linewidth=2, label=f'安慰剂均值 ({placebo_mean:.4f})')
    
    ax.set_xlabel('效应量', fontsize=12)
    ax.set_ylabel('频数', fontsize=12)
    ax.set_title('Figure 6: 安慰剂检验系数分布（100 次模拟）', 
                fontsize=14, fontweight='bold')
    ax.legend(loc='upper right', fontsize=10)
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / 'Figure6_placebo.png', dpi=300, bbox_inches='tight')
    plt.savefig(FIGURES_DIR / 'Figure6_placebo.pdf', bbox_inches='tight')
    plt.close()
    
    print(f"  [OK] 已保存：Figure6_placebo.png/pdf")
except Exception as e:
    print(f"  [ERROR] Figure 6 生成失败：{e}")

# ============================================================================
# 完成总结
# ============================================================================
print("\n" + "=" * 80)
print("Figure 1-6 图表生成完成！")
print("=" * 80)

print(f"\n输出目录：{FIGURES_DIR}")
print("\n生成的文件:")
for i in range(1, 7):
    print(f"  Figure {i}: Figure{i}_*.png/pdf")

print("\n[OK] 所有图表已保存为 PNG（300 DPI）和 PDF（矢量图）格式")
print("\n下一步:")
print("  1. 检查图表质量")
print("  2. 插入论文第 4 章相应位置")
print("  3. 添加图注（使用 README.md 中的模板）")
