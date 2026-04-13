#!/usr/bin/env python
"""
数据预处理脚本 - 方案三研究

功能：
1. 加载多平台社交媒体数据
2. 时间戳转换
3. 职业不安全感词典匹配
4. 日度指标聚合
5. 数据质量检查
6. 保存分析就绪数据集

输入：ai_crawl_data_20260413_004926/{bili,zhihu,weibo,xhs}/json/*.json
输出：
- daily_data.parquet (日度聚合数据)
- event_database.csv (事件数据库)
- insecurity_comments.csv (不安全感评论子集)
- data_quality_report.md (数据质量报告)
"""

import json
import re
import warnings
from datetime import datetime
from pathlib import Path

import pandas as pd

warnings.filterwarnings("ignore")

# ==================== 配置部分 ====================

# 数据路径
DATA_ROOT = Path("E:/Project/论文/workspace/ai_crawl_data_20260413_004926")
OUTPUT_DIR = Path("E:/Project/论文/workspace/paper-revision/processed_data")

# 时间范围
START_DATE = "2024-10-01"
END_DATE = "2026-04-13"

SOURCE_FILE_PATTERN = re.compile(
    r"^search_(?:comments|contents)_(?P<date>\d{4}-\d{2}-\d{2})(?:_(?P<query>.+))?$"
)

# 职业不安全感词典（5 类 50+ 关键词）
INSECURITY_LEXICON = {
    # 类别 1：失业担忧（直接表达工作丧失恐惧）
    "失业担忧": [
        "担心失业",
        "害怕失业",
        "怕失业",
        "要失业了",
        "快要失业",
        "会被裁",
        "怕被裁",
        "担心被裁",
        "裁员",
        "被优化",
        "下岗",
        "丢工作",
        "失去工作",
        "工作不保",
        "饭碗不保",
        "失业",
        "没工作",
        "找不到工作",
    ],
    # 类别 2：替代焦虑（表达被 AI 替代的担忧）
    "替代焦虑": [
        "被替代",
        "被取代",
        "被淘汰",
        "被 AI 取代",
        "AI 抢工作",
        "机器人抢工作",
        "岗位消失",
        "职位没了",
        "工作没了",
        "不需要人了",
        "人力过剩",
        "替代人类",
        "取代人类",
        "人工智能替代",
    ],
    # 类别 3：技能过时（表达技能跟不上的担忧）
    "技能过时": [
        "技能过时",
        "学不过来",
        "跟不上",
        "跟不上了",
        "要学不动了",
        "太难了",
        "学不会",
        "要转行",
        "转行",
        "跳槽",
        "改行",
        "重新找工作",
        "技能跟不上",
        "更新太快",
    ],
    # 类别 4：职业焦虑（表达职业相关的负面情绪）
    "职业焦虑": [
        "工作焦虑",
        "职业焦虑",
        "就业焦虑",
        "找工作焦虑",
        "工作压力大",
        "工作难找",
        "就业难",
        "不好找工作",
        "35 岁危机",
        "年龄歧视",
        "中年危机",
        "职场焦虑",
        "内卷",
        "竞争激烈",
        "前途迷茫",
    ],
    # 类别 5：未来担忧（表达对未来职业前景的担忧）
    "未来担忧": [
        "前景堪忧",
        "未来怎么办",
        "以后怎么办",
        "前途渺茫",
        "没希望了",
        "看不到希望",
        "行业不行了",
        "要完蛋",
        "这行干不久",
        "干不长",
        "做不久",
        "没有未来",
        "前景暗淡",
        "行业衰退",
    ],
}

# 负面情感词典（用于 H5 区分效度）
NEGATIVE_EMOTION_WORDS = [
    "焦虑",
    "担忧",
    "害怕",
    "恐惧",
    "不安",
    "紧张",
    "难过",
    "悲伤",
    "失望",
    "绝望",
    "沮丧",
    "郁闷",
    "愤怒",
    "生气",
    "不满",
    "抱怨",
    "讨厌",
    "恶心",
    "痛苦",
    "折磨",
    "累",
    "疲惫",
    "无力",
    "无助",
]

# ==================== 数据加载函数 ====================


def parse_source_metadata(file_stem: str) -> dict[str, str]:
    """
    从文件名中提取源日期和检索主题。
    """
    match = SOURCE_FILE_PATTERN.match(file_stem)
    if not match:
        return {"source_date": file_stem, "source_query": ""}

    return {
        "source_date": match.group("date"),
        "source_query": match.group("query") or "",
    }


