# 研习手记

一个适合 GitHub Pages 的静态学习日志。内容用 Markdown 编写，网页由 Python 标准库生成，不依赖 npm、主题包或数据库。

## 最常用的更新方式

1. 复制 `content/logs/_template.md`。
2. 将文件名改为 `年-月-日-英文短名.md`，例如 `2026-09-25-medmnist-data.md`。
3. 修改开头的标题、日期、阶段、标签、摘要和学习时长，再写正文。
4. 提交并推送到 GitHub。GitHub Actions 会自动重新生成并发布网站。

也可以直接在 GitHub 网页中打开 `content/logs`，使用 **Add file → Create new file** 新建 Markdown 文件，提交后自动发布。

不要直接修改 `dist/` 中的网页；它们会在构建时重新生成。

## 更新首页进度

编辑 `content/site.json`：

- `current_focus`：首页当前学习重点；
- `current_note`：当前阶段的具体目标；
- `milestones`：路线卡片；
- `status` 只使用 `done`、`current` 或 `todo`。

学习路线的长说明在 `content/roadmap.md`。

## 本地预览

默认使用 `bio` 环境：

```bash
conda activate bio
python build.py
python -m http.server 8765 --directory dist
```

浏览器访问 `http://127.0.0.1:8765`。每次修改 Markdown 后重新运行 `python build.py`。

## 发布到 GitHub Pages

1. 在 GitHub 新建一个仓库，例如 `study-log`。如果希望任何人能访问，选择 Public。
2. 在本目录初始化并推送：

```bash
git init -b main
git add .
git commit -m "Create study log site"
git remote add origin https://github.com/你的用户名/study-log.git
git push -u origin main
```

3. 打开仓库的 **Settings → Pages**，在 **Build and deployment** 中选择 **GitHub Actions**。
4. 打开仓库的 **Actions** 页面；工作流完成后，Pages 页面会显示网站地址。

项目站点通常位于 `https://你的用户名.github.io/study-log/`。本项目全部使用相对链接，可以部署在仓库子路径下。

## 文件结构

```text
content/
  site.json             首页信息和路线状态
  roadmap.md            学习路线说明
  logs/                 Markdown 学习日志
assets/
  style.css             网站样式
  site.js               深浅色主题切换
build.py                静态网站生成器
dist/                   构建好的网页
.github/workflows/      GitHub Pages 自动发布
```

## Markdown 支持

构建器支持标题、段落、链接、粗体、斜体、行内代码、代码块、引用、有序列表和无序列表。它有意保持简单，便于长期维护。
