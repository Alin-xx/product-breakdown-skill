# HTML 交付规范

## 1. 文件与顺序

- 创建完整 `<!doctype html>` 独立文件，不只输出 HTML 片段。
- 文件名使用 ASCII 小写连字符，例如 `product-architecture-report.html`。
- 保存到用户工作区或用户指定目录。
- 按用户要求排列 section，并使用稳定 `id` 和置顶目录。
- 在 `<head>` 中声明语言、UTF-8、viewport、标题和准确的 description。
- 最终回复提供绝对路径的可点击链接。

## 2. 可读性

- 正文默认不小于 16px；支持亮/暗色；中文字体回退到 PingFang SC、Microsoft YaHei、sans-serif。
- 长表格放在横向滚动容器；移动端把多列卡片改为单列。
- 标签固定四类：已确认、合理推断、建议设计、未知；风险单独用红色。
- 证据 ID 使用等宽字体；截图路径可点击。
- 不使用没有来源的分数或装饰性 KPI。
- 不依赖颜色单独表达证据、风险、胜负或交互状态。

## 3. 图表

- Mermaid 图保留源码；可使用允许的 CDN 加载 Mermaid。
- 图必须有标题、图例和文字结论。
- 全景图必须含 subgraph、带文字的边、证据线型和风险节点。
- Mermaid 渲染失败时，表格和源码仍应让报告可读。
- 不用一张过密图代替所有表格；图负责关系，表负责证据和字段。

## 4. 证据链接

- 相对链接必须以 HTML 文件所在目录解析成功。
- 本地真实文件使用可点击链接；最终 Markdown 链接使用绝对本地路径，不使用 `file://`。
- 若浏览器不能读取本地页面，记录为证据缺口，不绕过安全策略。

## 5. 交互

允许目录跳转、折叠详情、复制 Mermaid/System Prompt、显示/隐藏长表。

所有交互需有 `:focus-visible`，锚点标题需留出滚动偏移；尊重 `prefers-reduced-motion`。

禁止网络提交、自动上传、发送消息、触发产品动作或读取本地存储敏感信息。

## 6. 最终校验

运行验证脚本，并检查 UTF-8、重复 ID、内部导航、本地证据链接、必需章节、Mermaid 数量、正文完整性、响应式和打印样式：

```bash
python3 scripts/validate_html_report.py /absolute/path/report.html --profile architecture --quality visual
```

在浏览器至少检查约 1440×900 和 390×844 两个视口。浏览器中的异常横向滚动、遮挡、文字溢出、低对比或 Mermaid 渲染失败都需要修复或明确记录。

若无法进行浏览器视觉 QA，明确说明只完成结构和链接校验，不宣称已验证渲染。