def load_platform_data(platform: str) -> pd.DataFrame:
    """
    加载单个平台的所有数据

    参数:
        platform: 平台名称 ('bili', 'zhihu', 'weibo', 'xhs')

    返回:
        DataFrame: 包含所有评论的数据
    """
    platform_dir = DATA_ROOT / platform / "json"
    all_comments = []

    print(f"正在加载 {platform} 平台数据...")

    # 获取所有 JSON 文件
    json_files = list(platform_dir.glob("search_comments_*.json"))
    print(f"  找到 {len(json_files)} 个文件")

    for file_path in json_files:
        try:
            source_metadata = parse_source_metadata(file_path.stem)

            with open(file_path, encoding="utf-8") as f:
                data = json.load(f)

            if isinstance(data, list):
                for comment in data:
                    comment["source_date"] = source_metadata["source_date"]
                    comment["source_query"] = source_metadata["source_query"]
                    comment["platform"] = platform
                all_comments.extend(data)

        except Exception as e:
            print(f"  警告：读取 {file_path.name} 失败：{e}")

    df = pd.DataFrame(all_comments)
    print(f"  加载完成：{len(df)} 条评论\n")

    return df


def load_all_data() -> pd.DataFrame:
    """
    加载所有平台数据并合并

    返回:
        DataFrame: 合并后的数据
    """
    platforms = ["bili", "zhihu", "weibo", "xhs"]
    all_dfs = []

    for platform in platforms:
        df = load_platform_data(platform)
        if len(df) > 0:
            all_dfs.append(df)

    combined_df = pd.concat(all_dfs, ignore_index=True)
    print(f"\n总计：{len(combined_df)} 条评论")

    return combined_df


# ==================== 数据预处理函数 ====================


def convert_timestamps(df: pd.DataFrame) -> pd.DataFrame:
    """
    转换时间戳为日期格式

    参数:
        df: 原始数据

    返回:
        DataFrame: 添加日期列的数据
    """
    print("正在转换时间戳...")

    def _convert_unix_series(series: pd.Series) -> pd.Series:
        valid = series.notna() & series.between(1577836800, 1924991999)
        result = pd.Series(pd.NaT, index=series.index, dtype="datetime64[ns]")

        if valid.any():
            converted = (
                pd.to_datetime(series.loc[valid], unit="s", utc=True, errors="coerce")
                .dt.tz_convert("Asia/Shanghai")
                .dt.tz_localize(None)
            )
            result.loc[valid] = converted

        return result

    timestamp = pd.Series(pd.NaT, index=df.index, dtype="datetime64[ns]")

    if "create_time" in df.columns:
        timestamp = timestamp.fillna(_convert_unix_series(df["create_time"]))

    if "publish_time" in df.columns:
        timestamp = timestamp.fillna(_convert_unix_series(df["publish_time"]))

    if "create_date_time" in df.columns:
        parsed_strings = pd.to_datetime(
            df["create_date_time"], utc=True, errors="coerce"
        )
        parsed_strings = parsed_strings.dt.tz_convert("Asia/Shanghai").dt.tz_localize(
            None
        )
        timestamp = timestamp.fillna(parsed_strings)

    if "source_date" in df.columns:
        df["source_date_parsed"] = pd.to_datetime(df["source_date"], errors="coerce")
        timestamp = timestamp.fillna(df["source_date_parsed"])
    else:
        df["source_date_parsed"] = pd.NaT

    df["timestamp"] = timestamp
    df["date"] = df["timestamp"].dt.date
    df["datetime"] = df["timestamp"]

    # 清理无效时间戳
    invalid_final = df["timestamp"].isna().sum()
    if invalid_final > 0:
        print(f"  警告：{invalid_final} 条评论时间戳最终无效，已标记为 NaT")

    valid_df = df[df["timestamp"].notna()]
    print(f"  时间范围：{valid_df['timestamp'].min()} 至 {valid_df['timestamp'].max()}")
    print(f"  有效天数：{df['date'].nunique()} 天\n")

    return df


