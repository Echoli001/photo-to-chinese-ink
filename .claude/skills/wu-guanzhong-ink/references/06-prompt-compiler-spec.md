# Prompt 编译规则

> 状态：**首版已完成**。本文件是 `scripts/compiler.py` 的行为规范——脚本本
> 身是确定性代码，但代码按什么规则组装最终文本，规则来源是这个文件（以及
> 它引用的 `02a`/`02b`/`03`/`04`/`05`/`01`）。
>
> **重要说明**：下面的模块内容分两类。标注"**逐字引用**"的英文段落是从
> v17 原文逐字摘录（出处见各自小节），编译器应该原样拼接，不改写。没有标
> 注逐字引用、只写"拼装模板"的部分，是本 skill 在 v17 没有给出现成英文范
> 例时自己按 v17 的中文规则内容构造的英文短语——这些是本 skill 的推断产
> 出，不是 v17 原文，`compiler.py` 的实现和未来复核都要能区分这两类。

## 输入

- 诊断卡 JSON（`source_diagnosis` + 相关联卡，见 `00-source-diagnosis-card.md`）
- 路由决定 JSON（`scripts/router.py` 的输出，查表来源见
  `scripts/data/subject_routing_table.json` / `04-subject-routing-table.md`）

## 输出（本节两条决定，均为本 skill 自定，非 v17 原文规定）

- **语言**：最终 prompt 用**英文**。理由：`02a`/`02b`/`03`/`01` 里能直接
  使用的现成范例（材质基座、墨符号翻译、正向不规则化、负向提示词、色彩系
  统、白纸路由、平面构图负向提示词，共 7 段）全部是 v17 原文自带的英文段
  落，说明 v17 设计这套语法时本来就是准备喂给英文优先的文生图模型（Midjourney
  等）；直接复用这些原文段落比重新翻译更忠实。
- **格式**：一段连续英文文本（多个模块按顺序拼接成段落，句号分隔），不是
  逗号分隔的关键词堆砌——因为 7 段逐字引用本身就是完整句子体裁，硬拆成关
  键词会破坏原文语感。**不包含**画幅比例、版本号等工具专属参数（`--ar`
  `--v` 等）——不同工具语法不同，编译器不猜测用户要用哪个工具，第 4 步呈
  现给用户时用中文提示"如果你的工具需要比例/版本参数，请自己在这段英文
  prompt 后面加"。
- 附带一段**中文说明**（诊断摘要 + 路由摘要 + 使用提醒），这段中文不是
  prompt 本体，不会被粘贴进文生图工具。

## 组装总原则

1. **v17 §7.1 冲突优先级**贯穿整个编译过程：源图独有信息与用户反馈 >
   诊断结论 > 主体路由 > 通用取值范围 > 装饰性规则。任何模块的取值如果和
   诊断卡里明确写出的原图信息冲突，以诊断卡为准。
2. 模块按下面固定顺序拼接。每个模块要么是**逐字引用**（原样输出，不改写
   不缩写），要么是**拼装模板**（用诊断卡/路由 JSON 里的具体值填进模板）。
3. 任何模块如果因为诊断卡缺字段（标了 `unknown`）而无法拼装，编译器应该
   跳过该模块并在中文说明里提醒用户"这部分因信息不足被跳过"，不能编造。

## 组装模块清单（固定顺序）

### M1. 墨材质基座（全局强制，逐字引用）

来源：`02a-ink-base-rules.md` §3.1，v17 204-329 行。任何题材都必须包含这
一段，它定义"这是水墨不是水彩"的材质基调：

```text
Chinese ink on highly absorbent raw xuan paper, not watercolor. Build the image from
reserved paper white, concentrated wet ink cores, heavy middle-ink bodies, pale wet
breathing layers, and dry charred bone strokes. Treat ink concentration and brush
moisture as independent variables. Let wet ink pool, backflow, collide and feather
unevenly into the fibers; let dry ink drag, split, skip and expose flying-white bristle
gaps. Every major ink mass must contain internal tonal migration and at least two ink
states. Use layered ink, broken ink and selective water intervention, not uniform
transparent color washes. Color remains subordinate to the black-gray-white ink
structure and appears as sparse opaque, scraped or ink-mixed events. No smooth digital
gradients, no identical soft edges, no global paper-noise overlay, no watercolor postcard.
```

