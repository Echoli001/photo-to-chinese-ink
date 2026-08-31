# 源图诊断卡 — Schema 与判定维度

> 状态：骨架，字段名已根据 v17 YAML 生成协议（`visual_grammar.source_diagnosis`
> 一节，约在 v17 第 1805–2274 行的 YAML 协议块内）和用户既定的六张卡设计
> 整理，具体每个维度"怎么打分/怎么判断"的详细文字说明尚未从 v17 正文
> （第 1 章"结构提取"）拆入，需要人工核对填充。

## 用途

这是整个流程的第 1 步产出。模型看图（或读文字）后，按下面的 schema
输出一份 JSON，作为路由脚本和编译脚本的唯一输入。**不要跳过某个字段
直接编造合理值** —— 图里看不出来的维度，诚实标 `"unknown"`，而不是
用常识猜一个填上去。

## 六张卡（frozen schema，来自 P0）

1. `source_diagnosis` — 源图诊断卡（本文件主要覆盖）
2. `plant_relation` — 植物关系卡（仅当画面含植物/花卉主体时才需要）
3. `plane_composition` — 平面空间构成卡
4. `ink_symbol_composition` — 墨符号构成卡
5. `ink_material` — 笔墨材质卡
6. `quality_score` — 质量评分卡（仅在有实际出图后使用，见
   `05-quality-checklist.md`）

## `source_diagnosis` JSON 结构（草案）

```json
{
  "input_type": "photo | text",
  "subject_category": "TODO: 从 04-subject-routing-table.md 的 13 类里选一个，或 other",
  "point_line_plane_dependency": {
    "point": "low | medium | high",
    "line": "low | medium | high",
    "plane": "low | medium | high",
    "note": "TODO: 判断依据——例如画面里主要靠密集的点状元素（如繁花/灯光）还是靠线条骨架（如江河/山脊）还是靠大色块（如天空/水面）"
  },
  "negative_space_ratio": "TODO: 留白大致占比，如 low/medium/high 或百分比估计",
  "perspective": "TODO: 平视 | 俯视 | 仰视 | 散点透视 | 已经是抽象平面构成（无明确透视）",
  "light_condition": "TODO: 白天 | 夜晚 | 逆光 | 阴天 | 不适用",
  "color_tendency": "TODO: 原图主导色相，用于后续对照 03-color-routing.md 决定要不要保留",
  "structural_complexity": "low | medium | high",
  "unknown_fields": ["列出因为是纯文字输入、缺乏画面信息而无法判断的字段"]
}
```

## 判断这些维度时的原则

- **看真实结构，不看题材刻板印象**：例如同样是"树"，稀疏的孤树可能是
  线依赖为主，茂密的树冠可能是点依赖为主——不要看到"树"就默认套用同一
  套点线面配比。（这是 v17 第 7/8 章真实照片测试反复强调的坑，详见原文
  对应章节，标题关键字："真实照片测试结论"、"分类测试协议"。）
- **`unknown` 是合法输出**，尤其是纯文字输入的场景。宁可让第 2 步路由
  脚本报"信息不足，需要用户补充"，也不要在诊断卡里编造一个看似合理的
  画面细节。

## TODO（需要人工从 v17 拆入的内容）

- [ ] 第 1 章"结构提取"里关于如何从照片判断点/线/面依赖的具体方法论
- [ ] `plant_relation` / `plane_composition` / `ink_symbol_composition` /
      `ink_material` 四张卡各自的完整字段定义（目前只在 SKILL.md 里列了
      名字，字段细节需要对照 v17 YAML 协议块逐一核对）
