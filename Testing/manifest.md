# P6 回归测试照片清单

> 由 Claude 根据文件名 + 逐张视觉核对生成。文件名是你自己按题材命名的，这里只是把
> 它们对应到 `scripts/data/subject_routing_table.json` 里的 13 个 `subject_category`
> 枚举值，方便后续跑 `router.py` 时直接用。

## 映射表（30 张）

| 文件名 | subject_category | 说明 |
|---|---|---|
| 乱花.jpeg | `flower_branch` | 玉兰/辛夷花蕾枝头特写，蓝天背景 |
| 乱花1.jpg | `flower_branch` | 苹果花/海棠花枝，绿叶背景 |
| 乱花2.jpeg | `flower_field` | 白色密集小花簇（近似醉鱼草）+ 虚化背景，你确认按 flower_field 处理（原判为 flower_branch，已按你的说明改） |
| 乱花2.jpg | `flower_field` | 蓟属野花田，蓝天白云，大场景 |
| 乱花4.jpg | `flower_branch` | 藤蔓穗状花序，攀爬围栏 |
| 古建筑.jpg | `ancient_architecture` | — |
| 古建筑1.jpeg | `ancient_architecture` | — |
| 梯田.jpeg | `terraced_field` | — |
| 森林.jpeg | `forest_bamboo` ⚠️ | 实为白桦/针叶混交林秋景，不是竹林，与 label"森林/竹林"字面有出入，见下方说明 |
| 森林2.jpeg | `forest_bamboo` | 竹林逆光，晨雾/水面反光，密集竹竿构图，真实竹林 |
| 森林3.jpg | `forest_bamboo` | 竹林雨后特写，竹竿+竹叶带水珠 |
| 水乡.jpg | `jiangnan_water_town` | — |
| 水乡1.jpeg | `jiangnan_water_town` | — |
| 渔港.jpg | `fishing_port` | — |
| 渔港1.jpg | `fishing_port` | — |
| 渔港2.jpeg | `fishing_port` | — |
| 渔港3.jpeg | `fishing_port` | — |
| 渔港3.jpg | `fishing_port` | — |
| 漓江.png | `river_lake_reflection` ⚠️ | 经典喀斯特峰林+江面倒影，13 类里没有"普通山峦（非雪山）"专属类目，暂归入江河倒影类，见下方说明 |
| 都市夜晚.jpeg | `urban_night` | — |
| 都市夜晚1.jpeg | `urban_night` | — |
| 都市夜晚3.jpeg | `urban_night` | — |
| 都市白天.jpeg | `urban_day` | — |
| 都市白天.jpg | `urban_day` | — |
| 雪山.jpeg | `mountain_snow` | — |
| 雪山1.jpg | `mountain_snow` | — |
| farmland_grid.jpg | `farmland_grid` | 航拍农田拼接色块+田埂网格，风力发电机点缀远景，大场景网格感强 |
| abstract_line_network1.jpeg | `abstract_line_network` | 蓝色发散放射状线条，矢量抽象图（EPS 素材，深色背景） |
| abstract_line_network2.jpeg | `abstract_line_network` | 灰蓝色流线/涡旋纹理，矢量抽象图 |

## 类目覆盖统计

| subject_category | 张数 |
|---|---|
| fishing_port | 5 |
| flower_branch | 3 |
| forest_bamboo | 3（含 1 张内容与 label 有出入） |
| urban_night | 3 |
| abstract_line_network | 2 |
| ancient_architecture | 2 |
| jiangnan_water_town | 2 |
| urban_day | 2 |
| mountain_snow | 2 |
| flower_field | 2 |
| terraced_field | 1 |
| river_lake_reflection | 1（内容与 label 不完全贴合） |
| farmland_grid | 1 |

13 类现在全部有照片覆盖（共 29 张，`abstract_line_network.jpeg` 已删除，见下方说明）。

## 已确认事项

1. **`乱花2.jpeg`**：已按你的说明（"乱花2属于花园 flower_filed"）改为 `flower_field`，✅ 已处理。
2. **`森林.jpeg`**：实际内容仍是秋季白桦+针叶混交林、不是竹林——`森林2.jpeg`/`森林3.jpg` 是真实竹林照片，✅ 已解决"没有真竹林测试图"的问题。`森林.jpeg` 保留在 `forest_bamboo` 类下作为"非典型竹林/混交林"边界测试样本。
3. **`漓江.png`**：13 类里没有"普通山峦（非雪山）"专属类目，✅ 你已确认维持原判，归入 `river_lake_reflection`，不新增类目。
4. **`abstract_line_network.jpeg`**：数据机房走廊实景照片，与另外两张矢量抽象图风格不一致，且找不到更合适的纯线条/网格图形素材——✅ 你已确认直接删除，不测这个边界案例。文件已从 `Testing/` 目录移除，该类目下现有 `abstract_line_network1.jpeg`、`abstract_line_network2.jpeg` 两张矢量抽象图继续用于 P6 测试。
