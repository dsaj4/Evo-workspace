# 方案三（修订版）：AI 技术事件与职业不安全感表达的关联研究

## 一、研究题目

**主标题**：AI 技术事件与职业不安全感表达的关联：基于多源社交媒体数据的动态分析

**副标题（可选）**：一项时间序列研究

**英文题目**：The Association Between AI Technology Events and Job Insecurity Expression: A Dynamic Analysis Based on Multi-Source Social Media Data

---

## 二、研究背景与问题

### 2.1 研究背景

重大 AI 技术事件（如 GPT-4 发布、Sora 问世、大规模裁员新闻）频繁见诸媒体报道，引发公众广泛讨论。然而，这些事件是否触发公众的职业不安全感？影响持续多久？不同类型事件的影响是否有差异？现有研究多为横断面调查，无法捕捉事件后的动态演化过程。

### 2.2 核心概念界定

**职业不安全感表达（Job Insecurity Expression）**

> 本研究中的"职业不安全感表达"指社交媒体用户在公开评论中表达的与职业稳定性相关的担忧话语。这一指标与心理学构念"职业不安全感"存在关联但不等价：前者是公开的语言表达，后者是内在的心理状态。

**概念区别说明**：

| 维度 | 职业不安全感（构念） | 职业不安全感表达（本研究） |
|:---|:---|:---|
| **层次** | 内在心理状态 | 外在语言行为 |
| **测量** | 量表自评 | 文本分析 |
| **内容** | 个人工作稳定性担忧 | 公开评论中的相关话语 |
| **效度** | 个体层面构念效度 | 群体层面内容效度 |

**使用"表达"而非"感知"的理由**：
1. 社交媒体数据无法获取用户的内在心理状态
2. 公开表达可能受社会期许、平台规范影响
3. 避免因果暗示（表达≠真实感受）

### 2.3 研究问题

| RQ | 问题 | 类型 |
|:---|:---|:---|
| **RQ1** | 重大 AI 技术事件发生后，职业不安全感表达是否显著增加？ | 主效应 |
| **RQ2** | 不同类型事件（技术突破 vs 失业新闻）对不安全感表达的影响是否有差异？ | 调节效应 |
| **RQ3** | 不安全感表达的持续时间多长？恢复基线需要多久？ | 动态演化 |
| **RQ4** | 不同平台的不安全感表达强度是否存在差异？ | 群体差异 |
| **RQ5** | 不安全感表达与一般负面情绪的演化模式是否一致？ | 区分效度 |

---

## 三、理论框架与研究假设

### 3.1 理论基础

#### （1）议程设置理论（Agenda Setting Theory）
- 媒体对特定议题的报道频率影响公众对该议题重要性的感知
- 应用到本研究：AI 事件的媒体报道可能增加公众对职业风险的关注

#### （2）资源保存理论（Conservation of Resources Theory, COR）
- 个体努力获取、保持和保护自身资源（如工作、技能、地位）
- 当感知到资源威胁时，会产生压力和焦虑反应
- 应用到本研究：AI 技术事件可能被解读为资源威胁，触发不安全感表达

#### （3）情绪事件理论（Affective Events Theory, AET）
- 工作环境中的事件触发个体的情绪反应
- 情绪反应影响态度和行为
- 应用到本研究：AI 技术事件作为外部刺激，触发公众的情感反应和表达

### 3.2 分析框架

```
┌─────────────────────────────────────────────────────────────┐
│                      宏观层：技术环境变化                      │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │
│  │ 技术突破事件 │  │ 失业相关新闻 │  │ 政策出台    │          │
│  │ (GPT-4 发布) │  │ (AI 裁员)    │  │ (AI 监管)   │          │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘          │
│         │                │                │                   │
│         └────────────────┴────────────────┘                   │
│                          ↓                                    │
│                  时间序列关联分析                              │
│                          ↓                                    │
├─────────────────────────────────────────────────────────────┤
│                      微观层：不安全感表达                      │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │
│  │ 表达频率    │  │ 表达强度    │  │ 持续时间    │          │
│  │ (每日计数)  │  │ (情感得分)  │  │ (恢复时间)  │          │
│  └─────────────┘  └─────────────┘  └─────────────┘          │
└─────────────────────────────────────────────────────────────┘
```

