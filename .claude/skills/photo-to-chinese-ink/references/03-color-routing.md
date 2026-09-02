# 动态色域与纸色路由

> 来源：v17 第 3.1C 节（宣纸色彩路由，原文第 287–328 行）+ 第 4 章"色彩"
> （原文第 1449–1588 行）。以下内容为原文逐字/逐表迻录，未做改写或补充。

## 4.1 总原则（对应 v17 §4.1）

- 黑、白、灰是高频结构底盘，但不是所有作品的固定色卡。题材、季节、媒介、光线和情绪可以改变主导色场。
- "黑白为主、三原色点醒"是重要母型：彩点以极小面积获得高视觉权重。但三种原色不必同时出现，也不必使用标准印刷红、黄、蓝；可转为朱红/胭脂、柠黄/土黄、钴蓝/群青/青绿等"破原色"。
- 彩色既可作为点，也可成为短线、薄层或局部小面；颜色的承载方式必须随点线面分配改变。
- 色彩服从节奏和情感，不机械复制对象固有色；允许保留一至两个源图锚点色，再对其余颜色做压缩、移位或冷暖翻转。
- 多样性来自**色场、明度、冷暖、纯度、面积和位置**的变化，不等于每张图增加更多颜色。
- 避免数码霓虹、均匀高饱和、整片渐变、等量彩虹色和无主次的"撒彩纸屑"。

对 Yan Gallery 135 张公开预览图的图像统计显示：高饱和区域的中位面积约 11.7%，高亮区域中位面积约 40.8%，深暗区域中位面积约 8.7%。该组图为珂罗版复制品预览，数值只能作为生成启发，不应被当作原作测色标准。

权威馆藏文字提供了三个可执行的依据：香港艺术馆指出《水乡》以银灰、白墙、黑瓦为底，红黄绿只占极小面积，却像宝石一样集中发亮；《城市之夜》则让强烈红黄绿点面在黑白灰之上"舞动"；《补网》以一笔浓黑网架反衬彩色人物点。新加坡国家文物局的馆藏说明也指出，他从民间艺术吸收鲜明红、黄、绿以激活画面。由此，黑白与彩色不是固定比例，而是"结构底盘—色彩事件"的动态关系。

## 4.2 色彩路由器（对应 v17 §4.2）

每次生成前，先分析输入，再选择一种主配色模式。**不得直接套用上一次的颜色词。**

```yaml
color_input:
  dominant_hues: []                 # 源图面积最大的 1-3 个色相
  anchor_hues_to_keep: []           # 最多保留 2 个具有题材意义的颜色
  warm_cool_bias: warm | cool | balanced
  value_structure: high_key | mid_key | low_key | high_contrast
  source_saturation: low | medium | high
  season_time_weather: []
  emotional_temperature: quiet | fresh | festive | austere | restless | solemn

color_route:
  palette_mode: one_of_the_modes_below
  material_color_mode: transparent_ink | opaque_color | scraped_color | mixed
  achromatic_base: []
  dominant_chromatic_family: []
  secondary_chromatic_family: []
  accent_hues: []
  chromatic_carrier: point | line | plane | mixed
  transparent_to_opaque_balance: 0.0-1.0
  high_chroma_coverage_cap: 0.00-0.30
  painted_color_coverage_cap: 0.00-0.45
  forbidden_recent_palette: []
```

选择逻辑：

```text
1. 先判断画面需要高调、低调还是强反差，不先选红黄蓝。
2. 从源图保留最多两个锚点色；其余颜色根据情绪重新映射。
3. 选择一个主色家族、一个辅色家族和 0-3 个跳色；只有"全彩密点"模式允许更多色相。
4. 明确颜色由点、线还是面承担；不得所有颜色都变成相同大小的圆点。
5. 若会话中已有作品，默认避开最近三张的"主色家族＋跳色组合"；题材明确要求时除外。
6. 每条生成提示必须列出目标色、面积上限以及本次禁用的惯性配色。
```