### M2. 纸色声明（全局强制，条件拼装）

来源：`02a-ink-base-rules.md` §3.1C 纸色路由，六档纸色（洁白生宣/冷白生宣/
中性白生宣/自然白生宣/暖象牙纸/仿古米黄），默认候选顺序
`clean_white → neutral_white → cool_white → natural_white`。

- **若 `ink_material.paper_color_router` 选中"白纸家族"四档之一**（clean_white /
  cool_white / neutral_white / natural_white）：直接拼接下面这段**逐字引
  用**（来源：`02a` §3.1C，同一段文字在 `03-color-routing.md` 里重复出现）：

  ```text
  Use clean white highly absorbent raw xuan paper. The paper is white, fresh and
  unaged—not beige, cream, sepia or antique parchment. Keep most of the sheet quiet
  and nearly texture-free; reveal subtle fibers only where wet ink feathers or dry
  brush drags across them. Carry all environmental warmth in the ink-mixed color,
  mineral pigment or scraped opaque passages, never by yellowing the entire paper.
  No global paper texture, brown mottling, stains, deckled dark edges or vintage filter.
  ```

- **若选中暖象牙纸（warm_ivory）或仿古米黄（antique_beige）**：v17 没有给这
  两档现成的英文段落，且 `05-quality-checklist.md` 明确把"米黄仿古纸"列
  为题材惯例自动触发时的硬性禁止项——只有诊断卡对源图色调给出**具体、非
  题材套路的理由**时才允许选这两档。此时编译器用**拼装模板**（非逐字引
  用，需在中文说明里明确标注）：

  ```text
  Use {warm_ivory|antique_beige} raw xuan paper, justified specifically by
  {诊断卡里给出的具体理由，例如"原图整体处于暖黄逆光"}, not by subject convention.
  Keep the warmth confined to the paper base tone; do not add artificial aging
  texture, stains, foxing or a vintage-scan filter on top of it.
  ```

  编译器硬性检查：选中这两档但诊断卡/路由决定没有写出具体理由字符串时，
  必须报错或自动回退到白纸家族默认顺序，不能静默放行（对应 `05` 的
  "缺失配色理由则提醒"要求）。

### M3. 墨符号翻译（全局强制，逐字引用）

来源：`02b-point-line-plane-symbols.md` §3.1D-3.2，v17 330 行起。这段定义
"先把源图翻译成点/线/面墨符号，再谈构图和色彩"的核心方法论：

```text
Translate the source first into autonomous but source-derived ink symbols: ink points,
ink lines, ink planes and paper-negative space, established in black-gray-white before
any color is added. Let each symbol's form deviate roughly 10-25% from the literal
source silhouette rather than tracing exact object boundaries. Vary concentration and
moisture within each symbol group—mix charred, wet and pale states inside the same
cluster of points, along the same line, across the same plane. Introduce 1-3 moments
where a saturated color event juxtaposes, cuts, interlocks with, or opaquely overprints
the ink structure, always anchored to a source-derived node or focal point. Never pour
color inside a closed black outline like a coloring book. The black-gray-white ink
skeleton must remain legible and structurally self-sufficient even if the color were
removed.
```

### M4. 构图原型（拼装模板，来自路由决定）

来源：`01-composition-routing.md` 六种 `composition_mode`。v17 没有给这六
种构图给出可以直接逐字引用的英文段落（`01` 里现成的英文段落只有
flat_spatial 的负向提示词，见 M11），所以这里是**拼装模板**：编译器从路
由决定里取 `composition_mode` 的值，拼一句"State the composition
archetype as {mode 的英文关键词描述}"。

**`composition_mode` → 13 类主体默认映射表**（本节是本 skill 的推断产
出，不是 v17 逐字规定——v17 只给了 6 种构图原型各自的定义和 §2.6 的选择
逻辑关键词，没有给"每个题材默认用哪种构图"的现成对照表；下表按 `01` 的
构图定义和 `04` 各题材的点/线/面权重、墨块处理方式匹配得出，供
`router.py` 查表使用）：