### 3.3 研究假设

#### H1：主效应假设

> **H1**：重大 AI 技术事件发生后 7 天内，职业不安全感表达频率显著高于基线水平。

- **统计方法**：中断时间序列分析（Interrupted Time Series, ITSA）
- **预期效应**：事件后不安全感表达增加 20-40%
- **理论依据**：议程设置理论、情绪事件理论

#### H2：事件类型调节假设

> **H2**：负面事件（如 AI 裁员新闻）比技术发布事件引发更强的职业不安全感表达。

- **统计方法**：事件类型比较（单因素方差分析）
- **预期效应**：负面事件效应量是技术发布事件的 2-3 倍
- **理论依据**：资源保存理论（负面事件更直接威胁资源）

#### H3：恢复时间假设

> **H3**：职业不安全感表达在事件后 14-21 天内恢复到基线水平。

- **统计方法**：时间序列自回归模型、滑动窗口分析
- **预期效应**：半衰期 7-10 天，完全恢复 14-21 天
- **理论依据**：情绪适应理论、注意力衰减

#### H4：平台差异假设

> **H4**：专业平台（知乎）的职业不安全感表达强度低于大众生活平台（小红书）。

- **统计方法**：独立样本 t 检验、平台间比较 ANOVA
- **预期效应**：知乎表达强度低于小红书 30-50%
- **理论依据**：平台情境理论、用户构成差异

#### H5：区分效度假设

> **H5**：职业不安全感表达与一般负面情绪的时间序列相关性为中等程度（r = 0.3-0.6）。

- **统计方法**：交叉相关分析（Cross-correlation）
- **预期效应**：中等相关，表明两者相关但不完全重叠
- **理论依据**：构念区分效度

#### H6：长期趋势假设（探索性）

> **H6（探索性）**：在控制重大事件效应后，职业不安全感表达的基线水平随时间呈微弱上升趋势，反映 AI 技术影响的累积效应。

- **统计方法**：时间序列趋势检验（控制事件效应和季节性）
- **预期效应**：355 天内基线水平上升 5-15 个百分点（斜率β ≈ 0.0002-0.0004/天）
- **理论依据**：
  - **技术焦虑累积理论**：多次技术冲击产生累积心理影响（Acemoglu & Restrepo, 2019）
  - **不确定性螺旋**：AI 发展越快，公众不确定性越高
  - **适应失败假说**：公众无法完全适应快速技术变革
- ** competing hypotheses**：
  - **如果 H6 成立**：支持累积效应，建议建立长期监测和干预机制
  - **如果 H6 不成立**：支持适应假说，公众具有心理韧性
  - **如果 H6 反向**：公众逐渐适应 AI 技术，不安全感随时间下降

**H3 与 H6 的关系说明**：

| 假设 | 时间尺度 | 内容 | 关系 |
|:---|:---|:---|:---|
| **H3** | 短期（14-21 天） | 事件后恢复到"当时"基线 | 短期波动 |
| **H6** | 长期（355 天） | 基线本身随时间上升 | 长期趋势 |

```
不安全感表达
    ↑
    │      ╭───╮         ╭────╮
    │      │   │    ╭────┤    │
    │  ╭───┤   │    │    │    │    ╭────  ← 基线上升趋势
    │  │   │   │ ╭──┴────┤    │ ╭──┴────
    │  │   │   │ │       │    │ │
────┴──┴───┴───┴─┴───────┴────┴─┴────────→ 时间
   E1      E2        E3    E4
   
   └───────┘ └───────────┘ └───────────┘
    短期恢复   短期恢复      短期恢复
       ↓         ↓           ↓
    基线 1    基线 2      基线 3
       └────────┴───────────┘
              长期上升
```

---

## 四、研究方法

### 4.1 研究设计

**设计类型**：观察性时间序列研究

**分析单位**：日度聚合数据

**时间跨度**：355 天（2024 年 1 月 1 日 - 2026 年 3 月 18 日）

### 4.2 数据来源

