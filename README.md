# 研习手记

这是我的个人学习记录网站，用来整理医学影像、深度学习、多模态学习和计算生物学相关内容。学习记录使用 Markdown 编写，由 `build.py` 生成静态网页，再通过 GitHub Actions 部署到 GitHub Pages。

## 常用链接

- 在线网站：<https://elermidefault.github.io/LearningNotes/>
- GitHub 仓库：<https://github.com/ElermiDefault/LearningNotes>
- 部署记录：<https://github.com/ElermiDefault/LearningNotes/actions>
- Pages 设置：<https://github.com/ElermiDefault/LearningNotes/settings/pages>

本地仓库路径：

```text
/Volumes/GYF's HDD/预备工作/Web
```

## 网站如何工作

1. 学习记录保存在 `content/logs/`。
2. 首页内容和学习路线配置保存在 `content/site.json` 与 `content/roadmap.md`。
3. `python build.py` 读取这些源文件并生成 `dist/`。
4. 推送到 `main` 后，`.github/workflows/pages.yml` 会在 GitHub 上重新执行构建。
5. GitHub Pages 发布生成的 `dist/`。

`dist/` 是生成目录，已经被 `.gitignore` 忽略。不要直接修改或提交其中的文件；下次运行 `build.py` 时它们会被覆盖。

## 最常用的更新流程

开始写记录前，先同步远程仓库：

```bash
cd "/Volumes/GYF's HDD/预备工作/Web"
git status
git pull --ff-only origin main
```

复制模板并创建记录。文件名中的英文短名会成为网页地址的一部分，建议使用小写英文和连字符：

```bash
cp content/logs/_template.md content/logs/2026-09-24-pathmnist-training.md
```

编辑完成后，在本地构建并预览：

```bash
conda activate bio
python build.py
python -m http.server 8765 --directory dist
```

浏览器访问 <http://127.0.0.1:8765/>。停止预览服务器时，在终端按 `Control + C`。

确认页面正确后，只暂存本次修改涉及的源文件：

```bash
git status
git diff
git add content/logs/2026-09-24-pathmnist-training.md
git commit -m "content: add PathMNIST training notes"
git push origin main
```

