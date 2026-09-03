# 跨平台集成说明（给"其他 AI agent"看的接口文档）

> 这份文档只写**接口/调用方式**，不涉及吴冠中风格的具体规则内容——那些内容
> 仍然是 TODO，按约定由你对照 v17 原文填入 `references/00-07` 和
> `scripts/data/subject_routing_table.json`。这份文档不会、也不需要提前
> 假设那些内容长什么样。

## 现实约束：没有一种打包格式能被"各种 AI agent"原生安装

先把话说清楚，避免后面走弯路：

- Claude 的 `SKILL.md`（YAML frontmatter + markdown）是 Claude 专有格式，
  Claude Code / claude.ai 才认识，**ChatGPT、Gemini 等平台没有对应的转换
  路径**，不存在"一份文件到处装"的打包格式。
- 目前唯一有一定跨平台通用性的标准是 **MCP（Model Context Protocol）**，
  Claude Desktop/Code 支持，也有其他一些工具在接入，但 ChatGPT 并不原生
  支持。
- 所以"通用"现实的做法不是找一种万能格式，而是：**把不依赖任何平台的核心
  逻辑单独暴露出一份清晰的调用接口**，不同平台各自写一层薄薄的"适配器"去
  调用同一份核心，而不是每个平台复制一份内容。

## 核心已经是平台无关的

`router.py`、`compiler.py` 只依赖 Python 标准库（`argparse`/`json`/`re`/
`pathlib`），`subject_routing_table.json` 和 `references/*.md` 都是纯文本
文件。任何能执行命令行、或能读文件的 agent/平台，理论上都能直接用这三样
东西，不需要理解 Claude Skill 的任何约定。

### 调用方式（CLI，与平台无关）

```bash
# 第一步：诊断卡（目前诊断这一步是模型的语义判断，没法写成脚本，
# 由触发这次调用的 agent 自己按 references/00-source-diagnosis-card.md
# 里的 schema 生成一份 JSON，存成文件）
#   示例最小结构：
#   { "input_type": "image" | "text", "subject_category": "<13 类枚举之一>" , ... }

# 第二步：路由（确定性逻辑，任何 agent 都可以直接调用这个脚本）
python .claude/skills/photo-to-chinese-ink/scripts/router.py \
  --diagnosis <diagnosis.json> \
  --routing-table .claude/skills/photo-to-chinese-ink/scripts/data/subject_routing_table.json \
  --out <routing.json>

# 第三步：编译最终 prompt（同样是确定性逻辑）
python .claude/skills/photo-to-chinese-ink/scripts/compiler.py \
  --diagnosis <diagnosis.json> \
  --routing <routing.json> \
  --out <result.json>
```

`result.json` 里的 `status` 字段是各平台都应该检查的关键字段：

| status | 含义 | 平台应该怎么处理 |
|---|---|---|
| `ok`（router）/ `draft`（compiler，内容填完后应改为更明确的完成态）| 成功 | 把 `prompt` 字段展示/返回给用户 |
| `incomplete` | 该题材类目路由还没填内容 | 明确告知用户"这类题材还不支持"，不要瞎编 |
| `unresolved` | 诊断卡没给出 subject_category | 要求上游先补全诊断 |
| `unknown_category` | subject_category 拼错或不在 13 类里 | 报错，列出已知类目 |
| `blocked`（compiler）| 命中黑名单关键词，或技法关键词数量超范围 | 拒绝输出，报告原因，不能静默放行 |

退出码：`router.py`/`compiler.py` 在非成功状态时返回非零退出码，方便脚本化
调用方（不管是 Claude、还是别的 agent 的工具调用层）用退出码判断是否需要
人工介入，不需要额外解析 JSON 才能知道成不成功。

## "在 ChatGPT / 豆包等 agent 里安装"实际是什么意思

