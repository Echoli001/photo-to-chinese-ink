#!/usr/bin/env python3
"""
把诊断卡 + 路由决定，按 references/06-prompt-compiler-spec.md 定义的
固定模块顺序（M1-M11，M12 是代码层面的硬性检查，不是可见文本）拼成
最终英文 prompt，外加一段中文说明。

模块的"逐字引用"文本（M1/M3/M7/M9/M11）直接照抄 06 的原文，一个字不
改；"拼装模板"模块（M2/M4/M5/M6/M8/M9 的 palette 行/M10）按诊断卡和
路由结果的实际值组装。任何模块因为诊断字段是 unknown/缺失而无法组装
时，直接跳过该模块，并在中文说明里注明——不编造内容顶上去
（CLAUDE.md Rule 3：禁止静默失败和伪成功）。

用法：
    python compiler.py --diagnosis <diagnosis.json> --routing <routing.json> \
        [--out <result.json>]
"""
import argparse
import json
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# M12. 硬性禁止项黑名单（06 第 325-356 行，源自 05-quality-checklist.md）
# 命中即报错，不静默移除、不静默放行。
# ---------------------------------------------------------------------------
BLACKLIST_PATTERNS = [
    (r"签名", "签名描述"),
    (r"印章", "印章描述"),
    (r"题跋", "题跋描述"),
    (r"水彩|watercolor", "水彩化描述"),
    (r"in the style of wu guanzhong", "靠画家名字取效果的表达"),
    (r"仿吴冠中|吴冠中笔法", "靠画家名字/签名风格驱动的表达"),
    (r"米黄仿古纸", "被明确禁止的纸色描述"),
    (r"真迹|原作|官方授权", "误导性的“真迹/原作/官方授权”声称"),
    (r"双燕|狮子林|逍遥游", "把标志性作品名称直接当模板请求"),
]

MODULES = [
    "M1_ink_material_base",
    "M2_paper_color",
    "M3_ink_symbol_translation",
    "M3b_abstraction_tier",
    "M4_composition_archetype",
    "M5_flat_spatial_overlay",
    "M6_point_line_plane_ratio",
    "M7_positive_irregularity",
    "M8_deformation_techniques",
    "M9_color_system",
    "M10_subject_rules",
    "M11_negative_prompt",
]

# ---------------------------------------------------------------------------
# M1. 墨材质基座 — 全局强制，逐字引用（06 第 47-63 行）
# ---------------------------------------------------------------------------
M1_TEXT = (
    "Chinese ink on highly absorbent raw xuan paper, not watercolor. Build the image from "
    "reserved paper white, concentrated wet ink cores, heavy middle-ink bodies, pale wet "
    "breathing layers, and dry charred bone strokes. Treat ink concentration and brush "
    "moisture as independent variables. Let wet ink pool, backflow, collide and feather "
    "unevenly into the fibers; let dry ink drag, split, skip and expose flying-white bristle "
    "gaps. Every major ink mass must contain internal tonal migration and at least two ink "
    "states. Use layered ink, broken ink and selective water intervention, not uniform "
    "transparent color washes. Color remains subordinate to the black-gray-white ink "
    "structure and appears as sparse opaque, scraped or ink-mixed events. No smooth digital "
    "gradients, no identical soft edges, no global paper-noise overlay, no watercolor postcard."
)

# ---------------------------------------------------------------------------
# M2. 纸色声明 — 全局强制，条件拼装（06 第 65-99 行）
# ---------------------------------------------------------------------------
M2_WHITE_TEXT = (
    "Use clean white highly absorbent raw xuan paper. The paper is white, fresh and "
    "unaged—not beige, cream, sepia or antique parchment. Keep most of the sheet quiet "
    "and nearly texture-free; reveal subtle fibers only where wet ink feathers or dry "
    "brush drags across them. Carry all environmental warmth in the ink-mixed color, "
    "mineral pigment or scraped opaque passages, never by yellowing the entire paper. "
    "No global paper texture, brown mottling, stains, deckled dark edges or vintage filter."
)
WHITE_FAMILY = ("clean_white", "cool_white", "neutral_white", "natural_white")
WARM_FAMILY = ("warm_ivory", "antique_beige", "antique_cream")  # antique_cream: 07 的措辞，等同 06 的 antique_beige
WARM_LABEL = {"warm_ivory": "warm ivory", "antique_beige": "antique beige", "antique_cream": "antique beige"}
WHITE_DEFAULT_ORDER = ["clean_white", "neutral_white", "cool_white", "natural_white"]


