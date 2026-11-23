# 发布到 GitHub（仓库维护者指南）

此仓库建议公开发布为 `XT-42/editorial-data-viz-skill`，保留完整的 `SKILL.md`、`templates/`、`references/`、`scripts/`、`assets/` 与 `agents/`。

## 方式一：通过 GitHub 网页发布（不需要命令行）

1. 登录 GitHub，创建名称为 `editorial-data-viz-skill` 的**公开**仓库。创建时不要预先添加 README 或 License，避免与此目录文件冲突。
2. 在新仓库点击 **uploading an existing file**，上传当前目录的所有文件（含隐藏目录 `.github`）。部分浏览器不能直接拖入目录时，请改用命令行方式，确保目录结构完整。
3. 提交到 `main` 分支，并在 Actions 中确认 **Validate Skill** 工作流通过。

## 方式二：GitHub CLI（Windows PowerShell / macOS / Linux）

首先安装 Git 与 GitHub CLI，并登录拥有 `XT-42` 仓库创建权限的账号。

```powershell
gh auth login
gh auth status
git init -b main
git add .
git commit -m "feat: publish Chinese editorial data visualization skill"
gh repo create XT-42/editorial-data-viz-skill --public --source . --remote origin --push
```

注意：上述命令用于**新仓库**，如同名仓库已存在，请先确认仓库内容，再决定是克隆后合并还是使用其他名称，勿强制推送覆盖。

## 开源许可证

当前**未自动附加 LICENSE**，因为公开可见不等同于授权任意使用。发布前请确定是否采用 MIT、Apache-2.0 或其他许可证。选定后在仓库根目录添加对应 LICENSE 文件。

## 后续维护

- 新模板：`python scripts/add_template.py --slug your-template --name '模板名称' --source 'https://example.com'`
- 本地校验：`python scripts/validate_skill.py`
- 每次推送 GitHub Actions 会自动运行校验。