| 平台 | 预期评论数 | 用户特征 | 数据字段 |
|:---|:---:|:---|:---|
| 知乎 | 3,000 | 高学历、专业化 | 内容、时间戳、点赞数 |
| 小红书 | 5,000 | 年轻女性为主 | 内容、时间戳、收藏数 |
| 哔哩哔哩 | 2,000 | 年轻、创意产业 | 内容、时间戳、弹幕数 |

**纳入标准**：
- 包含 AI 相关关键词（AI、人工智能、大模型等）
- 包含职业相关关键词（工作、失业、就业、岗位等）
- 时间戳完整
- 评论长度 ≥ 10 字

### 4.3 职业不安全感表达的操作化定义

#### 方案 A：关键词匹配法（推荐）

**职业不安全感词典**：

```python
INSECURITY_LEXICON = {
    # 类别 1：失业担忧（直接表达工作丧失恐惧）
    "失业担忧": [
        "担心失业", "害怕失业", "怕失业", "要失业了", "快要失业",
        "会被裁", "怕被裁", "担心被裁", "裁员", "被优化",
        "下岗", "丢工作", "失去工作", "工作不保", "饭碗不保"
    ],
    
    # 类别 2：替代焦虑（表达被 AI 替代的担忧）
    "替代焦虑": [
        "被替代", "被取代", "被淘汰", "被 AI 取代",
        "AI 抢工作", "机器人抢工作", "岗位消失", "职位没了",
        "工作没了", "不需要人了", "人力过剩"
    ],
    
    # 类别 3：技能过时（表达技能跟不上的担忧）
    "技能过时": [
        "技能过时", "学不过来", "跟不上", "跟不上了",
        "要学不动了", "太难了", "学不会", "要转行",
        "转行", "跳槽", "改行", "重新找工作"
    ],
    
    # 类别 4：职业焦虑（表达职业相关的负面情绪）
    "职业焦虑": [
        "工作焦虑", "职业焦虑", "就业焦虑", "找工作焦虑",
        "工作压力大", "工作难找", "就业难", "不好找工作",
        "35 岁危机", "年龄歧视", "中年危机", "职场焦虑"
    ],
    
    # 类别 5：未来担忧（表达对未来职业前景的担忧）
    "未来担忧": [
        "前景堪忧", "未来怎么办", "以后怎么办", "前途渺茫",
        "没希望了", "看不到希望", "行业不行了", "要完蛋",
        "这行干不久", "干不长", "做不久"
    ]
}

# 合并所有关键词
ALL_INSECURITY_KEYWORDS = set()
for category_keywords in INSECURITY_LEXICON.values():
    ALL_INSECURITY_KEYWORDS.update(category_keywords)
```

**判定规则**：

```python
def is_insecurity_expression(comment):
    """
    判断评论是否为职业不安全感表达
    
    参数:
        comment: 评论文本
    
    返回:
        bool: 是否为不安全感表达
        category: 所属类别（如有）
    """
    comment_lower = comment.lower()
    
    for category, keywords in INSECURITY_LEXICON.items():
        for keyword in keywords:
            if keyword in comment_lower:
                return True, category
    
    return False, None
```

#### 方案 B：情感 + 职业双过滤法（辅助验证）

```python
def is_insecurity_expression_v2(comment, sentiment_score):
    """
    双过滤法：负面情感 + 职业关键词
    
    参数:
        comment: 评论文本
        sentiment_score: 情感得分（-1 到 1）
    
    返回:
        bool: 是否为不安全感表达
    """
    # 条件 1：负面情感
    if sentiment_score >= -0.1:
        return False
    
    # 条件 2：包含职业关键词
    job_keywords = ["工作", "失业", "就业", "岗位", "职业", "职场", "行业"]
    if not any(kw in comment for kw in job_keywords):
        return False
    
    # 条件 3：包含 AI 关键词
    ai_keywords = ["AI", "人工智能", "大模型", "自动化", "机器人", "算法"]
    if not any(kw in comment for kw in ai_keywords):
        return False
    
    return True
```

### 4.4 事件编码方案

**事件数据库构建**：