def _build_m2_paper_color(diagnosis, notes):
    ink_material = diagnosis.get("ink_material", {}) or {}
    router = ink_material.get("paper_color_router")

    if not router:
        notes.append("M2（纸色声明）跳过：diagnosis.ink_material.paper_color_router 缺失/unknown。")
        return None

    if router in WHITE_FAMILY:
        return M2_WHITE_TEXT

    if router in WARM_FAMILY:
        justification = ink_material.get("paper_color_justification")
        if not justification:
            notes.append(
                f"M2：诊断卡选择了暖纸 '{router}' 但没有给出具体理由"
                "（ink_material.paper_color_justification 缺失），"
                f"按硬性检查规则回退到白纸默认档 '{WHITE_DEFAULT_ORDER[0]}'，不静默用暖纸顶上去。"
            )
            return M2_WHITE_TEXT
        label = WARM_LABEL.get(router, router)
        notes.append(f"M2：本图使用 {label} 纸色（拼装模板，非 v17 逐字），理由：{justification}")
        return (
            f"Use {label} raw xuan paper, justified specifically by "
            f"{justification}, not by subject convention. "
            "Keep the warmth confined to the paper base tone; do not add artificial aging "
            "texture, stains, foxing or a vintage-scan filter on top of it."
        )

    notes.append(f"M2（纸色声明）跳过：paper_color_router 值 '{router}' 不在已知的 6 档枚举里。")
    return None


# ---------------------------------------------------------------------------
# M3. 墨符号翻译 — 全局强制，逐字引用（06 第 101-118 行）
# ---------------------------------------------------------------------------
M3_TEXT = (
    "Translate the source first into autonomous but source-derived ink symbols: ink points, "
    "ink lines, ink planes and paper-negative space, established in black-gray-white before "
    "any color is added. Let each symbol's form deviate roughly 10-25% from the literal "
    "source silhouette rather than tracing exact object boundaries. Vary concentration and "
    "moisture within each symbol group—mix charred, wet and pale states inside the same "
    "cluster of points, along the same line, across the same plane. Introduce 1-3 moments "
    "where a saturated color event juxtaposes, cuts, interlocks with, or opaquely overprints "
    "the ink structure, always anchored to a source-derived node or focal point. Never pour "
    "color inside a closed black outline like a coloring book. The black-gray-white ink "
    "skeleton must remain legible and structurally self-sufficient even if the color were "
    "removed."
)

# 抽象化程度（06 第 304-323 行）：target_abstraction_tier 是整图目标，
# 影响 M1/M3/M7 的措辞；这里作为紧跟 M3 之后的独立拼装句子追加，
# 不改动 M1/M3/M7 本身的逐字文本。
ABSTRACTION_TIER_RANGE = {"A": "70-85", "B": "45-70", "C": "20-45"}


def _build_m3b_abstraction(diagnosis, notes):
    tier = diagnosis.get("target_abstraction_tier", "B")
    rng = ABSTRACTION_TIER_RANGE.get(tier)
    if not rng:
        notes.append(f"M3b（抽象化程度）跳过：target_abstraction_tier 值 '{tier}' 不在 A/B/C 枚举里。")
        return None
    return f"For this piece, keep overall recognizability of the source subject around {rng}%."


# ---------------------------------------------------------------------------
# M4. 构图原型 — 拼装模板（06 第 120-148 行）
# ---------------------------------------------------------------------------
COMPOSITION_MODE_PHRASE = {
    "jiangnan_geometry": (
        "a Jiangnan geometric composition, where large white walls or water surfaces "
        "(roughly 45-70% of the frame) and dark-tile, window and bridge accents form the "
        "geometric structure of the image, with space allowed to flatten and perspective "
        "not strictly unified"
    ),
    "monumental_void": (
        "a monumental-void composition, anchored by a single vertical or diagonal mass "
        "(a tree, peak, figure or building) not necessarily centered, with a high reserved "
        "negative-space ratio (roughly 55-75%) and a few concentrated ink masses locking "
        "down the visual weight"
    ),
    "panoramic_flow": (
        "a panoramic-flow composition, using a wide horizontal format where a riverbank, "
        "road, ridge or building band forms a continuous curve carrying the eye across the "
        "frame, with no single central focal point"
    ),
    "immersive_network": (
        "an immersive-network composition, where lines, ink dots and gray traces cover most "
        "of the frame so the viewer feels immersed inside the scene rather than viewing it "
        "from a distance, with clear variation in thickness, density, direction and layering "
        "so it never reads as uniform noise"
    ),
    "urban_ink_volume": (
        "an urban ink-volume composition, treating the city as clusters of ink-color volumes "
        "of varying height, width and density—several adjacent buildings merged into a single "
        "volume—organized through overlap, interlock, offset and cropping, with an "
        "uneven-paced skyline rather than a flat, evenly notched one"
    ),
    "urban_grid_variation": (
        "an urban grid-variation composition for a night scene, where horizontal and vertical "
        "structural lines and light-point accents are reinforced without regressing into "
        "building-by-building line description"
    ),
}

