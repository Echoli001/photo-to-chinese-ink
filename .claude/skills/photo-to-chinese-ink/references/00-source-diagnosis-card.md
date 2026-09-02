# 源图诊断卡 — Schema 与判定维度

> 状态：内容已从 v17 拆入（v17 第 1 章"结构提取"，第 18–118 行；`visual_grammar.source_diagnosis`
> 及相关字段定义，约第 1805–2274 行 YAML 协议块）。本文件是这份流程第 1 步的
> 操作说明，模型看图/读文字后按这里的 schema 和判定依据产出 JSON 诊断卡。

## 用途

这是整个流程的第 1 步产出。模型看图（或读文字）后，按下面的 schema
输出一份 JSON，作为路由脚本和编译脚本的唯一输入。**不要跳过某个字段
直接编造合理值** —— 图里看不出来的维度，诚实标 `"unknown"`，而不是
用常识猜一个填上去。

## 六张卡（frozen schema，来自 P0）

1. `source_diagnosis` — 源图诊断卡（本文件主要覆盖）
2. `plant_relation` — 植物关系卡（仅当画面含植物/花卉主体时才需要，字段定义见下方"关联卡"一节）
3. `plane_composition` — 平面空间构成卡（字段定义见下方"关联卡"一节）
4. `ink_symbol_composition` — 墨符号构成卡（字段定义见下方"关联卡"一节）
5. `ink_material` — 笔墨材质卡（字段定义见下方"关联卡"一节）
6. `quality_score` — 质量评分卡（仅在有实际出图后使用，见
   `05-quality-checklist.md`）

## 第 1 章"结构提取"方法论（v17 第 18–118 行）

诊断的核心不是"识别画面里有什么物体"，而是把输入转换成五层结构（v17 §1.1）：

1. **语义锚点**：保留 2-4 个能让人认出原图的对象，如桥、屋、树、山脊、人物、船、街区轮廓。
2. **主形块**：把对象压缩成 3-7 个大面积形状，优先识别黑块、白块、灰色过渡块。
3. **方向骨架**：提取一条主势线和 1-3 条次势线，例如水平延展、拱桥弧线、树干竖线、河流蛇形线、城市网格。
4. **节奏节点**：寻找可被转化为点、短线、小色块的重复元素，如窗、灯、花、叶、鸟、人物、石块。
5. **虚空间**：把天空、水面、白墙、雾、雪地或未画区域作为积极形状，不把留白理解成"缺少内容"。

诊断卡里 `point_line_plane_dependency` 字段的判断依据就是这五层结构：点依赖看
"节奏节点"是否密集主导画面（如繁花、灯光、人群），线依赖看"方向骨架"是否
是画面骨干（如江河、山脊、枝网），面依赖看"主形块"是否靠大色块支撑画面
（如天空、水面、大片白墙）。**不要看题材刻板印象**——同样是"树"，稀疏孤树
可能是线依赖为主，茂密树冠可能是点依赖为主。

### 抽象层级（v17 §1.2）——描述"目标应该多抽象"

默认使用"半抽象"而非完全抽象：

| 层级 | 可识别性 | 处理方式 | 适用内容 |
| --- | ---: | --- | --- |
| A 具象提炼 | 70%-85% | 减少细节，保留轮廓与空间关系 | 人像、宠物、建筑纪念图 |
| B 半抽象重组 | 45%-70% | 形块变形、视点压缩、线点重排 | 默认模式、壁纸、屏保 |
| C 意象抽象 | 20%-45% | 只保留主势、结构节奏和少数语义锚点 | 情绪化背景、装饰画 |

吴冠中晚期作品更接近 B-C 之间：现实形态仍是起点，但画面优先表达状态、情感
和概念。完全脱离对象的随机抽象不符合"风筝不断线"的逻辑。

> **本 skill 新增字段**（v17 原文有这张 A/B/C 分级表，但没有把判断结果落到
> 一个具体字段名上——这是撰写 `06-prompt-compiler-spec.md` 时发现的缺口）：
> 诊断卡需要把这里选定的档位写进 `target_abstraction_tier` 字段（取值
> `A`/`B`/`C`，默认 `B`），供编译脚本引用。它和
> `01-composition-routing.md` 里 `flat_spatial_composition_route.abstraction_continuum_level`
> （0-3，仅 `flat_spatial` 触发时才有值）是两个不同的字段，不要混用：
> 前者描述整张目标图的抽象程度，后者只描述"平面空间构成叠加层"内部的
> 抽象连续体档位。

