# 02c 题材专属墨线规则（v17 §3.13-3.18）

> 来源：`Wu_Guanzhong_Style_Grammar.md` v17 第 1177-1447 行左右区间（本文件对应
> 原文 §3.13-3.18，行号标注见各节标题）。这是原文"第 3 章 墨与线"里**题材触发
> 规则**最集中的部分：每一节只在诊断卡命中特定主体类目时生效，不是全局强制
> 规则（全局强制规则见计划中的 `02a-ink-base-rules.md`，尚待从 §3.1-3.1C 整理）。
>
> 与 `01-composition-routing.md` 的分工：01 文件管**构图骨架选择**（选哪种
> composition_mode / 高角度压平构图骨架）；本文件管**选定题材后，点/线/面
> 三符号的具体配比、执行顺序、可直接用的 prompt 文本与负面提示**。两者应联
> 合使用，不是互斥。

## 目录

- [3.13 森林类专用比例](#313-森林类专用比例-v17-643-674)
- [3.13A 植物生命线模块](#313a-植物生命线模块起伏纠缠与跳跃-v17-676-759)
- [3.13B 植物关系语法](#313b-植物关系语法线是关系点是事件白是距离-v17-761-865)
- [3.13C 植物照片艺术化处理](#313c-植物照片艺术化处理形态识别优先于物种名称-v17-866-936)
- [3.14 已有线性抽象源图专用规则](#314-已有线性抽象源图专用规则-v17-937-979)
- [3.15 摄影性强线源图：线群重谱规则](#315-摄影性强线源图线群重谱规则-v17-983-1053)
- [3.16 江南水乡专用：屋顶墨面与白墙负形](#316-江南水乡专用屋顶墨面与白墙负形-v17-1056-1231)
- [3.17 江南混合媒介语法](#317-江南混合媒介语法墨彩油彩波动水线与倒斜墨块-v17-1235-1337)
- [3.18 都市墨色体积模块](#318-都市墨色体积模块高低错落与现代平面构成-v17-1339-1445)

---

## 3.13 森林类专用比例（v17 643-674）

**触发条件**：高树林、竹林、梅林等以"树干+枝叶"为主体的输入。

默认起始配比：

```yaml
point_line_plane:
  point_weight: 25
  line_weight: 55
  plane_weight: 20
  painted_plane_coverage_cap: 0.24
  dominant_language: line
```

可直接使用的正面 prompt（原文英文，逐字保留）：

```text
Treat the trunks and branches as the primary linear skeleton. Use three to five
major lines and many partial filaments, hooks, broken verticals and crossing strokes.
Translate leaf texture into non-periodic point clusters with sharp changes of scale
and density. Do not replace forest complexity with broad watercolor clouds. Keep
painted wash planes subordinate: they may connect, interrupt or push back the lines,
but must not carry most of the forest texture. At least half of the important line
energy should remain visible through or around the washes.
```

森林专属负面提示（原文英文，逐字保留）：

```text
Avoid broad cloudy wash dominating the image, repeated foliage blobs, soft-edged
watercolor masses covering the trunks, generic misty forest painting, and using
large planes as a substitute for branch and bark structure.
```

**要点**：面（plane）在森林题材里天生受限（`painted_plane_coverage_cap: 0.24`），
线是主导语言。这条规则的核心失败模式是"把森林的复杂度用大片水彩云代替"——
即用面偷懒地覆盖本该由线表达的枝干信息。

---

## 3.13A 植物生命线模块：起伏、纠缠与跳跃（v17 676-759）

**触发条件**：藤蔓、紫藤、梅枝、老树、垂柳、攀爬植物等"生长路径是主要信息"
的输入。目标不是忠实描出植物轮廓，而是把生长过程中的**阻力、反弹、纠缠、
延伸、突变**转译成线的运动。

### 参数卡

```yaml
plant_life_line_module:
  activation: branching_and_growth_path_are_primary
  point_weight: 25-38
  line_weight: 52-66
  plane_weight: 8-18
  painted_plane_coverage_cap: 0.18
  source_detail_deletion: 0.60-0.78
  primary_growth_lines: 4-9
  black_bone_line_share: 0.18-0.28
  gray_rebound_line_share: 0.32-0.46
  filament_and_escape_line_share: 0.26-0.40
  quiet_field_min: 0.20-0.38
  knot_release_knot_rhythm: required
  point_events_at_energy_nodes: required
```

### 生命力不是"曲线很多"，而是线内发生力量变化

每条主生长线必须包含 **≥3 种运动事件**（不能机械重复同一组合）：

1. **蓄势**：线条以淡、细、慢的状态进入，或从纸白中间歇性浮现
2. **突进**：突然加粗、加黑、转向，或跨越大片空白形成视觉重音
3. **受阻**：在交叉、结点、转折处停顿、积墨、勾回或短暂纠缠
4. **回弹**：一条不同步的灰线在黑线旁生长，弯曲、错位或反向再起
5. **逸出**：细线从密结中逸出，转淡、转白，突然中断，再于别处以不同角度重现

主线不能只是平滑 S 形曲线——线的力量应呈现**不等幅度**的起伏：大弧后接短
促折线，缓行后突然急转，下沉后反弹上扬，密结后跃入空白。单条线的粗细、
墨色、干湿可有约 3-6 次明显变化，但变化点不能等距分布。

### 黑线、灰线与游丝的分工

| 类型 | 占比 | 用途 | 要点 |
| --- | --- | --- | --- |
| **黑色骨线** | 约 18%-28% | 2-4 处关键生长段、粗藤、老干、力量结点 | 粗而不封闭，含干湿变化，不是连续均匀黑带 |
| **灰色回弹线** | 约 32%-46% | 黑线的错位回声、内外摆动、前后空间、再生长节奏 | 不得紧贴黑线形成双线轮廓；应远近交替、交叉、脱离或反向 |
| **游丝与逸出线** | 约 26%-40% | 卷须、嫩枝、空间穿插 | 可环绕、打结、交叉、消失、跃出画外；不能变成满幅均匀缠麻 |

粗细线关系不是"主干+平均小枝"，而是**粗线主导构成、灰线回环、细线破局**。
保留约 20%-38% 的安静纸白场，供线跃入、冲入、退出。

### 纠缠采用"结—放—再结"，不做满幅缠绕

- 设置 2-4 个密度不等的纠缠结；结与结之间用 1-3 条长线跨接，不连续填满
- 一个结可由"黑线折回+灰线环绕+细线穿刺+墨点沉积"共同构成；另一个结应换用不同组合，避免重复
- 线群可在进入结前加速/汇聚，出结后突然发散/转淡/甩出反向线
- 线可越过植物实际边缘成为独立形式，但须保留源图 3-5 个主要生长方向与重力特征

### 墨点与彩点是能量事件

- 落点位置：结点、交叉、折回、线端、浓度突变处；可洇、可飞溅、可拖出短痕；不沿线等距排列
- 彩点落点：生长方向改变处、需要视觉反拍处、纸白过空处；可依附于线、脱离悬浮，或在一侧突然形成跳跃簇
- 点须有大小/浓淡/干湿/形状差异：大点压重、小点提速、孤点停顿、连续碎点造成颤动
- 花/叶只提供点的**来源**，不是"一花一点、一叶一点"的强制映射；有线无点、有点无线均可，点被线穿过也可以

### 垂花与藤蔓的专门变奏

适用于紫藤等垂挂花簇：

- 不能把所有花簇都画成平行珠帘：保留垂坠感的同时，让部分黑/灰线先横向游走/盘绕/回弹，再突然下垂
- 花簇点链须有长度/方向/密度/完整度差异；约一半只保留局部点段，不画完整锥形
- 至少 1-2 条线须逆垂坠方向上升或横切，制造生命反力
- 紫色点不能是唯一主体——黑线、灰线、墨点与少量绿点须共同组织动态

### 可直接使用的正面 prompt（原文英文，逐字保留）

```text
Extract the plant's growth forces rather than its botanical contour. Orchestrate four to
nine main trajectories as a rise-fall-recoil rhythm: moist black bone lines surge, thicken,
turn and pool; displaced gray lines echo, resist and bend away; fine filaments knot, cross,
vanish and leap out into quiet paper. Organize density as knot—release—knot, not an evenly
tangled web. Place ink dots at collisions, bends and stalled joints; place unequal color
points as jumps and counterbeats, sometimes attached to lines and sometimes suspended.
Let hanging flowers retain gravity while several lines curl sideways, rise or cut across it.
The first reading must be living linear energy; the second reading may reveal the plant.
```

### 负面提示（原文英文，逐字保留）

```text
Avoid graceful but weak decorative curves, smooth continuous S-lines, identical hanging
tassels, parallel bead strings, one branch traced for every source branch, one dot for every
flower, uniform black outlines, gray shadow lines glued to black contours, evenly tangled
webs, all-over density, pastel flower illustration, botanical accuracy, and random splatter
without structural knots or directional force.
```

---

## 3.13B 植物关系语法：线是关系，点是事件，白是距离（v17 761-865）

**核心立场**：植物类输入不能只提取"主干轮廓、分枝数量、花叶位置"，而要先
提取一张**生长关系图**：哪些线承重、哪些线只是回声；哪些交叉是真连接、哪些
只是空间重叠；彩点在哪里附着、在哪里脱离；纸白如何把密集生长切分出可呼吸
的距离。

### 参数卡

```yaml
plant_relation_card:
  source_mode: upright_canopy | drifting_garden | layered_grove | all_over_growth_field | fruit_node_tree
  dominant_growth_axes: []             # 2-9 条主方向，不是逐枝列表
  load_bearing_junctions: []           # 2-6 个承重或转折结点
  density_zones: []                    # 结、放、再结或满幅密度波
  major_paper_voids: []                # 大小、位置、是否连通
  ground_or_water_counterlines: []     # 可为空
  point_sources: [leaf, flower, fruit, bud, light, abstract_event]
  color_memory: []
  selected_route_reason: string
```

> **注意（与诊断卡的关系）**：`plant_relation_card` 这个 YAML 名称与本项目
> 6 张冻结诊断卡中的 `plant_relation` 卡直接同名。若源图属于植物类目，诊断
> 阶段产出的 `plant_relation` 卡应直接采用（或高度参照）此处的字段结构
> （`source_mode` / `dominant_growth_axes` / `load_bearing_junctions` /
> `density_zones` / `major_paper_voids` / `ground_or_water_counterlines` /
> `point_sources` / `color_memory`），而不是另造一套字段。**这一点需要在
> 写 `00-source-diagnosis-card.md` 时对照检查、避免重复定义两套不一致的
> schema。**（详见本文件末尾"待办"一节。）

### 五种植物关系路由

| 路由 | 源图关系 | 点／线／面起始区间 | 构成要点 | 不应强加 |
| --- | --- | --- | --- | --- |
| **直立冠层 `upright_canopy`** | 多根向上主干，上部叶花聚成冠层，下部较空 | 点 28%-38%／线 52%-64%／面 6%-14% | 4-10 根不等粗直立骨线；上部点密、下部点疏；枝线在顶部互相借势但不封闭成树冠块 | 满幅均匀点、每棵树独立轮廓、大块绿色树冠 |
| **游园散点 `drifting_garden`** | 植物对象已高度消解，只剩游走线、墨团与彩块 | 点 30%-42%／线 38%-50%／面 14%-26% | 2-5 个浓墨停顿点，曲伸线穿行其间；3-7 个高饱和彩块与墨并置切割；不设稳定地平线 | 强行补树干、写实叶片、中心式花束 |
| **林中层叠 `layered_grove`** | 竖干反复出现，枝线前后穿插，地面或水面提供灰色横向反拍 | 点 20%-32%／线 56%-68%／面 8%-18% | 7-16 根高低不齐竖线；黑干、灰干、细枝分层；3-8 条断续灰横线建立地面、水气或前后关系 | 透视林荫道、等距树列、灰线紧贴黑线 |
| **满幅生长场 `all_over_growth_field`** | 无单一主体和地平线，线网与点群穿透全幅 | 点 26%-38%／线 54%-66%／面 4%-12% | 以密度波而非中心构图；粗、中、细三尺度线穿插；保留多个微型白隙和少量较大休止，不平均填满 | 随机乱麻、统一密度、装饰壁纸式重复 |
| **果实节点树 `fruit_node_tree`** | 粗干分叉承重，较大果实／花团成为节点，细枝点线形成空气层 | 点 24%-36%／线 44%-58%／面 14%-26% | 粗墨干形成 3-7 个承重分叉；6-18 个大小不等的果实节点可由色面、破圈与内点组成；细线点群向外扩散 | 每个果实同圆同大、完整描边、写实静物树 |

区间是起始值，不是模板。源图若已经完成高度抽象，优先保留其密度拓扑、主线
穿插和色点位置；源图若为摄影，则提高删并、错位与形式自主性。

### 四种连接关系：避免机械树状图

植物关系至少混用以下三种，不能所有交叉都画成真实枝杈连接：

1. **真连接**：粗线分叉、汇入或积墨，承担重量与生长因果；数量少而明确
2. **叠交**：两条线在画面上交叉但不合并，通过浓淡、断续或覆盖区分前后
3. **近失**：一条线在另一条线、彩点或墨团附近停止、偏转或消失，制造张力与未完成感
4. **悬浮**：墨点和彩点脱离枝线，在纸白中成为反拍、回声或空气层

建议关系占比从**真连接 30%-50%、叠交 20%-35%、近失 10%-25%** 起步；彩点中
约 20%-40% 可以悬浮。比例必须随源图调整，但"全部真实连接"和"全部随机
悬浮"都判定失败。

### 线的三级空间关系

- **承重黑线**：约占线性能量 15%-28%。粗而不封闭，含浓湿积墨、重墨行笔与焦干飞白；决定重心和主要生长方向
- **关系灰线**：约占 25%-42%。不是黑线阴影，而是前后空间、回弹方向、地面水气与第二套生长节奏；可与黑线交叉、远离或反向
- **空气细线**：约占 30%-52%。枝梢、草茎和游丝被压缩成时现时隐的细线场，负责把不同点簇联系起来，但不填满每个空隙

三类线不得同宽同黑。部分线从画外进入或出画；部分线在彩块中消失；部分线只
画中段而不交代根与梢。闭合轮廓应是例外。

### 彩点不是叶片替身，而是生长与空间事件

- 彩点不按"一叶一点、一花一点"映射。约 55%-80% 的点可依附在分叉、转折和细线密区，20%-40% 可脱离枝线形成悬浮回声
- 点形混用：湿润墨滴、干涩擦点、不规则叶片碎形、三角／楔形、短色痕、小色面、破圈果实节点；禁止全是圆点
- 大点压重，中点连接，小点制造空气；孤点形成停顿，突然密簇形成爆发，连续碎点形成颤动
- 黑点负责结节和视觉铆钉；高饱和绿、洋红、胭脂、黄、朱红或青色负责跳跃与切割。颜色从源图提取，不自动套用同一组三原色
- 彩点可以被墨线穿过、被墨面压住一角、与纸白相邻或跨越密区边界；不得整齐装饰在线条两侧

### 空白的四种职责

植物画中的白不是剩余背景：

1. **冠层下空白**：托起上部点群，使主干有上升感
2. **线间孔隙**：让密网保持空气，而非变成黑色毛团
3. **路径空白**：让一条长线跨越后更有速度与方向
4. **无地平线白场**：在高度抽象路线中取消自然景深，使点线面成为平面构成

不能机械规定"大留白"。`all_over_growth_field` 可以整体密集，但仍须有大小
不一的微型白隙和局部休止；`upright_canopy` 与 `layered_grove` 则应保留更
明确的疏区。

### 植物色彩路由

| 色彩记忆 | 主色关系 | 点形建议 | 墨彩关系 |
| --- | --- | --- | --- |
| 春日冠层 | 翡翠绿／孔雀绿＋洋红／胭脂＋少量嫩黄 | 叶片碎形、湿点、短色痕 | 绿与黑线穿插，红点在枝梢反拍，黄只作提速 |
| 桃林／花林 | 灰绿／青绿＋珊瑚粉／淡绯 | 细碎粉点、绿楔形、少量黑结点 | 粉点成空气层，灰线建立前后，不铺粉色花云 |
| 抽象花园 | 高饱和绿＋洋红＋朱红＋信号黄中的 2-4 色 | 自由色块、三角碎片、墨滴 | 彩块与墨团并置切割，线穿过色块，允许局部不透明覆盖 |
| 果木 | 赭黄／淡金／米橙＋少量朱红、青绿 | 破圈色面、内点、大小果实节点 | 果实不是写实球体；黑线切入圆面，内点改变重心 |
| 冷色植物 | 青绿／湖蓝／灰紫＋源图暖色一项 | 冷色短痕、灰湿点、少量暖色孤点 | 冷色退入纸白，暖点作为方向转折，不用暖黄旧纸统一调色 |

### 可直接使用的正面 prompt（原文英文，逐字保留）

```text
Read the plant as a relational growth graph, not a botanical object. Preserve the source's
dominant growth axes, load-bearing junctions, density zones and paper-void topology, while
deleting literal leaf-by-leaf and twig-by-twig correspondence. Choose one route: upright
canopy, drifting garden, layered grove, all-over growth field, or fruit-node tree. Mix true
connections, visual overlaps, near-misses and suspended points. Let concentrated wet-and-dry
black lines carry weight; displaced gray lines create rebound, depth and counter-rhythm;
intermittent fine lines build an air layer. Convert leaves, flowers and fruit into unequal ink
and color events—wet dots, dry broken marks, wedges, short strokes, free patches or broken
fruit circles—some attached to growth nodes, others floating as counterbeats. Keep paper white
as active distance between lines. First read: a living point-line relationship and density
rhythm. Second read: the plant. No mechanical tree diagram, no one-leaf-one-dot mapping, no
uniform branch network, no watercolor foliage mass.
```

### 植物关系失败判定（用于质量检查清单）

- 所有枝线都真实连接，像植物学分枝图，没有叠交、近失与悬浮关系
- 所有树都使用相同的粗干、细枝和红绿黄点，未区分冠层、林地、满幅网或果实节点
- 彩点平均撒满全画，或严格贴附在线条上，没有空气层与反拍
- 细线数量很多但同粗、同弯曲幅度、同分叉角度，只形成机械复杂度
- 满幅路线没有密度波与微型白隙；留白路线又把植物删得只剩孤立装饰枝
- 果实、叶与花仍以完整轮廓和写实体积出现，点线面没有获得形式自主性

---

## 3.13C 植物照片艺术化处理：形态识别优先于物种名称（v17 866-936）

**核心立场**：植物照片进入生成前，不先问"这是什么树"，而先判断它以什么
视觉关系成立：粗干承重、花点爆发、果实结节、竖线重复、细线随风，还是叶面
与水面互相托举。物种只影响色彩记忆和少量识别锚点，**照片的主几何、密度、
方向和遮挡关系决定艺术路由**。

### 植物彩墨基础语法

- **主干**：焦墨／浓墨，侧锋提按，粗细突然转换；以扭动的有机骨线概括重量，不刻画树皮。前景主干默认半干或渴笔，允许飞白，湿墨只在转折和交接处积聚
- **细枝**：中墨、淡墨与游丝线连绵穿插；可以叠交、近失、断开或跨越植物个体边界，不必服从真实分枝生理
- **两种结构模式**：`dense_mode` 以大弧度盘旋、回旋和编织形成密网；`sparse_forest_mode` 以大量近垂直简线重复，靠高低、粗细和间距变化形成节拍
- **墨阶**：焦、浓、中、淡灰直接并置，避免用连续柔滑渐变模拟体积。前景偏半干，背景偏淡湿；湿墨点为团簇圆点，干墨点为飞溅碎点
- **形态配额**：植物默认以线和点为主体；大墨面应克制，只可用于少量山石、远景团块、深荫或确有大叶面的题材，不能把树冠涂成水彩云
- **彩点**：小圆点、碎色块、楔形和短色痕，无写实外轮廓、无体积明暗。明黄、玫红、艳绿、浅青为可选矿物色，不是固定四色；先提取源图色彩记忆，再选 2-4 个色轴
- **点墨关系**：彩点沿枝网不等量聚散，黑点与彩点混杂，部分黑点压住彩点；保留少量游离点，使点成为节拍与空间颗粒，而非花叶果实的逐个替身
- **虚实关系**：前景浓实、枝干与点最密；中景中墨、点较疏；背景淡湿灰影、枝形模糊、极少彩点。这个次序可被构图重心局部反转，但不能全幅同浓同密
- **白场**：白色或由源图决定冷暖的生宣纸底是主动空间。白场必须穿入枝线与点群之间，不能以统一背景色或满幅纸纹铺满

### 照片形态卡

```yaml
plant_photo_morphology_card:
  photo_type: old_single_tree | flowering_branch_canopy | dense_flower_shrub | fruit_node_tree | vine_hanging | bamboo_sparse_forest | dense_woodland | grasses_reeds | aquatic_large_leaf | wind_swept_foliage
  dominant_geometry: diagonal | vertical | radial | arching | hanging | all_over | horizontal_wave
  main_trunk_visibility: high | medium | low | none
  canopy_density: sparse | clustered | dense | all_over
  direction_field: []
  overlap_complexity: low | medium | high
  point_source: [flower, bud, fruit, leaf, seed, light, abstract_event]
  source_color_memory: []
  white_space_pattern: under_canopy | interbranch_apertures | vertical_corridors | water_gaps | distributed_micro_voids
  structural_mode: dense_mode | sparse_forest_mode | mixed
  selected_route_reason: string
  reject_from_source: []
```

### 十类照片路由

| 照片形态 | 点／线／面起始值 | 艺术化提炼 | 关键禁项 |
| --- | --- | --- | --- |
| **孤立老树 `old_single_tree`** | 16／70／14 | 以 1-3 条焦浓主干建立重量，删去约 50%-70% 末梢；树冠只留点簇和断线，主干飞白最强 | 写实树皮、完整树冠、每根枝条都接回主干 |
| **仰视花枝 `flowering_branch_canopy`** | 38／55／7 | 保留 2-5 条斜向主势和无地平线构图；花变成粉、红、白彩点的"结—放—再结"，背景枝退为淡灰空气网 | 逐朵五瓣花、均匀撒粉点、透明水彩天空 |
| **密花／灌木 `dense_flower_shrub`** | 58／32／10 | 把数百花叶压成 5-11 个大小悬殊的点簇；少量穿行线连接点簇，内部保留纸白孔隙 | 花海糊成综合色面、逐花描绘、满幅同密度 |
| **果实节点树 `fruit_node_tree`** | 36／50／14 | 粗干分叉承重，果实化为破圆、内点和综合色节点；枝线穿、切、遮果点，大小与圆缺不一 | 写实球体、高光阴影、同大同圆果实 |
| **藤蔓／垂挂 `vine_hanging`** | 34／59／7 | 长线盘旋、垂落后回挑；附着点链有缺口，并加入逆重力细线和悬浮点 | 平行花序、整齐珠链、柔弱装饰曲线 |
| **竹林／疏林 `bamboo_sparse_forest`** | 17／72／11 | 近垂直线重复但高低、浓淡、间距突变；少量斜枝或灰横线反拍，形成可行走的白色竖廊 | 等距栅栏、全部直线同宽、透视林荫道 |
| **密林／杂木 `dense_woodland`** | 26／61／13 | 黑干、中灰枝、淡湿远树分三层；删除叶片，转为黑灰点和极少源色彩点 | 深绿树冠云团、全黑乱网、背景与前景同清晰 |
| **草丛／芦苇 `grasses_reeds`** | 22／70／8 | 以成束长线、断续短线和方向波构成风势；种穗转为稀疏点链，根部可有少量湿墨结 | 每根草等高、机械平行、绿色平涂草坪 |
| **荷叶／水生植物 `aquatic_large_leaf`** | 32／42／26 | 大叶只保留少数偏心墨面或纸白负形；茎为穿水长线，花与水光化为点；水面用断续横线反拍 | 完整圆叶铺满、蓝色水彩底、写实荷花轮廓 |
| **风动枝叶 `wind_swept_foliage`** | 31／58／11 | 先提取统一风向，再让黑线突进、灰线回弹、点簇拖尾；逆向孤线作为阻力 | 每片叶同方向、数字运动模糊、平均弯曲幅度 |

这些数值是照片转译的起点。若照片中最强信息不是植物物种，而是水面、山体、
建筑或天空色场，应由对应主路由控制构图，植物路由只负责局部线点语言。

### 从照片到彩墨的六步压缩

1. **删对象**：先删除约 45%-75% 可逐一对应的叶、花、果和末梢，避免"照片换材质"
2. **立骨架**：提取 3-9 条主生长线与 2-6 个承重结点；先在无彩色条件下建立黑灰白构图
3. **分干湿**：前景焦浓半干，背景淡湿洇润；同一层也允许局部反转，避免机械"近深远浅"
4. **重谱点群**：把源图小单元压缩为大、中、小三档点簇，安排密簇、双点、孤点和悬浮点
5. **保留色忆**：从源图取 2-4 个色轴；彩点可鲜明但总是受黑白骨架统摄，不自动复用明黄、玫红、艳绿、浅青全套
6. **检查白场**：确认白纸以孔隙、通道或大停顿穿过网络；若画面只剩满铺颜色和统一线网，重新删减

### 植物照片统一负面约束（原文英文，逐字保留）

```text
No photorealistic plant rendering, pencil shading, modeled light and volume, detailed bark,
literal leaf veins, complete fruit or flower contours, smooth uniform wire lines, one source
branch copied into one painted branch, continuous realistic terrain, large watercolor foliage
clouds, excessive all-over wet bleeding, pastel transparent washes, equal-size color dots,
evenly spaced points, identical density across the sheet, antique yellow paper by default,
or decorative randomness unrelated to the source growth forces.
```

---

## 3.14 已有线性抽象源图专用规则（v17 937-979）

**触发条件**：源图本身已经以线条完成抽象表达（例如用户上传的已是线描/抽象
构成图，而非写实照片）。默认采用**低干预**策略。

```yaml
source_style_reading:
  source_abstraction_level: high
  primary_information_carrier: line

transformation_policy:
  intervention_level: low
  topology_preservation_target: 0.75-0.90
  detail_deletion_target: 0.10-0.25

point_line_plane:
  point_weight: 5-12
  line_weight: 68-82
  plane_weight: 10-25
  dominant_language: line
```

### 必须保留

- 源图的密度分区，例如上密下疏、中心纠结、两侧分散
- 主要线群的方向、穿插关系、闭合与半闭合形态，以及粗线锚点所在区域
- 原有色场与线网的前后关系；背景颜色不得被新造留白或大墨面替换
- 线的数量感。可以不逐条复制，但观看时必须仍然感到"同等强度的线性世界"

### 只优化

- 等宽线变为三层线级：约 55%-70% 细游丝、20%-35% 中等结构线、5%-12% 浓重骨线
- 线的枯湿、顿挫、飞白、渗化、接笔、断裂和墨色层次
- 局部节奏重音与少量意外，不改变整个构图的视觉重心

### 禁止（原文英文，逐字保留）

```text
Do not simplify an already abstract line field into a few isolated botanical stems.
Do not replace dense angular networks with large blank paper, broad watercolor clouds,
recognizable illustrative lotus leaves, or a new monumental composition. Preserve the
source density map, topological crossings, angular rhythm, vertical progression and
warm-to-cool field placement. Translate material and line hierarchy, not composition.
```

---

## 3.15 摄影性强线源图：线群重谱规则（v17 983-1053）

**触发条件**：梯田、海浪、沙纹、道路、密集屋脊等"照片本身具有强烈线势、
但尚未完成艺术抽象"的输入。**不能套用 §3.14 的低干预保真**，也不能用大面
积水彩面覆盖线势。

```yaml
source_style_reading:
  source_abstraction_level: low | medium
  primary_information_carrier: line
  line_origin: photographic_repetition

transformation_policy:
  intervention_level: medium | high
  macro_topology_preservation: 0.60-0.75
  literal_micro_edge_correspondence_cap: 0.20-0.35
  micro_detail_deletion: 0.45-0.65
  free_rhythmic_line_share: 0.35-0.55

point_line_plane:
  point_weight: 8-15
  line_weight: 72-85
  plane_weight: 7-15
  painted_plane_coverage_cap: 0.10-0.18
  dominant_language: line
```

### 线群重谱执行顺序

1. 选 2-5 个语义锚点和一条总势，先保证远看仍能辨认对象
2. 把相邻 3-7 条摄影轮廓压成一个有起伏的"复合乐句"；不是平均抽掉每隔一条
3. 让一部分线提前停止，一部分跨越两个原有形体继续运行，一部分在空白中接续；制造线与对象边界的错位
4. 在转折、拥堵或碰撞处放少量浓墨孔、短折线或彩点作为重音，不用连续色带填满轮廓之间的区域
5. 保留 50%-70% 的纸白或极淡底场作为视觉上的主要平面；纸白不计入"施墨面"
6. 让远景或次要层级降为淡灰残线，避免每一层景物都拥有同样清晰度

### 梯田专用起始值

```yaml
terrace_field_profile:
  point_weight: 9
  line_weight: 81
  plane_weight: 10
  painted_plane_coverage_cap: 0.14
  paper_white_field: 0.55-0.68
  macro_topology_preservation: 0.65-0.75
  literal_micro_edge_correspondence_cap: 0.25-0.32
  micro_detail_deletion: 0.50-0.62
  rhythm_verbs: [回旋, 逃逸]
```

梯田中的绿色主要由断续短线、细线、稀疏点簇和少量透明薄痕承担，而不是填满
每块田面。前景回旋可最密，中景突然跳跃，远景只留少数淡线；允许几组线跨丘
连接，使观看者先感到旋律，再识别地貌。

正面 prompt（原文英文，逐字保留）：

```text
Preserve the large directional flow and a few recognizable terrace anchors, but do
not trace each agricultural boundary. Compress three to seven neighboring contour
bands into one elastic phrase. Delete roughly half of the literal micro-edges and
recompose the missing energy as wandering, broken, reconnecting ink lines derived
from the terrain flow. Let lines cross local field borders, vanish into paper and
resume elsewhere. Make untouched paper the dominant plane. Carry green mainly as
broken colored lines, small points and thin stains, never as continuous filled fields.
The image should read first as a polyphonic linear rhythm and second as terraced land.
```

负面提示（原文英文，逐字保留）：

```text
Avoid literal topographic tracing, one line for every terrace step, realistic watercolor
landscape rendering, continuous green or yellow field fills, evenly spaced contour rows,
soft mountain washes dominating the sheet, uniform line width, and decorative dots that
are unrelated to structural turns.
```

---

## 3.16 江南水乡专用：屋顶墨面与白墙负形（v17 1056-1231）

**触发条件**：白墙、黑瓦、河道、桥和密集屋舍构成主要视觉关系的输入。
**此路由不能把屋顶处理成"线描轮廓＋灰色填充"，也不能让山景、秋树或水色
压过屋舍的黑白形式。**

```yaml
jiangnan_ink_profile:
  point_weight: 8-15
  line_weight: 30-40
  plane_weight: 45-58
  dominant_language: ink_plane_negative_space_and_water_line
  paper_white_field: 0.38-0.58
  dense_roof_ink_coverage: 0.18-0.28
  wet_roof_mass_share: 0.45-0.65
  semi_wet_roof_mass_share: 0.20-0.35
  dry_roof_mass_share: 0.10-0.25
  sharp_roof_perimeter_cap: 0.20-0.35
  concentrated_ink_core_share: 0.25-0.40
  middle_ink_body_share: 0.30-0.45
  pale_ink_breathing_share: 0.20-0.35
  pure_black_roof_area_cap: 0.08-0.15
  literal_eave_cue_share: 0.08-0.18
  pale_gray_wash_coverage: 0.10-0.22
  high_saturation_color_cap: 0.03-0.08
  individually_traceable_roof_cap: 0.12-0.28
  recognizability_target: 0.48-0.68
  literal_micro_edge_cap: 0.25-0.42
```

### 屋顶不是填色，而是一笔生成的墨面

每个主要屋顶群先作为一个整体墨团成立，而不是先分出每栋房子的屋檐。一个墨
团可合并 2-7 片相邻屋顶，并至少包含三种墨态；**湿墨承担整体体积，浓墨制造
重心，淡墨制造呼吸，干墨只负责极少量方向和骨点**：

1. **湿墨主体**：先水后墨，让墨在湿区中自然扩散、相遇和沉积；形成圆融外缘、深浅过渡和内部墨晕
2. **浓墨核**：在湿墨主体内部或一端注入浓墨，形成自然墨核、回流和沉积；浓而仍润，不成为均匀纯黑剪影
3. **中淡墨过渡**：以中墨连接墨核，以淡墨接向纸白，可出现柔软毛边、云絮状扩散、淡灰晕圈和局部水痕。浓、中、淡必须在同一墨团内协调，而不是把屋顶全部处理成同一深度
4. **少量干墨骨线**：只用于选定屋脊、挑檐或转折，露出纸纹与飞白，为圆融湿墨提供方向对比

一个屋顶墨团不应四边同样清楚。通常只让一两段屋脊或挑檐保持方向提示，具象
屋檐提示不超过墨团可见边缘的约 8%-18%，全部锐边不超过约 20%-35%；其余边界
应圆融扩散、毛边渗化、淡出、相互汇合或与灰墙融接。屋檐线应从湿墨团的浓度
梯度中偶然长出，而不是先画完整轮廓再填黑。**第一眼应读成一团有重量、有水
分的斜向浓淡墨块，第二眼才联想到屋顶。**

### 3.16A 湿墨屋顶生成模块

> 背景：上一轮测试表明，仅写"one wet edge"不足以改变模型偏向——它仍会先
> 生成尖锐干黑屋顶，再在边缘添加小范围模糊。湿墨必须成为独立的**形体生成
> 机制**，而不是后期滤镜式的边缘修饰。

```yaml
wet_roof_module:
  activation: jiangnan_roofs | rain_washed_architecture | waterside_reflection
  water_first_ink_second: required
  wet_mass_share: 0.45-0.65
  semi_wet_transition_share: 0.20-0.35
  dry_directional_share: 0.10-0.25
  sharp_perimeter_cap: 0.20-0.35
  rounded_or_feathered_perimeter_min: 0.45
  internal_value_steps: 3-5
  wet_dry_contrast_required: true
```

湿墨屋顶必须至少出现四项可见特征：

- **圆融轮廓**：不是几何高斯模糊，而是随宣纸纤维不均匀推进的柔边、毛边和局部停水线
- **内部墨晕**：同一屋顶从焦墨核过渡到中墨、淡墨和近纸白，不使用统一黑值
- **水墨回流**：局部出现墨被水推开的浅心、浓边、沉积环或反向水痕
- **墨块相接**：相邻屋顶可在湿区轻微汇合，产生中间色和不可完全分割的屋群
- **干湿对撞**：在一片圆融湿墨旁，只用一小段干笔或锐利屋脊确定方向

不同屋顶不得使用同一种湿度。建议一组屋群中：约一半为湿墨主导，约四分之一
为半湿灰墨，剩余少量为枯笔重音。距离越远，边缘越湿、越淡、越容易与雾和墙
体相融；前景只保留少数干墨挑檐。

正面 prompt（原文英文，逐字保留）：

```text
Form the roofs water-first and ink-second. Let most roof volume emerge from rounded,
feathered wet-ink blooms with three to five internal value steps, capillary spread,
soft gray halos, pigment pooling and occasional backrun rings. Inject concentrated ink
inside the wet mass so black grows organically rather than becoming a flat wedge. Keep
dry, sharp brushwork to only a few ridge and eave fragments. At least forty-five percent
of the roof perimeter should feel rounded, absorbed or softly dissolved into paper.
Contrast one short dry directional edge against a much larger wet, breathing ink body.
```

负面提示（原文英文，逐字保留）：

```text
Avoid all-dry roof masses, charcoal cutout wedges, blade-sharp silhouettes, four crisp
edges, flat black opacity, dry-brush texture covering the entire roof, digital Gaussian
blur added around a hard shape, identical wet halos, and losing all roof direction in
featureless soft clouds.
```

### 3.16B 屋顶墨团化与浓淡协调模块

**触发信号**：当输出仍能逐片看清屋脊、飞檐和三角坡面时，即使边缘已经湿
润，也说明抽象层级仍停留在"具象建筑＋水墨滤镜"。此模块把表达单位从单片
屋顶提升为屋顶群的整体墨团。

```yaml
roof_group_mass_module:
  activation: roof_edges_remain_too_literal | roofs_read_as_separate_wedges
  merge_adjacent_roofs: 2-7
  first_read: single_integrated_breathing_ink_mass
  second_read: clustered_roofs
  concentrated_ink_share: 0.25-0.40
  middle_ink_share: 0.30-0.45
  pale_ink_share: 0.20-0.35
  pure_black_area_cap: 0.08-0.15
  literal_eave_edge_share: 0.08-0.18
  individually_legible_roof_cap: 0.12-0.28
  silhouette_simplification: 0.55-0.75
  internal_value_fusion: required
  wet_concentrated_ink_not_flat_black: required
```

执行规则：

- **先合形，后分浓淡**：先删除大部分屋檐折角，把相邻屋顶压缩成一个偏斜、厚薄不均的整体墨团；不得把几片完整屋顶仅仅叠放在一起
- **浓墨定重心**：浓墨集中于墨团的局部核心、下缘或转折处，约占 25%-40%；浓墨必须含湿润积墨、渗化或回流，不能成为全黑硬块
- **中墨成主体**：中墨连接各浓墨核，是墨团连续性的主要承担者，约占 30%-45%。中墨可吞没原照片中的瓦片、檐角和建筑接缝
- **淡墨留呼吸**：淡墨约占 20%-35%，向白墙、雾气和水面自然过渡，允许墨团局部断气、透纸或消失
- **纯黑是骨点，不是面积**：接近纯黑的部分限制在整个屋顶墨团的约 8%-15%，只作为节奏重音
- **檐线是暗示，不是轮廓**：只留下 1-3 段长度不等、角度不齐的短屋脊或挑檐；不得形成连续三角轮廓，不得让每栋房子都拥有完整屋顶
- **浓淡分布不平均**：一个屋群可以浓墨偏重，另一个屋群可中淡墨偏重；近景不必全部浓，远景也不必全部淡，应由构图重心、遮挡和水气共同决定

正面 prompt（原文英文，逐字保留）：

```text
Merge two to seven adjacent roofs into one integrated, oblique, breathing wet-ink mass.
Do not preserve a row of separate triangular eaves. Simplify fifty-five to seventy-five
percent of literal roof geometry. Build the shared mass from moist concentrated-ink cores,
a connected middle-ink body and pale-ink breathing transitions. Keep near-black pigment to
small rhythmic anchors only, never the whole mass. Let most eaves disappear inside value
fusion; reveal only one to three unequal ridge fragments after the ink body has formed.
The first reading must be an organic cloud-like ink mass with weight and moisture; the
second reading may suggest clustered Jiangnan roofs.
```

负面提示（原文英文，逐字保留）：

```text
Avoid individually outlined roofs, repeated triangular gables, continuous sharp eaves,
uniform soot-black masses, every roof equally dark, every distant roof equally pale,
separate wet blobs arranged like tiles, dry charcoal wedges, and soft blur pasted around
an otherwise literal architectural silhouette.
```

### 并屋成群，避免逐栋说明

- 将相邻 2-5 片屋顶合并成一个不规则黑色节奏群，只保留少数翘角、屋脊和高低错落作为识别锚点
- 只允许约 25%-40% 的屋顶仍可单独对应照片；其余应通过碰撞、覆盖、裁切和墨色相接完成抽象
- 黑墨群之间必须由大小不同的纸白通道分隔，形成"黑块推进—白墙停顿—灰水下沉"的节奏
- 禁止平均排列相似的黑色屋顶，也禁止重复的瓦片短线、统一灰填充和干净矢量边缘

### 白墙以负形成立

- 白墙主要由未施墨纸面构成，不为每堵墙画完整外轮廓
- 至少 30%-50% 的墙体边界应由黑屋顶、门窗墨点、邻墙错位或淡灰水痕共同暗示
- 门窗只保留少量黑点、短竖或小块，不能平均分配给每栋房子
- 允许白墙彼此相连、压扁或错位，使建筑群先成为黑白抽象构成，再成为可辨认的村落

### 水、远山与色彩退居次声部

- 水面优先使用纸白、淡灰垂直水痕与少量断线，不默认铺满青绿色渐变
- 倒影只保留屋顶黑块和白墙负形的松散回声，不做完整镜像
- 即使源图有雪峰、森林或鲜艳秋树，江南路由仍以屋舍黑白为主；远山降为 5%-15% 的淡墨层，树叶压成小型不等量彩点
- 彩色只落在结构转折、生活尺度或路径节点，不能形成大面积完整树冠

正面 prompt（原文英文，逐字保留）：

```text
Build the village from interlocking ink masses and untouched paper, not from outlined
houses. Merge two to five neighboring roofs into each irregular black rhythm group.
Within every main roof mass combine a concentrated ink core, dry-brush paper breaks and
one naturally feathered wet edge. Let only one ridge or eave stay sharp; dissolve, crop
or merge the remaining boundaries. Make the eave line grow out of the moving ink mass
instead of outlining a gray-filled roof. Let white walls exist mainly as negative paper
cut by black roof masses and a few door or window accents. Subordinate mountains, water
color and seasonal foliage to the black-white architectural rhythm.
```

负面提示（原文英文，逐字保留）：

```text
Avoid outlined roofs filled with uniform gray, individually rendered houses, repetitive
roof tiles, equal black wedges, clean vector eaves, four equally sharp roof edges, generic
watercolor village illustration, glossy turquoise water, complete mirrored reflections,
large orange tree crowns, and distant scenery competing with the roof-wall structure.
```

---

## 3.17 江南混合媒介语法：墨彩、油彩、波动水线与倒斜墨块（v17 1235-1337）

江南题材不只依赖纯黑白水墨。生成时可把水墨的透明、渗化与偶发性，与油彩式
的厚薄色层、刮擦和不透明重音组合在同一画面中。这里的"油彩"是**表面语言
与色层机制**，不是要求整幅作品变成厚涂油画。

### 三种混合媒介路由

```yaml
jiangnan_material_route:
  mode: ink_led_opaque_color | oil_led_ink_rhythm | balanced_hybrid
  transparent_ink_underlayer: 0.35-0.60
  opaque_color_patch_share: 0.08-0.22
  dry_scrape_and_scumble: 0.05-0.18
  saturated_point_share: 0.02-0.08
  preserve_paper_or_ground: 0.30-0.55
```

| 路由 | 主体语言 | 适用输入 | 约束 |
| --- | --- | --- | --- |
| 墨主导＋不透明彩 | 水墨晕染、墨块和纸白为骨，局部叠加哑光厚色 | 白墙黑瓦、雨雾、河道 | 厚色不超过局部结构重音，不能覆盖墨气 |
| 油彩主导＋墨线节奏 | 相邻色块、刮擦与覆盖为体，黑色长短线组织方向 | 强光村落、秋色、色彩本身是主题 | 仍需清楚的黑白骨架，不做写实厚涂风景 |
| 均衡混合 | 透明灰墨、综合色块、线与彩点互相穿插 | 多季节、多层景深、复杂水乡 | 必须指定一个主导声部，禁止各占相同比例 |

叠置顺序建议为：**淡墨/综合色底层 → 黑灰结构与倒斜墨块 → 波动水线 → 局部
不透明彩层 → 破局线和彩点**。允许后层刮破前层，使纸白或浅底重新显露。

### 波动水线：水不是一块平涂色面

当自然、江南或山水输入中出现河、湖、池塘、倒影或雨后地面时，水面至少选择
两类水线组合：

- **长波线**：松弛的长弧或水平蛇行线，建立水势
- **碎波线**：短折、短弧、停顿与接续，打散机械平行
- **回旋线**：不完整的椭圆、涟漪或回钩，只在局部形成中心
- **倒影线**：向下拖曳、倾斜、错位的湿墨线，与岸上线条不一一对应
- **逆拍线**：少量斜切或逆向细线，破坏过度平稳

```yaml
water_line_profile:
  line_families: 2-4
  dominant_flow: horizontal | diagonal | circular | mixed
  interrupted_share: 0.30-0.55
  spacing_variation: 0.45-2.80
  local_direction_reversal: 0.05-0.18
  exact_parallelism: forbidden
  exact_reflection_mapping: forbidden
```

水线不得等距平行，不得所有线具有相同振幅和长度。密线区、断线区与完全安静
的水面必须同时存在；水线可穿过淡墨或综合色层，但不能像数字波纹滤镜。

### 倒斜墨块：屋檐、灰墙与倒影的中间语言

"倒斜墨块"指介于可辨认物体与抽象平面之间的倾斜墨形，可来源于屋檐、山石
阴影、灰墙、岸线或水中倒影：

- 将真实屋檐或墙面压缩成不规则梯形、楔形、倾斜矩形或被截断的灰黑块
- 墨块倾斜方向来自源图的屋脊、河岸或倒影势线，但相邻墨块不使用同一角度
- 一组中同时出现浓墨块、半透明灰块和被刮开的综合色块；禁止全部为同尺寸纯黑剪影
- 约 20%-40% 墨块可以越出原物体边界、向水中倒伏或与邻近屋檐合并，使它既像屋檐又像抽象笔触
- 墨块的一边可以锐利，另一边以湿墨扩散或刮擦消失；不要四边整齐

倒斜墨块的功能不是增加更多"面"，而是把具象对象压缩为具有方向和重量的视
觉音符。它必须与水线、纸白和少量彩点形成穿插。

### 具象与半抽象之间的控制

江南题材默认不走完全抽象，也不保持摄影完整度：

```yaml
jiangnan_semi_abstract_balance:
  semantic_anchors: 3-5
  recognizability_target: 0.48-0.68
  macro_topology_preservation: 0.58-0.76
  literal_micro_edge_cap: 0.25-0.42
  fused_or_displaced_form_share: 0.35-0.60
```

保留的是"水岸如何转折、屋群如何聚合、黑瓦与灰白墙如何穿插、倒影位于何
处"等关系；牺牲的是逐栋房屋、完整屋檐、统一透视与准确倒影。观看顺序应
为：**先感到黑白灰和彩的形式关系，再辨认江南水乡，最后发现线与彩点造成
的意外。**

### 破局线与彩点

规整的白墙、屋顶和水岸建立秩序后，必须用少量"越界事件"破坏机械构图：

- 选择 1-3 条自由线：跨过屋顶、穿过纸白、伸入水面或在墨块之外突然停止
- 设置 2-5 个不等量彩点簇；至少一簇偏离几何中心或落在结构边界外
- 彩点可为朱红、胭脂、土黄、柠黄、青绿、钴蓝或由源图提取的锚点色，但每次只选有限色轴
- 点的大小、数量和间距必须不均；可有孤点、双点与密簇，不沿屋檐平均排队
- 破局线和彩点必须回应门窗、行人尺度、花木、灯光、倒影闪烁或路径节点，不能成为无来源装饰

正面 prompt（原文英文，逐字保留）：

```text
Combine transparent ink diffusion with a few opaque, scraped or scumbled color patches.
When water is present, organize it with broken undulating line families, dragged oblique
reflection strokes and quiet gaps rather than a flat colored field. Compress selected
eaves, gray walls and reflections into tilted ink wedges whose angles, opacity and edges
vary. Keep three to five semantic anchors so the scene remains between recognizable and
semi-abstract. After the architectural order is established, introduce only a few free
lines and unequal color-point clusters that cross or escape the grid and create surprise.
```

负面提示（原文英文，逐字保留）：

```text
Avoid flat blue water, digital ripple filters, evenly parallel wave lines, exact mirrored
reflections, identical tilted rectangles, uniform gray walls, roof blocks arranged on a
clean grid, pure watercolor softness everywhere, thick oil paint covering all paper and
ink, equal-size color dots, decorative confetti, and total abstraction that loses the
waterfront topology.
```

---

## 3.18 都市墨色体积模块：高低错落与现代平面构成（v17 1339-1445）

**触发条件**：城市全景、密集建筑群、天际线、商业中心与高低混杂的街区。核
心不是逐栋描绘建筑，而是将城市重组为**不同墨色、不同体积、不同高度的面群
关系**。

```yaml
urban_ink_volume_module:
  activation: dense_building_mass_and_skyline_are_primary
  point_weight: 10-20
  line_weight: 18-30
  plane_weight: 50-68
  dominant_language: tonal_ink_volume_assembly
  merge_buildings_per_volume: 3-12
  major_volume_groups: 7-16
  individually_legible_building_cap: 0.15-0.30
  literal_window_grid_cap: 0.05-0.18
  perspective_required: false
  spatial_modes: [flattened_frontality, stacked_strata, compressed_depth, multi_view_collage]
  concentrated_ink_share: 0.12-0.22
  middle_ink_share: 0.32-0.46
  pale_ink_share: 0.24-0.38
  paper_or_color_gap_share: 0.12-0.25
  overlap_or_interlock_share: 0.30-0.55
  skyline_height_tiers: 4-7
  height_outliers: 1-3
```

> 注：这里的 `plane_weight: 50-68` 与 `spatial_modes` 字段和
> `01-composition-routing.md` 里 `composition_mode.choose_from` 的
> `urban_ink_volume` / `urban_grid_variation` 两个骨架相呼应——本节是那两
> 个骨架**选定之后**的点/线/面执行细则，两个文件应联合读取，不要在
> 01 文件里重复本节的百分比数字。

### 从"建筑"转成"墨色体积"

- 先识别城市中的高度层级、宽窄节奏、密度带和 2-5 个地标，不从窗户、立面或透视线开始
- 将相邻 3-12 栋楼压缩为一个体积群。一个体积可以由浓墨核、中墨主体、淡墨边缘和纸白切口共同组成，不要求保持单栋建筑的完整矩形
- 主要体积群控制在约 7-16 个。它们应大小悬殊、浓淡不等、上下错位，不能成为相似矩形的整齐排列
- 只允许约 15%-30% 的建筑仍可单独对应照片；其余应被合并、遮挡、截断、压扁、拉高或转为缝隙
- 窗格和立面线只作为局部纹理，最多保留约 5%-18%；不能用满楼小格子制造"城市感"

### 四级墨色体积与重量

1. **浓墨重块**：约占施墨体积的 12%-22%，集中在少数基座、竖向锚点或块群交接处。浓墨不必纯黑，可含湿润墨核、干擦和纸缝
2. **中墨连接体**：约占 32%-46%，是城市连续性的主体，负责把高楼、低楼和街区拼成可阅读的整体节奏
3. **淡墨退让体**：约占 24%-38%，可透明、渗化、半消失，与天空或底色相接，制造远近和停顿
4. **纸白／色底缝隙**：约占 12%-25%，以窄缝、竖槽、天井、街道空隙或被裁开的形体出现，使密集体积仍能呼吸

不同墨阶不得按"前深后浅"机械分层。近处可以有淡块，远处可以有浓重地标；
墨色首先服务于构图重量，其次才暗示空间。

### 不依赖透视的现代构成法

每张都市图选择一种主空间模式，最多再加一种辅助模式：

- **压平正面**：楼体正面化，取消大部分侧面和消失线，依靠高度、宽度和墨阶构成
- **分层叠置**：把前、中、后景压成 3-5 条相互遮挡的横向城市带；各带内部仍有高度突变
- **压缩景深**：保留少量空间提示，但减弱尺度递减，让远近建筑像被推向同一平面
- **多视点拼接**：局部楼体可采用不同视角或轻微倾斜，只要总体重心、竖向节奏和地标关系成立

禁止在同一画面同时保留完整单点透视、完整立面细节和逐栋比例。若取消透视，
空间应通过以下至少三项建立：**叠压、墨阶、透明度、边缘清晰度、纸缝宽度、
体积尺度跳变**。

### 高低错落不是随机锯齿

天际线按不等节拍组织，例如：

```text
低密基座 → 中高密集 → 单一突高 → 快速骤降 → 横向停顿 → 次高反拍 → 低层收束
```

- 使用 4-7 个高度层级，并设置 1-3 个明显突高体作为节奏峰值
- 连续三组体积不得同时拥有相近高度、宽度和墨色；至少改变其中两项
- 体积之间以叠压、咬合、穿插、窄缝和错轴建立关系，不用等距留缝
- 最大高楼不必严格居中；即使源图居中，也可轻微偏移或用另一墨块形成不对称制衡
- 低层建筑不是"填满底部"的杂碎，可压成 1-3 条连续但起伏不齐的横向基座

### 边缘、线与点的辅助作用

- 约 25%-45% 的体积边缘可以较清楚，用于锁定建筑感；其余边缘应有断裂、渗化、覆盖或与相邻墨块共边
- 结构线只保留少量竖向、横向和斜向接缝；允许线跨过多个体积，成为城市整体节拍，而不是每栋楼的轮廓
- 门窗、灯光、车辆和标识转为大小不等的墨点、彩点和短色痕。点应成簇、停顿或孤立，不按窗格等距排列
- 可加入 1-3 条偏离楼体边缘的自由线或斜线，破坏过度规整的矩形秩序

### 源图配色记忆

城市不能固定套用黑白＋三原色。先提取天空、日照、玻璃、砖墙和夜灯的主色
记忆：

- 大面积天空可转为一个透明色场或纸白场，不逐朵描云
- 日照建筑可变成少量不透明暖色块或刮擦色面，与淡墨体积叠置
- 玻璃蓝、暮色紫、砖红、砂岩黄、钠灯橙等均可成为本图色轴，但每次只选择 1 个主色族和 1-2 个反拍色
- 彩色体积不应平均分配给所有楼群；色彩集中在少数节奏峰值、地标或横向基座

正面 prompt（原文英文，逐字保留）：

```text
Recompose the city as seven to sixteen unequal tonal ink volumes rather than a collection
of individually rendered buildings. Merge three to twelve neighboring structures into
each volume. Combine concentrated dark anchors, connected middle-gray bodies, pale
retreating masses and narrow paper or color gaps. Flatten or compress perspective when it
strengthens the composition; create space through overlap, tonal steps, transparency,
edge clarity and scale jumps. Build the skyline as an uneven phrase of low clusters,
dense mid-rise blocks, one sudden peak, abrupt drops, pauses and secondary counterpeaks.
Let planes interlock, overlap, crop and share edges. Keep only sparse structural lines,
window points and color accents. The first reading must be a modern arrangement of ink
volumes; the second reading may reveal a specific city.
```

负面提示（原文英文，逐字保留）：

```text
Avoid architectural rendering, photographic skyline, one building per rectangle, every
facade outlined, repeated window grids, equal-width towers, evenly stepped heights,
histogram skyline, strict one-point perspective, compulsory isometric depth, uniform
front-dark back-light grading, identical gray blocks, hard vector edges everywhere,
miniature city illustration, excessive street details, generic neon dots, text, logos,
signatures, seals and watermarks.
```

---

## 待办

- [ ] 核对 `plant_relation_card`（本文件 §3.13B）与 `00-source-diagnosis-card.md`
      里 `plant_relation` 冻结诊断卡字段是否一致；若诊断卡尚未定义这些字
      段，应直接采用本文件的 schema，不要另造一套
- [ ] §3.13-3.18 每条规则按 P0 三级分类（全局强制／题材触发／可选装饰）
      打标——目前本文件里的内容基本都属于"题材触发规则"（因为都挂在
      `activation` 条件下），但其中的通用负面提示（如"forbidden uniform
      blur"类）可能同时也是全局强制规则的重复表述，需要与
      `02a-ink-base-rules.md`（尚未整理）对照去重
- [ ] `subject_routing_table.json` 需要补上本文件覆盖的题材类目：森林/竹
      林、藤蔓垂花、植物照片十类、线性抽象源图、梯田/强线摄影、江南水乡、
      都市天际线——目前该 json 里这些路由多数仍是 `null`
- [ ] `01-composition-routing.md` 与本文件在"都市"和"梯田/高角度压平"两
      处有交叉，写 `06-prompt-compiler-spec.md` 时要确认两个文件的字段不
      冲突、不重复定义