# 13 类主体 -> composition_mode 默认映射（06 第 120-148 行的映射表）
SUBJECT_TO_COMPOSITION_MODE = {
    "terraced_field": "panoramic_flow",
    "mountain_snow": "monumental_void",
    "river_lake_reflection": "panoramic_flow",
    "forest_bamboo": "immersive_network",
    "flower_branch": "immersive_network",
    "flower_field": "panoramic_flow",
    "jiangnan_water_town": "jiangnan_geometry",
    "ancient_architecture": "jiangnan_geometry",  # aux: urban_ink_volume（墙体/台基为主时）
    "urban_day": "urban_ink_volume",
    "urban_night": "urban_grid_variation",
    "farmland_grid": "urban_grid_variation",
    "fishing_port": "urban_grid_variation",
    "abstract_line_network": "immersive_network",
}


def _build_m4_composition(diagnosis, routing, notes):
    mode = diagnosis.get("composition_mode")
    if not mode:
        subject = routing.get("subject_category")
        mode = SUBJECT_TO_COMPOSITION_MODE.get(subject)
        if mode:
            notes.append(f"M4：诊断卡未直接给 composition_mode，按主体 '{subject}' 的默认映射取 '{mode}'。")
    phrase = COMPOSITION_MODE_PHRASE.get(mode)
    if not phrase:
        notes.append(f"M4（构图原型）跳过：composition_mode 值 '{mode}' 无法解析出对应英文描述。")
        return None
    return f"State the composition archetype as {phrase}."


# ---------------------------------------------------------------------------
# M5. 平面空间构成叠加层 — 条件模块，not_global_default（06 第 150-178 行）
# ---------------------------------------------------------------------------
SUBJECT_ROUTE_TO_SUBJECT = {
    "seedling_field": "farmland_grid",
    "fishing_harbor": "fishing_port",
    "aerial_village": "jiangnan_water_town",  # 仅当 perspective=俯视
    "terrace_field": "terraced_field",
    "water_shore_fragments": "river_lake_reflection",  # 仅限鸟瞰/碎片化水岸
    "abstract_ink_block_landscape": None,  # 山体/风景类在强高角度/压平场景下的兜底路由
}
SUBJECT_TO_SUBJECT_ROUTE = {v: k for k, v in SUBJECT_ROUTE_TO_SUBJECT.items() if v}


def _flat_spatial_triggered(diagnosis):
    """
    触发条件（06 第 150-178 行；权威 schema 见 07-generation-protocol-yaml.md
    第 164-186 行 flat_spatial_composition_route）。诊断卡的权威信号是
    `plane_composition.activation_reason`（取值 high_angle | aerial_view |
    repeated_units | surface_mosaic | requested_flattening 之一，非空即视为
    触发）——这是模型在做诊断时直接选定的字段，优先级最高。如果诊断卡没填
    这张关联卡（例如比较简单的输入），才退回到 perspective 等弱信号兜底，
    避免因为模型没显式填卡就漏判。
    """
    plane = diagnosis.get("plane_composition")
    if isinstance(plane, dict) and plane.get("activation_reason"):
        return True
    explicit = diagnosis.get("flat_spatial_composition_route_triggered")
    if explicit is not None:
        return bool(explicit)
    perspective = diagnosis.get("perspective", "")
    if perspective in ("俯视", "鸟瞰", "高角度", "aerial", "high_angle", "bird's-eye"):
        return True
    return bool(diagnosis.get("repeated_surface_units_are_primary"))


def _build_m5_flat_spatial(diagnosis, routing, notes):
    if not _flat_spatial_triggered(diagnosis):
        return None

    plane = diagnosis.get("plane_composition")
    subject_route = plane.get("subject_route") if isinstance(plane, dict) else None
    if subject_route:
        notes.append(f"M5：subject_route 直接取自诊断卡 plane_composition.subject_route='{subject_route}'。")
    else:
        subject = routing.get("subject_category")
        perspective = diagnosis.get("perspective", "")
        subject_route = SUBJECT_TO_SUBJECT_ROUTE.get(subject)

        if subject_route == "aerial_village" and perspective not in ("俯视", "鸟瞰", "aerial", "high_angle", "bird's-eye"):
            notes.append("M5：主体是江南水乡但视角是平视，不满足 aerial_village 子触发条件，不叠加该层。")
            return None

        if not subject_route:
            subject_route = "abstract_ink_block_landscape"
            notes.append(f"M5：主体 '{subject}' 没有直接对应的 subject_route，按兜底规则用 'abstract_ink_block_landscape'。")
        else:
            notes.append(f"M5：诊断卡未填 plane_composition.subject_route，按主体 '{subject}' 的默认映射取 '{subject_route}'。")

    notes.append(
        f"M5（平面空间构成叠加层）已触发：subject_route='{subject_route}'，"
        "not_global_default——不是因为题材像鸟瞰就默认套用，而是诊断卡明确判断了俯视/重复面群主导。"
    )
    return (
        "Overlay a flat spatial composition treatment: adopt a high-angle or aerial-like "
        "viewpoint but cancel a single converging vanishing point. Flatten the three-dimensional "
        "scene into two-dimensional units first, then reorganize them through overlap, density, "
        "ink-tone steps, unit-scale variation and paper-white gaps—governed by the flat picture "
        "plane, not realistic depth. Do not rely on near-large-far-small scaling, realistic "
        "light and shadow, or atmospheric perspective; ink tone, not front-to-back placement, "
        "should carry the compositional weight. Select at least three depth substitutes such as "
        "density shifts, ink-tone steps, unit-scale variation, overlap or see-through layering, "
        "differing edge clarity, paper-white channel width, or directional conflict. Do not make "
        "every unit the same size like stickers, and do not turn the aerial view into a tidy "
        "infographic grid."
    )


