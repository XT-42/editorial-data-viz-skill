# 专业图表图谱 · v1.1.0

本目录是 `editorial-data-viz` 的**领域级图表资产**，与页面模板（`templates/T001`）相互独立。

- **30 个结构化图形配方**：`catalog.json`，按趋势 / 比较 / 归因 / 流程 / 构成 / 分布 / 零售 / 地理空间分类。
- **15 个原生 SVG 交互演示**：`../assets/pro-chart-gallery.html`。演示为**原创模拟数据**，不含第三方原站代码。
- **可检索 ID**：如 `waterfall`、`dumbbell`、`cohort-heatmap`、`control-chart` 等。调用时写出 ID 可以让 Agent 按确定的图形契约开发。
- **严谨的可信度字段**：每个图形都有 `evidence_status: independent-professional-extension`。这**不是**原 Google AI Studio 模板的真实图表清单，原站尚未完成实测核验。

## 选择优先级

先确定统计问题、数据粒度与单位，再选择图形形态，而不是让 AI 先画好看图：

1. 时间/波动：annotated-line、small-multiples、control-chart、calendar-heatmap、bump-chart。
2. 对比/排序：dumbbell、slopegraph、diverging-bars、bullet、pareto。
3. 归因/流程：waterfall、sankey、funnel、chord、flow-network。
4. 构成：treemap、marimekko、waffle。
5. 分布/关联：scatter-quadrant、hexbin、boxplot、violin、ridge、uncertainty-band。
6. 零售专业：cohort-heatmap、inventory-heatmap、seasonal-matrix、supply-otif。
7. 地理：geo-density。

## 一套图表配方包含什么

`catalog.json` 中每条都有：

- `question`：要回答的具体业务问题。
- `fields`：必要字段或衍生统计量。
- `encoding`：坐标、面积、颜色、线条分别编码什么。
- `interaction`：筛选、联动、缩放或钻取。
- `annotation`：最重要的文字注释。
- `risk`：容易产生统计错觉或口径错误的地方。
- `renderers`：适宜的实现技术而非强制依赖。
- `demo`：是否已有独立原创 SVG 图形演示。
- `evidence_status`：是否是专业扩展（目前均为专业扩展）。

这些配方在业务分析中和模板视觉风格进行组合：**图表选择是语义层，T001 是视觉层**。

## 升级规则

新增图形时，必须记录所有必填字段并更新校验脚本。将 `demo` 设为 `true` 前必须真实实现展示，不能把静态文案或占位图称为“已实现图形”。

更多细节：`../references/07-专业图表图谱.md`、`../references/08-图形工程契约.md`、`../references/10-图表计算配方.md`。