上面已经说清楚：没有一种打包格式能被这些平台原生识别、一键安装。所以今天
如果要在 ChatGPT 的 Custom GPT 或豆包 bot 里用这份 Skill，实际做法是**把
`SKILL.md` 的正文内容整段复制，粘贴进那个平台的"系统提示 / 人设设定"里**，
让宿主模型把这段文字当成自己的行为指令来读——不是安装一个包，是让模型
"读到"这份说明。核心的 `router.py`/`compiler.py`/`references/*.md` 仍然是
纯文本/纯 Python，可选地由该 agent 通过命令行调用（如果平台支持跑代码），
或者干脆让模型直接读 `references/*.md` 里的规则用自然语言模拟这三步。

### 直接出图 vs. 只给文本 prompt，判断依据是"工具"不是"平台"

`SKILL.md` 第 4 步里要求模型自己判断"当前会话是否能调用原生文生图工具"，
再决定是隐藏诊断卡/路由/prompt 直接出图，还是照常展示三样东西给用户去别的
工具粘贴。这个判断**依据的是宿主会话当时实际暴露给模型的工具列表，不是
"这是 ChatGPT 所以一定有/没有"这种基于平台名字的猜测**——因为：

- 同一个平台（比如 ChatGPT）在不同的 Custom GPT 配置下，可能挂了 DALL·E
  工具，也可能没挂；豆包 bot 同理。
- Skill 本身没有任何手段去探测"我现在跑在哪个平台上"——SKILL.md 只是一段
  文本，没有运行时环境查询能力。

所以不要指望这份文档，或 SKILL.md，能列出一张"ChatGPT=有、豆包=有、
Claude=没有"这样的平台对照表——唯一可靠的信号就是当次会话工具列表里
是否真的有一个可调用的图像生成工具。

## 现有适配器 vs. 以后可能加的适配器

| 适配器 | 状态 | 说明 |
|---|---|---|
| Claude Skill（`.claude/skills/photo-to-chinese-ink/`）| **已有，已测试** | Claude Code 项目内自动发现；也可以整个文件夹打包上传到 claude.ai 的 Skills 设置里 |
| MCP Server | **未搭建** | 现实中最接近"一次开发、多个 agent 能装"的路线，因为支持 MCP 的工具在变多。如果你明确要面向"支持 MCP 的其他 agent"，这是优先级最高的下一个适配器，值得单独开一轮开发，不是顺手加的小工作量 |
| ChatGPT Custom GPT Action | **未搭建** | 需要写 `openapi.yaml` + 把 router/compiler 包成一个可以被 HTTP 调用的服务（Custom GPT Actions 只认 HTTP API，不能直接跑本地脚本）。只有你明确要支持 ChatGPT 才值得做，工作量比 MCP 适配器更大（还要有个能公网访问的后端） |
| 其他（Gemini/自建 agent 框架等）| **未搭建** | 原理一样：写一层薄适配器去调用上面的 CLI 接口，不重复内容 |

**现在故意没有新建这些适配器**，只是把接口先写清楚——避免在还不确定你具体
要支持哪个平台之前，多开发出用不上的东西（对应 CLAUDE.md Rule 2：简洁优
先，不做未来可能用不到的抽象）。等你明确要支持哪个平台，再针对性地加对应
的适配器文件夹（例如 `adapters/mcp-server/`），复用同一份 `scripts/` 和
`references/`，不复制内容。

## 现有目录结构没有改动

这份文档不会把 `router.py`/`compiler.py`/`references/` 从
`.claude/skills/photo-to-chinese-ink/` 里搬出去——那样会破坏 Claude Skill 需要
"自包含一个文件夹"的打包约定（打包上传到 claude.ai 时，Skill 文件夹里的
脚本/文档必须在同一棵目录树下）。核心逻辑本来就是平台无关的纯 Python +
JSON，其他平台的适配器可以直接从项目根目录用相对路径调用，不需要先把文件
挪位置。