# ---------------------------------------------------------------------------
# M6. 点/线/面配比声明 — 拼装模板（06 第 180-195 行）
# 优先取诊断卡的 point_line_plane 判断（ordinal/数值），其次取路由表的
# 数值三元组参考值（v17 §7.1：诊断结论 > 主体路由）。
# ---------------------------------------------------------------------------
_TRIPLE_RE = re.compile(r"(\d+)\s*/\s*(\d+)\s*/\s*(\d+)")
_ORDINAL_WEIGHT = {"low": 1.0, "medium": 2.0, "high": 3.0}


def _parse_triple(value):
    if isinstance(value, dict):
        try:
            return float(value.get("point")), float(value.get("line")), float(value.get("plane"))
        except (TypeError, ValueError):
            pass
        # 00-source-diagnosis-card.md 里 point_line_plane_dependency 的 point/line/plane
        # 取值是 "low|medium|high" 序数词，不是数字——按序数权重折算成一个总和为 100 的百分比三元组。
        try:
            point_w = _ORDINAL_WEIGHT[str(value.get("point")).lower()]
            line_w = _ORDINAL_WEIGHT[str(value.get("line")).lower()]
            plane_w = _ORDINAL_WEIGHT[str(value.get("plane")).lower()]
        except KeyError:
            return None
        total = point_w + line_w + plane_w
        return (point_w / total * 100, line_w / total * 100, plane_w / total * 100)
    if isinstance(value, str):
        m = _TRIPLE_RE.search(value)
        if m:
            return float(m.group(1)), float(m.group(2)), float(m.group(3))
    return None


def _build_m6_point_line_plane(diagnosis, routing, notes):
    triple = _parse_triple(diagnosis.get("point_line_plane_dependency"))
    source = "diagnosis"
    if triple is None:
        triple = _parse_triple(routing.get("point_line_plane"))
        source = "routing"
    if triple is None:
        notes.append("M6（点/线/面配比）跳过：诊断卡和路由表都没有给出可解析的点/线/面数值。")
        return None

    point, line, plane = triple
    labels = [("point", point), ("line", line), ("plane", plane)]
    labels.sort(key=lambda x: x[1], reverse=True)
    dominant_name, dominant_pct = labels[0]
    secondary_names = " and ".join(n for n, _ in labels[1:])

    if source == "routing":
        notes.append("M6：诊断卡未给出点/线/面判断，回退用了路由表的参考数值三元组（次优先级，见 v17 §7.1）。")

    return (
        f"Let {dominant_name} carry roughly {dominant_pct:g}% of the visual weight as the "
        f"dominant language, with {secondary_names} playing supporting roles, not an equal "
        "three-way split."
    )


# ---------------------------------------------------------------------------
# M7. 正向不规则化 — 全局强制，逐字引用（06 第 197-211 行）
# ---------------------------------------------------------------------------
M7_TEXT = (
    "Do not trace the visible contours one by one. Instead, let the brush skip some edges, "
    "merge adjacent shapes, break a line mid-stroke, misalign neighboring elements, and "
    "suddenly shift density from sparse to crowded within the same passage. Let thick and "
    "thin strokes collide directly against each other. Insert one or two strokes that run "
    "against the dominant directional flow. Allow 1-3 controlled accidents—marks that read "
    "as spontaneous or slightly out of control. Keep negative space asymmetrical rather than "
    "evenly balanced. Let one or two color marks drift slightly off their expected position. "
    "Think of the line rhythm as wandering, rising, colliding, circling, falling, crowding, "
    "escaping or pausing—not as a mechanical outline-filling exercise."
)

