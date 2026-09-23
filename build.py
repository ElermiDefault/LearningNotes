#!/usr/bin/env python3
"""Build the static study log with Python's standard library only."""

from __future__ import annotations

import datetime as dt
import html
import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CONTENT = ROOT / "content"
DIST = ROOT / "dist"
ASSETS = ROOT / "assets"


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---\n", 4)
    if end == -1:
        raise ValueError("Front matter is missing its closing ---")
    metadata: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        key, separator, value = line.partition(":")
        if not separator:
            raise ValueError(f"Invalid front matter line: {line}")
        metadata[key.strip()] = value.strip().strip('"').strip("'")
    return metadata, text[end + 5 :]


def inline_markdown(text: str) -> str:
    escaped = html.escape(text, quote=False)
    escaped = re.sub(r"`([^`]+)`", r"<code>\1</code>", escaped)
    escaped = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", escaped)
    escaped = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", escaped)

    def link(match: re.Match[str]) -> str:
        label, url = match.group(1), match.group(2).strip()
        safe = url if re.match(r"^(https?://|mailto:|/|#|\.\.?/)", url) else "#"
        external = ' target="_blank" rel="noreferrer"' if safe.startswith("http") else ""
        return f'<a href="{html.escape(safe, quote=True)}"{external}>{label}</a>'

    return re.sub(r"\[([^\]]+)\]\(([^)]+)\)", link, escaped)


def markdown_to_html(markdown: str) -> str:
    lines = markdown.replace("\r\n", "\n").split("\n")
    out: list[str] = []
    paragraph: list[str] = []
    list_type: str | None = None
    in_code = False
    code_lines: list[str] = []

    def flush_paragraph() -> None:
        nonlocal paragraph
        if paragraph:
            out.append(f"<p>{inline_markdown(' '.join(part.strip() for part in paragraph))}</p>")
            paragraph = []

    def close_list() -> None:
        nonlocal list_type
        if list_type:
            out.append(f"</{list_type}>")
            list_type = None

    for line in lines:
        if line.startswith("```"):
            flush_paragraph()
            close_list()
            if in_code:
                out.append(f"<pre><code>{html.escape(chr(10).join(code_lines))}</code></pre>")
                code_lines = []
                in_code = False
            else:
                in_code = True
            continue
        if in_code:
            code_lines.append(line)
            continue
        if not line.strip():
            flush_paragraph()
            close_list()
            continue
        heading = re.match(r"^(#{1,3})\s+(.+)$", line)
        if heading:
            flush_paragraph()
            close_list()
            level = len(heading.group(1))
            out.append(f"<h{level}>{inline_markdown(heading.group(2))}</h{level}>")
            continue
        unordered = re.match(r"^[-*]\s+(.+)$", line)
        ordered = re.match(r"^\d+[.)]\s+(.+)$", line)
        if unordered or ordered:
            flush_paragraph()
            desired = "ul" if unordered else "ol"
            if list_type != desired:
                close_list()
                list_type = desired
                out.append(f"<{desired}>")
            item = (unordered or ordered).group(1)
            out.append(f"<li>{inline_markdown(item)}</li>")
            continue
        if line.startswith("> "):
            flush_paragraph()
            close_list()
            out.append(f"<blockquote><p>{inline_markdown(line[2:])}</p></blockquote>")
            continue
        paragraph.append(line)

    flush_paragraph()
    close_list()
    if in_code:
        out.append(f"<pre><code>{html.escape(chr(10).join(code_lines))}</code></pre>")
    return "\n".join(out)


def page_template(site: dict, title: str, content: str, path_prefix: str = "", current: str = "") -> str:
    site_title = html.escape(site["title"])
    page_title = site_title if title == site["title"] else f"{html.escape(title)} · {site_title}"
    description = html.escape(site["description"], quote=True)
    favicon = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='16' fill='%232563eb'/%3E%3Cpath d='M18 17h22a8 8 0 0 1 8 8v22H26a8 8 0 0 1-8-8V17Z' fill='none' stroke='white' stroke-width='5'/%3E%3Cpath d='M27 28h13M27 37h9' stroke='white' stroke-width='4' stroke-linecap='round'/%3E%3C/svg%3E"

    def nav_link(label: str, href: str, key: str) -> str:
        selected = ' aria-current="page"' if current == key else ""
        return f'<a href="{path_prefix}{href}"{selected}>{label}</a>'

    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="{description}">
  <meta name="color-scheme" content="light dark">
  <title>{page_title}</title>
  <link rel="icon" type="image/svg+xml" href="{favicon}">
  <link rel="stylesheet" href="{path_prefix}assets/style.css">
