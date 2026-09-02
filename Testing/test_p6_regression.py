"""
P6 回归测试套件（自动化版）。

背景：P6 阶段曾对 29 张测试图片做过一轮手动诊断卡 → router.py → compiler.py
验证，过程中发现并修复了 3 个真实 bug（见下方三个 pinned 测试的说明）。当时
只有一张诊断卡（水乡1.jpeg）落盘保存，其余验证结果没有留下可重跑的痕迹。

本文件把那次手动验证变成可重复执行的 pytest 套件：
- Testing/fixtures/*.json 是为全部 29 张测试图片手写的诊断卡（覆盖
  subject_routing_table.json 里全部 13 个 subject_category 取值），
  对每一张都跑一遍 router.py -> compiler.py，断言两步都成功产出
  status="ok" 的结果。
- 另外 3 个测试分别钉死当时修复的 3 个具体 bug 对应的正确行为，防止
  未来的改动在不知不觉中把它们改回错误状态（回归）。

运行方式：
    cd Testing
    python -m pytest test_p6_regression.py -v

（需要先 `pip install pytest`；仓库根目录运行也可以，用
`python -m pytest Testing/test_p6_regression.py -v`。）

注意：three 对文件名相同、扩展名不同的照片对（乱花2.jpeg/.jpg、
都市白天.jpeg/.jpg、渔港3.jpeg/.jpg）是两张不同的图，对应的 fixture 文件名
在 basename 后追加了扩展名（不带点）以避免互相覆盖，例如
`都市白天jpeg.json` / `都市白天jpg.json`。
"""
import importlib.util
import json
import sys
from pathlib import Path

import pytest

TESTING_DIR = Path(__file__).resolve().parent
REPO_ROOT = TESTING_DIR.parent
SCRIPTS_DIR = REPO_ROOT / ".claude" / "skills" / "wu-guanzhong-ink" / "scripts"
FIXTURES_DIR = TESTING_DIR / "fixtures"
ROUTING_TABLE_PATH = SCRIPTS_DIR / "data" / "subject_routing_table.json"


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


router = _load_module("wgz_router", SCRIPTS_DIR / "router.py")
compiler = _load_module("wgz_compiler", SCRIPTS_DIR / "compiler.py")

with open(ROUTING_TABLE_PATH, "r", encoding="utf-8") as f:
    ROUTING_TABLE = json.load(f)


def _load_diagnosis(fixture_path: Path) -> dict:
    with open(fixture_path, "r", encoding="utf-8") as f:
        return json.load(f)


def _route_and_compile(fixture_path: Path):
    diagnosis = _load_diagnosis(fixture_path)
    routing_result = router.route(diagnosis, ROUTING_TABLE)
    compile_result = compiler.compile_prompt(diagnosis, routing_result)
    return diagnosis, routing_result, compile_result


FIXTURE_PATHS = sorted(FIXTURES_DIR.glob("*.json"))


# ---------------------------------------------------------------------------
# 全量覆盖：29 张测试图片对应的诊断卡都要能顺利跑通 router -> compiler。
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("fixture_path", FIXTURE_PATHS, ids=lambda p: p.stem)
def test_fixture_routes_and_compiles_ok(fixture_path: Path):
    diagnosis, routing_result, compile_result = _route_and_compile(fixture_path)

    assert routing_result["status"] == "ok", (
        f"{fixture_path.name}: router.py 未返回 status=ok，"
        f"reason={routing_result.get('reason')!r}"
    )
    assert compile_result["status"] == "ok", (
        f"{fixture_path.name}: compiler.py 未返回 status=ok，"
        f"reason={compile_result.get('reason')!r}"
    )
    assert isinstance(compile_result.get("prompt"), str)
    assert compile_result["prompt"].strip() != ""


def test_all_29_fixtures_present():
    """确认 fixtures 目录覆盖了全部 29 张 Testing/ 下的测试图片。"""
    assert len(FIXTURE_PATHS) == 29


def test_all_13_subject_categories_covered():
    """确认 fixtures 覆盖了 subject_routing_table.json 里全部 13 个题材类目。"""
    categories = {
        _load_diagnosis(p).get("subject_category") for p in FIXTURE_PATHS
    }
    assert categories == set(ROUTING_TABLE["categories"].keys())


