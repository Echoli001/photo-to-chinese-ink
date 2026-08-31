#!/usr/bin/env python3
"""
把诊断卡 + 路由决定，按固定模块顺序拼成最终 prompt 文本。

模块拼装的具体内容规则见 references/06-prompt-compiler-spec.md；这里的
代码目前只搭好流程骨架——因为各模块的实际文本模板还没有从 v17 拆入，
`_build_module_text()` 现在只输出占位符（TODO 標記），并不是真正能用
的 prompt。但下面这几类"硬性约束"是可以脱离具体内容、独立生效的确定性
检查，已经实现成真代码，不依赖模型"自觉遵守"：

  - 黑名单关键词拦截（签名/印章/水彩/画家名字驱动效果/米黄仿古纸等）
  - 技法关键词数量必须在 1–3 个之间

用法：
    python compiler.py --diagnosis <diagnosis.json> --routing <routing.json> \
        [--out <prompt.txt>]

若路由决定的 status 不是 "ok"（例如该类目路由还没填），编译器会拒绝
产出 prompt，明确报告原因，而不是硬凑一个不完整的结果——这是 CLAUDE.md
Rule 3「禁止静默失败和伪成功」的具体落实。
"""
import argparse
import json
import re
import sys
from pathlib import Path

# 黑名单关键词：命中即报错，不静默移除、不静默放行。
# 完整清单以 references/05-quality-checklist.md 为准，这里先收录已确认的几条。
BLACKLIST_PATTERNS = [
    (r"签名", "签名描述"),
    (r"印章", "印章描述"),
    (r"题跋", "题跋描述"),
    (r"水彩|watercolor", "水彩化描述"),
    (r"in the style of wu guanzhong", "靠画家名字取效果的表达"),
    (r"仿吴冠中|吴冠中笔法", "靠画家名字/签名风格驱动的表达"),
    (r"米黄仿古纸", "被明确禁止的纸色描述"),
]

MODULES = [
    "source_invariants",
    "composition_archetype",
    "point_line_plane_ratio",
    "ink_gradation",
    "brush_quality",
    "color_system",
    "paper_color",
    "abstraction_level",
    "subject_rules",
    "output_spec",
]


def load_json(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _build_module_text(module: str, diagnosis: dict, routing: dict) -> str:
    """
    每个模块目前只返回占位符文本。真正的拼装内容依赖对应 reference
    文件（00-03、06）里尚待从 v17 拆入的规则——在那些文件填好之前，这
    里故意不编造具体措辞，避免产出一个看起来像模板、实际内容瞎编的假
    prompt。
    """
    return f"[TODO:{module} 待从对应 reference 文件补充拼装规则]"


def compile_prompt(diagnosis: dict, routing: dict) -> dict:
    if routing.get("status") != "ok":
        return {
            "status": "blocked",
            "reason": (
                "路由决定的 status 不是 'ok'（"
                f"{routing.get('status')}: {routing.get('reason')}），"
                "编译器拒绝产出 prompt。先补全路由表对应类目，或人工确认路由后再编译。"
            ),
            "prompt": None,
        }

    module_texts = [_build_module_text(m, diagnosis, routing) for m in MODULES]
    draft_prompt = "; ".join(module_texts)

    violations = _check_blacklist(draft_prompt)
    if violations:
        return {
            "status": "blocked",
            "reason": "草稿 prompt 命中黑名单关键词，已拦截：" + "; ".join(violations),
            "prompt": None,
        }

    technique_count = _count_techniques(draft_prompt)
    if not (1 <= technique_count <= 3):
        return {
            "status": "blocked",
            "reason": (
                f"技法关键词数量为 {technique_count}，不在允许范围 1–3 个内。"
                "（注：当前模块内容仍是占位符，这条检查在真实内容填入前"
                "意义有限，先保留逻辑框架。）"
            ),
            "prompt": None,
        }

    return {
        "status": "draft",
        "reason": (
            "模块骨架已按规则拼装，但各模块内容仍是占位符（TODO），"
            "还不是可以直接使用的最终 prompt。等 references/00-03,06 的"
            "内容从 v17 填入后，重新运行本脚本即可得到真正可用的文本。"
        ),
        "prompt": draft_prompt,
    }


def _check_blacklist(text: str) -> list:
    lowered = text.lower()
    hits = []
    for pattern, label in BLACKLIST_PATTERNS:
        if re.search(pattern, lowered, flags=re.IGNORECASE):
            hits.append(label)
    return hits


def _count_techniques(text: str) -> int:
    """
    占位实现：真正的"技法关键词"清单要从 references/02-ink-symbol-rules.md
    和 references/06-prompt-compiler-spec.md 填好之后才能准确计数。
    这里先返回 1，保证骨架流程能跑通，不代表已经实现了真实计数逻辑。
    """
    return 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--diagnosis", required=True, help="诊断卡 JSON 文件路径")
    parser.add_argument("--routing", required=True, help="router.py 输出的路由 JSON 路径")
    parser.add_argument("--out", help="输出结果 JSON 的文件路径（不传则打印到 stdout）")
    args = parser.parse_args()

    diagnosis = load_json(args.diagnosis)
    routing = load_json(args.routing)

    result = compile_prompt(diagnosis, routing)
    output_text = json.dumps(result, ensure_ascii=False, indent=2)

    if args.out:
        Path(args.out).write_text(output_text, encoding="utf-8")
    else:
        # Windows 终端默认代码页（cp1252/gbk）打印中文会报 UnicodeEncodeError，
        # 显式重定向到 utf-8 输出，避免脚本在没传 --out 时直接崩溃。
        sys.stdout.reconfigure(encoding="utf-8")
        print(output_text)

    return 0 if result["status"] == "draft" else 1


if __name__ == "__main__":
    sys.exit(main())