| 13 类主体（04） | 默认 `composition_mode` | 理由（简述） |
|---|---|---|
| `terraced_field` | `panoramic_flow` | 线群重谱、全景延展的重复线，非几何切割也非都市体积 |
| `mountain_snow` | `monumental_void` | 面权重高、大留白托体量，与"纪念碑式虚空"直接对应 |
| `river_lake_reflection` | `panoramic_flow` | 水面连绵流动、倒影镜像属于全景流动构图 |
| `forest_bamboo` | `immersive_network` | 分叉骨架+小重复，枝网沉浸感 |
| `flower_branch` | `immersive_network` | 生长路径+附着点链，藤蔓网络结构 |
| `flower_field` | `panoramic_flow` | 点簇聚散分布在开阔留白中，无网络交织也无几何切割，取全景流动 |
| `jiangnan_water_town` | `jiangnan_geometry` | 名称直接对应，白墙黑瓦几何切割型构图 |
| `ancient_architecture` | `jiangnan_geometry`（主）/ `urban_ink_volume`（辅，墙体台基类） | 复用 `jiangnan_water_town`；若走 aux_route（墙体/台基为主）则改用都市体积 |
| `urban_day` | `urban_ink_volume` | 名称直接对应，体积合并压平叠置 |
| `urban_night` | `urban_grid_variation` | 结构线网+灯点，网格变体比纯体积更贴合夜景线网结构 |
| `farmland_grid` | `urban_grid_variation` | 阵列/网格式重复单元，即使题材不是"都市"，网格变体的构图逻辑仍适用 |
| `fishing_port` | `urban_grid_variation` | 船群重复单元阵列化，与 `farmland_grid` 同一 v17 出处（R2-06C） |
| `abstract_line_network` | `immersive_network` | 名称与内容直接对应，已是成熟线网，低干预材质翻译 |

### M5. 平面空间构成叠加层（条件模块，触发时生效）

来源：`01-composition-routing.md` §3.12A `flat_spatial_composition_route`
——注意这**不是**第 7 种 `composition_mode`，是一个条件叠加层，触发条件是
`high_angle_or_aerial_view_or_repeated_surface_units_are_primary`（诊断
卡的 `perspective` 为"俯视"或画面以重复表面单元为主时）。

**`flat_spatial_composition_route.subject_routes`（6 个命名路线）↔ 13 类
主体映射表**（本节同样是本 skill 的推断产出，不是 v17 逐字规定；`01` 定
义了这 6 个路线各自的骨架/点线面起始值/压平技法，但没有给出和 `04` 13 类
的对照表——`01` 文件自己的 TODO 也明确写"等 04 开始编写时一起确定"，现
在 04 已经完成，可以定下来了。判断依据是名称直接对应，或 `04` 各类目
`_source` 引用的 v17 行号/R2 编号与 `01` 描述的对象重合）：

| `01` 的 6 个 `subject_routes` | 对应 04 的 13 类主体 | 触发条件 |
|---|---|---|
| `seedling_field`（青苗田） | `farmland_grid` | `04` 的 `_source` 明确引用"鸟瞰青苗田"，与 R2-06C 同一行 |
| `fishing_harbor`（渔港） | `fishing_port` | 名称直接对应，同一 R2-06C 行 |
| `aerial_village`（俯瞰村镇） | `jiangnan_water_town`（仅当 `perspective` 为俯视时触发，平视时走 M4 的 `jiangnan_geometry` 常规构图，不叠加本层） | R2-06C 同段提到"村镇屋顶"，与俯瞰视角的江南村镇重合 |
| `terrace_field`（梯田） | `terraced_field` | 名称直接对应 |
| `water_shore_fragments`（水岸破碎片段） | `river_lake_reflection`（仅当画面为俯视/破碎片段化的水岸，而非常规平视倒影时触发） | 内容对应"水岸"，与 `river_lake_reflection` 的水面主体重合，但常规平视倒影走 M4 的 `panoramic_flow`，不强制叠加本层 |
| `abstract_ink_block_landscape`（抽象墨块山水） | 无 13 类精确对应——作为**兜底路线**：当 `mountain_snow` 或其他山水类主体在高角度/强烈平面化时使用，因为它是 6 个路线里唯一以"墨块"而非线/点为核心的选项，与山水类的面权重高特性最接近 | 山水类主体 + 高角度/强平面化视角同时成立时 |

- 触发时，M5 拼装模板 = 对应 `subject_routes` 条目的骨架/点线面起始值/压
  平技法描述（拼装模板，取材自 `01` 对该路线的中文定义，非逐字引用），并
  且要把 M11 的 `flat_spatial` 专属负向提示词一并追加（见 M11）。
