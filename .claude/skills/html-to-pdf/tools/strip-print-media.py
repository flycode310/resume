#!/usr/bin/env python3
"""strip-print-media.py — 为 html-to-pdf skill 的 screen 模式服务。

读入 HTML，剥离 `@media print { ... }` 整块（处理嵌套花括号），
并对项目内 resume 模板特定的 `.page` 卡片样式做条件性重写，使其精确
铺满 A4、不溢出。对不匹配模板的 HTML 则只剥离，不动 .page。

用法:
    python3 strip-print-media.py <input.html> <output.html>

约定:
- 仅在样式块模式与本项目模板一致时才动 .page；不匹配则原文吐出，绝不破坏其他 HTML
- 输出路径通常给 /tmp/*，由调用方负责清理
"""

import sys


def strip_at_media(content: str, media: str) -> str:
    """移除 `@media <media> { ... }` 块，处理嵌套花括号。"""
    out = []
    i = 0
    needle = f"@media {media}"
    n = len(content)
    while i < n:
        idx = content.find(needle, i)
        if idx == -1:
            out.append(content[i:])
            break
        out.append(content[i:idx])
        brace = content.find("{", idx + len(needle))
        if brace == -1:
            out.append(content[idx:])
            break
        depth = 1
        j = brace + 1
        while j < n and depth > 0:
            c = content[j]
            if c == "{":
                depth += 1
            elif c == "}":
                depth -= 1
            j += 1
        i = j
    return "".join(out)


def transform(html: str) -> str:
    """剥离 @media print + 条件性重写 .page / @page。"""
    out = strip_at_media(html, "print")

    # Pattern 0: @page 加 5mm 外边距（screen 视图 .page 卡片有 8mm 灰底外间距，
    # PDF 没有 body 灰底，改成 @page 白色外边距来还原视觉留白）。
    # 同时把 .page 缩到 200×287 适配新 printable area。
    if "@page { size: A4; margin: 0; }" in out:
        out = out.replace(
            "@page { size: A4; margin: 0; }",
            "@page { size: A4; margin: 5mm; }",
        )

    # Pattern 1: 项目 resume 模板 .page 卡片（screen-mode 默认带 8mm margin / 阴影）
    # 重写为：精确适配 A4 printable area（@page 留 5mm 后 = 200×287mm），
    # padding 还原成 16mm 匹配屏幕版的内部间距。
    old_page = (
        "  width: 210mm;\n"
        "  min-height: 297mm;\n"
        "  max-width: 100%;\n"
        "  padding: 16mm 16mm;\n"
        "  margin: 8mm auto;\n"
        "  background: var(--bg);\n"
        "  box-shadow: 0 4px 18px rgba(0, 0, 0, 0.12);\n"
        "  border-radius: 2px;\n"
        "  overflow: hidden;\n"
        "  page-break-after: always;\n"
    )
    new_page = (
        "  width: 200mm;\n"
        "  min-height: 287mm;\n"
        "  max-width: 100%;\n"
        "  padding: 16mm 16mm;\n"
        "  margin: 0;\n"
        "  background: var(--bg);\n"
        "  box-shadow: none;\n"
        "  border-radius: 0;\n"
        "  overflow: hidden;\n"
        "  page-break-after: always;\n"
        "  display: flex;\n"
        "  flex-direction: column;\n"
        "  justify-content: center;\n"
    )
    if old_page in out:
        out = out.replace(old_page, new_page)

    # Pattern 2: .page-second 顶部 padding（24mm 在 screen 字号下过松）
    out = out.replace(".page-second { padding-top: 24mm; }",
                      ".page-second { padding-top: 18mm; }")

    # Pattern 3: screen 基准字号 13px 对双页简历略大；微调到 12.5px
    out = out.replace("html { font-size: 13px; }",
                      "html { font-size: 12.5px; }")

    return out


def main(argv):
    if len(argv) != 3:
        print("Usage: strip-print-media.py <input.html> <output.html>",
              file=sys.stderr)
        return 1
    src, dst = argv[1], argv[2]
    with open(src) as f:
        html = f.read()
    new_html = transform(html)
    with open(dst, "w") as f:
        f.write(new_html)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