</head>
<body>
  <a class="skip-link" href="#main">跳到正文</a>
  <header class="site-header">
    <nav class="nav" aria-label="主导航">
      <a class="brand" href="{path_prefix}index.html"><span class="brand-mark">记</span><span>{site_title}</span></a>
      <div class="nav-actions">
        <div class="nav-links">
          {nav_link('首页', 'index.html', 'home')}
          {nav_link('全部记录', 'archive/index.html', 'archive')}
          {nav_link('学习路线', 'roadmap/index.html', 'roadmap')}
        </div>
        <button class="theme-toggle" type="button" data-theme-toggle aria-label="切换主题">深色</button>
      </div>
    </nav>
  </header>
  <main id="main">{content}</main>
  <footer class="site-footer">
    <div class="footer-inner"><span>{site_title} · 持续记录，定期复盘</span><span>最后构建：{dt.date.today().isoformat()}</span></div>
  </footer>
  <script src="{path_prefix}assets/site.js"></script>
</body>
</html>
"""


def read_logs() -> list[dict]:
    logs: list[dict] = []
    for path in sorted((CONTENT / "logs").glob("*.md")):
        if path.name.startswith("_"):
            continue
        metadata, body = parse_frontmatter(path.read_text(encoding="utf-8"))
        required = {"title", "date", "summary"}
        missing = required - metadata.keys()
        if missing:
            raise ValueError(f"{path.name} is missing: {', '.join(sorted(missing))}")
        dt.date.fromisoformat(metadata["date"])
        logs.append(
            {
                **metadata,
                "body_html": markdown_to_html(body),
                "slug": path.stem[11:] if re.match(r"^\d{4}-\d{2}-\d{2}-", path.stem) else path.stem,
                "tags_list": [tag.strip() for tag in metadata.get("tags", "").split(",") if tag.strip()],
                "hours_value": float(metadata.get("hours", 0) or 0),
            }
        )
    return sorted(logs, key=lambda entry: entry["date"], reverse=True)


def tags_html(tags: list[str]) -> str:
    return "".join(f'<span class="tag">{html.escape(tag)}</span>' for tag in tags)


def log_card(entry: dict, prefix: str = "") -> str:
    return f"""<article class="panel log-card">
  <time class="log-date" datetime="{entry['date']}">{entry['date']}</time>
  <div>
    <h3><a href="{prefix}logs/{html.escape(entry['slug'])}/index.html">{html.escape(entry['title'])}</a></h3>
    <p class="log-summary">{html.escape(entry['summary'])}</p>
  </div>
  <div class="tags">{tags_html(entry['tags_list'])}</div>
</article>"""


def build() -> None:
    site = json.loads((CONTENT / "site.json").read_text(encoding="utf-8"))
    logs = read_logs()
    if DIST.exists():
        shutil.rmtree(DIST)
    (DIST / "assets").mkdir(parents=True)
    shutil.copy2(ASSETS / "style.css", DIST / "assets" / "style.css")
    shutil.copy2(ASSETS / "site.js", DIST / "assets" / "site.js")
    (DIST / ".nojekyll").write_text("", encoding="utf-8")

    done_count = sum(item["status"] == "done" for item in site["milestones"])
    active_count = sum(item["status"] == "current" for item in site["milestones"])
    total = len(site["milestones"])
    progress = round((done_count + 0.5 * active_count) / total * 100) if total else 0
    hours = sum(item["hours_value"] for item in logs)
    hours_label = f"{hours:g}"

    roadmap_cards = "".join(
        f"""<article class="panel roadmap-item {html.escape(item['status'])}">
  <span class="roadmap-index">{index:02d}</span>
  <h3>{html.escape(item['title'])}</h3>
  <p class="roadmap-repo">{html.escape(item['repo'])}</p>
  <p class="roadmap-description">{html.escape(item['description'])}</p>
