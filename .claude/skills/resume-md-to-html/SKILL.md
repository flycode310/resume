---
name: resume-md-to-html
description: 将符合规范的简历 Markdown 自动渲染成 A4 双页排版的 HTML（屏幕预览 + PDF 打印双优化）。使用场景：用户提供写好的简历 Markdown 文件，希望生成可直接打印 PDF 的精美 HTML 输出。会读取 md 结构、套用预设 CSS 模板、按 A4 自动分页。
---

# Resume Markdown → HTML 渲染 Skill

把规范的简历 Markdown 自动转换为 A4 双页排版的 HTML 文件，CSS 已针对屏幕预览和 PDF 打印双向优化。

## 触发场景

- 用户：「把这份简历 md 转成 html / pdf / 排版好的版本」
- 用户：「用我的简历 md 生成可直接投递的 pdf」
- 用户：「按 A4 排版这份简历」

## 输入约定

用户提供 Markdown 文件路径，结构必须严格匹配：

```markdown
# 姓名

## 基本信息
📱 手机号 · ✉️ 邮箱
**目标岗位**：xxx
**期望城市**：xx

## 教育背景
**学校** | 专业 | 学历 | 起止时间

## 工作经历
### 公司 | 职位 | 起止时间
- 职责描述
- 职责描述

## 技术栈
- **分类**：内容
- **分类**：内容

## 项目经验
### 项目一：标题
**时间** | **角色** | 团队

**项目背景**
- 背景 1
- 背景 2

**技术方案**
- **要点**：内容

**个人贡献**
- 贡献 1

**项目成果**
- **[类别]** 内容

`tag1` · `tag2` · `tag3`
```

## 输出

生成 `<输入文件名>.html`，与 md 同目录。

**默认分页（适合 2-3 个项目的简历）：**

| 页 | 内容 |
|---|---|
| 1 | 基本信息 + 求职意向 + 教育背景 + 工作经历 + **项目一** |
| 2 | **项目二** + **项目三** + **技术栈** |

**备选分页（如项目一内容过多导致第 1 页溢出）：**

| 页 | 内容 |
|---|---|
| 1 | 基本信息 + 求职意向 + 教育背景 + 工作经历 + 技术栈 + 项目一（紧凑模式） |
| 2 | 项目二 + 项目三 |

根据首个项目的 bullet 数判断：技术方案 + 个人贡献 + 项目成果 ≤ 12 条时用默认分页；超过用紧凑分页。

## 渲染流程

1. **Read** 用户提供的 md 文件，定位每个章节
2. **解析** 项目经验里的项目数；如有 3 个项目，按上表默认分页
3. **生成** HTML，按以下顺序组装（不要省略任何 section）：
   ```
   <div class="page">  <!-- 第 1 页 -->
     <div class="header"> 姓名 + 联系方式 </div>
     <section> 求职意向 </section>
     <section> 教育背景 </section>
     <section> 工作经历 </section>
     [默认] <section> 项目经验 (Project 1) </section>
     [紧凑] <section> 技术栈 </section>
     [紧凑] <section> 项目经验 (Project 1) </section>
   </div>
   <div class="page">  <!-- 第 2 页 -->
     [默认] <div class="project"> 项目二 </div>
     [默认] <div class="project"> 项目三 </div>
     [默认] <section> 技术栈 </section>
     [紧凑] <div class="project"> 项目二 </div>
     [紧凑] <div class="project"> 项目三 </div>
   </div>
   ```
4. **嵌入 CSS** — 直接把 `<skill-dir>/templates/resume.css` 全部内容粘贴到 `<style>` 标签内（不要外链，确保文件可独立打开）
5. **保存** 为 `<input-basename>.html`
6. **可选 PDF**（如果用户要求）：用 chrome headless 转 PDF
   ```bash
   /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
     --headless --disable-gpu --no-sandbox \
     --print-to-pdf=<input>.pdf --print-to-pdf-no-header \
     file://$PWD/<input>.html
   ```