# ---------------------------------------------------------------------------
# M8. 破形技法关键词选择 — 拼装模板，1-3 个硬性上限（06 第 213-232 行）
# 技法的“选择”属于诊断阶段（模型判断，Rule 8），compiler.py 只做数量/
# 枚举校验，并把选中的技法映射到 M7 句子池里对应的英文短语。
# ---------------------------------------------------------------------------
TECHNIQUE_PHRASES = {
    "删线": "skip some edges rather than tracing every contour",
    "并形": "merge adjacent shapes into a single silhouette",
    "断裂": "break a line mid-stroke rather than completing it continuously",
    "错位": "misalign neighboring elements instead of keeping them precisely aligned",
    "疏密突变": "shift density abruptly from sparse to crowded within the same passage",
    "粗细对撞": "let thick and thin strokes collide directly against each other",
    "方向反拍": "insert one or two strokes that run against the dominant directional flow",
    "偶发笔触": "allow one or two controlled accidents that read as spontaneous or slightly out of control",
    "非对称留白": "keep the negative space asymmetrical rather than evenly balanced",
    "彩点脱轨": "let one or two color marks drift slightly off their expected position",
}


def _get_selected_techniques(diagnosis):
    return (diagnosis.get("ink_symbol_composition", {}) or {}).get("selected_deformation_techniques", [])


def _build_m8_techniques(diagnosis, notes):
    techniques = _get_selected_techniques(diagnosis)
    unknown = [t for t in techniques if t not in TECHNIQUE_PHRASES]
    if unknown:
        notes.append(f"M8：诊断卡里的技法名称 {unknown} 不在已知的 10 项枚举里，已忽略，不编造映射。")
    valid = [t for t in techniques if t in TECHNIQUE_PHRASES]
    if not valid:
        notes.append("M8（破形技法）跳过：diagnosis.ink_symbol_composition.selected_deformation_techniques 为空或全部无效。")
        return None
    phrases = [TECHNIQUE_PHRASES[t] for t in valid]
    if len(phrases) == 1:
        body = phrases[0]
    else:
        body = "; ".join(phrases[:-1]) + f"; and {phrases[-1]}"
    return f"For this piece, specifically apply: {body}."


# ---------------------------------------------------------------------------
# M9. 色彩系统 — 全局强制，逐字引用 + 拼装模板（06 第 234-254 行）
# ---------------------------------------------------------------------------
M9_TEXT = (
    "Do not use the habitual coral-orange-blue-gray palette unless the source analysis "
    "selects it. First choose one palette mode from the color router. Preserve at most "
    "two meaningful source hues, then remap the rest by value, temperature and emotion. "
    "State one dominant chromatic family, one secondary family and zero to three accent "
    "hues. Treat primary colors as unequal rhythmic events rather than equal RGB dots. "
    "Vary which element carries color: points, broken short lines, translucent fragments "
    "or one small plane. Keep high-chroma coverage below the selected cap. Use pigment "
    "bleed, dilution, dry-brush loss and paper interruption so even vivid colors are not "
    "flat digital fills. Avoid repeating the palette signature of recent outputs."
)


def _build_m9_palette(diagnosis, notes):
    mode = (diagnosis.get("color") or {}).get("palette_mode") or diagnosis.get("palette_mode")
    if not mode:
        notes.append("M9：诊断卡未给出 palette_mode，色彩系统模块只输出通用规则，缺少具体选定色域声明。")
        return None
    return f"Selected palette mode: {mode}."


