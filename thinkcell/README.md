# think-cell 方法论 → 中文网页专业可视化模块（v1.2）

本模块为**独立开发的图表规范与演示**，并非 think-cell 官方 Skill、源码或插件，也不提供 PowerPoint 的原生 think-cell 授权功能。

## 内容与计数

- **16 个经官网手册/产品截图核验的插入菜单图形入口**：见 `catalog.json.menu`。
- **48 种可复用的变体/业务应用配方**：见 `catalog.json.variants`。其中多项是既有菜单图形的组合/旋转/特殊用途，**不代表另外 48 个菜单按钮**。
- **19 项图形增强机制**：见 `annotations.json`；差异箭头、CAGR、数值线、标签、百分比指示、图表与明细表联动等。**它们不是图表种类**。
- **16 个独立原创 SVG 示例**：见 `../assets/thinkcell-chart-gallery.html`，对应 16 个菜单入口。演示不复刻 think-cell 品牌图标或内部算法。
- **一份网页组件工程指南**：`../references/12-thinkcell-web-engineering.md`，包括统计不变量、数据契约与实现建议。
- **原有 30 种专业图表**：保留于 `../charts/catalog.json`，与本模块可以组合使用。

## 与 T001、未来模板的关系

```
T001 编辑式排版与滚动故事（视觉模板）
     │
     ├── charts/catalog.json （通用30图形）
     └── thinkcell/catalog.json （16基础入口 + 48变体）
           └── thinkcell/annotations.json （19增强标注和表格能力）
```

T001 不会被覆盖。未来的 T002/T003 模板也可调用同一图表语义系统。

## 何时应用

- 商业咨询、董事会汇报、品类策略、采购与供应链专题、预算与利润分解时：先读 `references/11-thinkcell-source-audit.md` 与 `thinkcell/catalog.json`。
- 对图表提出“想做成 think-cell 那样专业”的要求时：重点学习 **图形与标注自动协同、合计与分母、桥接守恒、标签不遮挡**，而不是模仿 UI 表面。
- 网页实现时：图表不依赖 PowerPoint，优先用 D3/visx/SVG、ECharts、React、TanStack Table 等开放 Web 技术。

## 直接使用示例

```
$editorial-data-viz 结合 T001 的编辑式风格，采用 thinkcell 模块的 waterfall-build-up、mekko-percent、combination、gantt，制作中文版采购/供应链专题，包含自动差异箭头、CAGR 与精确数据表。
```

## 证据范围与安全

think-cell 官网称拥有 40+ 图表类型（营销/产品统计口径）。官方手册列出的插入图形入口相对集中，不要混同。详见 `references/11-thinkcell-source-audit.md`。

参考来源：
- https://www.think-cell.com/en/resources/manual/basicconcepts
- https://www.think-cell.com/zh/product/think-cell-charts
- https://www.think-cell.com/en/resources/manual/chartdecorations
- https://www.think-cell.com/en/resources/manual/gantt
