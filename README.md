# 中文编辑式数据可视化 Skill（可扩展模板库）

本 Skill 将 Google AI Studio “Interactive Data Dashboard” 所讨论的四个理念——**SVG 图形、实时筛选、滚动叙事、可访问的数据表**——转化为可执行的中文前端设计工作流。

> 重要：T001 是根据**本次对话中提炼的设计理念**建立的原创风格方案，**未验证原网页截图、源码或精确图表种类**。所给颜色、字体、布局是本 Skill 的推荐方案，不代表 Google 官方原始配置。

## 文件结构

```text
editorial-data-viz-skill/
├── SKILL.md                         # 调用规则、流程、边界
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
└── assets/editorial-demo.html       # 本地可打开的原创交互示例
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

直接双击打开 `assets/editorial-demo.html`，无需安装依赖。演示的是零售分析场景，所有数值均为模拟数据，用于验证理念而非展示模板原站。

## 规范与溯源

- 原模板链接：https://aistudio.google.com/apps/bundled/interactive-data-dashboard?showPreview=true&showAssistant=true&remix=true
- Agent Skills 官方文档：https://learn.chatgpt.com/docs/build-skills
- 设计遵循：明确口径、优先洞察、直接标注、可访问与移动端重排。

## 发布与持续集成

仓库内提供 [GitHub 发布操作说明](PUBLISHING.md) 及 `.github/workflows/validate-skill.yml`。公开发布前由仓库所有者确定 LICENSE，当前不会自动替用户选择开源协议。
