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

## 目录结构

```
.claude/skills/wu-guanzhong-ink/
├── SKILL.md                          入口：三步流程说明（诊断→路由→编译）
├── references/                       研究内容拆分后的文档（模型按需读取）
│   ├── 00-source-diagnosis-card.md   六张卡 schema、诊断维度
│   ├── 01-composition-routing.md     六种 composition_mode
│   ├── 02-ink-symbol-rules.md        墨符号系统、笔墨材质
│   ├── 03-color-routing.md           动态色域、纸色路由
│   ├── 04-subject-routing-table.md   13 类主体路由骨架
│   ├── 05-quality-checklist.md       九维评分 + 二元否决项
│   ├── 06-prompt-compiler-spec.md    prompt 组装规则
│   └── 07-generation-protocol-yaml.md v17 原文 YAML 协议摘录（占位）
└── scripts/                          确定性逻辑，不依赖模型现场判断
    ├── router.py                     读诊断卡 → 查路由表 → 输出路由决定
    ├── compiler.py                   读诊断卡+路由决定 → 拼装最终 prompt
    └── data/subject_routing_table.json  13 类主体的路由数据（骨架，待填）
```

`Testing/` 现在有 24 张你自己命名分类的回归测试照片，按 13 类主体
路由整理成了 [`Testing/manifest.md`](Testing/manifest.md)（文件名 →
`subject_category` 映射表），其中 `farmland_grid`、`abstract_line_network`
两类目前还没有对应照片。

## 当前状态：骨架已搭好，内容待填

所有 `references/*.md` 文件和 `scripts/data/subject_routing_table.json`
里的具体规则内容都标了 TODO，尚未从研究文档
`Wu_Guanzhong_Style_Grammar.md`（v17）拆入——按照约定，这一步由你自己
对照原文核对后填入，避免内容被凭印象/凭常识编造。

每个 reference 文件末尾都列了自己的 TODO 清单，可以按 00 → 07 的顺序
逐个核对填充。填 `04-subject-routing-table.md` 里的路由规则时，同步把
`scripts/data/subject_routing_table.json` 对应类目的
`main_route`/`aux_route`/`rejected_routes` 也填上——这两个文件应该保持
内容一致，前者是人可读说明，后者是脚本实际读取的数据。

## 怎么验证脚本骨架能跑（内容填之前也能跑，只是产出占位符）

```bash
cd .claude/skills/wu-guanzhong-ink

# 1. 手写一份最小诊断卡样例
cat > /tmp/diagnosis.json <<'EOF'
{ "input_type": "text", "subject_category": "jiangnan_water_town" }
EOF

# 2. 跑路由脚本 —— 因为路由表还没填内容，这里预期会报 "incomplete"
python scripts/router.py --diagnosis /tmp/diagnosis.json \
  --routing-table scripts/data/subject_routing_table.json

# 3. 路由表填好某个类目后，重新跑一次应该能拿到 status: "ok"
```

`compiler.py` 同理：路由表没填完的类目，编译器会拒绝产出 prompt 并给出
明确原因，不会硬凑一个内容缺失的假 prompt。

## Skill 设计上的三个决定（回答之前提出的问题）

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

## 接下来谁做什么

- **需要你做的**：对照 v17 原文，把 `references/00-07` 和
  `scripts/data/subject_routing_table.json` 里的 TODO 内容填进去。
- **我可以继续做的**：
  - 内容填好后，帮你跑通完整的诊断→路由→编译流程，用真实场景测试
  - 跑一遍 P6 阶段的回归验证（`Testing/manifest.md` 里的 24 张照片，其中
    `farmland_grid`、`abstract_line_network` 两类还没有照片覆盖）
  - `compiler.py` 里 `_count_techniques()` 目前是占位实现（永远返回
    1），内容填好后需要我再实现真正的关键词计数逻辑
  - 你明确要支持某个具体平台（比如 MCP、ChatGPT）时，帮你加对应的适配器
    文件夹，复用现有的 `scripts/`/`references/`，不重复内容

## Git / GitHub

本地已经 `git init` 并做了首次提交（`.gitignore` 排除了 `__pycache__/`
等 Python 产物），但**还没有关联任何远程仓库、也没有推送到任何地方**——
"以后要放到 GitHub 上"这件事，等你确定好仓库名/公开还是私有/要不要加开源
协议（LICENSE，这个我不会替你选，需要你决定用哪种）之后，我再帮你加
remote 并推送。
