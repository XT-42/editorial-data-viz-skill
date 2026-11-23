#!/usr/bin/env python3
"""验证 Skill 主文件、模板注册表和模板资源是否一致。"""
from __future__ import annotations
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
errors: list[str] = []


def err(msg: str) -> None:
    errors.append(msg)


def main() -> None:
    main_file = ROOT / "SKILL.md"
    if not main_file.is_file():
        err("缺少 SKILL.md")
    else:
        content = main_file.read_text(encoding="utf-8")
        fm = re.match(r"^---\n(.+?)\n---\n", content, flags=re.S)
        if not fm:
            err("SKILL.md 缺少 YAML frontmatter")
        else:
            if not re.search(r"^name: editorial-data-viz\s*$", fm[1], flags=re.M):
                err("缺少或错误的 name")
            if not re.search(r"^description:\s*(?:>|\S)", fm[1], flags=re.M):
                err("缺少 description")
    reg_path = ROOT / "templates" / "registry.json"
    try:
        registry = json.loads(reg_path.read_text(encoding="utf-8"))
    except (ValueError, OSError) as exc:
        err(f"无法读取注册表：{exc}")
        registry = {"templates": [], "reserved_slots": [], "default_template_id": ""}

    seen_ids, seen_slugs, seen_aliases = set(), set(), set()
    for t in registry["templates"]:
        tid, slug = t.get("id"), t.get("slug")
        if not isinstance(tid, str) or not re.fullmatch(r"T\d{3,}", tid):
            err(f"模板 ID 非法：{tid}")
        if tid in seen_ids:
            err(f"模板 ID 重复：{tid}")
        seen_ids.add(tid)
        if slug in seen_slugs:
            err(f"模板 slug 重复：{slug}")
        seen_slugs.add(slug)
        if not isinstance(slug, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug):
            err(f"模板 slug 非法：{slug}")
        for value in [slug, t.get("name", ""), *t.get("aliases", [])]:
            norm = value.strip().lower()
            if norm in seen_aliases:
                err(f"模板名称/别名冲突：{value}")
            seen_aliases.add(norm)
        dirname = ROOT / t.get("path", "")
        if not dirname.is_dir() or not dirname.resolve().is_relative_to((ROOT / "templates").resolve()):
            err(f"模板目录丢失/非法：{tid}")
            continue
        style_path, json_path = dirname / "STYLE.md", dirname / "template.json"
        if not style_path.is_file():
            err(f"缺少 STYLE.md：{tid}")
        try:
            data = json.loads(json_path.read_text(encoding="utf-8"))
        except (ValueError, OSError) as exc:
            err(f"模板 JSON 无效：{tid}，{exc}")
            continue
        for k in ["id", "slug", "status", "evidence_status"]:
            if data.get(k) != t.get(k):
                err(f"注册表和 template.json 字段不一致：{tid}.{k}")
        for k in ["design_pillars", "tokens", "chart_patterns", "interaction_patterns", "responsive_rules", "implementation"]:
            if k not in data:
                err(f"模板缺少 {k}：{tid}")
        if data.get("evidence_status") not in {"derived-from-conversation", "reviewed-screenshot", "reviewed-source", "user-specified"}:
            err(f"未知 evidence_status：{tid}")

    if registry.get("default_template_id") not in seen_ids:
        err("默认模板 ID 不存在")
    if len(set(registry.get("reserved_slots", []))) != len(registry.get("reserved_slots", [])):
        err("预留槽位重复")
    if seen_ids.intersection(registry.get("reserved_slots", [])):
        err("预留槽位与现有模板冲突")
    if any(not re.fullmatch(r"T\d{3,}", x) for x in registry.get("reserved_slots", [])):
        err("预留槽位 ID 非法")
    for ref in ["01-基础设计原则.md", "02-图表和技术选型.md", "03-交互与叙事.md", "04-零售业务适配.md", "05-扩展模板规范.md", "06-验收清单.md"]:
        if not (ROOT / "references" / ref).is_file():
            err(f"缺少参考文件：{ref}")
    # Professional chart atlas v1.1
    atlas_path = ROOT / "charts" / "catalog.json"
    try:
        atlas = json.loads(atlas_path.read_text(encoding="utf-8"))
        charts = atlas["charts"]
        if len(charts) < 30:
            err("专业图表少于 30 种")
        identifiers = [c["id"] for c in charts]
        if len(set(identifiers)) != len(identifiers):
            err("专业图表 ID 重复")
        required = ["id", "name_zh", "name_en", "family", "question",
                    "fields", "encoding", "interaction", "annotation",
                    "risk", "renderers", "demo", "evidence_status"]
        for c in charts:
            missing = [x for x in required if x not in c]
            if missing:
                err(f"专业图表字段缺失：{c.get('id')}，{missing}")
            if c.get("evidence_status") != "independent-professional-extension":
                err(f"图表来源状态不可冒充原站：{c.get('id')}")
        demo_count = sum(bool(c.get("demo")) for c in charts)
        if demo_count < 15:
            err("已登记 SVG 演示少于 15 种")
    except (ValueError, OSError, KeyError, TypeError) as exc:
        err(f"无法读取专业图表目录：{exc}")
    for extra in ["charts/README.md", "assets/pro-chart-gallery.html",
                  "references/07-专业图表图谱.md",
                  "references/08-图形工程契约.md",
                  "references/09-原模板核验记录.md",
                  "references/10-图表计算配方.md"]:
        if not (ROOT / extra).is_file():
            err(f"缺少 v1.1 资源：{extra}")

    if not (ROOT / "assets" / "editorial-demo.html").is_file():
        err("缺少 HTML 演示文件")

    if errors:
        for e in errors:
            print("错误：", e)
        raise SystemExit(1)
    print(f"校验通过：{len(seen_ids)} 个已登记模板，{len(registry.get('reserved_slots', []))} 个预留槽位，主 Skill 与参考文件完整。")


if __name__ == "__main__":
    main()