## HTML 元素映射（md → HTML）

| Markdown 结构 | HTML 输出 |
|---|---|
| `# 姓名` | `<div class="header"><h1>姓名</h1>...</div>` |
| `📱 xxx · ✉️ xxx` | `<div class="contact"><span>📱 xxx</span>...</div>` |
| `**目标岗位**：xxx` | `<div class="intent"><span class="label">目标岗位：</span><span>xxx</span></div>` |
| `**学校** \| ... \| 时间` | `<div class="edu-item"><strong>学校</strong>\|...\|时间</div>` |
| `### 公司 \| 职位 \| 时间` + bullets | `<div class="work-item"><div class="work-head">...<span class="time">时间</span></div><ul>...</ul></div>` |
| `- **分类**：内容` (技术栈) | `<li><strong>分类</strong>：内容</li>` |
| `- 背景/方案/贡献/成果 bullet` | `<li>...</li>` |
| `**要点**：内容` (项目内) | `<li><strong>要点</strong>：内容</li>` |
| `**[类别]** 内容` (项目成果) | `<li><strong>[类别]</strong> 内容</li>` |
| `` `tag1` · `tag2` `` | `<div class="project-tags"><span class="tag">tag1</span>...</div>` |

## 项目模块结构（每个项目用此结构）

```html
<div class="project">
  <div class="project-head">
    <div class="project-title">项目一：xxx</div>
    <div class="project-meta">时间 · <strong>角色</strong> · 团队</div>
  </div>

  <div class="project-section">
    <span class="project-section-title">项目背景</span>
    <ul><li>...</li></ul>
  </div>

  <div class="project-section">
    <span class="project-section-title">技术方案</span>
    <ul><li><strong>要点</strong>：内容</li></ul>
  </div>

  <div class="project-section">
    <span class="project-section-title">个人贡献</span>
    <ul><li>...</li></ul>
  </div>

  <div class="project-section">
    <span class="project-section-title">项目成果</span>
    <ul><li><strong>[类别]</strong> 内容</li></ul>
  </div>

  <div class="project-tags">
    <span class="tag">tag</span>
  </div>
</div>
```

## 排版要点（CSS 已实现）

- **A4 单页容器：** `.page { width: 210mm; min-height: 297mm; padding: 16mm 16mm; }`
- **打印分页：** `@page { size: A4; margin: 0; }` + `.page { page-break-after: always; }` 让每张 div 强制对应一张物理 A4
- **中文优先字体：** `-apple-system, "PingFang SC", "Microsoft YaHei"`
- **统一蓝色小圆点 bullet：** `#2563eb` 色，6px 圆点
- **灰色 callout：** 仅 `.project-bg` 使用，背景 `#f9fafb` + 蓝色左边线
- **响应式：** `<768px` 切换为单列滚动布局，去掉 A4 阴影

## 已知约束

- 设计针对 2-3 个项目 + 5 条以内技术栈分类的典型技术简历
- 工作经历超过 8 条 bullet 时第 1 页会拥挤，建议精简
- 项目背景/方案/贡献/成果加起来超过 15 条 bullet 时考虑拆分为两页项目
- 不支持：单项目展示、英文简历、双栏布局、自定义主题色（需要手动改 CSS）

## 验证清单

生成完成后逐项检查：

- [ ] HTML 在浏览器打开显示 2 张 A4 卡片堆叠
- [ ] 标题 + 副标题 + 联系方式 都在第 1 页顶部
- [ ] 每个项目都有 项目背景/技术方案/个人贡献/项目成果 4 个小节（如果 md 里都有）
- [ ] tags 用蓝色 chip 渲染
- [ ] 浏览器「打印 → 另存为 PDF」输出正好 2 页 A4
- [ ] 第 1 页项目一没有溢出（A4 高度内）
