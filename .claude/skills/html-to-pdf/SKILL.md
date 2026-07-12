---
name: html-to-pdf
description: 把已排好版的 HTML 文件原样转成 PDF（CSS 样式、字体、页面大小、分页规则全部保留），通过 Chrome headless 渲染实现。典型场景：用户给出一个 A4 排版的简历 HTML 或任意网页 HTML，希望直接得到对应 PDF，不要二次加工。
---

# HTML → PDF 渲染 Skill

把 HTML 文件通过 Chrome headless 渲染成 PDF。**屏幕视图与打印视图两种模式可选**，详见下文「渲染模式」。

## 渲染模式

Chrome headless 的 `--print-to-pdf` 总是启用 `@media print`，由此引出两种渲染目标——选哪种取决于你想要的 PDF 像屏幕还是像打印：

| 模式 | 何时用 | 行为 |
|---|---|---|
| **`screen`**（默认） | 想让 PDF 看起来跟浏览器打开 HTML 时一致——宽松字号、阴影、卡片等屏幕效果 | 临时剥离 `@media print` 后渲染（绝不修改源 HTML），对项目内 resume 模板的 `.page` 卡片样式做条件性重写，使其正好铺满 A4 |
| **`print`** | 想让 PDF 严格遵从作者在 HTML 里写的 `@media print` 规则（如紧凑字号、纯白无阴影） | Chrome 直接渲染，不做任何 CSS 改写——这是早期 skill 的「原样输出」行为 |

参数格式：
- `/html-to-pdf <input.html>` → `screen` 模式（新默认，向后兼容老用户请显式传 `print`）
- `/html-to-pdf <input.html> screen` → 显式 `screen`
- `/html-to-pdf <input.html> print` → `print` 模式

## 输入

用户提供 HTML 文件的绝对路径或相对路径（相对当前工作目录），加上可选模式。

## 输出

默认输出 `<input-basename>.pdf`，与 HTML 同目录。
如用户提供 `<output>.pdf`，写到指定路径。

---

## 核心原则（仅 `print` 模式适用）

`print` 模式下严格不做改动：
- 不修改 HTML 源码
- 不追加/覆盖任何样式
- 不调整字号、边距、颜色
- A4、@page、page-break 等全部由 HTML 自身 CSS 决定
- 唯一目标是：HTML 在浏览器打印时是什么样，PDF 就是什么样

`screen` 模式则通过临时副本（不动源文件）剥离 `@media print`，最终产出的 PDF 与浏览器屏幕看到的视觉效果一致。

---

## 命令

### `print` 模式

```bash
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --headless --disable-gpu --no-sandbox \
  --print-to-pdf=<output>.pdf \
  --print-to-pdf-no-header \
  file://<input>.html
```

### `screen` 模式（三步）

```bash
# 1) 临时剥离 @media print（写到 /tmp，源 HTML 不动）
python3 <skill-dir>/tools/strip-print-media.py \
    <input>.html /tmp/html-to-pdf-stripped.html

# 2) 用 Chrome 渲染临时副本
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --headless --disable-gpu --no-sandbox \
  --print-to-pdf=<output>.pdf \
  --print-to-pdf-no-header \
  file:///tmp/html-to-pdf-stripped.html

# 3) 清理临时副本
rm /tmp/html-to-pdf-stripped.html
```

`<skill-dir>` 是这个 SKILL.md 所在的目录的绝对路径，例如：
`/Users/chenyayun/work/resume/.claude/skills/html-to-pdf/tools/strip-print-media.py`

参数说明：
- `--headless`：无界面渲染
- `--disable-gpu`：headless 模式下 GPU 不可用，必须禁掉
- `--no-sandbox`：在受限环境（CI、Docker）下避免沙盒失败
- `--print-to-pdf=<path>`：指定输出 PDF 路径
- `--print-to-pdf-no-header`：去掉 Chrome 自动注入的页眉/页脚（日期、URL、页码），保持 PDF 干净
- `file://<input>.html`：用 file:// 协议加载本地文件，确保字体/图片等相对资源可访问

---

## 执行流程

1. **确认 HTML 文件存在**，并读取前几行确认是 HTML（含 `<!DOCTYPE html>` 或 `<html>`）
2. **推导输出路径**：默认 `<input-basename>.pdf`，与 HTML 同目录
3. **解析模式**：从 args 取第二参数；缺省时 `screen`；遇到 `print`/`screen` 字面量按字面值走，其他情况按 `screen` 处理
4. **按模式渲染**：
   - `screen`：跑 `tools/strip-print-media.py` 出临时副本 → Chrome 渲染 → 清理临时副本
   - `print`：直接 Chrome 渲染
5. **验证输出**：
   - PDF 文件生成成功
   - 文件大小 > 1KB（避免空白 PDF）
   - 用 `mdls -name kMDItemNumberOfPages <pdf>` 确认页数符合预期
