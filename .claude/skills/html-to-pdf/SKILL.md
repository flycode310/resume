---
name: html-to-pdf
description: 把已排好版的 HTML 文件原样转成 PDF（CSS 样式、字体、页面大小、分页规则全部保留），通过 Chrome headless 渲染实现。典型场景：用户给出一个 A4 排版的简历 HTML 或任意网页 HTML，希望直接得到对应 PDF，不要二次加工。
---

# HTML → PDF 渲染 Skill

把 HTML 文件通过 Chrome headless 渲染成 PDF，**原封不动保留 HTML 中的所有 CSS、字体、页面尺寸与分页规则**——不会修改 HTML，不会注入额外样式，不会重排版。

## 触发场景

- 用户：「把这份 html 转成 pdf / 导出 pdf 版本」
- 用户：「按当前 html 输出 pdf」
- 用户：「用 chrome headless 给我生成一份 pdf」

## 核心原则

**只做渲染，不做改动。**

- 不修改 HTML 源码
- 不追加/覆盖任何样式
- 不调整字号、边距、颜色
- A4、@page、page-break 等全部由 HTML 自身 CSS 决定
- 唯一目标是：HTML 在浏览器打印时是什么样，PDF 就是什么样

## 输入

用户提供 HTML 文件的绝对路径或相对路径（相对当前工作目录）。

## 输出

默认输出 `<input-basename>.pdf`，与 HTML 同目录。
如用户提供 `<output>.pdf`，写到指定路径。

## 命令

```bash
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --headless --disable-gpu --no-sandbox \
  --print-to-pdf=<output>.pdf \
  --print-to-pdf-no-header \
  file://<input>.html
```

参数说明：
- `--headless`：无界面渲染
- `--disable-gpu`：headless 模式下 GPU 不可用，必须禁掉
- `--no-sandbox`：在受限环境（CI、Docker）下避免沙盒失败
- `--print-to-pdf=<path>`：指定输出 PDF 路径
- `--print-to-pdf-no-header`：去掉 Chrome 自动注入的页眉/页脚（日期、URL、页码），保持 PDF 干净
- `file://<input>.html`：用 file:// 协议加载本地文件，确保字体/图片等相对资源可访问

## 执行流程

1. **确认 HTML 文件存在**，并读取前几行确认是 HTML（含 `<!DOCTYPE html>` 或 `<html>`）
2. **推导输出路径**：默认 `<input-basename>.pdf`，与 HTML 同目录
3. **运行 Chrome headless 命令**
4. **验证输出**：
   - PDF 文件生成成功
   - 文件大小 > 1KB（避免空白 PDF）
   - 用 `mdls -name kMDItemNumberOfPages <pdf>` 确认页数符合预期
5. **报告**：告诉用户输出路径、页数、文件大小

## 已知约束

- **macOS 专属**：命令硬编码 `/Applications/Google Chrome.app/...`。Linux/Windows 用户需自行修改 Chrome 路径。
- **依赖本地 Chrome**：必须已安装 Google Chrome（Chromium 也可以，路径不同）。
- **不处理 webfont 远程加载**：如果 HTML 引用了远程字体（@font-face 远程 URL），需要确保目标机器可访问公网，否则会 fallback 到系统字体。
- **不处理 `<script>` 动态内容**：Chrome headless 默认会执行 JS，但若页面依赖异步数据（如 fetch + setState），需要在 HTML 中保证 DOM 已渲染完成。
- **中文渲染**：依赖系统字体。macOS 自带 PingFang SC，Windows 自带 Microsoft YaHei，Linux 需自行安装 Noto Sans CJK。

## 验证清单

- [ ] PDF 在 PDF 阅读器中打开正常
- [ ] 页数与 HTML 在浏览器「打印预览」中显示的页数一致
- [ ] 字体、颜色、布局与 HTML 屏幕预览完全一致（无 fallback 到默认字体）
- [ ] 没有 Chrome 注入的页眉/页脚（URL、日期、页码）

## 常见问题

**Q: 为什么不用 weasyprint / wkhtmltopdf？**
A: weasyprint 在 macOS 上依赖 GTK/pango 等系统库，安装繁琐；wkhtmltopdf 基于老版 QtWebKit，对现代 CSS 支持差。Chrome headless 用的是真实 Blink 渲染引擎，对现代 CSS（grid、flex、custom properties、@page）支持最完整，且 macOS 默认已装 Chrome。

**Q: HTML 用相对路径引用图片/CSS，PDF 能加载到吗？**
A: 可以。用 `file://` 协议加载 HTML 时，相对路径相对于 HTML 文件所在目录解析，与浏览器行为一致。