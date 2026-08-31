# 构图路由 — composition_mode

> 状态：骨架。六种模式的**名称**已经从 v17 YAML 协议块（约第 1805–2274
> 行，`composition_mode` 枚举）确认，每种模式的具体判定条件、构图口诀、
> 适用/禁用场景需要从 v17 第 2 章"构图"正文拆入。

## 六种构图模式（已确认名称，待补判定条件与说明）

| 模式 | 中文含义（待核对） | 适用场景（TODO） | 禁用/慎用场景（TODO） |
|---|---|---|---|
| `jiangnan_geometry` | 江南几何（白墙黑瓦式的几何切割） | | |
| `monumental_void` | 纪念碑式留白（大山大水式的巨物+大面积留白） | | |
| `panoramic_flow` | 全景流动（横向展开的连续性构图） | | |
| `immersive_network` | 沉浸式网络（密集线网/枝蔓包裹式构图） | | |
| `urban_ink_volume` | 城市水墨体量（都市建筑的墨块化处理） | | |
| `urban_grid_variation` | 城市网格变体（都市夜景/灯光网格的变奏） | | |

## 与诊断卡的关系

`composition_mode` 的选择应该主要依据 `00-source-diagnosis-card.md` 里的
`point_line_plane_dependency` 和 `perspective` 字段，而不是单纯看题材名字
——比如"都市"题材，白天可能更适合 `urban_ink_volume`，夜景可能更适合
`urban_grid_variation`，这个判断依据需要对照 v17 原文补充。

## TODO（需要人工从 v17 拆入的内容）

- [ ] 六种模式各自的详细判定条件、口诀、代表性技法
- [ ] 每种模式与 13 类主体路由表（`04-subject-routing-table.md`）之间的
      对应关系——例如某个主体类目默认走哪个 composition_mode 作为主路线
- [ ] v17 第 2 章原文中给出的构图反例（不要做成什么样子）