| 事件 ID | 日期 | 事件类型 | 事件描述 | 媒体曝光度 |
|:---|:---|:---|:---|:---|
| E001 | 2024-03-15 | tech_positive | GPT-4 Turbo 发布 | 高 |
| E002 | 2024-05-20 | job_negative | 某大厂 AI 部门裁员 500 人 | 中 |
| E003 | 2024-07-10 | tech_positive | Sora 视频生成模型发布 | 高 |
| E004 | 2024-09-01 | policy | 国家 AI 治理政策出台 | 中 |
| E005 | 2024-11-15 | report | 麦肯锡发布 AI 就业报告 | 低 |
| ... | ... | ... | ... | ... |

**事件类型编码**：

```python
EVENT_TYPES = {
    "tech_positive": "技术突破（正面）",
    "tech_negative": "技术事故（负面）",
    "job_negative": "失业/裁员新闻",
    "job_positive": "就业增长新闻",
    "policy": "政策出台",
    "report": "研究报告发布"
}
```

### 4.5 时间序列指标构建

**日度指标**：

```python
daily_metrics = {
    # 不安全感表达频率
    "insecurity_count": "每日不安全感评论数量",
    "insecurity_ratio": "不安全感评论占比（/总 AI 评论）",
    
    # 不安全感表达强度
    "insecurity_intensity": "不安全感评论平均情感得分",
    
    # 分类别统计
    "失业担忧_count": "失业担忧类评论数",
    "替代焦虑_count": "替代焦虑类评论数",
    "技能过时_count": "技能过时类评论数",
    "职业焦虑_count": "职业焦虑类评论数",
    "未来担忧_count": "未来担忧类评论数",
    
    # 控制变量
    "total_comments": "每日总评论数",
    "negative_ratio": "负面评论占比",
    "weekend": "是否周末（虚拟变量）"
}
```

### 4.6 统计分析方法

#### （1）中断时间序列分析（ITSA）- 检验 H1, H2, H3

```python
import statsmodels.api as sm

# 构建中断时间序列模型
def fit_itsa_model(daily_data, event_dates):
    """
    中断时间序列分析
    
    参数:
        daily_data: 日度时间序列数据
        event_dates: 事件日期列表
    
    返回:
        模型结果
    """
    # 创建虚拟变量
    daily_data['post_event'] = 0
    daily_data['time_since_event'] = 0
    
    for event_date in event_dates:
        # 事件后虚拟变量
        mask = daily_data['date'] >= event_date
        daily_data.loc[mask, 'post_event'] = 1
        
        # 事件后时间变量
        days_since = (daily_data.loc[mask, 'date'] - event_date).dt.days
        daily_data.loc[mask, 'time_since_event'] = days_since
    
    # 拟合 ARIMA 模型
    model = sm.tsa.ARIMA(
        daily_data['insecurity_count'],
        exog=daily_data[['post_event', 'time_since_event', 'weekend']],
        order=(1, 0, 1)
    )
    
    results = model.fit()
    return results
```

**结果解读**：
- `post_event` 系数：事件后基线水平变化
- `time_since_event` 系数：事件后趋势变化

#### （2）事件类型比较

```python
from scipy import stats

# 比较不同事件类型的影响
def compare_event_types(event_effects):
    """
    比较不同事件类型的影响幅度
    
    参数:
        event_effects: 字典 {事件类型：[影响幅度列表]}
    
    返回:
        ANOVA 结果
    """
    groups = list(event_effects.values())
    f_stat, p_value = stats.f_oneway(*groups)
    return f_stat, p_value
```

#### （3）恢复时间分析

```python
def estimate_recovery_time(daily_data, event_date, window=30):
    """
    估计恢复到基线所需时间
    
    参数:
        daily_data: 日度数据
        event_date: 事件日期
        window: 分析窗口（天）
    
    返回:
        恢复时间（天）
    """
    # 计算基线（事件前 14 天均值）
    baseline = daily_data[
        (daily_data['date'] >= event_date - pd.Timedelta(days=14)) &
        (daily_data['date'] < event_date)
    ]['insecurity_count'].mean()
    
    # 找到恢复到基线的时间点
    post_event = daily_data[daily_data['date'] >= event_date].copy()
    post_event['days_since'] = (post_event['date'] - event_date).dt.days
    
    for _, row in post_event.iterrows():
        if abs(row['insecurity_count'] - baseline) < baseline * 0.1:  # 10% 阈值
            return row['days_since']
    
    return window  # 窗口内未恢复
```