# ---------------------------------------------------------------------------
# M10. 题材专属规则 — 拼装模板（06 第 256-273 行）
# 13 类主体的 ink_block_handling/negative_space_ratio/texture_method 中文
# 原文（subject_routing_table.json）译成英文短语；rejected_routes 关键词
# 自查，命中则报错而不是照样输出。
# ---------------------------------------------------------------------------
SUBJECT_ROUTE_TRANSLATIONS = {
    "terraced_field": {
        "main": {
            "ink_block_handling": "Handle this primarily as line clusters with minimal ink blocks—place ink dots only as anchor accents where lines meet or turn, never as a solid wash covering the line network.",
            "negative_space_ratio": "Aim for a high negative-space ratio (roughly 65-85%): keep only about 15-35% of the repeated lines as a visible skeleton, omitting the rest rather than tracing every unit.",
            "texture_method": "Render line texture with dry-brush short strokes, using flying-white breaks at turns and stop points, not fine contour-by-contour gongbi-style rendering.",
        },
        "rejected_keywords": [r"逐线临摹|line by line", r"整块泼墨|solid ink wash"],
    },
    "mountain_snow": {
        "main": {
            "ink_block_handling": "Build mass with a solid ink core reinforced by layered, accumulated ink, giving the mountain or snow body real weight.",
            "negative_space_ratio": "Use a moderate negative-space ratio (roughly 50-70%): let snow surfaces or mist carry most of the reserved white, with ink coverage higher than in line-dominant subjects.",
            "texture_method": "Use charred dry-brush strokes to articulate ridge and rock-edge structural turns, with dry-brush scumbling across shadow transitions on the mountain body.",
        },
        "rejected_keywords": [r"只勾轮廓|outline only"],
    },
    "river_lake_reflection": {
        "main": {
            "ink_block_handling": "Layer water first, then ink; render reflections with tilted, skewed ink blocks that distort the mirrored building or mountain shapes rather than copying their outlines directly.",
            "negative_space_ratio": "Use a fairly high negative-space ratio (roughly 55-75%, the general baseline): let the water surface itself serve as a large reserved-white area.",
            "texture_method": "Use undulating water-lines for ripples and reflection texture, with broken accent dots at the reflection boundary to disrupt an overly tidy mirror effect.",
        },
        "rejected_keywords": [r"镜像复制|mirrored copy"],
    },
    "forest_bamboo": {
        "main": {
            "ink_block_handling": "Use small accumulated-ink accents only where canopy or foliage is densest, with no solid ink wash that would swallow the line network.",
            "negative_space_ratio": "Use a moderately high negative-space ratio (roughly 55-75%, general baseline): let the gaps between trunks and branches define the reserved-white channels.",
            "texture_method": "Use charred dry-brush strokes for trunk structure, with short texture strokes and flying-white for bark and foliage.",
        },
        "rejected_keywords": [r"整块墨面覆盖|solid ink mass"],
    },
    "flower_branch": {
        "main": {
            "ink_block_handling": "Mark growth-attachment points and blossoms with ink-color dots rather than solid ink planes; let ink blocks act only as node accents along the line path.",
            "negative_space_ratio": "Use a moderate negative-space ratio (roughly 55-75%, general baseline), varying locally with the density of the growth path.",
            "texture_method": "Use fine, thread-like lines for vines and branches, alternating black-line thrusts with gray-line rebounds to express a knot-release-reknot growth rhythm.",
        },
        "rejected_keywords": [r"整块墨团|solid ink mass or color block"],
    },
    "flower_field": {
        "main": {
            "ink_block_handling": "Express flower-cluster or light-spot density through gathering and scattering point clusters, not a solid color wash; distribute color and ink dots on a gather-scatter rhythm rather than filling evenly.",
            "negative_space_ratio": "Use a fairly high negative-space ratio (roughly 55-75%, general baseline): the gaps between point clusters are the main source of reserved white.",
            "texture_method": "Rely mainly on flying-white dotted color; texture method plays a secondary role here since points dominate (about 55%)—do not force a traditional texture stroke onto it.",
        },
        "aux": {
            "ink_block_handling": "For dense-shrub or full-frame flower masses: use a higher-density point cluster with a small amount of accumulated ink underneath.",
            "negative_space_ratio": "Use a moderate negative-space ratio (roughly 55-75%), slightly lower than sparser flower-branch scenes due to higher density.",
            "texture_method": "Use flying-white dotted color, with short texture strokes separating cluster boundaries in denser passages.",
        },
        "rejected_keywords": [r"统一饱和色块|single saturated color wash", r"面主导的墨块语言|plane-dominant"],
    },
    "jiangnan_water_town": {
        "main": {
            "ink_block_handling": "Merge adjacent rooftops into unified ink masses (joined-roof clustering) rather than rendering each ridge and tile individually; layer water first, then ink, with local overprinting of ink-color or oil-color on the water.",
            "negative_space_ratio": "Use a fairly high negative-space ratio (roughly 55-75%, general baseline): white walls are the primary carrier of reserved white for this subject.",
            "texture_method": "Use charred dry-brush strokes for roof-ridge and eave structural turns; apply broken ink, limited to 1-3 spots per image, at wall-shadow or water-boundary transitions for variation.",
        },
        "aux": {
            "ink_block_handling": "If water reflections are also present, add the river-lake-reflection route's tilted ink blocks and undulating water-lines.",
            "negative_space_ratio": "Same as the main route, roughly 55-75%.",
            "texture_method": "Undulating water-lines plus broken accent dots for the reflection portion.",
        },
        "rejected_keywords": [r"逐片描绘|one by one", r"米黄仿古纸|antique.?beige paper"],
    },
    "ancient_architecture": {
        "main": {
            "ink_block_handling": "Reuse the Jiangnan water-town route's joined-roof clustering for building groups with clear sloped roofs and eaves, such as palaces or temples.",
            "negative_space_ratio": "Same as Jiangnan water-town, roughly 55-75%.",
            "texture_method": "Same as Jiangnan water-town: charred dry-brush strokes for ridges and eaves, with broken ink at 1-3 spots for structural variation.",
        },
        "aux": {
            "ink_block_handling": "If the architecture is dominated by walls, platforms or city-wall mass rather than sloped roof groups, switch to the urban-day route's merged, flattened, layered volume treatment.",
            "negative_space_ratio": "Same as urban-day, depending on sky/reserved-white ratio.",
            "texture_method": "Dry-brush scumbling for wall shadow, charred dry-brush for structural edges.",
        },
        "rejected_keywords": [r"专属路由或专属纸色|dedicated route"],
    },
    "urban_day": {
        "main": {
            "ink_block_handling": "Merge dense building clusters into flattened, layered ink-color volumes with uneven highs and lows carrying the skyline rhythm; a single unified perspective is not required.",
            "negative_space_ratio": "Use a moderate negative-space ratio (roughly 40-60%): plane weight is high (about 60%), with sky and gaps as the main reserved white but at a lower share than in line- or point-dominant subjects.",
            "texture_method": "Use dry-brush scumbling for building-facade shadow, charred dry-brush for skyline structural edges.",
        },
        "rejected_keywords": [r"统一灭点透视|single-point.*perspective"],
    },
    "urban_night": {
        "main": {
            "ink_block_handling": "Lay down ink-color volume as the night scene's base, overlay a structural line network on top, and accent it with color dots for lights to activate night density.",
            "negative_space_ratio": "Use a low negative-space ratio (roughly 25-45%): the night scene's overall tone is darker and denser, so reserved white is lower than daytime urban subjects.",
            "texture_method": "Use a geometric structural line network for roads and building edges rather than traditional texture strokes.",
        },
        "rejected_keywords": [r"大面积高饱和色块|large.*solid.*color"],
    },
    "farmland_grid": {
        "main": {
            "ink_block_handling": "Arrange repeated units in an array, but introduce deliberate perturbation to break mechanical regularity—do not copy the grid with absolute uniformity.",
            "negative_space_ratio": "Use a fairly high negative-space ratio (roughly 55-75%, general baseline): paper-white fissures running through the array serve as the main reserved white and spacing.",
            "texture_method": "Use short dry-brush strokes for field-ridge edges rather than forcing a rock-texture method onto them.",
        },
        "rejected_keywords": [r"统一焦点透视|unified.*perspective", r"完全规则的机械重复|mechanical repetition"],
    },
    "fishing_port": {
        "main": {
            "ink_block_handling": "Same source as farmland_grid: arrange boats and dock clusters as a perturbed array of repeated units, not a perfectly tidy arrangement.",
            "negative_space_ratio": "Use a fairly high negative-space ratio (roughly 55-75%, general baseline): water gaps and paper-white fissures between boats serve as the main reserved white.",
            "texture_method": "Use dry-brush flying-white for hull and mast structural lines; avoid finely rendering every boat in realistic detail.",
        },
        "rejected_keywords": [r"精确写实描绘每艘船|realistic.*every boat", r"统一焦点透视|unified.*perspective"],
    },
    "abstract_line_network": {
        "main": {
            "ink_block_handling": "Use low intervention—only translate the material, for example turning line-art or vector lines into ink-line texture; do not add new ink mass or recompose the image.",
            "negative_space_ratio": "Preserve the source image's existing negative-space ratio; do not compress it or add/remove density.",
            "texture_method": "Keep the source's existing line language and technique itself; only convert the medium quality, for example giving the lines ink-tone variation, without redesigning a texture method.",
        },
        "rejected_keywords": [r"重新构图或大幅改动密度|(?<!or )recompose"],
    },
}