- **未触发时完全跳过本模块**，不能因为主体类目"看起来像"某个 subject_route
  就默认叠加——`flat_spatial_composition_route` 明确标注
  `not_global_default: true`。

### M6. 点/线/面配比声明（拼装模板）

来源：诊断卡 `point_line_plane_dependency` 三档定性值，以及 `04` 各题材
`point_line_plane` 数值三元组（溯源用，非路由表固定 schema 字段，但可供
编译器参考）。`02b` 明确规定**不是默认 33/33/33**，必须选一种主导语言。

拼装模板：`"Let {dominant 的那一项：point / line / plane} carry roughly
{对应数值}% of the visual weight as the dominant language, with
{次要两项} playing supporting roles, not an equal three-way split."`

数值优先级：若诊断卡对某具体主体有 `04` 给出的数值三元组（如
`jiangnan_water_town` 的 `12/32/56*`），优先用该数值；若诊断卡的
`point_line_plane_dependency` 三档定性判断和 `04` 默认数值冲突（例如诊断
卡明确判断这张图线权重比默认表更高），按 v17 §7.1 优先级——诊断结论高于
主体路由通用值，以诊断卡为准，编译器只用 `04` 数值做参考基线，不能覆盖
诊断卡的明确判断。

### M7. 正向不规则化（全局强制，逐字引用）

来源：`02b-point-line-plane-symbols.md`"破形与不规则节奏"一节，v17 §3.4：

```text
Do not trace the visible contours one by one. Instead, let the brush skip some edges,
merge adjacent shapes, break a line mid-stroke, misalign neighboring elements, and
suddenly shift density from sparse to crowded within the same passage. Let thick and
thin strokes collide directly against each other. Insert one or two strokes that run
against the dominant directional flow. Allow 1-3 controlled accidents—marks that read
as spontaneous or slightly out of control. Keep negative space asymmetrical rather than
evenly balanced. Let one or two color marks drift slightly off their expected position.
Think of the line rhythm as wandering, rising, colliding, circling, falling, crowding,
escaping or pausing—not as a mechanical outline-filling exercise.
```

### M8. 破形技法关键词选择（拼装模板，1-3 个，硬性上限）

来源：`02b` 的 10 种具体"破形"技法（删线/并形/断裂/错位/疏密突变/粗细
对撞/方向反拍/偶发笔触/非对称留白/彩点脱轨），对应 8 个情绪动词
（wandering/rising/colliding/circling/falling/crowding/escaping/pausing）。

**这一步本质是语义判断**（哪 1-3 种技法最贴合这张图的节奏），不是纯查表
——按 Rule 8（模型负责判断，代码负责执行），选择动作应该在**诊断阶段**
由模型做出，而不是 `compiler.py` 自己猜。因此：

- 需要在诊断卡里新增一个字段（目前 `ink_symbol_composition` 卡尚未包含，
  是本次编译规范梳理时发现的缺口，需要补充，见文末"需要回填到诊断卡的
  字段"一节）：`selected_deformation_techniques`（1-3 个，取值来自上面
  10 种技法枚举）。
- `compiler.py` 只做**硬性计数检查**（1 ≤ 数量 ≤ 3，且值必须在 10 种枚
  举内），不负责挑选逻辑本身——这部分判断留给诊断阶段。
- 拼装模板：把选中的 1-3 个技法名对应的英文短语接入正向段落（例如"并形"
  → "merge adjacent shapes into one silhouette"），具体英文短语在 `02b`
  正向不规则化逐字引用段落（M7）里已经覆盖了 10 种技法里的大部分表达，
  M8 只需要从 M7 的句子池里挑出对应 1-3 句强调重复，不需要另造新句子。

### M9. 色彩系统（全局强制，逐字引用）

来源：`03-color-routing.md` §4，v17 1449-1588 行：

```text
Do not use the habitual coral-orange-blue-gray palette unless the source analysis
selects it. First choose one palette mode from the color router. Preserve at most
two meaningful source hues, then remap the rest by value, temperature and emotion.
State one dominant chromatic family, one secondary family and zero to three accent
hues. Treat primary colors as unequal rhythmic events rather than equal RGB dots.
Vary which element carries color: points, broken short lines, translucent fragments
or one small plane. Keep high-chroma coverage below the selected cap. Use pigment
bleed, dilution, dry-brush loss and paper interruption so even vivid colors are not
flat digital fills. Avoid repeating the palette signature of recent outputs.
```

