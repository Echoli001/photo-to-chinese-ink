#!/usr/bin/env python3
"""
根据诊断卡里的 subject_category，从 subject_routing_table.json 查出
main_route / aux_route / rejected_routes。

这是确定性逻辑：同样的诊断卡输入，永远得到同样的路由输出。查不到、或
者查到的类目内容还没填（main_route 为 null），一律明确报告"待补充"，
不猜一个看起来合理的路线糊弄过去——这条原则见 SKILL.md 和
references/04-subject-routing-table.md。

用法：
    python router.py --diagnosis <diagnosis.json> \
        --routing-table <subject_routing_table.json> \
        [--out <routing.json>]

若不传 --out，结果打印到 stdout。
"""
import argparse
import json
import sys
from pathlib import Path


def load_json(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def route(diagnosis: dict, table: dict) -> dict:
    subject = diagnosis.get("subject_category")
    categories = table.get("categories", {})

    if not subject or subject == "other":
        return {
            "status": "unresolved",
            "reason": (
                "诊断卡里的 subject_category 缺失或标记为 other，"
                "无法在路由表里匹配到任何类目。"
            ),
            "subject_category": subject,
            "main_route": None,
            "aux_route": None,
            "rejected_routes": [],
        }

    entry = categories.get(subject)
    if entry is None:
        known = ", ".join(sorted(categories.keys()))
        return {
            "status": "unknown_category",
            "reason": (
                f"subject_category '{subject}' 不在路由表已知的 13 个类目里。"
                f"已知类目: {known}"
            ),
            "subject_category": subject,
            "main_route": None,
            "aux_route": None,
            "rejected_routes": [],
        }

    if entry.get("main_route") is None:
        return {
            "status": "incomplete",
            "reason": (
                f"类目 '{subject}'（{entry.get('label', subject)}）在路由表里"
                "还没有填 main_route，内容待从 v17 拆入。"
                "见 references/04-subject-routing-table.md 的 TODO。"
            ),
            "subject_category": subject,
            "main_route": None,
            "aux_route": None,
            "rejected_routes": entry.get("rejected_routes", []),
        }

    return {
        "status": "ok",
        "subject_category": subject,
        "label": entry.get("label", subject),
        "main_route": entry["main_route"],
        "aux_route": entry.get("aux_route"),
        "rejected_routes": entry.get("rejected_routes", []),
        "point_line_plane": entry.get("point_line_plane"),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--diagnosis", required=True, help="诊断卡 JSON 文件路径")
    parser.add_argument(
        "--routing-table", required=True, help="subject_routing_table.json 路径"
    )
    parser.add_argument("--out", help="输出路由 JSON 的文件路径（不传则打印到 stdout）")
    args = parser.parse_args()

    diagnosis = load_json(args.diagnosis)
    table = load_json(args.routing_table)

    result = route(diagnosis, table)
    output_text = json.dumps(result, ensure_ascii=False, indent=2)

    if args.out:
        Path(args.out).write_text(output_text, encoding="utf-8")
    else:
        # Windows 终端默认代码页（cp1252/gbk）打印中文会报 UnicodeEncodeError，
        # 显式重定向到 utf-8 输出，避免脚本在没传 --out 时直接崩溃。
        sys.stdout.reconfigure(encoding="utf-8")
        print(output_text)

    # status 不是 ok 时用非零退出码提醒调用方（模型/脚本调用者）需要人工介入，
    # 而不是让流程静默往下走。
    return 0 if result["status"] == "ok" else 1


if __name__ == "__main__":
    sys.exit(main())