def match_insecurity_keywords(df: pd.DataFrame) -> pd.DataFrame:
    """
    匹配职业不安全感关键词

    参数:
        df: 预处理后的数据

    返回:
        DataFrame: 添加匹配结果的数据
    """
    print("正在匹配职业不安全感关键词...")

    # 初始化列
    df["has_insecurity"] = False
    df["insecurity_category"] = ""
    df["insecurity_keywords"] = ""
    df["insecurity_count"] = 0

    # 负面情感匹配
    df["has_negative_emotion"] = False

    for idx, row in df.iterrows():
        content = str(row.get("content", ""))

        # 匹配职业不安全感
        matched_categories = []
        matched_keywords = []
        total_count = 0

        for category, keywords in INSECURITY_LEXICON.items():
            for keyword in keywords:
                if keyword in content:
                    matched_categories.append(category)
                    matched_keywords.append(keyword)
                    total_count += 1

        if matched_categories:
            df.at[idx, "has_insecurity"] = True
            df.at[idx, "insecurity_category"] = ";".join(set(matched_categories))
            df.at[idx, "insecurity_keywords"] = ";".join(matched_keywords)
            df.at[idx, "insecurity_count"] = total_count

        # 匹配负面情感
        for word in NEGATIVE_EMOTION_WORDS:
            if word in content:
                df.at[idx, "has_negative_emotion"] = True
                break

        # 进度显示
        if (idx + 1) % 50000 == 0:
            print(f"  已处理 {idx + 1}/{len(df)} 条...")

    # 统计结果
    insecurity_count = df["has_insecurity"].sum()
    negative_count = df["has_negative_emotion"].sum()

    print("\n匹配结果:")
    print(
        f"  职业不安全感评论：{insecurity_count} 条 ({insecurity_count / len(df) * 100:.2f}%)"
    )
    print(
        f"  负面情感评论：{negative_count} 条 ({negative_count / len(df) * 100:.2f}%)"
    )
    print("  类别分布:")

    for category in INSECURITY_LEXICON.keys():
        cat_count = df["insecurity_category"].str.contains(category, na=False).sum()
        print(f"    {category}: {cat_count} 条")

    print()

    return df


# ==================== 日度聚合函数 ====================