#### （4）交叉相关分析 - 检验 H5

```python
from statsmodels.tsa.stattools import ccf

# 计算不安全感表达与一般负面情绪的交叉相关
def cross_correlation_analysis(daily_data, lag=30):
    """
    交叉相关分析
    
    参数:
        daily_data: 日度数据
        lag: 最大滞后天数
    
    返回:
        交叉相关系数数组
    """
    ccf_values = ccf(
        daily_data['insecurity_ratio'],
        daily_data['negative_ratio'],
        adjusted=False
    )
    
    return ccf_values[:lag+1]
```

#### （5）时间序列趋势检验 - 检验 H6

```python
import statsmodels.api as sm
import numpy as np

def trend_analysis(daily_data, event_dates=None):
    """
    时间序列趋势检验（检验 H6）
    
    参数:
        daily_data: 日度时间序列数据
        event_dates: 事件日期列表（用于控制事件效应）
    
    返回:
        模型结果
    """
    # 构建趋势模型
    daily_data['time_index'] = np.arange(len(daily_data))
    daily_data['time_squared'] = daily_data['time_index'] ** 2  # 非线性趋势
    
    # 控制变量
    exog_vars = ['time_index', 'weekend']
    
    # 如果提供了事件日期，加入事件控制
    if event_dates is not None:
        for i, event_date in enumerate(event_dates):
            daily_data[f'event_{i}'] = (daily_data['date'] >= event_date).astype(int)
            exog_vars.append(f'event_{i}')
    
    # 加入季节性控制（月份）
    daily_data['month'] = daily_data['date'].dt.month
    for month in range(2, 13):  # 以 1 月为参照
        daily_data[f'month_{month}'] = (daily_data['month'] == month).astype(int)
        exog_vars.append(f'month_{month}')
    
    # 拟合 OLS 模型
    model = sm.OLS(
        daily_data['insecurity_ratio'].fillna(daily_data['insecurity_ratio'].mean()),
        sm.add_constant(daily_data[exog_vars])
    )
    
    results = model.fit()
    return results

# 解读趋势
def interpret_trend(results):
    """
    解读趋势检验结果
    
    参数:
        results: OLS 模型结果
    
    返回:
        趋势解读字典
    """
    time_coef = results.params['time_index']
    time_pval = results.pvalues['time_index']
    
    interpretation = {
        'slope': time_coef,
        'p_value': time_pval,
        'significant': time_pval < 0.05,
        'direction': '上升' if time_coef > 0 else '下降',
        'total_change_355days': time_coef * 355 * 100,  # 355 天总变化（百分点）
        'daily_change': time_coef * 10000  # 每日变化（万分点）
    }
    
    return interpretation

# 使用示例
# trend_results = trend_analysis(daily_data, event_dates)
# trend_interp = interpret_trend(trend_results)
# 
# print(f"趋势斜率：{trend_interp['slope']:.6f} /天")
# print(f"P 值：{trend_interp['p_value']:.4f}")
# print(f"355 天总变化：{trend_interp['total_change_355days']:.2f} 个百分点")
# print(f"结论：{'支持 H6（上升趋势）' if trend_interp['significant'] and trend_interp['slope'] > 0 else '不支持 H6'}")
```

**趋势检验模型解读**：

| 参数 | 含义 | 预期值 |
|:---|:---|:---|
| `time_index`系数 | 每日变化量 | 0.0002-0.0004 |
| P 值 | 显著性 | <.05 表示显著 |
| 355 天总变化 | 整个研究期间的变化 | +5 到 +15 个百分点 |

**结果解读模板**：

```python
if trend_interp['significant'] and trend_interp['slope'] > 0:
    conclusion = "支持 H6：职业不安全感表达随时间呈显著上升趋势，355 天内增加约 X 个百分点，支持技术焦虑累积理论。"
elif trend_interp['significant'] and trend_interp['slope'] < 0:
    conclusion = "反向发现：职业不安全感表达随时间显著下降，表明公众逐渐适应 AI 技术。"
else:
    conclusion = "不支持 H6：职业不安全感表达无显著时间趋势，表明公众具有心理韧性，能够适应技术变革。"
```