def _build_m10_subject_rules(routing, notes):
    subject = routing.get("subject_category")
    entry = SUBJECT_ROUTE_TRANSLATIONS.get(subject)
    if not entry:
        notes.append(f"M10（题材专属规则）跳过：主体 '{subject}' 没有对应的英文翻译条目。")
        return None

    main = entry["main"]
    sentence = (
        f"Ink-block handling: {main['ink_block_handling']} "
        f"Target negative space ratio: {main['negative_space_ratio']} "
        f"Texture method: {main['texture_method']}"
    )

    if routing.get("aux_route") and "aux" in entry:
        aux = entry["aux"]
        sentence += (
            f" In addition: {aux['ink_block_handling']} "
            f"{aux['negative_space_ratio']} {aux['texture_method']}"
        )

    rejected_patterns = entry.get("rejected_keywords", [])
    for pattern in rejected_patterns:
        if re.search(pattern, sentence, flags=re.IGNORECASE):
            notes.append(
                f"M10：组装出的句子疑似命中该题材的 rejected_routes 关键词模式 '{pattern}'，"
                "需要人工核对翻译措辞是否走偏——已跳过该模块而不是照样输出。"
            )
            return None

    return sentence


# ---------------------------------------------------------------------------
# M11. 负向提示词 — 全局强制，逐字引用 + 条件追加（06 第 275-297 行）
# ---------------------------------------------------------------------------
M11_TEXT = (
    "Avoid literal contour tracing, uniform outline weight, vector-smooth curves, evenly "
    "spaced parallel lines, symmetrical mirrored negative space, mechanically repeated "
    "patterns, coloring-book style flat fills inside closed outlines, and a perfectly clean "
    "line with no thickness variation, no break, and no accident anywhere in the composition."
)
M11_FLAT_SPATIAL_ADDITION = (
    "Avoid one-point perspective, converging vanishing lines, realistic near-large far-small "
    "scaling, atmospheric depth, modeled light and shadow, gradient volume rendering, complete "
    "closed object contours, mechanical perfect grids, identical repeated units, traditional "
    "layered-mountain recession, architectural or cartographic illustration, smooth digital "
    "color gradients, random abstraction without source topology, fully blocked dense fill, "
    "text, logos, signatures, seals and watermarks."
)


