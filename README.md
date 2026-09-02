# 吴冠中水墨转化 Skill

把用户上传的照片、或用户写的文字场景描述，转成一段可以直接粘贴进
Midjourney / 即梦等文生图工具的吴冠中风格水墨 prompt。当前是 MVP：只
产出文本，不调用任何图像生成 API。

Skill 本体在：[`.claude/skills/wu-guanzhong-ink/`](.claude/skills/wu-guanzhong-ink/)，
入口是 [`SKILL.md`](.claude/skills/wu-guanzhong-ink/SKILL.md)。

**跨平台说明**：`router.py`/`compiler.py` 只依赖 Python 标准库，
`references/*.md` 和 `subject_routing_table.json` 都是纯文本文件，本质上
和 Claude 无关，任何能读文件/执行命令行的 agent 都能直接用。但目前没有
一种打包格式能被"各种 AI agent"原生安装——`SKILL.md` 是 Claude 专有的，
其他平台没有对应的转换路径。现实的做法是"一个核心 + 多个薄适配器"：核心
（`scripts/` + `references/`）保持平台无关，Claude Skill 是目前唯一实现
的适配器，以后要支持别的平台（例如 MCP、ChatGPT Custom GPT）就单独加一层
薄适配器去调用同一份核心，不重复内容。详见
[`docs/agent-integration.md`](docs/agent-integration.md)。

## 当前状态：内容已完成，已通过 29 张真实照片的端到端回归验证

`references/00-08`（含拆分出的 `02a`/`02b`/`02c`）和
`scripts/data/subject_routing_table.json` 已全部对照原始研究文档
`Wu_Guanzhong_Style_Grammar.md`（v17）核对填入完毕。`router.py`/
`compiler.py` 均已按规格实现（含技法数量 1–3 个的真实关键词计数校验、
黑名单自查、题材专属规则），不是占位实现。