## 4.3 配色模式库（对应 v17 §4.3）

`color_route.palette_mode` 从下表中选择一个：

| 模式 | 无彩/底色 | 主色与辅色 | 跳色 | 高纯度面积 | 适用与处理 |
| --- | --- | --- | --- | --- | --- |
| 纯水墨/近单色 | 纸白、墨黑、五级灰 | 无或极淡灰紫/灰蓝 | 0-1 个朱砂点 | 0%-3% | 枯荷、老树、雪山、肃穆题材；以墨色层次而非彩色变化取胜 |
| 银灰江南＋破原色 | 暖白、银灰、墨黑 | 极淡青灰或米灰 | 红＋黄＋绿/蓝中任选 1-3 色 | 2%-8% | 白墙黑瓦、水乡、村落；彩点极少但集中，不得平均撒满 |
| 黑底宝石色 | 黑、深灰、铅白 | 靛青或深紫 | 胭脂、金黄、翠绿、湖蓝 | 8%-18% | 都市夜景、密网抽象；色点可成为主音，但黑色仍承担结构 |
| 冷雾靛青 | 纸白、淡灰、烟灰 | 靛蓝、灰蓝、青灰 | 极少锈红或柠黄 | 3%-12% | 雨、雾、江河、远山；色层透明，避免固定"灰蓝＋橙红"组合 |
| 春林黄绿 | 暖白、浅灰、少量墨黑 | 嫩黄绿、草绿、青绿 | 珊瑚红或钴蓝择一 | 8%-20% | 春林、竹、田野；以多种绿的明度差和疏密变化形成生机 |
| 青碧水域 | 纸白、灰黑 | 松石青、湖蓝、孔雀绿 | 朱红、橙黄或粉红择一 | 8%-22% | 池塘、海岸、南方景物；水色可成薄面，暖色只作反拍 |
| 粉紫花木 | 纸白、淡墨、灰绿 | 胭脂、洋红、藕粉、灰紫 | 黄绿、橙或青蓝择一 | 10%-25% | 花海、桃林、紫藤；同色家族内部要有浓淡、枯湿和冷暖偏移 |
| 赤赭秋山 | 米白、焦墨、暖灰 | 朱红、赭石、焦茶、土黄 | 少量青绿或群青 | 8%-24% | 红叶、秋山、黄土、夕照；以暖色簇与冷色小缝形成对照 |
| 土黄岩地 | 米白、炭黑、石灰色 | 黄赭、沙褐、橄榄绿 | 暗红或冷蓝择一 | 5%-18% | 岩山、村寨、荒原；降低纯度，用材质色差代替鲜艳彩点 |
| 高调淡彩 | 大量纸白、珍珠灰 | 淡粉、浅黄、薄荷绿、浅青 | 1-2 个浓色点 | 3%-12% | 雪景、早春、轻盈建筑；颜色像水迹，不使用糖果般平均粉彩 |
| 全彩密点/色场 | 白底或黑底二选一 | 选一个主导色族 | 另外 4-7 个不等量色相 | 15%-30% | 花团、都市密度、晚期抽象；必须有主导色与空隙，禁止等量彩虹 |
| 油彩记忆 | 暖灰或综合色底 | 邻近色大块＋冷暖对照色 | 少量高纯色刮点 | 15%-35% | 当源图的色彩本身是主题时；保留油画式综合色块，但仍用水墨线网控制 |
| 江南墨彩油彩混合 | 纸白、银灰、墨黑 | 淡青灰/米灰透明墨层＋1 个低纯度不透明色族 | 1-3 种不等量宝石色点或刮色 | 3%-12% | 水乡、河道、灰墙；透明墨气为底，不透明彩只压在屋檐、墙角、水光或路径节点 |

## 4.4 "三原色点缀"的多样化写法（对应 v17 §4.4）

三原色不是一个固定 RGB 色号，而是一组高对比色彩角色。**每张图只选一条轴，不连续复用**：

