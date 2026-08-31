# Prompt 编译规则

> 状态：骨架。这是 `scripts/compiler.py` 的行为规范文档——脚本本身是
> 确定性代码，但代码要按什么规则组装最终文本，规则来源是这个文件（以
> 及它引用的其他 reference 文件）。内容尚未从 v17 逐条拆入，目前只搭好
> 模块清单和硬性约束的框架。

## 输入

- 诊断卡 JSON（`source_diagnosis`，见 `00-source-diagnosis-card.md`）
- 路由决定 JSON（来自 `scripts/router.py` 的输出，见 `04-subject-routing-table.md`）

## 输出

一段文本 prompt，附带简短中文说明。具体的最终文本语言（纯英文关键词式？
中英混合？完整英文句子？）待定——这是留给用户在拿到目录结构后自己核对
v17 原文里 prompt 范例风格再决定的事项。

## 组装模块清单（TODO：每个模块具体拼什么内容）

编译器按固定顺序拼接以下模块，模块内容来自对应的 reference 文件：

1. **源图不变量**（source invariants）— 哪些原图元素必须保留，来自诊
   断卡的 `unknown_fields` 以外的字段
2. **构图原型**（composition archetype）— 来自路由决定的 main_route，
   对照 `01-composition-routing.md`
3. **点/线/面配比**（point/line/plane ratio）— 来自诊断卡的
   `point_line_plane_dependency`，对照 `02-ink-symbol-rules.md`
4. **墨色浓淡**（ink gradation）— 对照 `02-ink-symbol-rules.md` 的 `ink`
   字段
5. **干湿笔质感**（dry/wet brush quality）— 同上
6. **色彩系统**（color system）— 对照 `03-color-routing.md`
7. **纸色**（paper color）— 对照 `03-color-routing.md` 的
   `paper_color_router`
8. **抽象化程度**（abstraction level）— TODO：这个字段目前在诊断卡草
   案里还没有对应位置，需要确认是诊断阶段判断还是路由阶段判断
9. **题材专属规则**（subject rules）— 来自路由决定，对照
   `04-subject-routing-table.md` 里该类目的额外规则（如果有）
10. **禁止项**（prohibitions）— 见下方"硬性约束"一节
11. **输出规格**（output spec）— 画幅比例、分辨率相关关键词等，TODO：
    是否需要这一项待确认

## 硬性约束（编译器代码层面强制执行，不依赖模型自觉遵守）

这些约束应该写成 `compiler.py` 里的实际代码检查（例如关键词计数、黑名
单字符串匹配），而不是只写在文档里指望被"读到"：

- 技法关键词总数 ≤ 3，且 ≥ 1（不能一个技法都不给，也不能堆砌）
- 黑名单关键词（签名/印章/题跋/水彩/"in the style of Wu Guanzhong"/米
  黄仿古纸等，完整清单见 `05-quality-checklist.md`）— 一旦命中就要么
  自动移除要么报错，不能静默放行
- 不能直接用画家名字驱动效果（例如不能出现"仿吴冠中""吴冠中笔法"这类
  表达本身作为技法描述——这是 v17 强调的"不是模仿画家签名风格，而是遵
  循视觉语法"这一原则的具体体现）

## TODO（需要人工从 v17 拆入的内容）

- [ ] 确认最终 prompt 的目标语言/格式（纯关键词 vs 完整句子 vs 中英混
      合），参考 v17 里是否有现成的 prompt 范例
- [ ] 每个模块具体应该拼出什么样的文本片段（现在只有模块名，没有内容
      模板）
- [ ] "抽象化程度"这个字段到底应该出现在诊断卡还是路由决定里，需要在
      填内容时一并定下来并同步更新 `00-source-diagnosis-card.md`
- [ ] 黑名单关键词的完整列表（当前只列了已知的几条）
