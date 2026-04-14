# 最小稳妥成品化工作区说明

## 工作目标

当前 `workspace/` 只保留完成论文最小稳妥成品化所需的核心资产，避免旧实验脚本、旧草稿和过时章节继续干扰主工作流。

## 当前保留资产

### 1. 原始数据

- `ai_crawl_data_20260413_004926/`
  当前论文的核心新数据源。

### 2. 正文文件

- `canonical_chapters/`
  当前有效的章节正文、摘要、参考文献和一致性矩阵。

### 3. 分析脚本

- `preprocess_data.py`
  新数据预处理主脚本。
- `revised_hypothesis_analysis.py`
  新版假设分析主脚本。

### 4. 分析输出

- `paper-revision/processed_data/`
  预处理后的中间数据与质量报告。
- `paper-revision/revised_hypothesis_analysis/`
  新版假设分析结果输出。

### 5. 成品导出链路

- `scripts/build_ruc_thesis_docx.py`
  Word 导出脚本。
- `formal_docx/中国人民大学本科毕业论文_正式排版版.docx`
  当前正式导出稿。
- `formal_docx/assets/`
  导出时使用的资源文件。
- `format/`
  格式参考资源与 logo。

## 已迁出的旧材料

旧脚本、旧草稿、旧事件分析、旧文档版本、旧计划文档已统一迁移至：

- `workspace2/legacy_archive/workspace/`

后续如需回看旧材料，请优先去该目录，不要再把旧文件搬回主工作区。

## 建议工作流

1. 修改 `canonical_chapters/` 中的正文内容。
2. 如需刷新统计结果，运行：
   - `python workspace/preprocess_data.py`
   - `python workspace/revised_hypothesis_analysis.py`
3. 如需刷新 Word 成品，运行：
   - `python workspace/scripts/build_ruc_thesis_docx.py`
4. 仅在上述链路中新增资产，避免重新引入一次性脚本和分散草稿。

## 当前下一步

按“最小稳妥成品化”目标，后续工作优先级应为：

1. 检查正文与结果口径是否完全一致
2. 清理参考文献与引文系统
3. 补足必要的表述边界与局限
4. 生成可提交的正式稿