| 原色轴 | 红系 | 黄系 | 蓝/绿系 | 气质 |
| --- | --- | --- | --- | --- |
| 经典清亮 | 朱红 | 柠黄 | 钴蓝 | 明快、现代、几何感强 |
| 江南民间 | 胭脂红 | 土黄 | 翠绿 | 温暖、生活化、适合小彩点 |
| 冷暖克制 | 锈红 | 灰黄 | 靛蓝 | 含蓄、安静、适合雨雾与建筑 |
| 春日偏移 | 珊瑚红 | 嫩黄绿 | 湖蓝 | 清新、轻盈、适合植物与水域 |
| 夜色宝石 | 洋红 | 琥珀黄 | 孔雀绿/群青 | 强烈、跳跃、适合暗底 |
| 秋地矿物 | 赭红 | 金土黄 | 蓝绿灰 | 厚重、质朴、适合山地和秋林 |

约束：

- 默认不让红、黄、蓝/绿三者等量；建议视觉权重约 5:3:2、6:3:1 或只出现其中两色。
- 彩点的大小、形状、透明度和边缘必须不一致；允许一色成簇，另两色各自孤立。
- 原色可被墨、水、纸色"折损"：半透明、偏灰、混浊、擦除比纯色填充更自然。
- 当源图已有强烈主色，如花海的粉红或森林的绿色，三原色应退为对照角色，不得覆盖主色记忆。

## 4.5 面积与纯度控制（对应 v17 §4.5）

- 默认彩色面积：5%-15%。
- 稀疏留白画面：1%-8%。
- 密网或抽象画面：10%-22%，但单一高饱和色不宜占据主导。
- 当"色彩本身就是题材"时，可提高到 22%-35%，但至少 40% 的彩色应为低纯度、透明或被墨打断的综合色。
- 至少保留一种主导无彩色关系：白多于灰、灰多于黑，或黑色骨架穿插亮底。
- 区分"彩色覆盖面积"与"彩色视觉权重"：极小的纯红点可能比一大片灰绿色更响亮。

## 4.6 防止配色惯性（对应 v17 §4.6）— 二元否决触发条件

以下情况判定为**配色失败**，需要重新路由（同步计入 `05-quality-checklist.md` 的否决项）：

- 连续三张都使用"灰蓝/灰绿＋珊瑚红＋橙黄"。
- 无论源图季节和光线为何，纸面都被处理成相同的米黄旧纸。
- 所有题材都以黑白为主、红黄绿平均撒点，缺少近单色、冷雾、暖土、青碧或粉紫模式。
- 彩色只承担圆点，从不进入短线、薄面、擦痕或水渍。
- 为追求多样性而使用等量彩虹色，导致没有主色和节奏层级。

每次输出前应生成一行内部色彩决策：

```text
Palette = [模式]；Value = [高调/中调/低调/强反差]；
Dominant = [主色家族]；Counterpoint = [对照色]；Carrier = [点/线/面]；
High-chroma cap = [百分比]；Avoid = [最近使用或本题不适合的色组]。
```

## 4.7 生成提示词模板（对应 v17 §4.7，英文原文，供 compiler 直接嵌入）

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

## 4.8 研究依据（对应 v17 §4.8）

- Hong Kong Museum of Art, *Wu Guanzhong's Paintings and Personal Archives*: `https://hk.art.museum/en/web/ma/collections/wu-guanzhongs-paintings-and-personal-archives.html`
- National Heritage Board / National Gallery Singapore, *Thick Leaves*: `https://www.roots.gov.sg/collection-landing/listing/1320797`
- Asia Society, *Revolutionary Ink: The Paintings of Wu Guanzhong*: 上传研究文档中强调明亮色彩、自由水洗与激进构图对传统水墨的突破。

---

## `paper_color_router`：宣纸色彩路由（对应 v17 §3.1C，原文第 287–328 行）