# ---------------------------------------------------------------------------
# Pinned 回归测试 1：黑名单误伤 bug。
#
# M1 是逐字引用的固定文本，本身合法地包含 "not watercolor" /
# "no watercolor postcard"（用来告诉模型"不要画成水彩画"）。M12 自查
# 曾经错误地把 M1 这类固定文本也纳入黑名单扫描范围，导致任何走到 M1 的
# 诊断卡都会被 "水彩|watercolor" 规则误判为命中黑名单而拦截。
#
# 修复后，compile_prompt() 只把 dynamic_paragraphs（M2/M3b/M4/M5/M6/M8/
# M9b/M10 这些拼装模板内容）送去过黑名单，不会扫描 M1/M3/M7/M9/M11 这些
# 逐字引用文本。用一张能正常走到 M1（所有诊断卡都会走到，因为 M1 是
# paragraphs 的第一段固定文本）的水乡诊断卡验证：只要 compile 仍然返回
# status=ok，就说明黑名单没有被 M1 的合法否定式表达误伤。
# ---------------------------------------------------------------------------
def test_m1_watercolor_negation_does_not_trip_blacklist():
    fixture_path = FIXTURES_DIR / "水乡1.json"
    diagnosis, routing_result, compile_result = _route_and_compile(fixture_path)

    assert routing_result["status"] == "ok"
    assert compile_result["status"] == "ok", (
        "M1 固定文本里的 'not watercolor' / 'no watercolor postcard' 不应该被 "
        "M12 黑名单自查误判——它只应该扫描 dynamic_paragraphs，不应该扫描 M1 这类"
        f"逐字引用的固定文本。实际 reason={compile_result.get('reason')!r}"
    )
    assert "Chinese ink on highly absorbent raw xuan paper, not watercolor" in compile_result["prompt"]


# ---------------------------------------------------------------------------
# Pinned 回归测试 2：M5（平面空间构成叠加层）必须由诊断卡的
# plane_composition.activation_reason / subject_route 权威字段触发，而不是
# 靠"这个题材看起来像鸟瞰"这种基于 subject_category 的启发式猜测。
#
# 用渔港1.json（真实的航拍视角渔港照片，diagnosis 里显式填了
# plane_composition={"activation_reason": "aerial_view", "subject_route":
# "fishing_harbor"}）验证：编译结果里包含 M5 的固定英文措辞
# "Overlay a flat spatial composition treatment"，并且 notes 里明确记录了
# "subject_route 直接取自诊断卡 plane_composition.subject_route="，
# 证明触发来源是诊断卡的权威字段，而不是兜底的 subject_category 猜测路径。
# ---------------------------------------------------------------------------
def test_m5_triggered_by_authoritative_plane_composition_field():
    fixture_path = FIXTURES_DIR / "渔港1.json"
    diagnosis, routing_result, compile_result = _route_and_compile(fixture_path)

    assert diagnosis["plane_composition"]["activation_reason"] == "aerial_view"
    assert routing_result["status"] == "ok"
    assert compile_result["status"] == "ok"

    prompt = compile_result["prompt"]
    assert "Overlay a flat spatial composition treatment" in prompt

    notes = compile_result.get("notes", [])
    subject_route = diagnosis["plane_composition"]["subject_route"]
    expected_note_fragment = (
        f"M5：subject_route 直接取自诊断卡 plane_composition.subject_route='{subject_route}'。"
    )
    assert any(expected_note_fragment in note for note in notes), (
        "M5 应该记录 subject_route 是直接取自诊断卡的 plane_composition.subject_route 字段"
        "（权威信号），而不是从 subject_category 猜出来的兜底值。"
        f"实际 notes={notes!r}"
    )


# ---------------------------------------------------------------------------
# Pinned 回归测试 3：abstract_line_network 的 M10 自我误伤 bug。
#
# abstract_line_network 题材的 M10 组装文本里，main.ink_block_handling
# 合法地包含 "...do not add new ink mass or recompose the image."（"不要
# ...或重新构图"）。该题材的 rejected_keywords 用负向后顾断言
# `(?<!or )recompose` 排除"or recompose"这种合法搭配，只在"recompose"前面
# 不是"or "时才判定命中。如果这条正则写错（比如误伤 "or recompose"），
# M10 会把自己组装出的合法句子当成命中黑名单，调用
# notes.append("M10：组装出的句子疑似命中该题材的 rejected_routes 关键词
# 模式...") 后跳过整个 M10 模块。
#
# 用 abstract_line_network1.json / abstract_line_network2.json 两张诊断卡
# 验证：编译结果里既不出现这条自我误伤的 note，M10 对应的 "Ink-block
# handling:" 句子也确实出现在最终 prompt 里（证明 M10 没有被跳过）。
# ---------------------------------------------------------------------------
@pytest.mark.parametrize(
    "fixture_name", ["abstract_line_network1.json", "abstract_line_network2.json"]
)
def test_abstract_line_network_m10_not_self_suppressed(fixture_name: str):
    fixture_path = FIXTURES_DIR / fixture_name
    diagnosis, routing_result, compile_result = _route_and_compile(fixture_path)

    assert routing_result["status"] == "ok"
    assert compile_result["status"] == "ok"

    notes = compile_result.get("notes", [])
    for note in notes:
        assert "M10：组装出的句子疑似命中该题材的 rejected_routes 关键词模式" not in note, (
            f"{fixture_name}: M10 不应该把自己组装出的合法句子 "
            "('...or recompose the image.') 误判为命中 rejected_keywords 而跳过。"
            f"实际命中的 note={note!r}"
        )

    assert "Ink-block handling: Use low intervention" in compile_result["prompt"], (
        f"{fixture_name}: M10 应该正常输出该题材的专属规则句子，不应该因为自我误伤而被跳过。"
    )