6. **报告**：告诉用户输出路径、页数、文件大小、所采用的模式

---

## 已知约束

- **macOS 专属**：命令硬编码 `/Applications/Google Chrome.app/...`。Linux/Windows 用户需自行修改 Chrome 路径。
- **依赖本地 Chrome**：必须已安装 Google Chrome（Chromium 也可以，路径不同）。
- **不处理 webfont 远程加载**：如果 HTML 引用了远程字体（@font-face 远程 URL），需要确保目标机器可访问公网，否则会 fallback 到系统字体。
- **不处理 `<script>` 动态内容**：Chrome headless 默认会执行 JS，但若页面依赖异步数据（如 fetch + setState），需要在 HTML 中保证 DOM 已渲染完成。
- **中文渲染**：依赖系统字体。macOS 自带 PingFang SC，Windows 自带 Microsoft YaHei，Linux 需自行安装 Noto Sans CJK。
- **`screen` 模式 + 模板不匹配**：`tools/strip-print-media.py` 只对项目内 resume 模板特化的 `.page`（`width: 210mm; min-height: 297mm; margin: 8mm auto; box-shadow: ...; border-radius: 2px;`）做条件性重写。如果你改了 `.page` 结构、或 HTML 不是这个模板，`.page` 不会被改，只剥 `@media print`。这时 `.page` 上屏的阴影、圆角、大 margin 会原样进 PDF——属预期行为，必要时改 HTML 或用 `print` 模式。
- **`screen` 模式 `.page` 缩放与 `@page` 外边距**：模板命中时，strip 会把 `.page` 由 210×297 改写为 200×287mm，并在 `@page` 上加 5mm 外边距，模拟屏幕视图里灰色 body 底色围绕 `.page` 卡片的 8mm 视觉间距。content area 从 178×265mm 缩到 168×255mm，能容纳现有页一 / 页二内容而不溢出。
- **新版 resume 模板直接 print 模式即可**：`templates/resume.css` 已重写为 PDF-ready（基线即 200×287 + flex 居中 + @page 5mm），没有 `@media print` 块。对使用新模板生成的 HTML，`screen` 模式 strip 后无差别（四个 pattern 全部 no-op）；可用 `print` 模式直接渲染，产物相同。

---

## 验证清单

- [ ] PDF 在 PDF 阅读器中打开正常
- [ ] 页数与 HTML 在浏览器对应模式下看到的页数一致（`screen` 看屏幕渲染，`print` 看 Chrome 打印预览）
- [ ] 字体、颜色、布局与对应视图（屏幕或打印预览）完全一致
- [ ] 没有 Chrome 注入的页眉/页脚（URL、日期、页码）

---

## 常见问题

**Q: 为什么默认 `screen` 而不是 `print`？**
A: 你说"把 HTML 转 PDF"，自然想看到跟浏览器打开一致的画面，而不是 `@media print` 里专门为节省纸张做的紧凑样式。`screen` 是新默认；要恢复旧的 print 行为，加 `print` 参数即可。

**Q: `screen` 模式下，PDF 里出现了阴影/卡片圆角/灰背景是怎么回事？**
A: 这些本来就在 HTML 的屏幕 CSS 里。`screen` 模式只剥 `@media print`，其他屏上样式（包括 `.page` 卡片的阴影/圆角/外 margin）会原样进 PDF。当前项目模板里 `strip-print-media.py` 会自动检测并清除 resume 模板特有的 `.page` 卡片样式（`width: 210mm; min-height: 297mm; margin: 8mm auto;` 那一段），保证打印干净；其他 HTML 没有这个特殊处理，需要自己调整 HTML。

**Q: 能不能不输出临时文件、不用 Python 脚本就做到 `screen` 渲染？**
A: 不能。Chrome headless 的 `--print-to-pdf` 没有公开的命令行 flag 强制 print media 关闭；必须借助「改 HTML → 渲染 → 还原」三步曲，或 Chrome DevTools Protocol 的 `Emulation.setEmulatedMedia`。前者更便于审计与离线工作流，所以选了前者。

**Q: 为什么不直接改源 HTML 把 `@media print` 删掉？**
A: 那是破坏性操作，会污染 git 历史、影响用户后续编辑。skill 通过 `/tmp` 临时副本做这件事，源文件永远不动。

**Q: 为什么不用 weasyprint / wkhtmltopdf？**
A: weasyprint 在 macOS 上依赖 GTK/pango 等系统库，安装繁琐；wkhtmltopdf 基于老版 QtWebKit，对现代 CSS 支持差。Chrome headless 用的是真实 Blink 渲染引擎，对现代 CSS（grid、flex、custom properties、@page）支持最完整，且 macOS 默认已装 Chrome。

**Q: HTML 用相对路径引用图片/CSS，PDF 能加载到吗？**
A: 可以。用 `file://` 协议加载 HTML 时，相对路径相对于 HTML 文件所在目录解析，与浏览器行为一致。
