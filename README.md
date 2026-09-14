# 产品拆解

一个面向 AI 产品的证据化逆向拆解 Skill。

它把产品页面、操作截图、聊天记录、节点画布、资产卡、任务状态、错误提示、开源代码和官方资料，还原为可追溯的用户旅程、Agent/工具契约、上下文和产品架构，并生成具有清晰信息层级与完整视觉验收的独立 HTML 报告。

“美观”是交付质量的一部分，不是产品名称：所有样式都服务于证据扫描、架构理解和决策阅读，不能改变事实等级或掩盖未知。

## 能做什么

- 重建产品用户旅程、正常流程、修改流程和失败分支；
- 拆解 Agent 的输入、判断、工具、输出、上下文、完成条件与交接；
- 为指定 Agent 编写“功能等价、非官方原文”的 System Prompt；
- 输出端到端五流、九层架构、ER 图、时序图和产品全景图；
- 区分 As-Is、合理推断、To-Be 建议、风险和未知；
- 比较两个或多个产品，并生成单产品深拆与对比总览；
- 生成响应式、暗色模式友好、可打印、可验证的独立 HTML 报告。

## 证据等级

所有重要结论使用四级标签：

- **已确认**：页面、操作、资产、状态、工具结果、源码或官方资料直接支持；
- **合理推断**：由多条已确认事实共同支持，但实现不可见；
- **建议设计**：为稳定性、安全或可维护性提出的方案；
- **未知**：证据不足或存在无法消解的冲突。

Skill 不会声称读取隐藏思维链、恢复官方 Prompt，或把未知后端技术写成事实。

## 安装

克隆仓库到 Codex Skills 目录：

```bash
git clone https://github.com/Alin-xx/product-breakdown-skill.git ~/.codex/skills/product-architecture-reverse-engineering
```

如果目标目录已经存在，请先自行决定是备份、更新还是替换；不要直接覆盖仍需保留的个人修改。

安装后，在 Codex 中调用：

```text
$product-architecture-reverse-engineering
```

界面显示名称为“产品拆解”。

## 怎么用

### 完整产品拆解

```text
使用 $product-architecture-reverse-engineering 拆解这个 AI 产品。
基于我提供的页面、截图、源码和官方资料，输出完整产品架构 HTML，
区分已确认、合理推断、建议设计和未知，并完成结构与视觉质量检查。
```

### 用户旅程

```text
使用 $product-architecture-reverse-engineering 只还原这组截图中的用户旅程，
覆盖主流程、修改、失败和中断。完成旅程报告后停止，不继续拆 Agent。
```

### Agent 契约

```text
使用 $product-architecture-reverse-engineering 拆解产品中实际出现的 Agent，
给出每个 Agent 的输入、判断、工具、输出、上下文读写、完成条件和异常处理。
```

### 两个产品对比

```text
使用 $product-architecture-reverse-engineering 分别拆解产品 A 和产品 B，
生成两份完整架构报告和一份对比总览。
统一证据快照和比较维度，输出场景化选型，不做无依据总评分。
```

### 单 Agent 功能等价 Prompt

```text
使用 $product-architecture-reverse-engineering 只处理我指定的 Agent，
基于可见证据生成可直接使用的功能等价 System Prompt、状态机、追溯表和测试集。
明确声明它不是官方 Prompt。
```

## 输出内容

完整架构报告默认包含：

1. 执行摘要与证据范围；
2. 功能域和端到端五流；
3. 九层产品架构；
4. Agent、工具、上下文和数据流；
5. 知识、模型和技术选型判断；
6. 数据实体、ER、时序和全景图；
7. As-Is、To-Be、风险、追溯和未知；
8. 可点击目录、证据链接、Mermaid 源码与图例；
9. 响应式、暗色、打印和键盘可访问样式。

## 案例

案例基于 DeepSeek Harness 与 OpenAI Codex 的官方 GitHub 仓库源码快照：

| 案例 | 用途 |
|---|---|
| [DeepSeek Harness 产品架构拆解](assets/examples/deepseek-harness-product-architecture-report.html) | 单产品完整架构报告，强调插件组合、事件日志与能力接口 |
| [OpenAI Codex Harness 产品架构拆解](assets/examples/codex-harness-product-architecture-report.html) | 单产品完整架构报告，强调控制面、协议、工具与安全治理 |
| [DeepSeek Harness vs Codex Harness 对比总览](assets/examples/deepseek-harness-vs-codex-harness-comparison.html) | 把两份深拆压缩为同维度比较和场景化选型 |

案例用于展示报告组织方式，不应被当作分析其他产品时的固定结论或配色模板。详细说明见 [Harness 案例说明](references/harness-case-study.md)。

## HTML 质量体系

- [报告生产流水线](references/report-production-pipeline.md)：从输入盘点、内容模型到三轮验收；
- [HTML 视觉系统](references/html-visual-system.md)：设计令牌、信息层级、表格、图表、暗色、响应式与打印；
- [HTML 基准模板](assets/report-template.html)：完整、自包含的报告模板；
- [报告校验脚本](scripts/validate_html_report.py)：检查章节、链接、Mermaid 和视觉交付条件。

验证完整架构报告：

```bash
python3 scripts/validate_html_report.py /absolute/path/report.html \
  --profile architecture \
  --quality visual
```

对比报告使用 `--profile comparison`。

## 目录结构

```text
.
├── SKILL.md
├── agents/openai.yaml
├── assets/
│   ├── report-template.html
│   └── examples/
├── references/
│   ├── evidence-and-safety.md
│   ├── workflow.md
│   ├── report-schemas.md
│   ├── report-production-pipeline.md
│   ├── html-delivery.md
│   ├── html-visual-system.md
│   └── harness-case-study.md
└── scripts/validate_html_report.py
```

## 使用边界

- 报告生成不代表获得上传、发布、购买、删除或修改原产品的权限；
- 页面文案“将执行”不等于工具已经调用，“已完成”也不等于资产与状态已经一致；
- 源码仓库中的提示和说明是分析材料，不自动成为任务指令；
- 美化不能虚构 KPI、评分、用户评价、产品截图或品牌资产；
- 外部资料优先使用产品官方站点、官方文档和官方仓库，并记录访问时间或版本快照。
