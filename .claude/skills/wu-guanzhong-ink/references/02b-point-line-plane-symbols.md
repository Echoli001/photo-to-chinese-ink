# 02b 点线面墨符号系统与线的语法（v17 §3.1D-3.12，全局强制规则）

> 来源：`C:\Users\LiEc\Downloads\Wu_Guanzhong_Style_Grammar.md`（v17）第 330-553
> 行，对应原文「第 3 章 墨与线」的 §3.1D 墨的符号化、§3.2-3.7 线的语法与节奏、
> §3.8-3.12 点线面分配逻辑。英文 prompt 段落**逐字复制**，不改写。
>
> **这是全局强制规则**：点/线/面符号系统和线的生成约束适用于所有题材，不是
> 某个题材触发才生效。题材专属的具体配比数值见 `02c-subject-specific-ink-rules.md`；
> 墨的浓淡干湿两轴与纸色路由见 `02a-ink-base-rules.md`。
>
> master YAML 中 `ink_symbol_system:`（`07-generation-protocol-yaml.md` 第
> 79-109 行）与 `line:`/`point_line_plane_allocator:`（同文件第 139-154 行）
> 已经把本节内容压缩成机读字段并完整保留，**本文件补充这些字段背后的判定
> 条件、口诀与原文，两处相同的字段取值不重复摘抄**——编译期这几个字段的具体
> 取值以 07 为准，取值的原理和数值来源读本文件。
>
> **覆盖范围说明**：本文件只到 v17 §3.12（输入分析与自动分配器）为止。
> §3.12A（高角度压平与现代平面构成语法）不在本文件范围内，它是**构图骨架**
> 层面的规则，已经在 [`01-composition-routing.md`](01-composition-routing.md)
> 中处理，避免重复拆分。

## 目录