**生宣、熟宣描述的是纸张对水墨的反应，不自动规定纸张必须泛黄。** 纸的吸水性、纤维反应与纸面色相必须作为两套独立变量。不得把"暖米色、旧纸斑驳、仿古纤维纹"当成中国水墨的固定背景。

生成前必须从源图重新选择纸色：

| 纸色模式 | 适用条件 | 视觉要求 |
| --- | --- | --- |
| 洁白生宣 | 高调摄影、白墙、雪景、花卉、明亮天空、清洁现代构图，或用户要求白纸 | 白而不发黄；依靠墨迹边缘显出纤维，不做纯数字白底，也不叠加旧纸污渍 |
| 冷白生宣 | 蓝天、雪山、清晨、水景、冷色植物等源图 | 轻微蓝灰倾向只能来自纸色平衡，不得变成蓝色水彩底 |
| 中性白生宣 | 默认模式；源图冷暖较均衡或色彩需要真实保留 | 不抢色，不统一改变原图色温；纸白是主要留白 |
| 自然白生宣 | 源图本身温润、乡土、秋景或室内暖光，但仍需清洁纸面 | 仅轻微象牙倾向；不能出现明显黄褐做旧 |
| 暖象牙纸 | 暖色历史场景、夕照、赭石建筑，并且暖纸确实能加强构图 | 暖度低于画中色层；夕阳必须由颜料和墨彩承担，不能靠整张纸发黄 |
| 仿古米黄／旧纸 | **仅当用户明确要求**古纸、手卷旧貌、历史档案感 | 必须显式选择；**禁止作为自动默认值** |

**选择优先级：**

1. 用户明确指定的纸色。
2. 源图大面积亮部、白墙、天空、雪、水光等负形的实际冷暖。
3. 选定配色与墨阶是否需要中性承托。
4. 题材惯例只能作为弱参考；"古建筑、江南、水墨"不能自动触发黄纸。

**硬性规则：**

- 默认候选顺序为：`clean_white → neutral_white → cool_white → natural_white`；暖象牙纸必须说明理由，仿古米黄纸必须由用户显式触发。
- 同一批测试图不得无理由复用相同纸色；纸色也属于每张图的配色路由。
- 纸面色不承担夕阳、秋色、夜色或雾气。环境色必须由墨、矿物色、油彩式刮色或留白关系建立。
- 白色宣纸不等于无材质：纸纤维只应在墨水沁化、干笔摩擦和局部侧光处轻微显现。
- 禁止全画面均匀的高对比纤维、褐色污点、折痕、泛黄边缘或旧纸噪点。
- 若去掉所有笔墨和彩色后，纸面自身仍像一张显眼的复古纹理素材，则判定纸张材质过度。
- 原图具有清澈蓝天、白墙、粉花、雪地或现代高调光线时，优先使用洁白或冷白生宣，让源图的色彩记忆通过彩墨与彩点保留，而不是被暖纸统一染黄。

白宣纸路线可直接加入 prompt（英文原文）：

```text
Use clean white highly absorbent raw xuan paper. The paper is white, fresh and
unaged—not beige, cream, sepia or antique parchment. Keep most of the sheet quiet
and nearly texture-free; reveal subtle fibers only where wet ink feathers or dry
brush drags across them. Carry all environmental warmth in the ink-mixed color,
mineral pigment or scraped opaque passages, never by yellowing the entire paper.
No global paper texture, brown mottling, stains, deckled dark edges or vintage filter.
```

## 与 `04-subject-routing-table.md` 的联动

v17 原文未给出"某主体类目自动锁定某种纸色/配色模式"的显式映射表——纸色与配色的选择流程（见上方"选择优先级"与 §4.2 选择逻辑）本身就是**每次都从源图重新判断**，不是按题材查表。因此 `04-subject-routing-table.md` 的 13 类主体路由表**不需要**、也不应该额外增加色彩覆盖规则；`subject_routing_table.json` 的 `route_schema` 里没有色彩字段是正确的，色彩路由始终独立于主体路由单独运行一次。