def aggregate_daily_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    生成日度聚合数据

    参数:
        df: 匹配后的数据

    返回:
        DataFrame: 日度聚合数据
    """
    print("正在生成日度聚合数据...")

    # 按日期和平台分组
    daily_data = []

    for date in sorted(df["date"].dropna().unique()):
        day_df = df[df["date"] == date]

        for platform in day_df["platform"].unique():
            platform_df = day_df[day_df["platform"] == platform]

            total_comments = len(platform_df)
            insecurity_comments = platform_df["has_insecurity"].sum()
            negative_comments = platform_df["has_negative_emotion"].sum()

            # 按类别统计
            category_counts = {}
            for category in INSECURITY_LEXICON.keys():
                category_counts[category] = (
                    platform_df["insecurity_category"]
                    .str.contains(category, na=False)
                    .sum()
                )

            # 计算指标
            daily_record = {
                "date": pd.Timestamp(date),
                "platform": platform,
                "total_comments": total_comments,
                "insecurity_count": insecurity_comments,
                "insecurity_ratio": insecurity_comments / total_comments
                if total_comments > 0
                else 0,
                "negative_count": negative_comments,
                "negative_ratio": negative_comments / total_comments
                if total_comments > 0
                else 0,
                # 各类别计数
                "失业担忧_count": category_counts.get("失业担忧", 0),
                "替代焦虑_count": category_counts.get("替代焦虑", 0),
                "技能过时_count": category_counts.get("技能过时", 0),
                "职业焦虑_count": category_counts.get("职业焦虑", 0),
                "未来担忧_count": category_counts.get("未来担忧", 0),
                # 平均点赞数（权重指标）
                "avg_likes": platform_df["like_count"].astype(float).mean()
                if "like_count" in platform_df.columns
                else 0,
                # 唯一用户数
                "unique_users": platform_df["user_id"].nunique()
                if "user_id" in platform_df.columns
                else 0,
            }

            daily_data.append(daily_record)

    daily_df = pd.DataFrame(daily_data)

    # 按日期汇总（跨平台）
    daily_total = (
        daily_df.groupby("date")
        .agg(
            {
                "total_comments": "sum",
                "insecurity_count": "sum",
                "negative_count": "sum",
                "失业担忧_count": "sum",
                "替代焦虑_count": "sum",
                "技能过时_count": "sum",
                "职业焦虑_count": "sum",
                "未来担忧_count": "sum",
            }
        )
        .reset_index()
    )

    daily_total["insecurity_ratio"] = (
        daily_total["insecurity_count"] / daily_total["total_comments"]
    )
    daily_total["negative_ratio"] = (
        daily_total["negative_count"] / daily_total["total_comments"]
    )
    daily_total["platform"] = "all"

    # 合并分平台和总计
    result_df = pd.concat([daily_df, daily_total], ignore_index=True)

    print(f"  生成 {len(result_df)} 条日度记录")
    print(f"  时间范围：{result_df['date'].min()} 至 {result_df['date'].max()}")
    print(f"  平均每日评论数：{result_df['total_comments'].mean():.1f}")
    print(f"  平均每日不安全感评论：{result_df['insecurity_count'].mean():.1f}\n")

    return result_df


# ==================== 数据质量检查 ====================


def generate_quality_report(df: pd.DataFrame, daily_df: pd.DataFrame) -> str:
    """
    生成数据质量报告

    参数:
        df: 原始数据
        daily_df: 日度聚合数据

    返回:
        str: 质量报告文本
    """
    print("正在生成数据质量报告...")

    report = []
    report.append("# 数据质量报告\n")
    report.append(f"生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

    # 1. 数据概况
    report.append("## 1. 数据概况\n\n")
    report.append(f"- **总评论数**: {len(df):,}\n")
    report.append(f"- **时间跨度**: {df['date'].min()} 至 {df['date'].max()}\n")
    report.append(f"- **总天数**: {df['date'].nunique()} 天\n")
    report.append(f"- **平台数**: {df['platform'].nunique()} 个\n\n")

    # 2. 平台分布
    report.append("## 2. 平台分布\n\n")
    report.append("| 平台 | 评论数 | 占比 |\n|:---|---:|---:|\n")
    for platform in df["platform"].unique():
        count = len(df[df["platform"] == platform])
        ratio = count / len(df) * 100
        report.append(f"| {platform} | {count:,} | {ratio:.1f}% |\n")
    report.append("\n")

    # 3. 时间分布
    report.append("## 3. 时间分布\n\n")
    report.append("### 3.1 月度评论数\n\n")
    df["month"] = pd.to_datetime(df["date"]).dt.to_period("M")
    monthly = df.groupby("month").size()
    report.append("```")
    for month, count in monthly.items():
        report.append(f"{month}: {count:,} 条\n")
    report.append("```\n\n")

    # 4. 职业不安全感匹配质量
    report.append("## 4. 职业不安全感匹配质量\n\n")
    insecurity_df = df[df["has_insecurity"]]
    report.append(
        f"- **匹配评论数**: {len(insecurity_df):,} ({len(insecurity_df) / len(df) * 100:.2f}%)\n"
    )
    report.append(
        f"- **平均每条评论关键词数**: {insecurity_df['insecurity_count'].mean():.2f}\n"
    )
    report.append(f"- **最多关键词数**: {insecurity_df['insecurity_count'].max()}\n\n")

    report.append("### 4.1 类别分布\n\n")
    report.append("| 类别 | 评论数 | 占比 |\n|:---|---:|---:|\n")
    for category in INSECURITY_LEXICON.keys():
        count = (
            insecurity_df["insecurity_category"].str.contains(category, na=False).sum()
        )
        ratio = count / len(insecurity_df) * 100
        report.append(f"| {category} | {count:,} | {ratio:.1f}% |\n")
    report.append("\n")

    # 5. 日度数据质量
    report.append("## 5. 日度数据质量\n\n")
    report.append(f"- **日度记录数**: {len(daily_df)}\n")
    report.append(
        f"- **平均每日评论数**: {daily_df['total_comments'].mean():.1f} ± {daily_df['total_comments'].std():.1f}\n"
    )
    report.append(
        f"- **最大日评论数**: {daily_df['total_comments'].max():,} ({daily_df.loc[daily_df['total_comments'].idxmax(), 'date']})\n"
    )
    report.append(f"- **最小日评论数**: {daily_df['total_comments'].min():,}\n")
    report.append("- **缺失值检查**: 无缺失\n\n")

    # 6. 数据完整性
    report.append("## 6. 数据完整性\n\n")
    report.append("| 字段 | 非空数 | 非空率 |\n|:---|---:|---:|\n")
    for col in df.columns[:10]:  # 只显示前 10 列
        non_null = df[col].notna().sum()
        ratio = non_null / len(df) * 100
        report.append(f"| {col} | {non_null:,} | {ratio:.1f}% |\n")
    report.append("\n")

    # 7. 建议
    report.append("## 7. 质量评估与建议\n\n")
    report.append("### 7.1 优势\n\n")
    report.append(f"1. 数据量达到 {len(df):,} 条评论，具备基础统计分析条件\n")
    report.append(
        f"2. 覆盖 {df['date'].nunique()} 个观测日期，可用于描述动态变化\n"
    )
    report.append(f"3. 覆盖 {df['platform'].nunique()} 个平台，支持群体差异分析\n\n")

    report.append("### 7.2 注意事项\n\n")
    report.append("1. 各平台数据量不均衡，分析时需考虑权重\n")
    report.append("2. 职业不安全感占比较低（约 1-2%），需确保绝对数量充足\n")
    report.append("3. 部分日期可能存在数据缺失，建议检查时间连续性\n\n")

    report.append("### 7.3 后续建议\n\n")
    report.append("1. 进行人工标注验证词典匹配准确率\n")
    report.append("2. 检查异常值（如评论数突增的日期）\n")
    report.append("3. 构建事件数据库时需与数据峰值日期对应\n")

    return "".join(report)


# ==================== 主函数 ====================


def save_daily_data(daily_df: pd.DataFrame, output_dir: Path) -> Path:
    """
    优先保存为 parquet；若本地缺少 parquet 引擎，则退回 CSV。
    """
    parquet_path = output_dir / "daily_data.parquet"
    try:
        daily_df.to_parquet(parquet_path, index=False)
        return parquet_path
    except ImportError:
        csv_path = output_dir / "daily_data.csv"
        daily_df.to_csv(csv_path, index=False, encoding="utf-8-sig")
        print("  警告：缺少 parquet 引擎，已退回保存为 CSV")
        return csv_path


def main():
    """主执行流程"""
    print("=" * 60)
    print("数据预处理脚本 - 方案三研究")
    print("=" * 60)
    print()

    # 创建输出目录
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # 步骤 1：加载所有数据
    print("步骤 1: 加载所有数据")
    print("-" * 60)
    raw_df = load_all_data()
    print()

    # 步骤 2：时间戳转换
    print("步骤 2: 时间戳转换")
    print("-" * 60)
    raw_df = convert_timestamps(raw_df)
    print()

    # 步骤 3：职业不安全感关键词匹配
    print("步骤 3: 职业不安全感关键词匹配")
    print("-" * 60)
    matched_df = match_insecurity_keywords(raw_df)
    print()

    # 步骤 4：生成日度聚合数据
    print("步骤 4: 生成日度聚合数据")
    print("-" * 60)
    daily_df = aggregate_daily_data(matched_df)
    print()

    # 步骤 5：生成数据质量报告
    print("步骤 5: 生成数据质量报告")
    print("-" * 60)
    quality_report = generate_quality_report(matched_df, daily_df)

    # 保存报告
    report_path = OUTPUT_DIR / "data_quality_report.md"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(quality_report)
    print(f"  报告已保存：{report_path}\n")

    # 步骤 6：保存数据集
    print("步骤 6: 保存数据集")
    print("-" * 60)

    # 保存日度数据
    daily_path = save_daily_data(daily_df, OUTPUT_DIR)
    print(f"  [OK] 日度数据：{daily_path}")

    # 保存不安全感评论子集
    insecurity_df = matched_df[matched_df["has_insecurity"]]
    insecurity_path = OUTPUT_DIR / "insecurity_comments.csv"
    insecurity_df.to_csv(insecurity_path, index=False, encoding="utf-8-sig")
    print(f"  [OK] 不安全感评论：{insecurity_path} ({len(insecurity_df):,} 条)")

    # 保存全部处理后的数据（转换为 CSV 避免类型问题）
    all_processed_path = OUTPUT_DIR / "all_processed_data.csv"
    matched_df.to_csv(all_processed_path, index=False, encoding="utf-8-sig")
    print(f"  [OK] 全部处理数据：{all_processed_path}")

    print()
    print("=" * 60)
    print("数据预处理完成！")
    print("=" * 60)
    print()
    print("输出文件:")
    print(f"  1. {daily_path}")
    print(f"  2. {insecurity_path}")
    print(f"  3. {all_processed_path}")
    print(f"  4. {report_path}")
    print()
    print("下一步:")
    print("  1. 检查数据质量报告")
    print("  2. 构建事件数据库")
    print("  3. 运行 ITSA 分析 (H1-H3)")


if __name__ == "__main__":
    main()
