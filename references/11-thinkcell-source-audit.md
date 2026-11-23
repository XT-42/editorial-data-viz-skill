# 11｜think-cell 官方图表审查与来源（2026-11-23）

## 结论

官网使用“40+ 图表类型”的公开描述；官方插入菜单、元素图标和手册中，关键图形入口主要是**16 种**（其中 Doughnut 在官方产品截图中独立出现）。将堆积/百分比/横向/组合/特殊应用进一步展开后可列出更多可视化形态，但不可把这些形态全都当成独立按钮。

**覆盖方式**：
- `thinkcell/catalog.json.menu`：16 个菜单入口，字段 `evidence=official-menu-or-product-icon`。
- `thinkcell/catalog.json.variants`：48 个图形变体/实际应用，标注 `evidence=documented-variant` 或 `documented-application`，全部 `is_separate_insertion_button=false`。
- `thinkcell/annotations.json`：19 个功能点（不是图表类型）。
- `assets/thinkcell-chart-gallery.html`：16 个独立原创 SVG 演示，均为虚构/模拟数据。

## 菜单图形逐类覆盖

| 入口 | 可映射的业务问题 | 官方依据 |
|---|---|---|
| 堆积柱形/条形 | 总量 + 构成 | Column, line, and area charts |
| 100% 堆积柱形/条形 | 占比比较 | Column, line, and area charts |
| 簇状柱形/条形 | 组内并列对比 | Column, line, and area charts |
| 上行瀑布 | 增量桥接 | Waterfall charts |
| 下行瀑布 | 收入到利润桥接 | Waterfall charts |
| 单位轴 Mekko | 同时编码列宽与单位轴 | Mekko charts |
| 百分比轴 Mekko | 类别总体量 × 内部占比 | Mekko charts |
| 堆积面积 | 随时间的总量与结构 | Column, line, and area charts |
| 100% 堆积面积 | 随时间的结构比例 | Column, line, and area charts |
| 折线/轮廓 | 时间变化、旋转轮廓 | Column, line, and area charts |
| 组合 | 柱+线/双轴/帕累托 | Combination charts |
| 饼图 | 份额 | Pie and doughnut charts |
| 圆环 | 份额、同心比较、量规式应用 | Pie and doughnut charts + product |
| 散点 | 双变量关联、拟合、分区 | Scatter and bubble charts |
| 气泡 | 第三维量值以面积表示 | Scatter and bubble charts |
| 甘特 | 项目时间轴/里程碑 | Gantt charts |

## 自动注释的关键地位

think-cell 的优势不仅在“有哪些图”，更在图表更新时同步处理：
- **差异箭头、CAGR 箭头/标签、数值线、100% 指示、系列连接线、通用连接线**；
- **轴断裂、图例、类别/系列/点/总数标签与可编辑标注**；
- **数据驱动表格、甘特日历、活动条、里程碑和状态符号**。

网页端应该通过 `AnnotationLayer`（统一布局引擎）把这些能力与图形绑定，不能仅通过 CSS 静态覆盖文字。

## 不当等同提醒

- `Butterfly / Tornado`、`Candlestick / Football field`、`Gauge` 是官方产品页明确提到的**可构建应用形态**，并非本表声称的独立插入菜单图标。
- `CAGR arrows`、`Harvey balls`、`checkboxes`、`charts with data tables` 是增强元素/表格，不是图形类别。
- `build-up` 与 `build-down` 是同一瀑布分析模型的不同初始方向。
- 所有 SVG 示例均为本仓库原创、独立、零外部库的教学图形，不包含 think-cell 代码。

## 官方来源

1. [Elements 菜单与图形](https://www.think-cell.com/en/resources/manual/basicconcepts)
2. [产品介绍与 40+ 声明](https://www.think-cell.com/zh/product/think-cell-charts)
3. [柱、线、面积和组合](https://www.think-cell.com/en/resources/manual/column-line-area-charts)
4. [瀑布图](https://www.think-cell.com/en/resources/manual/waterfall)
5. [Mekko 图](https://www.think-cell.com/en/resources/manual/mekko)
6. [散点与气泡](https://www.think-cell.com/en/resources/manual/scatterbubble)
7. [甘特时间线](https://www.think-cell.com/en/resources/manual/gantt)
8. [图表自动注释](https://www.think-cell.com/en/resources/manual/chartdecorations)
9. [标签](https://www.think-cell.com/en/resources/manual/textlabels)
10. [绑定数据表](https://www.think-cell.com/en/resources/manual/charts-with-data-tables)
11. [官方 think-cell 插入菜单图](https://www.think-cell.com/en/resources/manual/think-cell-charts)

资料核验日期：2026-11-23。所有“可应用形态”按官方文档理解作独立网页实现，并非对原商用软件内部技术的逆向还原。
