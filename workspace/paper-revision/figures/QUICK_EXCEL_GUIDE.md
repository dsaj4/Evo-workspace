# Figure 1-6 Excel 绘图快速指南

**数据文件位置**: `E:\Project\论文\workspace\paper-revision\figures_data\`

---

## Figure 1: 时间序列图

**数据文件**: `fig1_timeseries.csv`

**Excel 步骤**:
1. 打开 `fig1_timeseries.csv`
2. 选择 A 列 (date) 和 B 列 (insecurity_rate)
3. 插入 → 折线图
4. 右键点击折线 → 添加趋势线 → 移动平均 (7 天)
5. 添加图表标题："Figure 1 职业不安全感表达的时间序列（2024.10-2026.03）"
6. X 轴标题："日期"，Y 轴标题："不安全感表达率 (%)"
7. 右键 → 另存为图片 → PNG (300 DPI)

**预计时间**: 5 分钟

---

## Figure 2: 森林图

**数据文件**: `fig2_forest.csv`

**Excel 步骤**:
1. 打开 `fig2_forest.csv`
2. 选择 event_id, irr, ci_low, ci_high 列
3. 插入 → 散点图
4. 添加误差线（自定义：+/- 值）
5. 添加垂直线 x=1（插入 → 形状 → 直线）
6. 添加图例（不同颜色表示事件类型）
7. 另存为图片

**预计时间**: 10 分钟

---

## Figure 3: 动态衰减曲线

**数据文件**: `fig3_decay.csv`

**Excel 步骤**:
1. 打开 `fig3_decay.csv`
2. 选择 day, mean_effect 列
3. 插入 → 散点图（带误差线）
4. 添加趋势线 → 指数衰减
5. 添加水平线 y=0（基线）
6. 添加文本框："半衰期 = 1.36 天"
7. 另存为图片

**预计时间**: 8 分钟

---

## Figure 4: 箱线图

**数据文件**: `fig4_boxplot.csv`

**Excel 步骤**:
1. 打开 `fig4_boxplot.csv`
2. 按平台分组（筛选或数据透视表）
3. 插入 → 箱线图（Excel 2016+）
4. 添加均值点（插入 → 散点）
5. 设置颜色（知乎=蓝色，B 站=紫色，小红书=橙色）
6. 另存为图片

**预计时间**: 8 分钟

---

## Figure 5: 时间趋势图

**数据文件**: `fig5_trend.csv`

**Excel 步骤**:
1. 打开 `fig5_trend.csv`
2. 选择 date, residual_rate, loess, trend 列
3. 插入 → 折线图（多系列）
4. 设置线条样式（残差=细线，LOESS=粗线，趋势=虚线）
5. 添加图例
6. 另存为图片

**预计时间**: 8 分钟

---

## Figure 6: 安慰剂检验

**数据文件**: `fig6_placebo.csv`

**Excel 步骤**:
1. 打开 `fig6_placebo.csv`
2. 选择 coef 列
3. 插入 → 直方图
4. 添加垂直线（真实效应量=0.1574，红色虚线）
5. 添加垂直线（安慰剂均值，绿色点线）
6. 添加图例
7. 另存为图片

**预计时间**: 8 分钟

---

## 总预计时间：约 47 分钟

**提示**:
- 所有图表保存为 PNG 格式，300 DPI
- 使用统一的字体（宋体或 Arial）
- 图表尺寸建议：宽 14cm，高 10cm
- 图注放在图表下方（参考第 4 章草稿）

**输出目录**: `E:\Project\论文\workspace\paper-revision\figures\`