---

## 五、预期结果

### 5.1 描述性统计

**表 1：研究样本基本特征**

| 变量 | 类别 | 频数 | 百分比 (%) |
|:---|:---|:---:|:---:|
| **平台** | 知乎 | 3,000 | 30.0 |
| | 小红书 | 5,000 | 50.0 |
| | 哔哩哔哩 | 2,000 | 20.0 |
| **不安全感表达** | 有 | 1,200 | 12.0 |
| | 无 | 8,800 | 88.0 |
| **表达类别** | 失业担忧 | 450 | 37.5 |
| | 替代焦虑 | 380 | 31.7 |
| | 技能过时 | 180 | 15.0 |
| | 职业焦虑 | 120 | 10.0 |
| | 未来担忧 | 70 | 5.8 |

### 5.2 假设检验结果

**表 2：假设检验结果汇总**

| 假设 | 预期效应 | 统计方法 | 预期结果 |
|:---|:---|:---|:---|
| H1 | 事件后表达增加 20-40% | ITSA | β = 0.35, p < .001 ✓ |
| H2 | 负面事件效应 > 技术事件 | ANOVA | F(1, 98) = 15.6, p < .001 ✓ |
| H3 | 恢复时间 14-21 天 | 滑动窗口 | 平均 16.5 天 (SD = 4.2) ✓ |
| H4 | 知乎 < 小红书 | t 检验 | t(198) = 3.42, p = .001 ✓ |
| H5 | 中等相关 (r = 0.3-0.6) | 交叉相关 | r = 0.45, p < .001 ✓ |
| **H6** | **355 天上升 5-15 个百分点** | **趋势检验** | **β = 0.0003, p < .05 ✓** |

### 5.3 时间序列可视化

**图 1：职业不安全感表达的时间序列演化**

```
不安全感表达频率
    ↑
    │                    ╭───╮
    │              ╭───╮ │   │         ╭───╮
    │    ╭───╮     │   │ │   │    ╭───╮│   │
    │    │   │ ╭───╯   │ │   │ ╭───╯ │   │
────┴────┴───┴─┴───────┴─┴───┴─┴─────┴───┴────→ 时间
   E1      E2        E3    E4      E5
   
图例：
E1: GPT-4 发布（技术突破）
E2: 某大厂裁员（失业新闻）
E3: Sora 发布（技术突破）
E4: AI 监管政策（政策出台）
E5: 麦肯锡报告（研究报告）
```

**图 2：不同事件类型的影响幅度比较**

```
影响幅度 (%)
    ↑
 50 │         ╭───╮
    │         │   │
 40 │    ╭────┤   │
    │    │    │   │
 30 │ ╭──┤    │   │
    │ │  │    │   │
 20 │ │  │ ╭──┤   │
    │ │  │ │  │   │
 10 │ │  │ │  │   │
    │ │  │ │  │   │
  0 └─┴──┴─┴──┴───┴────→ 事件类型
     技术  失业  政策  报告
     突破  新闻  出台  发布
```

---

## 六、效度验证方案

### 6.1 人工标注验证

**抽样方案**：
- 随机抽取 500 条评论
- 覆盖所有平台和时间段
- 包含关键词匹配和非匹配样本

**标注类别**：

| 类别 | 定义 | 示例 |
|:---|:---|:---|
| **明确不安全感** | 直接表达职业担忧 | "我担心被 AI 替代" |
| **模糊表达** | 间接提及但不明确 | "AI 发展真快" |
| **无关** | 与职业不安全感无关 | "AI 技术真厉害" |

**一致性检验**：

```python
from sklearn.metrics import cohen_kappa_score, classification_report

# 计算评分者间一致性
def calculate_inter_rater_reliability(annotations_1, annotations_2):
    """
    计算 Cohen's Kappa
    
    参数:
        annotations_1: 评分者 1 的标注
        annotations_2: 评分者 2 的标注
    
    返回:
        Kappa 系数
    """
    kappa = cohen_kappa_score(annotations_1, annotations_2)
    return kappa

# 预期结果
# Kappa > 0.7: 良好一致性
# Kappa > 0.8: 优秀一致性
```

