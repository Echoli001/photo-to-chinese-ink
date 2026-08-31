# P6 回归测试照片清单

> 由 Claude 根据文件名 + 逐张视觉核对生成。文件名是你自己按题材命名的，这里只是把
> 它们对应到 `scripts/data/subject_routing_table.json` 里的 13 个 `subject_category`
> 枚举值，方便后续跑 `router.py` 时直接用。

## 映射表（24 张）

| 文件名 | subject_category | 说明 |
|---|---|---|
| 乱花.jpeg | `flower_branch` | 玉兰/辛夷花蕾枝头特写，蓝天背景 |
| 乱花1.jpg | `flower_branch` | 苹果花/海棠花枝，绿叶背景 |
| 乱花2.jpeg | `flower_branch` ⚠️ | 白色密集小花簇特写（近似醉鱼草），偏"枝头"而非"花海"大场景，与 flower_field 有点像，见下方说明 |
| 乱花2.jpg | `flower_field` | 蓟属野花田，蓝天白云，大场景 |
| 乱花4.jpg | `flower_branch` | 藤蔓穗状花序，攀爬围栏 |
| 古建筑.jpg | `ancient_architecture` | — |
| 古建筑1.jpeg | `ancient_architecture` | — |
| 梯田.jpeg | `terraced_field` | — |
| 森林.jpeg | `forest_bamboo` ⚠️ | 实为白桦/针叶混交林秋景，不是竹林，与 label"森林/竹林"字面有出入，见下方说明 |
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

## 类目覆盖统计

| subject_category | 张数 |
|---|---|
| fishing_port | 5 |
| flower_branch | 3~4（含 1 张存疑） |
| urban_night | 3 |
| ancient_architecture | 2 |
| jiangnan_water_town | 2 |
| urban_day | 2 |
| mountain_snow | 2 |
| flower_field | 1~2（含 1 张存疑） |
| terraced_field | 1 |
| forest_bamboo | 1（内容与 label 有出入） |
| river_lake_reflection | 1（内容与 label 不完全贴合） |
| **farmland_grid** | **0** |
| **abstract_line_network** | **0** |

## 需要你确认的三件事

1. **`乱花2.jpeg`**：我判断偏 `flower_branch`（是一丛花枝特写，不是大场景花海），但它密集小花簇的观感也很像 `flower_field`（label 是"花海/密集光斑"）。如果你想让它测 `flower_field` 路由，改文件名成 `乱花3.jpg` 之类避免和 `乱花2.jpg` 撞名，或者告诉我直接按 `flower_field` 处理。
2. **`森林.jpeg`**：实际内容是秋季白桦+针叶混交林，不是竹林。13 类里 `forest_bamboo` 目前是唯一能落的类目，但如果 v17 原文对"竹林"和"普通森林"有不同的构图/墨符号规则，这张测试图可能测不出竹林专属的部分——你要是有专门的竹林照片，可以再补一张。
3. **`farmland_grid`（农田网格阵列）和 `abstract_line_network`（抽象线网）这两类完全没有测试照片覆盖**——如果这两类在 v17 里有独立的路由规则要验证，P6 阶段跑完整回归测试时会漏掉，需要你之后补几张。

其余 21 张分类都比较确定，不需要你额外确认。
