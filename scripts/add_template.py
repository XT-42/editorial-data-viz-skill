#!/usr/bin/env python3
"""创建新的可扩展可视化风格模板：标准库、无需 pip 安装。"""
from __future__ import annotations
import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "templates" / "registry.json"


def write_json(path: Path, value: dict) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def next_id(registry: dict) -> str:
    reserved = registry.get("reserved_slots", [])
    if reserved:
        return reserved.pop(0)
    nums = [int(x["id"][1:]) for x in registry["templates"] if re.fullmatch(r"T\d+", x["id"])]
    return f"T{max(nums, default=0)+1:03d}"


def main() -> None:
    p = argparse.ArgumentParser(description="给 editorial-data-viz Skill 新增模板")
    p.add_argument("--slug", required=True, help="英文小写、数字、短横线组成的唯一标识")
    p.add_argument("--name", required=True, help="模板中文显示名")
    p.add_argument("--source", default="", help="参考网页或资料链接，可留空")
    p.add_argument("--description", default="", help="本模板与已有模板的主要区别")
    p.add_argument("--aliases", default="", help="可选，逗号分隔别名")
    args = p.parse_args()

    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", args.slug):
        p.error("--slug 只支持小写字母、数字、短横线，首尾不能有短横线")
    if not args.name.strip():
        p.error("--name 不可为空")
    folder = ROOT / "templates" / args.slug
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    slugs = {v["slug"] for v in registry["templates"]}
    if args.slug in slugs or folder.exists():
        p.error(f"模板标识已存在：{args.slug}")

    aliases = [s.strip() for s in args.aliases.split(",") if s.strip()]
    known_aliases = {item.lower() for v in registry["templates"] for item in [v["slug"], v["name"], *v.get("aliases", [])]}
    if args.name.lower() in known_aliases or any(a.lower() in known_aliases for a in aliases):
        p.error("模板名称或别名与已有模板冲突")
    if len({a.lower() for a in aliases}) != len(aliases):
        p.error("本次 aliases 中出现了重复值")

    new_id = next_id(registry)
    base = ROOT / "templates" / "_template-blueprint"
    template = json.loads((base / "template.json").read_text(encoding="utf-8"))
    template.update({
        "id": new_id,
        "slug": args.slug,
        "name": args.name,
        "aliases": aliases,
        "status": "draft",
        "evidence_status": "user-specified",
        "source_url": args.source,
        "description": args.description,
        "verification_notes": ["未核验来源视觉。请根据截图或获准的源码完善 STYLE.md"]
    })
    # 如果没有原始网页，就避免把空白来源误写成“实测”。
    folder.mkdir(parents=True)
    write_json(folder / "template.json", template)
    style = (base / "STYLE.md").read_text(encoding="utf-8").replace("# 模板名（请在新增时替换）", f"# {new_id}｜{args.name}")
    style = style.replace("- 来源链接或用户上传的素材：待填写", f"- 来源链接或用户上传的素材：{args.source or '待提供'}")
    style += f"\n## 新增时记录的定位\n- {args.description or '待补充'}\n"
    (folder / "STYLE.md").write_text(style, encoding="utf-8")
    registry["templates"].append({
        "id": new_id, "slug": args.slug, "name": args.name, "aliases": aliases,
        "status": "draft", "evidence_status": "user-specified",
        "path": f"templates/{args.slug}", "source_url": args.source
    })
    existing = {v["id"] for v in registry["templates"]} | set(registry["reserved_slots"])
    max_num = max(int(v[1:]) for v in existing)
    while len(registry["reserved_slots"]) < 3:
        max_num += 1
        registry["reserved_slots"].append(f"T{max_num:03d}")
    write_json(REGISTRY, registry)
    print(f"新增成功：{new_id} → {folder.relative_to(ROOT)}")
    print("下一步：填写 STYLE.md 和 template.json；核验后将 status 改为 active。")


if __name__ == "__main__":
    main()