### 先判断源图本身的抽象程度（v17 §1.2A）——`image_medium` 字段的真正依据

这是 `image_medium` 字段存在的理论基础：**抽象层级不能只描述目标图，还必须
描述输入图**。生成前先回答——源图的信息主要由真实物体、光影材质，还是已经
被提炼过的点线面关系承载？

```yaml
source_style_reading:
  source_abstraction_level: low | medium | high
  existing_visual_language: []
  primary_information_carrier: object | line | point | plane | color | mixed
  rhythm_profile: []
  valuable_invariants: []
  missing_quality: []

transformation_policy:
  intervention_level: low | medium | high
  topology_preservation_target: 0.0-1.0
  detail_deletion_target: 0.0-1.0
  allowed_changes: []
  forbidden_changes: []
```

| 源图状态 | 干预级别 | 拓扑保留 | 细节删减 | 主要动作 |
| --- | --- | ---: | ---: | --- |
| 写实照片，形式关系尚未提炼 | 高 | 25%-50% | 50%-80% | 取舍、破形、重组、改变透视 |
| 已有清晰构图，但仍以摄影材质为主 | 中 | 50%-75% | 30%-55% | 压缩对象、强化节奏、转换材料 |
| 已有强烈点线面秩序或近似艺术作品 | 低 | 70%-90% | 10%-30% | 保留构图和密度拓扑，只优化笔性、墨色、层级和局部节奏 |

若源图的抽象度高，不得以"更像艺术"为理由重新概括。此时应执行**材质翻译**
而不是**结构重写**：把已有线条转为枯湿浓淡不同的墨线，把已有色场转为有纸
性和水痕的综合色场，但保留其位置、密度梯度、方向冲突和主要空隙。

## `image_medium` 到 `abstraction_level`/`preserve_from_input` 的映射（已从 v17 拆入）

`image_medium` 取值对应到上表"源图状态"三档、进而决定 `transformation_policy`：

| `image_medium` 取值 | 对应 v17 源图状态 | intervention_level | topology_preservation_target | detail_deletion_target |
| --- | --- | --- | --- | --- |
| `real_photo`（真实摄影） | 写实照片，形式关系尚未提炼 | high | 0.25–0.50 | 0.50–0.80 |
| `screenshot_or_render`（软件截图/3D 渲染图） | 已有清晰构图，但仍以摄影材质为主——渲染/截图通常已有明确构图和边界，但表面仍是"摄影式"材质（光影、阴影、渲染纹理） | medium | 0.50–0.75 | 0.30–0.55 |
| `painting_or_scan`（画作翻拍/扫描件） | 已有强烈点线面秩序或近似艺术作品——本身已是一幅画，画面已经是别人（或同一体系）提炼过的形式语言 | low | 0.70–0.90 | 0.10–0.30 |
| `vector_illustration`（矢量插画/图形素材/图表） | 视具体画面复杂度落在"已有清晰构图"或"已有强烈点线面秩序"两档之一——矢量图本身已去除摄影材质噪声，多数情况按低干预处理，执行材质翻译而非结构重写；若矢量图内容仍是写实图形的简单描边（保留了大量摄影式细节层级），则按中干预处理 | low（默认）/ medium（内容仍偏写实描边时） | 0.70–0.90（默认）/ 0.50–0.75 | 0.10–0.30（默认）/ 0.30–0.55 |
| `not_applicable`（纯文字输入） | 不适用——没有源图可读，`transformation_policy` 由文字描述的具体程度直接决定，不经过这张对照表 | — | — | — |
| `unknown`（图片但形式不明确） | 不要瞎猜——诊断卡里此字段应联动 `unknown_fields`，路由脚本按"信息不足"处理，不能默认套用某一档 | — | — | — |

判断 `vector_illustration` 落在哪一档的具体依据：参照 `Testing/manifest.md`
里 `abstract_line_network1/2.jpeg`（矢量抽象线条图，已是纯粹的点线面构成）
应判为低干预；如果矢量图只是把写实照片简单描边转成矢量线稿、仍保留大量
照片式细节层级（例如矢量化的建筑立面图纸），应判为中干预。

`preserve_from_input`（保留哪些具体信息不丢）对应 v17 §1.4A 的"双尺度模型"：