紧接这段之后，拼装模板追加一句具体的 `palette_mode` 声明：`"Selected
palette mode: {03 的 13 档 palette_mode 之一，例如'银灰江南'
silver-gray jiangnan}."`——`palette_mode` 的选择依据 `03` 的路由逻辑（不
按主体类目查表，每张图独立判断，见 `03` 明确说明"v17 没有题材→配色的固
定映射"），这是诊断/路由阶段的判断结果，编译器只负责把选定值填进模板。

### M10. 题材专属规则（拼装模板，来自路由决定）

来源：`04-subject-routing-table.md` 该题材的 `main_route`（或按需附加
`aux_route`）三字段：`ink_block_handling` / `negative_space_ratio` /
`texture_method`。这三个字段本身是中文，`04` 没有给对应英文逐字段落，所
以是**拼装模板**：

```text
Ink-block handling: {ink_block_handling 译成英文短语}.
Target negative space ratio: {negative_space_ratio 数值区间}.
Texture method: {texture_method 译成英文短语}.
```

若路由决定同时给出 `aux_route`（例如 `jiangnan_water_town` 带水面倒影
时），追加一句衔接 `aux_route` 的对应内容。`rejected_routes` 不出现在最
终 prompt 正文里，但编译器应该用它做**自我核查**：如果拼出来的句子里出
现了 `rejected_routes` 描述的反例关键词（例如"逐片描绘""统一灭点透视"这
类），要报错重新生成，而不是原样输出。

### M11. 负向提示词（全局强制，逐字引用 + 条件追加）

全局固定部分，来源 `02b`：

```text
Avoid literal contour tracing, uniform outline weight, vector-smooth curves, evenly
spaced parallel lines, symmetrical mirrored negative space, mechanically repeated
patterns, coloring-book style flat fills inside closed outlines, and a perfectly clean
line with no thickness variation, no break, and no accident anywhere in the composition.
```

**若 M5（平面空间构成叠加层）被触发**，追加下面这段（来源 `01` §3.12A）
——**注意这段只在 flat_spatial 触发时追加，不能无条件追加**，因为它和
`monumental_void` 等需要大气透视/体量层次的构图模式互相矛盾：

```text
Avoid one-point perspective, converging vanishing lines, realistic near-large far-small
scaling, atmospheric depth, modeled light and shadow, gradient volume rendering, complete
closed object contours, mechanical perfect grids, identical repeated units, traditional
layered-mountain recession, architectural or cartographic illustration, smooth digital
color gradients, random abstraction without source topology, fully blocked dense fill,
text, logos, signatures, seals and watermarks.
```

### M12. 禁止项强制检查（代码层面，不是可见 prompt 文本）

见下方"硬性约束"一节——这些是拼完全文后 `compiler.py` 要跑的检查，不是
拼进 prompt 里的一段话。

## 抽象化程度：两个字段，分别解决 00 的 A/B/C 和 01 的 0-3

`00-source-diagnosis-card.md` 的 A/B/C 抽象层级（可识别性 70-85%/45-70%/
20-45%）和 `01-composition-routing.md` 的 `abstraction_continuum`（0-3
级）是两个不同的概念，不能合并成一个字段：

- **`diagnosis.target_abstraction_tier`**（A/B/C，默认 B）——描述**整张
  画**该有多抽象，任何题材都适用，在诊断阶段判断，需要补充到
  `00-source-diagnosis-card.md` 的 `source_diagnosis` JSON schema 里（目
  前该 schema 里没有这个字段，只有描述"源图本身"抽象程度的
  `source_style_reading.source_abstraction_level`，两者含义不同：一个是
  读原图，一个是定目标）。
- **`routing.abstraction_continuum_level`**（0-3，可空）——只有 M5 的
  `flat_spatial_composition_route` 触发时才有意义，描述压平构图这条线上
  的具体抽象梯度，属于路由决定的一部分，不属于诊断卡。

拼装位置：`target_abstraction_tier` 影响 M1/M3/M7 的"细节删减程度"整体基
调（可以在这几个模块的模板里插入一句"keep recognizability around
{A:70-85%|B:45-70%|C:20-45%}"）；`abstraction_continuum_level` 只在 M5 内
部使用。