</article>"""
        for index, item in enumerate(site["milestones"], start=1)
    )
    recent = "\n".join(log_card(entry) for entry in logs[:4]) or '<div class="panel empty-state">第一篇学习记录会出现在这里。</div>'

    home = f"""<div class="page-shell">
  <section class="dashboard-grid" aria-labelledby="current-focus">
    <div class="panel focus-panel">
      <div class="focus-copy">
        <p class="eyebrow">Current focus</p>
        <h1 id="current-focus">{html.escape(site['current_focus'])}</h1>
        <p class="focus-note">{html.escape(site['current_note'])}</p>
      </div>
    </div>
    <aside class="panel summary-panel" aria-label="学习概览">
      <div class="progress-ring" style="--progress: {progress}%"><strong>{progress}%</strong><span>路线进度</span></div>
      <div class="summary-stats">
        <div class="stat"><strong>{len(logs)}</strong><span>学习记录</span></div>
        <div class="stat"><strong>{hours_label}</strong><span>记录小时</span></div>
      </div>
    </aside>
  </section>
  <section class="section" aria-labelledby="roadmap-heading">
    <div class="section-heading"><div><h2 id="roadmap-heading">学习路线</h2><p>按成果推进，不按日期赶进度。</p></div><a class="text-link" href="roadmap/index.html">查看说明 →</a></div>
    <div class="roadmap-list">{roadmap_cards}</div>
  </section>
  <section class="section" aria-labelledby="recent-heading">
    <div class="section-heading"><div><h2 id="recent-heading">最近记录</h2><p>写下做过的事，也保留没有解决的问题。</p></div><a class="text-link" href="archive/index.html">全部记录 →</a></div>
    <div class="log-list">{recent}</div>
  </section>
</div>"""
    (DIST / "index.html").write_text(page_template(site, site["title"], home, current="home"), encoding="utf-8")

    archive_content = f"""<div class="page-shell article-shell">
  <header class="article-header"><p class="eyebrow">Learning log</p><h1>全部记录</h1><p class="focus-note">共 {len(logs)} 篇，累计记录 {hours_label} 小时。</p></header>
  <div class="log-list">{''.join(log_card(entry, '../') for entry in logs) or '<div class="panel empty-state">还没有记录。</div>'}</div>
</div>"""
    (DIST / "archive").mkdir()
    (DIST / "archive" / "index.html").write_text(page_template(site, "全部记录", archive_content, "../", "archive"), encoding="utf-8")

    roadmap_body = markdown_to_html((CONTENT / "roadmap.md").read_text(encoding="utf-8"))
    roadmap_content = f'<div class="page-shell article-shell"><article class="article-content">{roadmap_body}</article></div>'
    (DIST / "roadmap").mkdir()
    (DIST / "roadmap" / "index.html").write_text(page_template(site, "学习路线", roadmap_content, "../", "roadmap"), encoding="utf-8")

    for entry in logs:
        output = DIST / "logs" / entry["slug"]
        output.mkdir(parents=True)
        metadata_bits = [f'<time datetime="{entry["date"]}">{entry["date"]}</time>']
        if entry.get("stage"):
            metadata_bits.append(f'<span>{html.escape(entry["stage"])}</span>')
        if entry["hours_value"]:
            metadata_bits.append(f'<span>{entry["hours_value"]:g} 小时</span>')
        article = f"""<div class="page-shell article-shell">
  <article>
    <header class="article-header">
      <p class="eyebrow">Learning log</p>
      <h1>{html.escape(entry['title'])}</h1>
      <div class="article-meta">{''.join(metadata_bits)}{tags_html(entry['tags_list'])}</div>
    </header>
    <div class="article-content">{entry['body_html']}</div>
  </article>
</div>"""
        (output / "index.html").write_text(page_template(site, entry["title"], article, "../../"), encoding="utf-8")

    print(f"Built {len(logs)} log(s) into {DIST}")


if __name__ == "__main__":
    build()
