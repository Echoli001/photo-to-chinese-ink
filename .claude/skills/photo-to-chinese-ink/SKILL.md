---
name: photo-to-chinese-ink
description: >
  Photo to Chinese Ink — transforms photos into expressive Chinese ink-wash
  artwork. Converts a user-uploaded photo, or a user-written scene
  description, into a Wu Guanzhong (吴冠中)-style modern ink-wash art prompt
  — structured as a diagnosis card, a routing decision, and a final compiled
  text prompt ready to paste into an external image generator (Midjourney,
  即梦, etc.). This skill's own logic (diagnose/route/compile) never calls
  any image-generation API — it only produces text. If the host session the
  assistant is running in already has a native image-generation tool
  available, the assistant MAY call that tool itself with the compiled
  prompt and show only the resulting image (see "第 4 步" below for the
  exact condition and fallback). Use this skill whenever the user asks to
  turn a photo into "吴冠中风格"、"水墨风格"、"国画风格"、ink-wash art, or
  Chinese modern ink painting — even if they just upload a photo and say
  something short like "帮我做成水墨画" or "转成国画" without naming Wu
  Guanzhong explicitly, or if they paste/describe a scene and ask for an
  ink-painting-style prompt for it.
compatibility: Requires Python 3.8+ available on PATH (stdlib only, no
  external packages) for scripts/router.py and scripts/compiler.py.
---

# Photo to Chinese Ink（照片转中国水墨）Skill

## 这是什么

把"一张照片"或"一段文字描述"转成一段可以直接粘贴进 Midjourney / 即梦 等
文生图工具的吴冠中风格水墨 prompt。整个流程分三步，产出三个东西：

1. **源图诊断卡**（结构化 JSON/表格）— 描述这张图/这段文字的视觉结构
2. **路由决定**（主路线 + 至多一条辅助路线 + 明确拒绝的路线）
3. **最终 prompt**（编译好的一段文本，附带简短的中文说明）

本 Skill 自身的诊断/路由/编译逻辑**只产出文本**，不调用任何图像 API——
这一点不变。但如果触发这次对话的宿主环境（Claude、ChatGPT 自定义
GPT、豆包 bot 等——只要是把这份 SKILL.md 内容当系统指令加载、并且当前
会话里挂了原生文生图工具的场景）本身具备可调用的原生文生图能力，模型
可以在完成第 1–3 步后自己调用那个工具直接出图，不需要用户再手动复制
prompt 去别的工具里粘贴——具体条件和呈现方式见"第 4 步"。**能否识别出
"这是 ChatGPT/豆包"这件事本身做不到**（Skill 没有运行时环境探测手段），
真正可判断、也是这里唯一依据的信号是"当前会话我是否能调用一个图像生成
工具"，不是平台名字。

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
- 这张路由表的 13 类主体已经从 `Wu_Guanzhong_Style_Grammar.md`（v17）对
  应章节人工核对填入完毕，每类都附带 v17 行号/章节出处（`_source` 字
  段），细节见 `references/04-subject-routing-table.md`。如果诊断卡给出
  的主体类别不在这 13 类里，脚本会报"该类目路由待补充"，不会瞎猜一个
  路线糊弄过去。
- 如果画面同时包含多个主体类别（例如江南建筑+水面倒影），诊断阶段要
  判断出一个 `dominant_subject`（主语言）——路由只按主语言查表，不把多
  条路线的字段平均或叠加。这条规则的依据和当前实现状态见
  `references/04-subject-routing-table.md` 的"多主体混合场景"一节。
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
    （注：这条在 v17 原文全文检索不到逐字依据，是补充防护而非原文规则，
    见 `references/05-quality-checklist.md` 对应条目的说明）
  - 不使用米黄仿古纸这类被 v17 明确禁止的纸色描述（清单见
    `references/05-quality-checklist.md`）
  - 不出现"吴冠中真迹/原作/官方授权"等误导性描述，不把《双燕》《狮子林》
    《逍遥游》等标志性作品名称直接当模板请求（原创性硬性禁止项，见
    `references/08-originality-guardrails.md` §6.1）

### 第 4 步：呈现结果给用户（先判断有没有原生文生图工具）

先判断：**当前这个对话会话里，我（模型）自己是否能直接调用一个原生的
图像生成工具**（例如工具列表里有类似 `generate_image` / DALL·E /
即梦 / 豆包文生图这类可调用的工具，且不需要用户手动跳出去操作）。

- **判断依据只能是"当前会话工具是否可用"，不能靠猜平台名字**（不能因为
  "系统提示里提到这是 ChatGPT"就假设一定有文生图工具，也不能因为"这是
  Claude"就假设一定没有——以实际可调用的工具列表为准）。
- 拿不准、或者没有明确证据证明有这个工具可用时，一律按"没有"处理，走
  下面的【情况 A】——不要因为想"减少中间步骤"就贸然假设工具存在而直接
  出图失败。

**【情况 A：没有原生文生图工具（默认 / 当前大多数场景）】**