## 硬性约束（`compiler.py` 代码层面强制执行，不依赖模型自觉遵守）

拼完全文后，`compiler.py` 必须对最终文本跑下面这些检查——这份清单逐字取
自 `05-quality-checklist.md` 第 193-223 行"编译期二元否决清单"，是这份
清单的权威落地位置：

1. **不出现签名/印章/题跋类描述**——命中即报错，不能静默移除后放行（因
   为签名类描述通常意味着上游某个模块拼错了内容，不是简单删词就能修好）。
2. **不出现水彩化描述**（`watercolor` 等关键词）——命中即报错。M1 的逐字
   引用段落本身已经明确"not watercolor"，理论上不该出现，一旦出现说明
   上游模板被破坏。
3. **不直接写 "in the style of Wu Guanzhong" 这类靠画家名字取效果的表达**
   ——这条明确标注**非 v17 原文逐字规则**，是本 skill 自行加入的补充防
   护（v17 全文检索不到这句话的逐字依据）。命中即报错。
4. **不使用"米黄仿古纸"这类被明确禁止的纸色描述**——除非 M2 走了"暖纸
   +具体理由"分支且理由字段非空，否则命中即报错（见 M2 的硬性检查）。
5. **技法关键词总数 1-3 个**——对应 M8，数量为 0 或 >3 时报错。
6. **同一次生成不无理由复用同一套配色**——文本层面只能检查"是否显式写
   了配色理由"这类结构性存在，不能判断语义上是否真的有理由；实现为"缺
   失配色理由则提醒"（M9 的 `palette_mode` 声明句缺失时提醒），不是关键
   词硬拦截。
7. **不出现"吴冠中真迹/原作/官方授权"等误导性描述**——命中即报错。
8. **不直接把《双燕》《狮子林》《逍遥游》等标志性作品名称当模板请求**
   ——命中即报错，这类作品名如果出现在诊断卡的 `unknown_fields` 之外的
   任何字段里，说明诊断阶段已经出错，要连带检查诊断卡而不只是删词。

此外两条不在 `05` 清单里、但在旧版骨架已经写出的约束，继续保留：

- 不能直接用画家名字驱动效果本身作为技法描述（例如"仿吴冠中笔法"）——
  和第 3 条同属一类问题，一并检查。
- M8 的 1-3 个技法关键词必须来自 `02b` 的 10 种枚举值，不能是编译器/模
  型现造的技法名。

## 需要回填到诊断卡的字段（本次编译规范梳理时发现的缺口，非本文件范围内
直接修改，留给下一步同步更新 `00-source-diagnosis-card.md`）

1. `target_abstraction_tier`（A/B/C）——见上方"抽象化程度"一节。
2. `dominant_subject` / `secondary_subjects`——`04` 的"多主体混合场景"
   一节已经确定了这条规则本身（router.py 只按主语言查表），但字段还没
   加进 `00` 的 schema，`scripts/data/subject_routing_table.json` 的
   `mixed_subject_rule.todo_for_router_py` 里也记了同一件事。
3. `ink_symbol_composition.selected_deformation_techniques`（1-3 个，见
   M8）——这是本文件梳理 M8 时才发现的新缺口，之前的 `02b` 拆分只列出了
   10 种技法本身，没有明确"谁来选、选完写在哪个字段"。

## 已解决的历史 TODO（对照旧版骨架逐条关闭）

- ~~确认最终 prompt 目标语言/格式~~ → 已在"输出"一节定为英文连续段落。
- ~~每个模块具体拼什么内容~~ → 已在 M1-M12 逐一给出，逐字引用和拼装模板
  已明确区分。
- ~~抽象化程度字段该放诊断卡还是路由决定~~ → 已拆成两个字段分别归位，见
  "抽象化程度"一节；`target_abstraction_tier` 需要回填 `00` 的 schema
  （见上一节第 1 条），本文件先记录决定，实际 schema 编辑是下一步。
- ~~黑名单关键词完整列表~~ → 已在"硬性约束"一节直接引用 `05` 的权威 8
  条清单，不再自己维护第二份清单。
- 输出规格（画幅比例等）→ 已在"输出"一节决定 MVP 不包含工具专属参数。