### 6.2 分类性能指标

**表 3：关键词匹配法的分类性能**

| 指标 | 预期值 | 可接受阈值 |
|:---|:---:|:---:|
| 准确率 | 85% | > 80% |
| 召回率 | 75% | > 70% |
| F1 分数 | 0.80 | > 0.75 |
| Cohen's κ | 0.78 | > 0.70 |

### 6.3 敏感性分析

**测试不同关键词阈值的影响**：

| 阈值 | 不安全感评论数 | 占比 (%) | 准确率 |
|:---|:---:|:---:|:---:|
| 宽松（3 类匹配） | 1,800 | 18.0 | 78% |
| **标准（5 类匹配）** | **1,200** | **12.0** | **85%** |
| 严格（所有类匹配） | 450 | 4.5 | 92% |

---

## 七、研究局限与应对

### 7.1 概念效度局限

**局限**：社交媒体表达≠内在心理状态

**应对**：
- 明确使用"表达"而非"感知"
- 增加效度验证（人工标注）
- 在讨论部分说明边界

### 7.2 因果推断局限

**局限**：观察性设计无法确立因果关系

**应对**：
- 使用"关联"而非"影响"表述
- 时间序列分析提供时间顺序证据
- 讨论可能的混淆变量

### 7.3 样本代表性局限

**局限**：社交媒体用户不代表总体人口

**应对**：
- 说明样本特征（年龄、教育、平台）
- 多平台数据提高代表性
- 讨论推广边界

---

## 八、分析代码框架

### 8.1 主分析流程

```python
# main_analysis.py

import pandas as pd
import numpy as np
from insecurity_analyzer import InsecurityAnalyzer
from time_series import TimeSeriesAnalyzer

# 1. 加载数据
comments = pd.read_parquet('data/comments.parquet')

# 2. 识别不安全感表达
analyzer = InsecurityAnalyzer()
comments['is_insecurity'] = comments['content'].apply(
    lambda x: analyzer.is_insecurity_expression(x)[0]
)
comments['insecurity_category'] = comments['content'].apply(
    lambda x: analyzer.is_insecurity_expression(x)[1]
)

# 3. 构建日度时间序列
daily_data = comments.groupby('date').agg({
    'is_insecurity': ['sum', 'mean'],
    'content': 'count'
}).reset_index()
daily_data.columns = ['date', 'insecurity_count', 'insecurity_ratio', 'total_comments']

# 4. 事件分析
events = pd.read_csv('data/events.csv')
ts_analyzer = TimeSeriesAnalyzer()

# 5. 中断时间序列分析
itsa_results = ts_analyzer.fit_itsa_model(
    daily_data, 
    events['date'].tolist()
)
print(itsa_results.summary())

# 6. 事件类型比较
event_effects = ts_analyzer.compare_event_types(events, daily_data)
print(event_effects)

# 7. 恢复时间分析
recovery_times = ts_analyzer.estimate_recovery_times(events, daily_data)
print(f"平均恢复时间：{recovery_times.mean():.1f} 天")

# 8. 可视化
ts_analyzer.plot_time_series(daily_data, events)
ts_analyzer.plot_event_comparison(event_effects)
```

### 8.2 关键词分析器

```python
# insecurity_analyzer.py

class InsecurityAnalyzer:
    def __init__(self):
        self.lexicon = self._load_lexicon()
    
    def _load_lexicon(self):
        """加载职业不安全感词典"""
        return {
            "失业担忧": ["担心失业", "害怕失业", "怕失业", "裁员", "被优化"],
            "替代焦虑": ["被替代", "被取代", "被淘汰", "AI 抢工作"],
            "技能过时": ["技能过时", "学不过来", "跟不上", "要转行"],
            "职业焦虑": ["工作焦虑", "就业难", "35 岁危机", "职场焦虑"],
            "未来担忧": ["前景堪忧", "未来怎么办", "没希望了"]
        }
    
    def is_insecurity_expression(self, comment):
        """判断是否为不安全感表达"""
        for category, keywords in self.lexicon.items():
            for keyword in keywords:
                if keyword in comment:
                    return True, category
        return False, None
    
    def calculate_insecurity_score(self, comment):
        """计算不安全感得分（0-5）"""
        score = 0
        for category, keywords in self.lexicon.items():
            if any(kw in comment for kw in keywords):
                score += 1
        return score
```

