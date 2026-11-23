# 12｜think-cell 式商业图形：网页端完整工程规范

目标：在 React/Next.js + SVG/D3/visx/ECharts 环境中实现商业咨询级图表叙事，保持可解释与可访问；不使用 think-cell 专有实现。

## 1. 分层架构

```
Business question / Metric dictionary / Calculation engine
  ↓ normalized chart-data table (grain, unit, period, provenance)
  ↓ ChartSpec (chart_id from thinkcell/catalog.json, variant_id)
  ↓ Transforms (stack, percent, waterfall, mekko, regression, dates)
  ↓ Renderer (D3 scales + visx/SVG, or ECharts / canvas)
  ↓ Annotations (difference/CAGR/subtotals/value lines/labels)
  ↓ Accessible table + source + date + export
```

## 2. chart spec（生产项目建议）

```ts
interface ThinkcellStyleChartSpec {
  chartId: string;              // thinkcell/catalog.json.menu[].id
  variantId?: string;           // thinkcell/catalog.json.variants[].id
  templateId?: string;          // 视觉模板 T001; future T002/T003...
  title: string;
  purpose: string;              // 业务问题
  dimensions: string[];
  measures: {name:string; field:string; unit:string; formula:string; grain:string}[];
  dataSource: {status:'real'|'mock'|'unknown'; updatedAt?:string; period:string; denominator?:string};
  axis: {x:string; y:string; y2?:string; percent?:boolean; zeroBaseline?:boolean};
  categories?: string[];
  annotations?: {type:string; anchor:string; label?:string; value?:number}[];
  comparison?: {baseline:string; sampleRule:string};
  interactive?: {filters:string[]; crossFilter?:boolean; exportTable?:boolean};
  responsive?: {smallScreen:'transpose'|'stack'|'swap-chart'|'scroll'};
}
```

## 3. 统计与布局公式

### 堆积 / 100% 堆积
- `total(category)=Σseries value`；单位一致才能求和。
- `share(category,series)=value/total(category)`；总量0或无效时显示 N/A，不画0%当正常。
- 100% 面积、100% 柱图各时点独立标准化，**不能让比例变化伪装规模变化**。

### Waterfall
- `running[0]=baseline`，`running[i+1]=running[i]+delta[i]`；总计标签单独编码。
- 上行/下行只改变叙事方向；数值由带符号 delta 决定。
- 多系列堆积瀑布分步骤聚合；小计只引用当前累计值，**不要在累计中二次加小计**。
- 跨越零基线的负数段自动定位到两端的最小/最大范围。
- `abs(expectedTotal-finalRunning) <= tolerance`；超出时显示“未对齐”。

### Mekko（区分两种轴）
- 百分比轴：`width[c] = category_total[c] / grand_total`，`height[c,s] = value[c,s]/category_total[c]`；因此 `area[c,s]=value[c,s]/grand_total`。
- 单位轴：**列宽由 X extent 独立输入，纵轴段高由各系列绝对数值独立输入**。不能把总量作为该变体的自动列宽。与百分比轴 Mekko 的百分比高度算法不同。
- `Other` 长尾聚合必须留有分类映射并给出数据表。负数及0按业务定义另行处理。

### Difference + CAGR
- 差额：`B-A`，变化率：`(B-A)/abs(A)`；若 A=0，变化率不可计算。
- CAGR：`(end/start)^(1/years)-1`；`years > 0` 且首末值满足公式定义。负值、0、跨零须解释“不适用”。
- 注释锚点随数据点、视口和字体动态布局，不能静态绝对定位。

### Pie / Doughnut / Gauge
- `share_i=value_i/Σvalue`，要求分母为正，数值非负。
- Gauge 可用圆环分段实现，但超额情形必须提供文字说明或另一幅图；不可裁剪并谎称完成度只有100%。

### Scatter / Bubble
- 散点线性拟合需说明算法；分区阈值必须来自真实业务阈值或可复核分位数。
- Bubble 图 `radius ∝ sqrt(size)`，显示面积图例；数量不应该线性映射半径。
- think-cell 中部分回归可按气泡大小加权；网页端也要将权重/方法写在图注中。

### Gantt
- 每个活动有 `start <= end`，UTC 与本地日期转换一致，财年与自然年分开。
- `x(date)` 使用真实时间比例尺；里程碑菱形绑定日期，鼠标悬停/键盘焦点展示日期。
- 任务状态（待开始/进行中/阻塞/完成）和项目完成百分比是两个字段，不自动等同。

## 4. 自动注释布局引擎（最值得学习）

1. 计算每幅图的 plot area 与 anchor point。
2. 根据优先级（主结论 > 差额/CAGR > 总计 > 系列 > 次级坐标）构建标签候选位置。
3. 利用估算文本宽度/测量 DOM bbox 检测碰撞；尝试上下、左右偏移、引导线。
4. 对超出边界的标签放入旁列，或在移动端转“注释列表”；不得无提示删除关键标注。
5. 所有标注值由 chart-data 计算并订阅筛选状态，屏幕变化时重新布局。
6. `prefers-reduced-motion` 与可访问表格是必需项，不只是动画装饰。

## 5. 数据绑定与性能

- 图与表共享 `MetricStore`（指标口径、单位、更新时间、筛选、样本数），减少图表和明细“两个版本真相”。
- StarRocks 大明细必须 API 层分区裁剪、聚合与分页；React 前端只接受已裁剪数据。
- 常规咨询式图（几十个 marks）用 SVG；大规模门店/时间点则改 Canvas / WebGL / 预聚合。
- 允许导出带版本与口径的 CSV 和 SVG/PDF（用户要求时），禁止直接冒充 think-cell 的原生 PPT 编辑对象。

## 6. 非图表元素与关系

数据表、Harvey Ball、复选框、议程、卡片与图形化注释属于报告展示部件，详见 `thinkcell/annotations.json`。可以借鉴其信息编码思想，但不计入 `menu_count`。

## 7. 开发验收

- 所有 menu 图型都有字段、编码、风险、来源与 SVG 例子。
- 瀑布守恒、Mekko 宽高/面积、气泡面积、CAGR 基期与日期、Gantt 时长通过单测。
- 图表/表格/注释显示同一时间与筛选。
- 无障碍标题、段落摘要、focus/hover 辅助信息、深浅主题对比度、360px 适配。
- 所有模拟值标 `MOCK`，不以示例数字暗示现实业绩。
