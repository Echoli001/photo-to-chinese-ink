---
name: wu-guanzhong-ink
description: >
  Converts a user-uploaded photo, or a user-written scene description, into a
  Wu Guanzhong (吴冠中)-style modern ink-wash art prompt — structured as a
  diagnosis card, a routing decision, and a final compiled text prompt ready
  to paste into an external image generator (Midjourney, 即梦, etc.). This
  skill does NOT call any image-generation API itself; it only produces text.
  Use this skill whenever the user asks to turn a photo into "吴冠中风格"、
  "水墨风格"、"国画风格"、ink-wash art, or Chinese modern ink painting —
  even if they just upload a photo and say something short like "帮我做成
  水墨画" or "转成国画" without naming Wu Guanzhong explicitly, or if they
  paste/describe a scene and ask for an ink-painting-style prompt for it.
compatibility: Requires Python 3.8+ available on PATH (stdlib only, no
  external packages) for scripts/router.py and scripts/compiler.py.
---

# 吴冠中水墨转化 Skill

## 这是什么

把"一张照片"或"一段文字描述"转成一段可以直接粘贴进 Midjourney / 即梦 等
文生图工具的吴冠中风格水墨 prompt。整个流程分三步，产出三个东西：

1. **源图诊断卡**（结构化 JSON/表格）— 描述这张图/这段文字的视觉结构
2. **路由决定**（主路线 + 至多一条辅助路线 + 明确拒绝的路线）
3. **最终 prompt**（编译好的一段文本，附带简短的中文说明）

这一版 MVP **只输出文本**，不生成图片、不调用任何图像 API。用户拿到
prompt 后自己去粘贴到别的工具里出图。

## 为什么分三步，而不是直接让模型"凭感觉"写一段吴冠中风格的 prompt

如果每次都让模型现场自由发挥，同一张图两次生成的风格会漂移，且很难复
盘"这次为什么效果不好"。三步拆分的目的：

- **诊断**是视觉判断，必须由模型看图/读文字来完成——没法写成规则。
- **路由**和**编译**是确定性逻辑（给定同样的诊断结果，路由和最终 prompt
  的组装方式应该每次都一样）——这类逻辑写成 `scripts/` 里的脚本，比写
  成一段"请你遵守以下规则"的自然语言指令更稳，也能被单独测试和回归验证。

所以本 Skill 的分工是：**模型负责诊断（第 1 步），脚本负责路由和编译
（第 2、3 步）**。

## 执行流程

### 第 1 步：生成源图诊断卡

- 如果用户上传了照片：仔细观察这张照片的构图、主体、点/线/面视觉依赖、
  留白比例、光影、色彩倾向。
- 如果用户只写了文字描述：从文字里提取同样这些维度，缺失的维度要在诊
  断卡里明确标注"未知/待用户补充"，不要替用户编造画面细节。
- 诊断卡的完整字段定义、六张卡的 schema、每个维度怎么打分，读
  `references/00-source-diagnosis-card.md`。
- 把诊断结果写成一个 JSON 文件（字段结构见该 reference 文件），保存到
  临时工作目录，例如 `/tmp/wgz-diagnosis.json`。

### 第 2 步：跑路由脚本

```bash
python scripts/router.py --diagnosis /tmp/wgz-diagnosis.json --routing-table scripts/data/subject_routing_table.json
```

- 路由脚本根据诊断卡里的主体类别，从 `scripts/data/subject_routing_table.json`
  这张表里查出：一条主路线、至多一条辅助路线、以及需要明确避免的路线。
- 这张路由表当前是**骨架**，具体的 13 类主体 × 路线内容需要从
  `Wu_Guanzhong_Style_Grammar.md`（v17）里对应章节人工核对后填入——不要
  凭空编造路由规则，路由表里没填的类目，脚本会报"待补充"而不是瞎猜一个。
  13 个主体类目和对应关系细节见 `references/04-subject-routing-table.md`。
- 脚本输出一个 routing JSON，同样保存到临时工作目录。

### 第 3 步：跑编译脚本，产出最终 prompt

```bash
python scripts/compiler.py --diagnosis /tmp/wgz-diagnosis.json --routing /tmp/wgz-routing.json
```

- 编译脚本把诊断卡 + 路由决定，按照固定模板拼成最终 prompt 文本。
- 拼装规则（模块列表、点线面配比、墨色/枯湿、纸色路由、抽象化程度、
  技法数量上限 1–3 个、题材专属规则、以及硬性禁止项）见
  `references/06-prompt-compiler-spec.md`；墨符号/线型细则见
  `references/02-ink-symbol-rules.md`；色彩细则见
  `references/03-color-routing.md`；构图细则见
  `references/01-composition-routing.md`。
- 编译脚本内置的硬性检查（不需要看参考文件也会自动拦截）：
  - 最终 prompt 里最多出现 1–3 个具体技法关键词
  - 不出现签名、印章、题跋、水彩化描述
  - 不直接写"in the style of Wu Guanzhong"这类靠画家名字取效果的表达
  - 不使用米黄仿古纸这类被 v17 明确禁止的纸色描述（清单见
    `references/05-quality-checklist.md`）

### 第 4 步：把三样东西呈现给用户

把诊断卡摘要、路由决定摘要、最终 prompt 原文，用清晰的中文小标题分段
展示给用户，并提醒："这段 prompt 需要你自己粘贴到 Midjourney / 即梦等
工具里出图，本 Skill 当前不直接生成图片。"

## 质量自查（人工判图阶段，本 MVP 暂不自动跑）

`references/05-quality-checklist.md` 里的九维评分表是给**看到实际生成
图片之后**用的人工/未来自动化质检标准。当前 MVP 只产出文本 prompt，看
不到生成结果，所以这一步先跳过——等用户有了实际出图，可以把图片描述回
来，再手动比对这份清单。不要在没看到图的情况下假装完成了质量评分。

## 参考文件索引

| 文件 | 内容 | 什么时候读 |
|---|---|---|
| `references/00-source-diagnosis-card.md` | 六张卡的完整 schema、诊断维度定义 | 做第 1 步诊断时 |
| `references/01-composition-routing.md` | 六种构图模式（jiangnan_geometry 等） | 判断构图类型时 |
| `references/02-ink-symbol-rules.md` | 点/线/面/留白墨符号系统、笔墨材质 | 编译墨线相关模块时 |
| `references/03-color-routing.md` | 动态色域、纸色路由 | 编译色彩相关模块时 |
| `references/04-subject-routing-table.md` | 13 类主体的路由骨架 | 做第 2 步路由时 |
| `references/05-quality-checklist.md` | 九维评分 + 二元否决项 | 有实际出图后人工质检 |
| `references/06-prompt-compiler-spec.md` | prompt 组装规则、模块清单、硬性禁止项 | 做第 3 步编译时 |
| `references/07-generation-protocol-yaml.md` | v17 原文里现成的 YAML 生成协议（原文摘录，未拆分） | 需要对照原始协议措辞时 |

以上 references 文件目前多数是**骨架 + TODO**，具体内容要从
`C:\Users\LiEc\Downloads\Wu_Guanzhong_Style_Grammar.md`（v17，2377 行）里
对应章节拆分填入——不要在没有对照原文的情况下凭印象编写规则内容。