见 [Testing 章节](#testing--回归验证) 了解验证过程和已修复的问题。

## 目录结构

```
.claude/skills/wu-guanzhong-ink/
├── SKILL.md                            入口：三步流程说明（诊断→路由→编译）
├── references/                         研究内容拆分后的文档（模型按需读取）
│   ├── 00-source-diagnosis-card.md     六张卡 schema、诊断维度
│   ├── 01-composition-routing.md       六种 composition_mode
│   ├── 02-ink-symbol-rules.md          墨符号系统索引（指向 02a/02b/02c）
│   ├── 02a-ink-base-rules.md           生宣笔墨引擎与纸色路由（全局强制）
│   ├── 02b-point-line-plane-symbols.md 点线面墨符号系统与线的语法（全局强制）
│   ├── 02c-subject-specific-ink-rules.md 题材专属墨线规则（题材触发）
│   ├── 03-color-routing.md             动态色域、纸色路由
│   ├── 04-subject-routing-table.md     13 类主体路由表（已全部填入）
│   ├── 05-quality-checklist.md         九维评分 + 二元否决项（人工质检用）
│   ├── 06-prompt-compiler-spec.md      prompt 组装规则、模块清单、硬性禁止项
│   ├── 07-generation-protocol-yaml.md  v17 原文 YAML 生成协议摘录
│   └── 08-originality-guardrails.md    原创性限制、相似度检查、公开发布建议
└── scripts/
    ├── router.py                       读诊断卡 → 查路由表 → 输出路由决定
    ├── compiler.py                     读诊断卡+路由决定 → 拼装最终 prompt
    └── data/subject_routing_table.json 13 类主体的路由数据（已填完）
```

`Testing/` 有 29 张真实/半真实照片，按 13 类 `subject_category` 整理成了
[`Testing/manifest.md`](Testing/manifest.md)（文件名 → 类别映射表 + 覆盖率
统计），全部类别都至少有一张覆盖。

## 怎么跑

```bash
cd .claude/skills/wu-guanzhong-ink

# 第 1 步（诊断卡）由模型完成，不是脚本——参考 references/00 的 schema
# 手写或让模型生成一份诊断卡 JSON，例如 /tmp/diagnosis.json

# 第 2 步：路由
python scripts/router.py --diagnosis /tmp/diagnosis.json \
  --routing-table scripts/data/subject_routing_table.json \
  --out /tmp/routing.json

# 第 3 步：编译成最终 prompt
python scripts/compiler.py --diagnosis /tmp/diagnosis.json \
  --routing /tmp/routing.json \
  --out /tmp/compiled.json
```

两个脚本都遵循"明确失败，不编造"的原则：诊断卡缺字段、主体类别不在 13
类路由表里、或黑名单自查命中时，返回的 JSON 里 `status` 会是
`"incomplete"`/`"unresolved"`/`"unknown_category"` 等非 `"ok"` 值并附
`notes`/`unknown_fields`，同时进程以非零退出码提醒调用方需要人工介入——
不会为了凑一个完整输出而瞎猜。完整状态码说明见
[`docs/agent-integration.md`](docs/agent-integration.md)。

## Testing / 回归验证

**P6 阶段**：用 `Testing/manifest.md` 里 29 张真实/半真实照片（覆盖全部 13
个 `subject_category`）逐张手写诊断卡，跑通 `router.py` → `compiler.py`
端到端，**29/29 全部 `status: "ok"`**。其中含俯视构图（触发 `M5` 压平构图
模块）和平视构图两类场景的组合覆盖。

这一验证过程中发现并修复了 3 个真实 bug（均非假设性问题）：

1. **黑名单自查误判固定文本**：`compiler.py` 的黑名单自查原先扫描拼装后
   的整段 prompt，导致 M1 固定文本里 "not watercolor" 这类否定式表达被
   误判为命中"水彩化描述"关键词。改为只扫描动态拼装的模块内容。
2. **M5 读取了不存在的诊断卡字段**：压平构图模块的触发判断和路由取值原
   先检查诊断卡里并不存在的字段名，`subject_route` 靠 `subject_category`
   硬映射猜测，而不是读诊断卡本该提供的权威字段
   （`plane_composition.activation_reason` / `plane_composition.subject_route`）。
   已改为优先读这两个权威字段，旧逻辑降级为兜底。
3. **`abstract_line_network` 题材的正则永久误报**：M10 固定模板文本本身
   写的是合规否定句（"do not ... recompose the image"），但自查正则裸词
   匹配 `recompose`，导致该题材每次编译都 100% 触发误报、M10 被跳过。用
   否定前瞻修正正则，使其只在真正违规时触发。

这一轮手动验证已经固化成自动化 pytest 回归套件：
[`Testing/test_p6_regression.py`](Testing/test_p6_regression.py)。诊断卡
落盘在 `Testing/fixtures/`（29 个 JSON，逐张对应 `Testing/manifest.md`
里的照片，字段完整度对齐 `references/00-source-diagnosis-card.md` 的
"六张卡"结构），套件用 `importlib` 直接加载 `router.py` / `compiler.py`
的函数（不走子进程），覆盖：

- **全量回归**：29 个诊断卡逐一跑通 `router.py` → `compiler.py`，断言两
  步都返回 `status: "ok"` 且产出非空 prompt；另外两个测试分别确认 29 个
  fixture 都在、且 13 个 `subject_category` 全覆盖。
- **3 个 pinned 回归测试**，分别钉死上面 3 个 bug 修复后的正确行为：
  1. 用 `水乡1.json` 验证 M1 固定文本里的 "not watercolor" 不会被黑名单
     自查误判为命中。
  2. 用 `渔港1.json`（航拍构图）验证 M5 确实由诊断卡的
     `plane_composition.activation_reason` / `subject_route` 权威字段触
     发，而不是靠 `subject_category` 猜测。
  3. 用 `abstract_line_network1.json` / `abstract_line_network2.json` 验
     证 M10 不会因为自身固定文本里的 "or recompose" 而误伤自查、被跳过。

运行方式：

```bash
python -m pytest Testing/test_p6_regression.py -v
```

（需要 `pip install pytest`；截至本次验证共 35 个测试全部通过。）

## Skill 设计上的三个决定

1. **触发方式**：`SKILL.md` 的 `description` 字段里覆盖了"吴冠中"、
   "水墨风格"、"国画风格"，以及用户没提画家名字、只说"帮我做成水墨画"
   这类短表达，按 skill-creator 的建议写得偏"push"一些，降低漏触发概
   率。
2. **为什么拆成 references/ 而不是全塞进 SKILL.md**：v17 原文 2377 行，
   全塞进去会让 SKILL.md 本身臃肿到每次触发都要整篇读入上下文。拆分后
   SKILL.md 只保留"什么时候读哪个文件"的索引，具体内容按需加载。
3. **路由和编译为什么是脚本、不是 SKILL.md 里的自然语言步骤**：这两步
   是确定性逻辑——给定同样的诊断卡，路由和最终 prompt 的组装方式每次都
   应该一样。写成 `scripts/*.py` 的好处：可以独立单元测试、可以用退出
   码/JSON status 字段明确报告"待补充"而不是模型现场编一个，符合
   CLAUDE.md Rule 8（职责分离：模型负责判断，代码负责执行）。诊断这一
   步没有写成脚本，因为它本质是视觉/语义判断，没法写成规则。

## 接下来

- 确定仓库名和公开/私有后，加 GitHub remote 并推送
- 你明确要支持某个具体平台（比如 MCP、ChatGPT Custom GPT）时，加对应的
  适配器文件夹，复用现有的 `scripts/`/`references/`，不重复内容
- 质量自查清单（`references/05-quality-checklist.md` 的九维评分）目前是
  给"看到实际生成图片之后"用的人工标准，MVP 阶段只产出文本 prompt，暂不
  自动执行

## License

[MIT](LICENSE)，另附一条说明：本许可只覆盖本仓库的代码和文档，不涉及
"吴冠中"姓名的商标权，也不授予用这个工具生成的美术作品/图片任何权利；本
项目是独立的、非官方的风格研究工具，与吴冠中先生的遗产管理方/基金会/权
利人没有任何关联或合作关系。详见
[`references/08-originality-guardrails.md`](.claude/skills/wu-guanzhong-ink/references/08-originality-guardrails.md)。

## Git / GitHub

本地已经拆成几个有意义的独立 commit（内容填充、脚本实现+bug修复、
LICENSE、P6 回归验证、README 各自一个 commit）。还没有关联任何远程仓
库，等你确定仓库名和公开/私有后，再加 remote 并推送。
