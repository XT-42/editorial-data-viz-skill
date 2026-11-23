# 中文编辑式数据可视化 Skill v1.1 · 专业图形系统 + 可扩展模板库

本 Skill 将 Google AI Studio “Interactive Data Dashboard” 所讨论的四个理念——**SVG 图形、实时筛选、滚动叙事、可访问的数据表**——转化为可执行的中文前端设计工作流。

> 重要：T001 是根据**本次对话中提炼的设计理念**建立的原创风格方案，**未验证原网页截图、源码或精确图表种类**。所给颜色、字体、布局是本 Skill 的推荐方案，不代表 Google 官方原始配置。

## v1.1 新增：专业图形设计资产

原有 T001 主要解决版式、叙事和筛选，专业图形种类不足。v1.1 引入独立的 `charts/` 层：

- **30 种图表配方**：完整目录在 [charts/catalog.json](charts/catalog.json)，每种带字段、视觉编码、交互、图上注释、风险、实现技术与证据状态。
- **15 个可运行的原创 SVG 演示**：双击打开 [assets/pro-chart-gallery.html](assets/pro-chart-gallery.html)，可以中文搜索、按类别筛选、切换主题，并查看每幅图的数据契约。
- **专业规范**：[references/07-专业图表图谱.md](references/07-专业图表图谱.md)、[references/08-图形工程契约.md](references/08-图形工程契约.md)、[references/10-图表计算配方.md](references/10-图表计算配方.md)。
- **来源分级**：[references/09-原模板核验记录.md](references/09-原模板核验记录.md)明确哪些能力有来源、哪些图是后加的专业扩展。未访问到原页面实际图形，不能声称精确学习了 Google 原始图表形态。

推荐调用：`$editorial-data-viz 使用 T001 + charts/catalog.json 中的 waterfall、dumbbell、cohort-heatmap，为采购业务开发中文图表`。

## 文件结构

```text
editorial-data-viz-skill/
├── SKILL.md                         # 调用规则、流程、边界
├── charts/catalog.json              # 30 种专业图表配方
├── charts/README.md                 # 选型原则与图表目录
├── README.md                        # 使用与安装
├── agents/openai.yaml               # 显示名称与默认调用语
├── templates/
│   ├── registry.json                # 模板索引：T001 已启用，T002～T004 预留
│   ├── google-ai-studio-interactive-dashboard/
│   │   ├── template.json            # 机器可读模板定义
│   │   └── STYLE.md                 # 人可读设计理念及规范
│   └── _template-blueprint/         # 新模板蓝图（未注册）
├── references/                       # 分层读取的通用规则
├── scripts/
│   ├── add_template.py              # 新增模板、自动占用下个槽位
│   └── validate_skill.py            # 校验完整性
├── assets/editorial-demo.html       # 基础编辑式叙事示例
└── assets/pro-chart-gallery.html    # 15 种专业 SVG 图形演示
```

## 如何安装/调用

1. 解压 ZIP，保留整个 `editorial-data-viz-skill` 文件夹。
2. 在 **Codex 项目**中放入：`你的项目/.agents/skills/editorial-data-viz/`，保证最终路径下直接有 `SKILL.md`。亦可放入本机用户级 Skills 目录（按当前客户端文档设置）。
3. 在 Codex 输入：`$editorial-data-viz 帮我按 T001 做一个采购/供应链经营分析页面`。
4. 在支持自定义 Skill 的其他 Agent 中导入整个文件夹；不同产品的支持方式可能有差异。**仅下载文件并不会自动安装到当前聊天。**

## 四种实际调用范例

- `$editorial-data-viz 使用 T001 做一页中文品类经营分析，重点是增长贡献与异常定位，先给信息架构。`
- `$editorial-data-viz 按 T001 开发 React 页面，筛选包括省份、品类、月份，数据用模拟值并明确标注。`
- `$editorial-data-viz 检查我的 Dashboard 截图：图表标注、颜色、网格和移动端有什么问题？`
- `$editorial-data-viz 新增一个设计模板，来源是[地址/截图]，命名为 Folio Editorial，保留 T001 不变。`

## 添加第二、第三套模板

```bash
python scripts/add_template.py --slug folio-editorial --name 'Folio 编辑式视觉' --source 'https://example.com' --description '强调版式、注释与留白的分析页面'
python scripts/validate_skill.py
```

新增后：
- 自动占用 `T002`，并从预留槽位中移除；随后补充新槽位。
- 生成 `templates/folio-editorial/template.json`、`STYLE.md`，不覆盖 T001。
- 打开 `STYLE.md`，根据真实截图/源码补充视觉证据；在 `template.json` 中标记核验状态。
- 如要将新模板设成默认值，手动改 `templates/registry.json` 的 `default_template_id`。

**多模板组合**：用户明确要求混搭时，将“页面层排版”、“图形编码”、“交互系统”拆成独立来源说明，不盲目叠加所有风格。详见 `references/05-扩展模板规范.md`。

## 演示

直接双击打开 `assets/editorial-demo.html`（编辑式叙事）或 `assets/pro-chart-gallery.html`（15 种专业 SVG 图形），无需安装依赖。演示均为原创模拟数据，而非 Google 模板原站复刻。

## 规范与溯源

- 原模板链接：https://aistudio.google.com/apps/bundled/interactive-data-dashboard?showPreview=true&showAssistant=true&remix=true
- Agent Skills 官方文档：https://learn.chatgpt.com/docs/build-skills
- 设计遵循：明确口径、优先洞察、直接标注、可访问与移动端重排。

## 发布与持续集成

仓库内提供 [GitHub 发布操作说明](PUBLISHING.md) 及 `.github/workflows/validate-skill.yml`。公开发布前由仓库所有者确定 LICENSE，当前不会自动替用户选择开源协议。