推送后，在 [GitHub Actions](https://github.com/ElermiDefault/LearningNotes/actions) 等待部署完成，然后打开[在线网站](https://elermidefault.github.io/LearningNotes/)检查结果。

## 如何编写学习记录

### 文件名

学习记录放在 `content/logs/`，建议使用以下格式：

```text
年-月-日-英文短名.md
```

例如：

```text
2026-09-24-pathmnist-training.md
2026-10-03-monai-tutorial.md
```

日期前缀便于管理文件；英文短名会用于网页路径。不要在短名中使用空格。

### 一篇完整记录

可以复制 `content/logs/_template.md`，也可以使用下面的格式：

````markdown
---
title: A2：训练 PathMNIST 基线模型
date: 2026-09-24
stage: Project A · MedMNIST
tags: 病理影像, 分类, PyTorch
summary: 完成 PathMNIST 基线训练，并记录数据划分、评价指标和错误样本。
hours: 2.5
---

## 今天做了什么

- 完成训练和验证流程
- 记录准确率与宏平均 F1
- 检查容易混淆的类别

## 我弄明白了什么

写下今天真正理解的概念，而不是只罗列运行过的代码。

## 遇到的问题

1. 问题是什么
2. 尝试过哪些方法
3. 最后是否解决

## 结果与文件

- Notebook：[查看实验代码](https://github.com/ElermiDefault/项目仓库/blob/main/notebooks/example.ipynb)
- 关键结果：`macro_f1 = 0.82`

## 下一步

- [ ] 完成错误样本可视化
- [ ] 比较不同数据增强方法
````

Front matter 是文件顶部两条 `---` 之间的元数据：

| 字段 | 是否必填 | 用途 |
| --- | --- | --- |
| `title` | 是 | 网页标题和记录列表标题 |
| `date` | 是 | 日期，必须使用 `YYYY-MM-DD` |
| `summary` | 是 | 首页和归档页上的简短摘要 |
| `stage` | 否 | 当前项目或学习阶段 |
| `tags` | 否 | 使用英文逗号分隔多个标签 |
| `hours` | 否 | 学习时长，填写数字，例如 `1.5` |

`summary` 适合写一两句话。`---` 后面的 Markdown 正文会显示在独立详情页，也可以在首页和归档页点击“查看完整记录”展开。

当前构建器支持：

- 一级至三级标题；
- 普通段落；
- 有序列表和无序列表；
- 粗体、斜体和行内代码；
- Markdown 链接；
- 引用；
- 围栏代码块。

### 记录 Notebook 和实验文件

下面这种本机绝对路径只能作为文字显示，部署后其他设备无法访问：

```text
/Volumes/GYF's HDD/预备工作/Project_A/work/01_data_audit.ipynb
```

如果希望网页上的链接能够打开文件，应先把文件放入某个 GitHub 仓库，再使用完整链接：

```markdown
[查看数据审计 Notebook](https://github.com/ElermiDefault/仓库名/blob/main/work/01_data_audit.ipynb)
```

也可以把小型文件复制到本仓库的合适目录，再使用相对于网页的链接。不要把大型数据集、模型权重或包含隐私的数据提交到 GitHub。

## 修改首页和学习路线

首页配置位于 `content/site.json`：

| 字段 | 用途 |
| --- | --- |
| `hero_eyebrow` | 首页主标题上方的小标题 |
| `current_focus` | 首页主标题 |
| `current_note` | 当前学习状态 |
| `summary_quote` | 右侧引语 |
| `summary_items` | 引语下方的状态列表 |
| `roadmap_note` | 学习路线标题下方的说明 |
| `footer_text` | 页脚文字 |
| `milestones` | 学习路线卡片 |

`milestones` 中的 `status` 只使用以下三个值：

- `current`：正在进行；
- `done`：已经完成；
- `todo`：尚未开始。

学习路线的长篇说明保存在 `content/roadmap.md`。

修改配置后必须重新运行：

```bash
python build.py
```

## 本地构建与预览

这个项目只使用 Python 标准库，不需要安装额外的 Python 包。默认使用 `bio` conda 环境：

```bash
cd "/Volumes/GYF's HDD/预备工作/Web"
conda activate bio
python build.py
python -m http.server 8765 --directory dist
```

访问：<http://127.0.0.1:8765/>

在 macOS 中也可以运行：

```bash
open http://127.0.0.1:8765/
```

每次修改 Markdown、`content/site.json`、`build.py` 或 `assets/` 后，都要重新运行 `python build.py`。如果页面仍显示旧内容，可以按 `Command + Shift + R` 强制刷新。

## Git 日常命令

### 查看当前状态和历史

```bash
git status
git diff
git log --oneline --decorate --graph -10
git remote -v
```

- `git status`：查看哪些文件被修改、暂存或忽略。
- `git diff`：查看尚未暂存的具体修改。
- `git log`：查看最近的提交。
- `git remote -v`：检查远程仓库地址。

### 暂存、提交和推送

优先明确写出要提交的文件，避免用 `git add .` 把无关修改一起提交：

```bash
git add content/logs/2026-09-24-pathmnist-training.md
git status
git diff --cached
git commit -m "content: add PathMNIST training notes"
git push origin main
```

常用提交信息示例：

```text
content: add MedMNIST experiment notes
content: update multimodal learning roadmap
site: improve learning log layout
fix: correct Markdown rendering
chore: update GitHub Pages workflow
docs: improve repository instructions
```

一次提交尽量只完成一类事情。学习内容、网站功能和部署配置不要混在同一个提交里。

### 拉取远程修改

最好在开始编辑前拉取：

```bash
git status
git pull --ff-only origin main
```

`--ff-only` 可以防止 Git 在不知情的情况下自动创建合并提交。如果已经在本地提交，而远程也出现了新提交，可以先检查双方差异：

```bash
git fetch origin
git log --oneline --left-right main...origin/main
```

确认需要把本地提交放到远程提交之后时，再运行：

```bash
git pull --rebase origin main
```

如果 rebase 出现冲突：

```bash
# 手动编辑冲突文件，然后：
git add 冲突文件
git rebase --continue

# 如果不想继续：
git rebase --abort
```

### 撤销尚未提交的操作

取消暂存，但保留文件修改：

```bash
git restore --staged 文件路径
```

丢弃某个文件尚未提交的修改：

```bash
git restore 文件路径
```

第二条命令会删除该文件未提交的修改，运行前应先用 `git diff` 检查。

## 从零初始化一个新 Git 仓库

这一节只用于以后创建新项目。当前 `LearningNotes` 已经初始化，不要在其中重复运行 `git init`。

首次使用 Git 时配置身份：

```bash
git config --global user.name "你的 GitHub 用户名"
git config --global user.email "你的 GitHub 邮箱"
```

初始化本地仓库：

```bash
mkdir 新项目名称
cd 新项目名称
git init -b main
printf "# 新项目名称\n" > README.md
git add README.md
git commit -m "Initial commit"
```

然后打开 <https://github.com/new> 创建远程仓库。如果本地已经有 README 和提交，创建远程仓库时不要勾选自动添加 README、`.gitignore` 或 License。

连接远程仓库并首次推送：

```bash
git remote add origin git@github.com:ElermiDefault/仓库名.git
git remote -v
git push -u origin main
```

如果使用 HTTPS：

```bash
git remote add origin https://github.com/ElermiDefault/仓库名.git
git push -u origin main
```

如果安装并登录了 GitHub CLI，也可以直接创建：

```bash
gh auth login
gh repo create 仓库名 --public --source=. --remote=origin --push
```

## 在另一台电脑获取这个仓库

使用 SSH：

```bash
git clone git@github.com:ElermiDefault/LearningNotes.git
cd LearningNotes
```

或者使用 HTTPS：

```bash
git clone https://github.com/ElermiDefault/LearningNotes.git
cd LearningNotes
```

克隆后检查：

```bash
git status
git remote -v
conda activate bio
python build.py
```

## GitHub Pages 远程部署

当前远程部署地址：

<https://elermidefault.github.io/LearningNotes/>

部署由 `.github/workflows/pages.yml` 管理。每次向 `main` 推送提交后，GitHub Actions 会：

1. 检出仓库；
2. 配置 Python 3.12；
3. 执行 `python build.py`；
4. 上传 `dist/`；
5. 发布到 GitHub Pages。

查看部署状态：<https://github.com/ElermiDefault/LearningNotes/actions>

正常情况下，推送后等待工作流显示绿色对勾，再刷新在线网站。若部署失败：

1. 打开失败的 Actions 运行；
2. 展开带红色叉号的步骤；
3. 先阅读最后一段错误信息；
4. 在本地运行 `python build.py` 复现；
5. 修复后重新提交并推送。

GitHub 仓库的 **Settings → Pages → Build and deployment** 应选择 **GitHub Actions**。

## 常见问题

### 修改后本地页面没有变化

重新构建，然后强制刷新：

```bash
python build.py
```

不要直接修改 `dist/index.html`，因为它会被重新生成。

### 推送被拒绝

通常表示远程已有新提交：

```bash
git fetch origin
git status
git pull --rebase origin main
git push origin main
```

出现冲突时不要盲目继续，先检查冲突标记并确认要保留的内容。

### 在线网站还是旧内容

依次检查：

1. `git status` 是否还有忘记提交的文件；
2. `git log -1 --oneline` 是否显示最新提交；
3. Actions 是否部署成功；
4. 浏览器是否需要强制刷新；
5. 修改的是源文件还是会被覆盖的 `dist/`。

## 项目结构

```text
.
├── .github/workflows/pages.yml   # GitHub Pages 自动部署
├── .gitignore                    # 忽略本机文件和生成目录
├── assets/
│   ├── site.js                   # 深浅色主题切换
│   └── style.css                 # 网站样式
├── content/
│   ├── logs/                     # Markdown 学习记录
│   ├── roadmap.md                # 学习路线长说明
│   └── site.json                 # 首页和路线配置
├── build.py                      # 静态网站生成器
├── dist/                         # 本地构建产物，不纳入版本控制
└── README.md                     # 当前使用说明
```
