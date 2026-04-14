import glob

import pandas as pd

# 读取 CSV 文件
csv_file = glob.glob("E:/Project/论文/workspace/eventdatabase/*.CSV")[0]
df = pd.read_csv(csv_file, encoding="gbk", skiprows=3)

print("=" * 70)
print("AI 事件数据库统计分析")
print("=" * 70)
print(f"\n总事件数：{len(df)}")
print(f"时间范围：{df['event_date'].min()} 至 {df['event_date'].max()}")
print("\n事件类型分布:")
print(df["event_type"].value_counts())
print("\n影响程度分布:")
print(df["impact_level"].value_counts())
print("\n媒体曝光度分布:")
print(df["media_coverage"].value_counts())

# 保存分析结果
df.to_excel(
    "E:/Project/论文/workspace/eventdatabase/事件数据库分析_已整合.xlsx", index=False
)
print("\n已保存整合后的 Excel 文件")