def _build_m11_negative(flat_spatial_triggered):
    text = M11_TEXT
    if flat_spatial_triggered:
        text += " " + M11_FLAT_SPATIAL_ADDITION
    return text


# ---------------------------------------------------------------------------
# 拼装主流程
# ---------------------------------------------------------------------------


def load_json(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


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

    notes = []
    paragraphs = [M1_TEXT]
    dynamic_paragraphs = []  # 只有这部分（拼装模板/诊断卡衍生内容）参与 M12 黑名单自查；
                              # M1/M3/M7/M9/M11 是逐字引用的固定文本，本身就包含
                              # "not watercolor"/"no watercolor postcard" 这类否定式表达，
                              # 拿它们去过黑名单会把自己的合法措辞误判成命中。

    m2 = _build_m2_paper_color(diagnosis, notes)
    if m2:
        paragraphs.append(m2)
        dynamic_paragraphs.append(m2)

    paragraphs.append(M3_TEXT)

    m3b = _build_m3b_abstraction(diagnosis, notes)
    if m3b:
        paragraphs.append(m3b)
        dynamic_paragraphs.append(m3b)

    m4 = _build_m4_composition(diagnosis, routing, notes)
    if m4:
        paragraphs.append(m4)
        dynamic_paragraphs.append(m4)

    flat_spatial_triggered = _flat_spatial_triggered(diagnosis)
    m5 = _build_m5_flat_spatial(diagnosis, routing, notes)
    if m5:
        paragraphs.append(m5)
        dynamic_paragraphs.append(m5)
    else:
        flat_spatial_triggered = False  # M5 没有真正组装出文本时，M11 的条件追加也不该触发

    m6 = _build_m6_point_line_plane(diagnosis, routing, notes)
    if m6:
        paragraphs.append(m6)
        dynamic_paragraphs.append(m6)

    paragraphs.append(M7_TEXT)

    m8 = _build_m8_techniques(diagnosis, notes)
    if m8:
        paragraphs.append(m8)
        dynamic_paragraphs.append(m8)

    paragraphs.append(M9_TEXT)
    m9b = _build_m9_palette(diagnosis, notes)
    if m9b:
        paragraphs.append(m9b)
        dynamic_paragraphs.append(m9b)

    m10 = _build_m10_subject_rules(routing, notes)
    if m10:
        paragraphs.append(m10)
        dynamic_paragraphs.append(m10)

    paragraphs.append(_build_m11_negative(flat_spatial_triggered))

    draft_prompt = "\n\n".join(paragraphs)

    violations = _check_blacklist("\n\n".join(dynamic_paragraphs))
    if violations:
        return {
            "status": "blocked",
            "reason": "草稿 prompt 命中黑名单关键词，已拦截：" + "; ".join(violations),
            "prompt": None,
        }

    technique_count = len(_get_selected_techniques(diagnosis))
    if not (1 <= technique_count <= 3):
        return {
            "status": "blocked",
            "reason": (
                f"diagnosis.ink_symbol_composition.selected_deformation_techniques 数量为 "
                f"{technique_count}，不在允许范围 1-3 个内。"
            ),
            "prompt": None,
        }

    return {
        "status": "ok",
        "reason": "已按 06-prompt-compiler-spec.md 的模块顺序拼装完成。",
        "prompt": draft_prompt,
        "notes": notes,
    }


def _check_blacklist(text: str) -> list:
    lowered = text.lower()
    hits = []
    for pattern, label in BLACKLIST_PATTERNS:
        if re.search(pattern, lowered, flags=re.IGNORECASE):
            hits.append(label)
    return hits


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
        sys.stdout.reconfigure(encoding="utf-8")
        print(output_text)

    return 0 if result["status"] == "ok" else 1


if __name__ == "__main__":
    sys.exit(main())