把诊断卡摘要、路由决定摘要、最终 prompt 原文，用清晰的中文小标题分段
展示给用户，并提醒：
- "这段 prompt 需要你自己粘贴到 Midjourney / 即梦等工具里出图，本 Skill
  当前不直接生成图片。"
- "这是风格研究性质的转换，不是吴冠中真迹、官方授权或艺术家基金会产品；
  出图后如果要公开发布，注意遵守 `references/08-originality-guardrails.md`
  §6.4 的说明。"（该文件的相似度检查三层法当前 MVP 无法自动执行，属于
  未来图生成阶段的工作，不需要在这一步替用户跑）

**【情况 B：确认有原生文生图工具可用】**

- 静默完成第 1–3 步（诊断卡、路由决定、编译 prompt 三样都照常生成），
  但**不要**把诊断卡、路由决定、prompt 原文展示给用户——跳过中间产物的
  展示环节。
- 直接用编译好的 prompt 调用该图像生成工具，把生成的图片作为最终结果
  展示给用户。
- 即使跳过了中间产物展示，以下两条提醒仍然必须保留（简短一两句即可，
  不用展开成清单）：
  - 这是风格研究性质的转换，不是吴冠中真迹、官方授权或艺术家基金会产品。
  - 如果要公开发布这张图，建议先看一眼
    `references/08-originality-guardrails.md` §6.4。
- 如果用户后续想看当时用的诊断卡/路由/prompt 具体内容（例如想微调效果、
  或怀疑出图跑偏了），要能补充展示——不是永久丢弃，只是默认不主动展示。
- 如果图像生成工具调用失败或被拒绝（内容策略拦截等），不要静默放弃：
  如实告诉用户失败原因，并回退到【情况 A】的文本展示方式，把已经编译好
  的 prompt 给用户，让用户自己去别的工具尝试。

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
| `references/02-ink-symbol-rules.md` | 点/线/面/留白墨符号系统、笔墨材质（索引，指向 02a/02b/02c） | 编译墨线相关模块时 |
| `references/03-color-routing.md` | 动态色域、纸色路由 | 编译色彩相关模块时 |
| `references/04-subject-routing-table.md` | 13 类主体的路由表（已从 v17 填入完毕） | 做第 2 步路由时 |
| `references/05-quality-checklist.md` | 九维评分 + 二元否决项 | 有实际出图后人工质检 |
| `references/06-prompt-compiler-spec.md` | prompt 组装规则、模块清单、硬性禁止项 | 做第 3 步编译时 |
| `references/07-generation-protocol-yaml.md` | v17 原文里现成的 YAML 生成协议（原文摘录，未拆分） | 需要对照原始协议措辞时 |
| `references/08-originality-guardrails.md` | 原创性限制：硬性禁止项、原创生成要求、相似度检查方法、公开发布建议 | 编译第 3 步做否决检查时；撰写 README/公开说明时 |

以上 references 文件的完成状态并不一致：`00`/`01`/`02`/`03`/`04`/`05`/`07`/`08`
已经从 `C:\Users\LiEc\Downloads\Wu_Guanzhong_Style_Grammar.md`（v17，2377 行）
对应章节核对填入完毕（`08` 仅剩一条项目文档层面的 TODO，不影响运行时逻辑）。
`02-ink-symbol-rules.md` 现在只是一个索引文件，指向 `02a-ink-base-rules.md`
（生宣笔墨引擎与纸色路由，全局强制）、`02b-point-line-plane-symbols.md`
（点线面墨符号系统与线的语法，全局强制）、`02c-subject-specific-ink-rules.md`
（题材专属墨线规则，题材触发）三个文件——具体规则内容在这三个文件里，不在
`02` 本身。`06-prompt-compiler-spec.md` 已完成第一版（模块清单、点线面/墨色/纸色/
抽象化组装规则、硬性禁止项）。`scripts/router.py` 和 `scripts/compiler.py`
均已按 `06` 和 `04-subject-routing-table.md` 实现完毕，并且已经用一份
合成的 `jiangnan_water_town` 诊断卡跑通了第 2、3 步端到端流程（router.py
输出正确的 main/aux/rejected 路由，compiler.py 产出了完整的英文 prompt，
含 M6 aux_route 的水面倒影补充句）。这一轮测试还发现并修复了一个真实
bug：M12 黑名单自查之前是对拼装后的整段 prompt 扫描，导致 M1 固定文本
里"not watercolor"/"no watercolor postcard"这类否定式表达被误判为命中
"水彩化描述"，现已改为只扫描动态拼装的模块内容，不再扫描 M1/M3/M7/M9/M11
这几段逐字引用的固定文本。

后续又核对并修复了第二个真实 bug：`compiler.py` 里 M5
（`flat_spatial_composition_route`）的触发判断和 `subject_route` 取值，
原先检查的是诊断卡里并不存在的字段名（`flat_spatial_composition_route_triggered`、
`repeated_surface_units_are_primary`），`subject_route` 也是靠
`subject_category` 硬映射猜出来的，没有读诊断卡本该提供的权威字段。核对
`references/07-generation-protocol-yaml.md` 第 164-186 行的原始 YAML 后
确认：权威字段应为 `plane_composition.activation_reason`（触发信号）和
`plane_composition.subject_route`（模型直接选定的路由名）。已改为优先读
这两个字段，原来的 `perspective` 启发式判断和 `subject_category` 映射降级
为诊断卡未填 `plane_composition` 时的兜底逻辑，不再是唯一判据。