---

## 九、论文结构建议

### 9.1 标准实证论文结构

```
1 引言
  1.1 研究背景
  1.2 问题提出
  1.3 研究目的与意义
  1.4 论文结构

2 文献综述与理论框架
  2.1 职业不安全感的理论基础
  2.2 AI 技术事件的社会影响研究
  2.3 社交媒体数据分析方法
  2.4 理论框架与研究假设

3 研究方法
  3.1 研究设计
  3.2 数据来源与采集
  3.3 职业不安全感表达的操作化定义
  3.4 事件编码方案
  3.5 时间序列指标构建
  3.6 统计分析方法
  3.7 效度验证方案

4 研究结果
  4.1 描述性统计
  4.2 假设检验结果
  4.3 时间序列演化模式
  4.4 事件类型比较
  4.5 恢复时间分析
  4.6 敏感性分析

5 讨论
  5.1 主要发现解释
  5.2 与现有文献对话
  5.3 理论贡献
  5.4 实践启示
  5.5 研究局限与未来方向

6 结论
  6.1 研究总结
  6.2 政策建议

参考文献
附录（关键词词典、事件列表）
```

---

## 十、发表建议

### 10.1 目标期刊

| 期刊 | 领域 | 影响因子 | 适配度 |
|:---|:---|:---:|:---:|
| **Journal of Vocational Behavior** | 职业心理学 | 4.5 | ⭐⭐⭐⭐⭐ |
| **Journal of Occupational Health Psychology** | 职业健康 | 3.8 | ⭐⭐⭐⭐ |
| **New Media & Society** | 新媒体研究 | 5.2 | ⭐⭐⭐⭐ |
| **Computers in Human Behavior** | 人机交互 | 9.9 | ⭐⭐⭐⭐ |
| **Journal of Business Research** | 商业研究 | 10.9 | ⭐⭐⭐ |

### 10.2 关键审稿点预测

**可能的问题**：
1. 概念效度：社交媒体表达能否代表职业不安全感？
2. 因果推断：观察性设计能否支持因果结论？
3. 样本代表性：社交媒体用户是否代表总体？

**应对策略**：
1. 明确概念界定，增加效度验证
2. 使用关联性表述，避免因果语言
3. 讨论样本特征和推广边界

---

## 十一、时间规划

| 阶段 | 任务 | 时间 | 产出 |
|:---|:---|:---:|:---|
| **第 1 周** | 构建关键词词典 | 3 天 | 词典 v1.0 |
| | 人工标注训练 | 2 天 | 标注指南 |
| **第 2 周** | 数据预处理 | 3 天 | 清洗后数据 |
| | 不安全感识别 | 2 天 | 标注结果 |
| **第 3 周** | 时间序列构建 | 2 天 | 日度指标 |
| | 事件数据库 | 3 天 | 事件列表 |
| **第 4 周** | 主效应分析 | 3 天 | ITSA 结果 |
| | 调节效应分析 | 2 天 | 比较结果 |
| **第 5 周** | 效度验证 | 3 天 | 一致性检验 |
| | 敏感性分析 | 2 天 | 稳健性检验 |
| **第 6-8 周** | 论文撰写 | 3 周 | 初稿 |
| **第 9-10 周** | 修改润色 | 2 周 | 投稿稿 |

---

## 十二、总结

本方案通过时间序列分析方法，研究 AI 技术事件与职业不安全感表达的关联模式。核心优势在于：

1. **概念创新**：提出"职业不安全感表达"构念，明确区别于内在心理状态
2. **方法严谨**：中断时间序列 + 效度验证 + 敏感性分析
3. **数据新颖**：多源社交媒体数据，355 天连续追踪
4. **实践价值**：为 AI 治理和就业政策提供实证依据

**关键注意事项**：
- 全文使用"表达"而非"感知"
- 因果表述谨慎（关联≠因果）
- 充分的效度验证和局限性讨论

---

**文档版本**：v1.0  
**更新日期**：2026-03-29  
**作者**：研究团队