```yaml
information_balance:
  semantic_anchors: 2-5
  macro_topology_preservation: 0.55-0.80
  literal_micro_edge_correspondence_cap: 0.20-0.40
  micro_detail_deletion: 0.40-0.65
  rhythmic_line_density_target: 0.70-1.10
  free_rhythmic_line_share: 0.30-0.55
```

"保留信息"必须拆成两个尺度，不能用一个拓扑保留率同时控制全图与局部：

1. **宏观拓扑**：保留对象群的方向、包围、连续、层叠、疏密分区与主要空隙。它保证作品仍来自用户的照片。
2. **微观边缘**：照片里可逐条指认的轮廓、纹理和色块边界。它必须被删、并、断、错位或重新谱写，避免作品只是水墨化描摹。

对"摄影中的强线性重复"和"已经完成抽象的线性作品"必须分流（这一条同时是
`abstract_line_network` 类目路由的直接依据）：

| 源图类型 | 宏观处理 | 微观处理 | 默认干预 |
| --- | --- | --- | --- |
| 摄影中的梯田、波浪、枝桠、道路等强线性重复 | 保留整体流向、层叠和主形 | 只让 20%-40% 线条对应真实边缘，其余删除或按主势重新谱写 | 中至高 |
| 已完成抽象的成熟线网作品 | 保留密度地图、方向冲突、闭合关系和主要空隙 | 不逐线复制，但只删 10%-30% 弱线，以笔性翻译为主 | 低 |

因此，**"源图以线为主"不自动等于低干预**。先判断这些线是摄影事实，还是
已经经过艺术提炼的形式语言——这正是 `image_medium` 字段要回答的问题。

## `source_diagnosis` JSON 结构

```json
{
  "input_type": "photo | text",
  "image_medium": "real_photo | vector_illustration | painting_or_scan | screenshot_or_render | not_applicable | unknown",
  "subject_category": "从 04-subject-routing-table.md 的 13 类里选一个，或 other",
  "dominant_subject": "本 skill 新增字段（v17 没有这个字段名）：当画面同时包含多个 04-subject-routing-table.md 里的主体类目时（例如江南建筑+水面倒影），必须在这里明确选出一个主语言——路由脚本只按这一个字段查表，不平均/叠加多条路线。单一主体场景里这个字段和 subject_category 取值相同。",
  "secondary_subjects": "本 skill 新增字段，可选：数组，列出画面里存在但不是主语言的次要主体类目（同样取自 04 的 13 类），仅供参考，不参与路由查表。没有次要主体时留空数组。",
  "point_line_plane_dependency": {
    "point": "low | medium | high",
    "line": "low | medium | high",
    "plane": "low | medium | high",
    "note": "判断依据——参照上方'五层结构'：节奏节点密集主导 → 点依赖高；方向骨架是画面骨干 → 线依赖高；主形块靠大色块支撑 → 面依赖高。不要看题材刻板印象。"
  },
  "negative_space_ratio": "留白大致占比，如 low/medium/high 或百分比估计——对应五层结构里的'虚空间'",
  "perspective": "平视 | 俯视 | 仰视 | 散点透视 | 已经是抽象平面构成（无明确透视）",
  "light_condition": "白天 | 夜晚 | 逆光 | 阴天 | 不适用",
  "color_tendency": "原图主导色相，用于后续对照 03-color-routing.md 决定要不要保留",
  "color_route": {
    "palette_mode": "从 03-color-routing.md §4.3 的 13 档配色模式库里选一个，如'银灰江南＋破原色'（字段结构逐字来自该文件 §4.2 的 color_route YAML 协议块，供 06 的 M9 模块模板直接取值）",
    "material_color_mode": "transparent_ink | opaque_color | scraped_color | mixed",
    "achromatic_base": [],
    "dominant_chromatic_family": [],
    "secondary_chromatic_family": [],
    "accent_hues": [],
    "chromatic_carrier": "point | line | plane | mixed",
    "transparent_to_opaque_balance": "0.0-1.0",
    "high_chroma_coverage_cap": "0.00-0.30",
    "painted_color_coverage_cap": "0.00-0.45",
    "forbidden_recent_palette": []
  },
  "target_abstraction_tier": "A | B | C，默认 B——本 skill 新增字段，见上文'抽象层级'一节说明，供 06 的 M1/M3/M7 模块拼装'保留可识别度'短语时取值",
  "structural_complexity": "low | medium | high",
  "source_style_reading": {
    "source_abstraction_level": "low | medium | high",
    "existing_visual_language": [],
    "primary_information_carrier": "object | line | point | plane | color | mixed",
    "rhythm_profile": [],
    "valuable_invariants": [],
    "missing_quality": []
  },
  "transformation_policy": {
    "intervention_level": "low | medium | high",
    "topology_preservation_target": "0.0-1.0，取值参照 image_medium 映射表",
    "detail_deletion_target": "0.0-1.0，取值参照 image_medium 映射表",
    "allowed_changes": [],
    "forbidden_changes": []
  },
  "unknown_fields": ["列出因为是纯文字输入、缺乏画面信息而无法判断的字段"]
}
```