修复后用两组新诊断卡验证：(1) 江南水乡 + `perspective: 俯视` +
`plane_composition: {activation_reason: aerial_view, subject_route:
aerial_village}`，确认 M5 正确触发、subject_route 正确取自诊断卡而非猜测，
且 M11 的压平构图专属负面约束也正确联动追加；(2) 换一个此前从未测试过的
题材类目 `ancient_architecture`（古建筑），`perspective: 平视`（不触发
M5），确认 router.py/compiler.py 端到端对新题材同样跑通、M10 题材专属
规则正确取用路由表的主/辅路线文本、M5 在不满足条件时正确保持不触发、
黑名单自查无误判。至此 router.py/compiler.py 的端到端链路已经过三类
题材（江南水乡·平视、江南水乡·俯视触发 M5、古建筑）的组合验证。

再后续做了 P6：用 `Testing/manifest.md` 里 29 张真实/半真实照片（覆盖全部
13 个 `subject_category`）逐张手写诊断卡，跑通 router.py→compiler.py 端到端，
29/29 全部 `status: "ok"`。其中 3 张（渔港1.jpg、farmland_grid.jpg、
都市夜晚3.jpeg）按俯视场景设置 `plane_composition.activation_reason:
aerial_view`，验证 M5 正确触发；其余按各题材默认视角走非 M5 路径。

这一轮测试又发现并修复了第三个真实 bug：`abstract_line_network` 这个题材
在 `SUBJECT_ROUTE_TRANSLATIONS` 里的 M10 固定模板文本本身写的是合规的否定
句——"do not add new ink mass or **recompose** the image"——但该题材的
`rejected_keywords` 自查正则只是裸词匹配 `recompose`，不区分否定语境，导致
每次编译该题材都 100% 必然触发自查报警、M10 整个模块被跳过，而不是只在
真的拼出违规内容时才跳过。这跟之前修复的 M12 黑名单 bug是同一类"裸关键词
匹配不认否定句"的缺陷，但这次是永久性的（固定模板文本不会变，每次都会误
判），而不是偶发的。修复方式：把该题材的正则从 `r"重新构图或大幅改动密度
|recompose"` 改成 `r"重新构图或大幅改动密度|(?<!or )recompose"`，用否定
前瞻排除"...or recompose the image"这句合规否定文本，同时仍能捕获未来若
真的误写成主动要求"recompose"的情况。修复后重跑 P6 全部 29 张验证：两张
`abstract_line_network` 测试图的 M10 自查笔记消失、compiled prompt 长度
从约 4839/4819 字符回升到约 5355/5335 字符（M10 文本正确出现），其余 27
张的 compiler_notes 无变化，29/29 仍全部通过。

用真实照片（`Testing/水乡1.jpeg`，江南夜景水乡+水面倒影）走一遍完整
诊断→路由→编译流程时，又发现并修复了第四个真实 bug：`compiler.py` 的
M6（点/线/面配比声明）读的是 `diagnosis.get("point_line_plane")`，且假设
`point`/`line`/`plane` 三个键的值是可以直接 `float()` 转换的数字；但
`00-source-diagnosis-card.md` 定义的权威字段名是 `point_line_plane_dependency`，
取值是 `low | medium | high` 三档序数词，不是数字。字段名不对、类型也解析
不了，导致 `_parse_triple` 每次都返回 `None`，M6 100% 必然回退到路由表里
该题材的通用参考三元组（例如江南水乡固定回退成 `12/32/56*`），诊断卡里
模型对这张具体图片的点/线/面真实判断（例如这张照片是"点依赖高、线依赖
高、面依赖中"）被完全忽略，跟前三个 bug 是同一类"字段名/取值格式跟 schema
对不上、且没有测试覆盖"的缺陷，但这个影响面更大——意味着**所有**题材、
**所有**诊断卡的 M6 输出此前都从未真正采用过诊断结果，而不是像第三个 bug
那样只影响单个题材。修复方式：`_build_m6_point_line_plane` 改为读
`point_line_plane_dependency`；`_parse_triple` 新增对 `low/medium/high`
序数词的解析分支，按权重 1/2/3 归一化成一个总和 100 的百分比三元组，
数字 dict、`"12/32/56*"` 这类路由表字符串格式的旧解析路径原样保留不受
影响。修复后用单元测试逐一验证：序数词 high/medium/low 正确算出
50/33.3/16.7；旧数字 dict 格式、旧字符串三元组格式（含 v17 溯源尾注文字）
解析结果不变；诊断卡缺该字段时仍正确回退到路由表参考值且带回退提示
note。用水乡1.jpeg 实测：M6 从固定回退文案"Let plane carry roughly 56%..."
变成真实反映诊断判断的"Let point carry roughly 37.5%..."，`notes` 里对应
的回退提示消失。