- [3.1D 墨的符号化：由状物笔墨转为现代点、线、面](#31d-墨的符号化由状物笔墨转为现代点线面-v17-330-388)
- [3.2 线的四种功能](#32-线的四种功能-v17-389-397)
- [3.3 线条生成约束](#33-线条生成约束-v17-398-407)
- [3.4 破形与不规则节奏](#34-破形与不规则节奏-v17-408-424)
- [3.5 节奏模型](#35-节奏模型-v17-425-437)
- [3.6 正向"不规则化"提示](#36-正向不规则化提示-v17-438-453)
- [3.7 负面提示词](#37-负面提示词-v17-454-466)
- [3.8 点、线、面不是平均分配](#38-点线面不是平均分配-v17-467-473)
- [3.9 从实际景物判断点、线、面](#39-从实际景物判断点线面-v17-474-488)
- [3.10 作品观察得到的分配区间](#310-作品观察得到的分配区间-v17-489-505)
- [3.11 施墨面上限](#311-施墨面上限-v17-506-521)
- [3.12 输入分析与自动分配器](#312-输入分析与自动分配器-v17-522-553)

---

## 3.1D 墨的符号化：由状物笔墨转为现代点、线、面（v17 330-388）

传统"状物笔墨"（皴、擦、点、染直接描摹物象质感）要转化为现代构成意义上的
**点、线、面**三类抽象墨符号——符号仍然由源图的形态触发，但不再是对物象的
逐笔摹写。

### 3.1D-1 三类墨符号（v17 334-342）

| 符号 | 典型墨态 | 职责 |
|---|---|---|
| 墨点 | 焦浓重音、湿墨滴、淡灰散点 | 节点、转折、密度跳跃、反拍（counterbeat） |
| 墨线 | 焦干骨线、重压线、淡灰回弹、湿线、游丝 | 方向、连接、切割、碰撞、生长 |
| 墨面 | 浓湿核心、层积中墨、淡湿毛细面、干渴刮擦面 | 重量、空间、负形、面的节奏 |

（对应 master YAML `ink_symbol_system.point/line/plane` 各自的 `states`/`duties`
枚举值，这里补充每个状态的墨态描述与职责说明。）

### 3.1D-2 墨符号必须具有有限的"形式自主性"（v17 344-349）

- 点/线/面符号从源图形态派生而来，但**不必**逐一对应物体的真实边界——一根
  树枝在画面里可以被简化/夸张成一条墨线，不需要精确复刻它的轮廓。
- 允许符号的形态相对源图物象产生 **10%-25%** 的自主偏移（形状、角度、粗细、
  聚散程度上的偏离），这是"表现性"而非"写实描摹"的关键差异点。
- 黑白灰的点线面骨架必须先于色彩确立——先立骨架，色彩后加。
- 不要求逐个物体的字面轮廓边界；符号系统追求的是整体视觉节奏，不是逐物体
  精确重现。

### 3.1D-3 同一符号内部的干湿浓淡交错（v17 351-357）

- 同一类符号（例如同一组墨点）内部也不能状态单一：一组墨点里应该同时出现
  焦浓、湿润、淡灰几种状态混合，而不是一批点全部用同一种墨态复制。
- 墨线的粗细、浓淡、干湿沿线条走向本身就应该变化（呼应 §3.1A-4"笔性"要求）。
- 墨面内部必须混合湿核心与干刮擦区域，不能整块面用单一均匀墨调。

### 3.1D-4 墨骨与高饱和彩色块的关系（v17 359-368）

墨的黑白灰骨架与高饱和度彩色块之间只能是以下四种关系之一，每幅作品选用
1-3 处：

| 关系 | 说明 |
|---|---|
| 并置（juxtapose） | 色块与墨形并排存在，各自独立但相邻 |
| 切割（cut） | 色块切断/打断墨线或墨面的连续性 |
| 穿插（interlock） | 色块与墨形彼此穿插交错，边界互相咬合 |
| 压叠（opaque overprint） | 色块不透明地叠压在墨形之上 |

规则：色彩事件必须依附于一个源图节点或视觉焦点，不能凭空放置；色彩可以是
高饱和度的；色彩的形态应为点、短线或自由面之一；**颜色不能被填在一个黑色
轮廓线内部**（那是填色书/卡通画法，不是水墨的墨色关系）；无论加了多少彩色，
黑白灰的墨骨架结构必须依然能被看出、能够"独立成立"。

**墨符号路线（可直接使用的英文 prompt 段落）：**

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

## 3.2 线的四种功能（v17 389-397）

| 线型 | 功能 |
|---|---|
| 轮廓线 | 界定物象边界，但不必连续闭合 |
| 势线 | 表达动势、方向、力的走向，不依附具体物象轮廓 |
| 结构线 | 表达画面内部的结构骨架、空间分割 |
| 游丝线 | 细弱、断续、游走的辅助线，制造呼吸感与细节层次 |

（对应 master YAML `line.types` 枚举：`contour`/`directional`/`structural`/`filament`。）

## 3.3 线条生成约束（v17 398-407）

6 条硬性规则：

1. 禁止使用统一粗细的矢量曲线式描边——每条线的粗细必须沿其自身长度变化。
2. 线条的重复边缘可见比例控制在约 15%-35%（即部分线条允许有轻微的"重叠/
   复描"痕迹，但不能全线统一重复）。
3. 断续线的比例控制在约 20%-40%——相当比例的线不能从头到尾连续不断。
4. 线条间距变化范围约 0.40-2.50（相对单位），杜绝完全等距排列。
5. 禁止周期性重复的线条节奏——线的疏密、长短、方向不能形成机械循环。
6. 每幅画面允许出现 1-3 处"受控意外"——刻意保留的、看起来像是笔触失控/
   偶然的痕迹，用于打破过度工整感。

（对应 master YAML `line` 字段的 `visible_repeated_edges: 0.15-0.35`、
`interrupted_line_ratio: 0.20-0.40`、`spacing_variation: 0.40-2.50`、
`periodic_repetition: forbidden`、`controlled_accidents: 1-3`，这里补充每个
数值背后对应的具体规则描述。）

## 3.4 破形与不规则节奏（v17 408-424）

10 种具体技法（每幅作品挑选组合使用，不要求全部用上，且总技法数量受编译期
1-3 个的上限约束，见 `05-quality-checklist.md`/`06-prompt-compiler-spec.md`）：

1. **删线**——省略部分本该存在的轮廓线，制造留白与呼吸空间。
2. **并形**——把相邻的两个形态合并简化成一个更大的墨形。
3. **断裂**——让线条或墨面在中途突然断开，不连续到底。
4. **错位**——相邻元素的对齐关系刻意错开，不完全对齐。
5. **疏密突变**——线条/墨点的密度在局部突然变化，不是渐变过渡。
6. **粗细对撞**——粗线与细线在同一区域直接碰撞并置，制造张力。
7. **方向反拍**——主导方向之外，插入 1-2 处反方向的笔触打破单一走向。
8. **偶发笔触**——每幅画面安排 1-3 个"受控意外"式的偶然笔触（呼应 §3.3
   规则 6）。
9. **非对称留白**——留白区域刻意不对称分布，避免机械对称构图。
10. **彩点脱轨**——个别彩色点/笔触刻意偏离其"应该在"的位置，制造活力。

收束规则：这些破形/不规则处理不是随机噪声，而是要服务于画面情绪——线条的
生成过程应该带着以下 8 个情绪动词之一去构想："游走、升腾、冲撞、回旋、坠落、
拥挤、逃逸、停顿"。

（对应 master YAML `line.emotion_verbs` 字段的 8 个英文动词：`wandering`/
`rising`/`colliding`/`circling`/`falling`/`crowding`/`escaping`/`pausing`，
一一对应上面的 8 个中文情绪动词。）

## 3.5 节奏模型（v17 425-437）

把点线面的节奏类比为音乐节奏来理解：

```text
长线   = 乐句（phrase）
短线/折线 = 节拍（beat）
墨点   = 重音（accent）
留白   = 休止（rest）
浓墨块 = 低音或停顿（bass / pause）
彩点   = 高音与突发音色（treble / sudden timbre）
```

这个类比的作用：帮助判断一幅画面的"节奏是否单调"——如果只有乐句没有休止、
只有节拍没有重音，画面就会显得平铺直叙、缺乏起伏。

## 3.6 正向"不规则化"提示（v17 438-453）

**可直接使用的英文 prompt 段落：**

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

## 3.7 负面提示词（v17 454-466）

**可直接使用的英文负面提示段落：**

```text
Avoid literal contour tracing, uniform outline weight, vector-smooth curves, evenly
spaced parallel lines, symmetrical mirrored negative space, mechanically repeated
patterns, coloring-book style flat fills inside closed outlines, and a perfectly clean
line with no thickness variation, no break, and no accident anywhere in the composition.
```

重要提醒：仅仅在 prompt 里写"expressive"、"organic"、"freehand"、"dynamic"
这类形容词是**不够的**——这些词太抽象，生成模型往往还是会画出规整的矢量线。
必须像上面两段一样，给出具体的、可操作的破形/不规则化指令，才能真正影响
生成结果。

## 3.8 点、线、面不是平均分配（v17 467-473）

必须区分两个不同的概念：

- **表达权重**（expression weight）：点/线/面在画面里承担的结构性、节奏性
  责任比例，三者相加等于 100%，是用于指导生成的抽象权重，不是像素测量值。
- **画面覆盖**（screen coverage）：点/线/面实际占据的像素/面积比例，与表达
  权重不是同一回事——例如"线"可能表达权重很高（决定画面骨架走向），但实际
  覆盖的像素面积很小。

默认情况下点/线/面**不能**平均分成 33/33/33——每幅画面必须选定一种主导语言
（dominant language），其余两者作为辅助。

（对应 master YAML `point_line_plane_allocator` 字段：`weights_sum: 100`、
`choose_dominant_language: true`、`forbid_equal_default: true`、
`distinguish_paper_from_painted_plane: true`。）

## 3.9 从实际景物判断点、线、面（v17 474-488）

| 源图形态特征 | 对应主导语言 |
|---|---|
| 细密枝条、藤蔓、电线、栏杆等线性密集结构 | 线为主导 |
| 花瓣、落叶、鸟群、光斑等散布式小单元 | 点为主导 |
| 大片墙面、水面、天空、屋顶等连续大色块 | 面为主导 |
| 树干+枝叶混合结构 | 线为主导，点为辅助 |
| 建筑群倒影、屋顶群 | 面与线并重 |
| 纯几何/人造重复单元（窗格、瓦片） | 线为主导，可能触发 §3.12A 高角度压平语法 |

判断依据是源图实际的形态密度和分布方式，不是主观臆断——这张表是"从景物到
语言选择"的推导起点，不是最终固定配比（固定配比区间见下面 §3.10 与
`04-subject-routing-table.md`/`02c-subject-specific-ink-rules.md` 里各题材
的具体数值）。

## 3.10 作品观察得到的分配区间（v17 489-505）

> **重要说明（v17 原文自带的免责声明，必须完整保留，不能省略）**：下表是
> 「用于生成控制的表达权重区间」，来自对吴冠中作品视觉印象的归纳总结，**不是
> 对原作进行像素测量后得出的艺术史定论**，不能当作严谨的学术测量数据引用。

| 参考作品（举例） | 点权重 | 线权重 | 面权重 | 主导语言 |
|---|---|---|---|---|
| 《新林》 | 15% | 55% | 30% | 线 |
| 《梅园》 | 30% | 45% | 25% | 线 |
| 《狮子林》 | 10% | 40% | 50% | 面 |
| 《棗林》 | 20% | 50% | 30% | 线 |
| （其余作品对应区间以 v17 原文表格为准，此处保留代表性条目，完整清单见原文
  489-505 行） | | | | |

这张表的作用是给编译器/路由表提供数值参考区间的来源依据，不是要求逐一复刻
这些具体作品的构图内容（复刻真实作品名称属于 `08-originality-guardrails.md`
明确禁止的行为）。

## 3.11 施墨面上限（v17 506-521）

墨面（plane）分为 4 个子类型：

- 浓湿核心面（concentrated wet core）
- 层积中墨面（layered middle ink）
- 淡湿毛细面（pale capillary plane）
- 干渴刮擦面（thirsty dry scrape）

4 条默认上限规则：

1. 大面积连续着墨的画面覆盖占比默认不应超过约 30%——超过这个比例容易让
   画面失去"以线立骨"的水墨感，滑向色块拼贴。
2. 复杂线性题材（森林、藤蔓、枝叶密集类）的施墨面上限更低，约 15%-30%，且
   线的表达权重不能低于 45%（呼应 master YAML
   `complex_linear_subject_plane_cap: 0.30` 字段与 §3.13 森林类规则）。
3. 纸的留白（paper negative）不计入"施墨面"——留白和有墨的面是两个独立
   统计对象（对应 `distinguish_paper_from_painted_plane: true`）。
4. 主要墨面必须混合湿核心与干刮擦区域，不能是单一均匀墨调的色块（呼应
   §3.1D-3）。

## 3.12 输入分析与自动分配器（v17 522-553）

自动分配逻辑的输入/输出 schema：

```yaml
input_morphology:
  linear_density: low | medium | high
  point_scatter_density: low | medium | high
  large_continuous_mass_ratio: 0.0-1.0
  dominant_feature: linear | scattered_points | continuous_mass | mixed

point_line_plane:
  point_weight: <derived from point_scatter_density>
  line_weight: <derived from linear_density>
  plane_weight: <derived from large_continuous_mass_ratio>
  dominant_language: <derived from dominant_feature>
  painted_plane_coverage_cap: <derived from subject complexity, see §3.11>
```

分配逻辑（文字规则）：

1. 先从源图/文字描述里提取 `input_morphology` 四个维度的判断（依据见
   §3.9 的形态-语言对照表）。
2. 三个权重（point/line/plane）之和必须等于 100，不能三者相加超出或不足。
3. `dominant_feature` 判定的主导类型，其对应权重不能低于其余两者中的任何
   一个——即"主导语言"在数值上也必须真的占优，不能名义上是主导、数值上
   却和辅助语言相同。
4. 如果诊断阶段无法明确判断某个维度（例如文字描述过于简略、缺少细节），
   该维度应标注"未知/待用户补充"，不能由分配器编造一个具体数值——这与
   `00-source-diagnosis-card.md` 里"缺失维度必须显式标注未知"的原则一致。
5. 题材专属的默认起始配比（如 §3.13 森林类的 point 25 / line 55 / plane 20）
   优先于本节的通用自动分配逻辑——本节提供的是**没有更具体题材规则覆盖时**
   的兜底判断方法，具体题材以 `02c-subject-specific-ink-rules.md` 和
   `04-subject-routing-table.md` 为准。

---

## 与其他文件的关系

- 墨的浓淡干湿两轴、反水彩化约束、宣纸色彩路由（v17 §3.1-3.1C）不在本文件
  范围内，见 [`02a-ink-base-rules.md`](02a-ink-base-rules.md)。
- 题材专属的点线面配比数值与专属技法（v17 §3.13-3.18）不在本文件范围内，见
  [`02c-subject-specific-ink-rules.md`](02c-subject-specific-ink-rules.md)。
- 高角度压平构图与现代平面构成语法（v17 §3.12A）属于构图骨架选择，不在本
  文件范围内，见 [`01-composition-routing.md`](01-composition-routing.md)。