## 关联卡：`plant_relation` / `plane_composition` / `ink_symbol_composition` / `ink_material`

这四张卡的完整字段定义已从 v17 的 `visual_grammar` YAML 协议块（约第
1807–2272 行）里逐一核对拆出，具体 schema 不重复写在本文件，避免和权威定义
不同步：

- `plant_relation` 卡的字段来源是 `visual_grammar.plant_growth_route` 下的
  `relation_card` 和 `photo_morphology_card` 两个子 schema，连同
  `route_selector`（5 档路线）和 `photo_type_router`（10 种照片类型）一起，
  完整拆入 `01-composition-routing.md`（植物类主体的构图路由一节）。
- `plane_composition` 卡的字段来源是
  `visual_grammar.flat_spatial_composition_route.flat_spatial_composition_card`，
  连同该模块下 6 条命名 `subject_routes`、4 种 pattern 类型、4 级抽象连续体，
  完整拆入 `01-composition-routing.md`。
- `ink_symbol_composition` 卡的字段来源是 `visual_grammar.ink_symbol_system`
  （4 个符号各自的状态/职责、`ink_color_collision` 事件），完整拆入
  `02-ink-symbol-rules.md`。
  > **本 skill 新增字段**：`ink_symbol_system` 这份 master YAML（以及
  > `02a`/`02b` 里对应的散文规则）只定义了点/线/面符号的**全局静态规则**，
  > 没有任何字段记录"这一张具体画面选用了哪几种破形/不规则技法"——
  > 也就是说这张卡此前在 v17 全文和本参考文件集里都**没有正式的 JSON
  > schema**，只有 `02b-point-line-plane-symbols.md` §3.4 的 10 种技法
  > 散文列表，和 `07-generation-protocol-yaml.md` 里
  > `pre_generation_gate.require_ink_symbol_composition_card: true` 这个
  > 布尔门禁标记。因此诊断卡需要补上
  > `ink_symbol_composition.selected_deformation_techniques` 字段（数组，
  > 1-3 项，取值必须是 `02b` §3.4 里的 10 个技法之一：删线/并形/断裂/
  > 错位/疏密突变/粗细对撞/方向反拍/偶发笔触/非对称留白/彩点脱轨），
  > 这是本 skill 第一次把这张卡落成具体 schema，不是在延伸一份已有定义。
- `ink_material` 卡的字段来源是 `visual_grammar.ink_material_card` 和
  `visual_grammar.paper_color_router`（6 档纸色枚举及默认优先级/理由要求），
  完整拆入 `02-ink-symbol-rules.md`。

## 判断这些维度时的原则

- **看真实结构，不看题材刻板印象**：例如同样是"树"，稀疏的孤树可能是
  线依赖为主，茂密的树冠可能是点依赖为主——不要看到"树"就默认套用同一
  套点线面配比。（这是 v17 第 7/8 章真实照片测试反复强调的坑，参见
  §7"真实照片测试结论"22 行结论表和 §8"分类测试协议"15 行测试矩阵。）
- **`unknown` 是合法输出**，尤其是纯文字输入的场景。宁可让第 2 步路由
  脚本报"信息不足，需要用户补充"，也不要在诊断卡里编造一个看似合理的
  画面细节。
- **五级规则冲突优先级**（v17 §7.1）：源图独有信息与用户反馈 > 诊断结论 >
  主体路由 > 通用取值范围 > 装饰性规则。诊断卡的判断结果在这个优先级里
  排第二位——它可以被源图里明显的、路由表没预料到的独有信息覆盖，但一旦
  诊断卡下了结论，后续的路由和编译步骤要服从它，不能因为"看起来更像某个
  常见套路"就绕开诊断结果。
