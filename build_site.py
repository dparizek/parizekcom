#!/usr/bin/env python3
"""
Build a static HTML site from the Markdown files in output/.

Produces:
  site/
    index.html          — all posts by year + pages list
    posts/<slug>.html   — individual post pages
    pages/<slug>.html   — individual pages
"""

import re
import markdown
from pathlib import Path
from collections import defaultdict

BASE    = Path(__file__).parent
MD_DIR  = BASE / "output"
SITE    = BASE / "site"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def preprocess_urls(text: str) -> str:
    # Convert [word https://url] shortcodes → [word](https://url)
    text = re.sub(r'\[(\w+)\s+(https?://[^\]\s]+)\]', r'[\1](\2)', text)

    # Linkify bare URLs not already wrapped in markdown or angle brackets.
    # Match three alternatives; only replace the third (bare URL).
    pattern = re.compile(
        r'(\]\(https?://[^\)]*\))'    # group 1: already inside ](url) — skip
        r'|(<https?://[^>]*>)'         # group 2: angle-bracket URL — skip
        r'|(https?://[^\s<>\[\]"\']+)' # group 3: bare URL — linkify
    )
    def _replace(m):
        if m.group(1) or m.group(2):
            return m.group(0)
        url = m.group(3).rstrip('.,;:!?)')
        return f'[{url}]({url})'
    return pattern.sub(_replace, text)


def parse_md_file(path: Path) -> dict:
    """Return {front_matter dict, body_html}."""
    text = path.read_text(encoding="utf-8")

    fm = {}
    body = text

    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            raw_fm = parts[1].strip()
            body   = parts[2].strip()
            for line in raw_fm.splitlines():
                if ":" in line and not line.startswith(" ") and not line.startswith("-"):
                    k, _, v = line.partition(":")
                    fm[k.strip()] = v.strip().strip('"')
                elif line.startswith("  - ") and "last_key" in fm:
                    fm.setdefault("_" + fm["last_key"], []).append(line[4:].strip().strip('"'))

            # Re-parse lists properly
            fm2 = {}
            current_key = None
            for line in raw_fm.splitlines():
                if line.startswith("  - "):
                    if current_key:
                        fm2.setdefault(current_key, []).append(line[4:].strip().strip('"'))
                elif ":" in line and not line.startswith(" "):
                    k, _, v = line.partition(":")
                    current_key = k.strip()
                    val = v.strip().strip('"')
                    if val:
                        fm2[current_key] = val
                        current_key = None  # scalar; reset
            fm = fm2

    # Remove the h1 title line (it's in the front matter already)
    body = re.sub(r"^#\s+.+\n", "", body, count=1).strip()

    body = preprocess_urls(body)
    body_html = markdown.markdown(
        body,
        extensions=["extra", "sane_lists"],
    )
    return {"fm": fm, "body_html": body_html, "path": path}


def load_all() -> tuple[list, list]:
    posts, pages = [], []
    for p in sorted((MD_DIR / "posts").glob("*.md")):
        item = parse_md_file(p)
        item["slug"] = p.stem
        item["url"]  = f"posts/{p.stem}.html"
        posts.append(item)
    for p in sorted((MD_DIR / "pages").glob("*.md")):
        item = parse_md_file(p)
        item["slug"] = p.stem
        item["url"]  = f"pages/{p.stem}.html"
        pages.append(item)
    # Sort posts newest-first
    posts.sort(key=lambda x: x["fm"].get("date", ""), reverse=True)
    return posts, pages


def extract_excerpt(body_html: str, max_chars: int = 220) -> str:
    """Return first paragraph as plain text, truncated to max_chars."""
    m = re.search(r'<p>(.*?)</p>', body_html, re.DOTALL)
    text = re.sub(r'<[^>]+>', '', m.group(1)) if m else ''
    text = text.strip()
    if len(text) > max_chars:
        text = text[:max_chars].rsplit(' ', 1)[0] + '\u2026'
    return text


def format_date_long(date_str: str) -> str:
    """Convert '2019-07-27' to 'July 27, 2019'."""
    try:
        from datetime import datetime
        return datetime.strptime(date_str, "%Y-%m-%d").strftime("%B %-d, %Y")
    except Exception:
        return date_str


def slugify(text: str) -> str:
    """Convert 'Web Development' to 'web-development'."""
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_]+', '-', text)
    return text.strip('-')


# ---------------------------------------------------------------------------
# HTML templates
# ---------------------------------------------------------------------------

CSS = """
* { box-sizing: border-box; margin: 0; padding: 0; }

html { font-size: 16px; }

body {
  font-family: Merriweather, Georgia, serif;
  font-size: 16px;
  line-height: 1.75;
  color: #1a1a1a;
  background: #1a1a1a;
}

a { color: #1a1a1a; text-decoration: none; }
a:hover, a:focus { color: #007acc; text-decoration: underline; }

/* ── Site wrapper (white card over dark body) ── */
.site-wrap {
  background: #fff;
  max-width: 1260px;
  margin: 0 auto;
}

/* ── Header ── */
.site-header {
  background: #fff;
  padding: 2.625em 7.6923%;
  border-bottom: 1px solid #d1d1d1;
}

.site-header-main {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 1rem;
}

.site-title {
  font-family: Montserrat, "Helvetica Neue", Arial, sans-serif;
  font-size: 1.75rem;
  font-weight: 700;
  line-height: 1.25;
  margin: 0;
}
.site-title a { color: #1a1a1a; text-decoration: none; }
.site-title a:hover { color: #007acc; text-decoration: none; }

.site-tagline {
  font-size: 0.8125rem;
  color: #686868;
  margin-top: 0.3em;
  font-family: Merriweather, Georgia, serif;
}

.site-nav {
  font-family: Montserrat, "Helvetica Neue", Arial, sans-serif;
  font-size: 0.875rem;
}
.site-nav a {
  color: #1a1a1a;
  margin-left: 1.5rem;
  text-decoration: none;
}
.site-nav a:first-child { margin-left: 0; }
.site-nav a:hover { color: #007acc; text-decoration: none; }

/* ── Two-column content layout ── */
.site-content-wrap {
  padding: 3.5em 7.6923%;
  overflow: hidden; /* clearfix for floats */
}

.content-area {
  width: 100%;
}

.sidebar {
  margin-top: 3.5em;
}

@media (min-width: 985px) {
  .content-area {
    float: left;
    width: 68%;
  }
  .sidebar {
    float: left;
    width: 24%;
    margin-left: 8%;
    margin-top: 0;
  }
}

/* ── Sidebar widgets ── */
.widget {
  border-top: 4px solid #1a1a1a;
  padding-top: 1.75em;
  margin-bottom: 3.5em;
  font-size: 0.8125rem;
  line-height: 1.615;
}

.widget-title {
  font-family: Montserrat, "Helvetica Neue", Arial, sans-serif;
  font-size: 0.875rem;
  font-weight: 700;
  letter-spacing: 0.046875em;
  text-transform: uppercase;
  margin-bottom: 1.3em;
  color: #1a1a1a;
}

.widget ul {
  list-style: disc;
  padding-left: 1.2em;
}
.widget li { padding: 0.15em 0; }
.widget a { color: #1a1a1a; }
.widget a:hover { color: #007acc; }

/* ── Blog feed (home page) ── */
.post-feed { }

.post-card {
  padding: 2.5em 0;
  border-bottom: 1px solid #d1d1d1;
}
.post-card:first-child { padding-top: 0; }

.post-card h2 {
  font-family: Montserrat, "Helvetica Neue", Arial, sans-serif;
  font-size: 1.75rem;
  font-weight: 700;
  line-height: 1.25;
  margin-bottom: 0.4rem;
}
.post-card h2 a { color: #1a1a1a; text-decoration: none; }
.post-card h2 a:hover { color: #007acc; }

.post-card-meta {
  font-size: 0.8125rem;
  color: #686868;
  font-family: Montserrat, "Helvetica Neue", Arial, sans-serif;
  margin-bottom: 0.85rem;
}
.post-card-meta .cat { color: #686868; }

.post-excerpt { color: #686868; margin-bottom: 0.85rem; }

.read-more {
  font-size: 0.8125rem;
  font-family: Montserrat, "Helvetica Neue", Arial, sans-serif;
  color: #1a1a1a;
}
.read-more:hover { color: #007acc; }

.feed-footer {
  margin-top: 3em;
  padding-top: 1.5em;
  border-top: 1px solid #d1d1d1;
  font-family: Montserrat, "Helvetica Neue", Arial, sans-serif;
  font-size: 0.875rem;
}

/* ── Archive index ── */
.year-group { margin-bottom: 2.5em; }

.year-label {
  font-family: Montserrat, "Helvetica Neue", Arial, sans-serif;
  font-size: 0.875rem;
  font-weight: 700;
  color: #686868;
  border-bottom: 1px solid #d1d1d1;
  padding-bottom: 0.4rem;
  margin-bottom: 0.9rem;
}

.post-list { list-style: none; }
.post-list li {
  display: flex;
  align-items: baseline;
  gap: 0.8rem;
  padding: 0.3rem 0;
  border-bottom: 1px solid #f0f0f0;
}

.post-date {
  font-size: 0.8125rem;
  color: #686868;
  white-space: nowrap;
  font-family: Inconsolata, monospace;
  min-width: 5.5rem;
}

.post-title { font-size: 1rem; }
.categories {
  font-size: 0.75rem;
  color: #686868;
  font-family: Montserrat, sans-serif;
}

.pages-section { margin-top: 3em; }
.pages-section h2 {
  font-family: Montserrat, "Helvetica Neue", Arial, sans-serif;
  font-size: 0.875rem;
  font-weight: 700;
  color: #686868;
  border-bottom: 1px solid #d1d1d1;
  padding-bottom: 0.4rem;
  margin-bottom: 0.9rem;
}
.page-list { list-style: none; }
.page-list li { padding: 0.2rem 0; }

/* ── Article ── */
.back-link {
  font-size: 0.8125rem;
  font-family: Montserrat, sans-serif;
  margin-bottom: 2rem;
  display: block;
  color: #686868;
}
.back-link:hover { color: #007acc; }

article { }

article h1 {
  font-family: Montserrat, "Helvetica Neue", Arial, sans-serif;
  font-size: 2.25rem;
  font-weight: 700;
  line-height: 1.2;
  margin-bottom: 0.5rem;
  color: #1a1a1a;
}

.post-meta {
  font-size: 0.8125rem;
  color: #686868;
  font-family: Montserrat, sans-serif;
  margin-bottom: 2rem;
}
.post-meta span { margin-right: 1rem; }

article h2 {
  font-family: Montserrat, "Helvetica Neue", Arial, sans-serif;
  font-size: 1.4rem;
  font-weight: 700;
  margin: 1.75rem 0 0.5rem;
}
article h3 {
  font-family: Montserrat, "Helvetica Neue", Arial, sans-serif;
  font-size: 1.1rem;
  font-weight: 700;
  margin: 1.5rem 0 0.4rem;
}
article p  { margin-bottom: 1.1rem; }
article ul, article ol { margin: 0.5rem 0 1.1rem 1.8rem; }
article li { margin-bottom: 0.3rem; }

article pre {
  background: #f7f7f7;
  border: 1px solid #d1d1d1;
  border-left: 4px solid #1a1a1a;
  padding: 1rem 1.2rem;
  overflow-x: auto;
  font-family: Inconsolata, monospace;
  font-size: 0.875rem;
  margin-bottom: 1.1rem;
  border-radius: 0;
}
article code {
  background: #f7f7f7;
  padding: 0.1em 0.3em;
  font-family: Inconsolata, monospace;
  font-size: 0.875em;
}
article pre code { background: none; padding: 0; }

article blockquote {
  border-left: 4px solid #d1d1d1;
  margin: 1.1rem 0;
  padding: 0.4rem 1.2rem;
  color: #686868;
  font-style: italic;
}

article img { max-width: 100%; height: auto; margin: 0.5rem 0; }
article hr { border: none; border-top: 1px solid #d1d1d1; margin: 2rem 0; }
article table { border-collapse: collapse; margin-bottom: 1.1rem; width: 100%; }
article th, article td { border: 1px solid #d1d1d1; padding: 0.5rem 0.75rem; }
article th {
  background: #f7f7f7;
  font-family: Montserrat, sans-serif;
  font-size: 0.875rem;
  font-weight: 700;
}

/* ── Comments ── */
.comments {
  margin-top: 3.5rem;
  border-top: 4px solid #1a1a1a;
  padding-top: 1.75rem;
}
.comments h2 {
  font-family: Montserrat, sans-serif;
  font-size: 0.875rem;
  font-weight: 700;
  letter-spacing: 0.046875em;
  text-transform: uppercase;
  margin-bottom: 1.5rem;
}
.comment { margin-bottom: 1.75rem; padding-bottom: 1.75rem; border-bottom: 1px solid #d1d1d1; }
.comment-meta { font-size: 0.8125rem; color: #686868; margin-bottom: 0.4rem; font-family: Montserrat, sans-serif; }

/* ── Footer ── */
footer {
  text-align: center;
  font-size: 0.8125rem;
  color: #686868;
  font-family: Montserrat, sans-serif;
  padding: 2.625em 7.6923%;
  border-top: 1px solid #d1d1d1;
  clear: both;
}
"""


def build_sidebar(posts: list, pages: list, site_root: str = "") -> str:
    cats = sorted({c for p in posts for c in p["fm"].get("categories", [])
                   if c.lower() != "uncategorized"})
    public_pages = [p for p in pages if not p["fm"].get("private")]
    pages_html = "".join(
        f'<li><a href="{site_root}{p["url"]}">{p["fm"].get("title", p["slug"])}</a></li>'
        for p in public_pages
    )
    cats_html = "".join(
        f'<li><a href="{site_root}categories/{slugify(c)}.html">{c}</a></li>'
        for c in cats
    )
    return f"""<aside class="sidebar">
  <div class="widget">
    <h3 class="widget-title">Pages</h3>
    <ul>{pages_html}</ul>
  </div>
  <div class="widget">
    <h3 class="widget-title">Categories</h3>
    <ul>{cats_html}</ul>
  </div>
</aside>"""


def html_shell(title: str, body: str, active: str = "", sidebar: str = "") -> str:
    if active == "home":
        site_root = ""
        nav = '<a href="archive.html">Archive</a>'
    elif active == "archive":
        site_root = ""
        nav = '<a href="index.html">Home</a>'
    else:
        site_root = "../"
        nav = '<a href="../index.html">Home</a> <a href="../archive.html">Archive</a>'
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} | parizek.com</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inconsolata:wght@400&family=Merriweather:ital,wght@0,400;0,700;0,900;1,400;1,700&family=Montserrat:wght@400;700&display=swap" rel="stylesheet">
<style>{CSS}</style>
</head>
<body>
<div class="site-wrap">
  <header class="site-header">
    <div class="site-header-main">
      <div class="site-branding">
        <h1 class="site-title"><a href="{site_root}index.html">parizek.com</a></h1>
        <p class="site-tagline">a blog</p>
      </div>
      <nav class="site-nav">{nav}</nav>
    </div>
  </header>
  <div class="site-content-wrap">
    <div class="content-area">
{body}
    </div>
{sidebar}
  </div>
  <footer>parizek.com</footer>
</div>
</body>
</html>"""


def build_feed(posts: list, pages: list, limit: int = 10) -> str:
    rows = ['<div class="post-feed">']
    for p in posts[:limit]:
        title   = p["fm"].get("title", p["slug"])
        date    = p["fm"].get("date", "")
        cats    = p["fm"].get("categories", [])
        excerpt = extract_excerpt(p["body_html"])
        date_display = format_date_long(date)
        cats_filtered = [c for c in cats if c.lower() != "uncategorized"]
        cat_links = ", ".join(f'<a href="categories/{slugify(c)}.html">{c}</a>' for c in cats_filtered)
        cat_str = f' &middot; <span class="cat">{cat_links}</span>' if cats_filtered else ""
        excerpt_html = f'<p class="post-excerpt">{excerpt}</p>' if excerpt else ""
        rows.append(
            f'<div class="post-card">'
            f'<h2><a href="{p["url"]}">{title}</a></h2>'
            f'<div class="post-card-meta">{date_display}{cat_str}</div>'
            f'{excerpt_html}'
            f'<a class="read-more" href="{p["url"]}">Read more &rarr;</a>'
            f'</div>'
        )
    rows.append('</div>')
    rows.append('<div class="feed-footer">')
    rows.append('<a href="archive.html">All posts &rarr;</a>')
    rows.append('</div>')

    body = "\n".join(rows)
    sidebar = build_sidebar(posts, pages)
    return html_shell("parizek.com", body, active="home", sidebar=sidebar)


def build_archive(posts: list, pages: list) -> str:
    by_year = defaultdict(list)
    for p in posts:
        year = p["fm"].get("date", "0000")[:4]
        by_year[year].append(p)

    rows = []
    for year in sorted(by_year.keys(), reverse=True):
        rows.append(f'<div class="year-group">')
        rows.append(f'<div class="year-label">{year}</div>')
        rows.append('<ul class="post-list">')
        for p in by_year[year]:
            title = p["fm"].get("title", p["slug"])
            date  = p["fm"].get("date", "")
            cats  = p["fm"].get("categories", [])
            cats_filtered = [c for c in cats if c.lower() != "uncategorized"]
            cat_links = ", ".join(f'<a href="categories/{slugify(c)}.html">{c}</a>' for c in cats_filtered)
            cat_str = f' <span class="categories">({cat_links})</span>' if cats_filtered else ""
            date_display = date[5:] if len(date) >= 7 else date  # MM-DD
            rows.append(
                f'<li>'
                f'<span class="post-date">{date_display}</span>'
                f'<span class="post-title"><a href="{p["url"]}">{title}</a>{cat_str}</span>'
                f'</li>'
            )
        rows.append("</ul></div>")

    rows.append('<div class="pages-section">')
    rows.append('<h2>Pages</h2>')
    rows.append('<ul class="page-list">')
    for p in pages:
        if p["fm"].get("private"):
            continue
        title = p["fm"].get("title", p["slug"])
        rows.append(f'<li><a href="{p["url"]}">{title}</a></li>')
    rows.append("</ul></div>")

    body = "\n".join(rows)
    sidebar = build_sidebar(posts, pages)
    return html_shell("All Posts — parizek.com", body, active="archive", sidebar=sidebar)


def build_article(item: dict, kind: str, posts: list, pages: list) -> str:
    fm    = item["fm"]
    title = fm.get("title", item["slug"])
    date  = fm.get("date", "")
    author = fm.get("author", "")
    cats  = fm.get("categories", [])
    tags  = fm.get("tags", [])

    meta_parts = []
    if date:   meta_parts.append(f'<span>{format_date_long(date)}</span>')
    if author: meta_parts.append(f'<span>by {author}</span>')
    if cats:
        cat_links = ", ".join(f'<a href="../categories/{slugify(c)}.html">{c}</a>' for c in cats)
        meta_parts.append(f'<span>{cat_links}</span>')
    if tags:   meta_parts.append(f'<span>#{" #".join(tags)}</span>')
    meta_html = f'<div class="post-meta">{"".join(meta_parts)}</div>' if meta_parts else ""

    # Split out comments block if present
    body_html  = item["body_html"]
    comments_html = ""
    if "<h2>Comments</h2>" in body_html:
        parts = body_html.split("<h2>Comments</h2>", 1)
        body_html = parts[0]
        comments_html = f'<div class="comments"><h2>Comments</h2>{parts[1]}</div>'

    body = f"""<a class="back-link" href="../index.html">&larr; All posts</a>
<article>
  <h1>{title}</h1>
  {meta_html}
  {body_html}
  {comments_html}
</article>"""
    sidebar = build_sidebar(posts, pages, site_root="../")
    return html_shell(title, body, active=kind, sidebar=sidebar)


def build_category_page(category: str, cat_posts: list, all_posts: list, pages: list) -> str:
    rows = [f'<h1 style="font-family:Montserrat,sans-serif;font-size:1.75rem;font-weight:700;margin-bottom:1.5rem;">{category}</h1>']
    by_year = defaultdict(list)
    for p in cat_posts:
        year = p["fm"].get("date", "0000")[:4]
        by_year[year].append(p)

    for year in sorted(by_year.keys(), reverse=True):
        rows.append(f'<div class="year-group">')
        rows.append(f'<div class="year-label">{year}</div>')
        rows.append('<ul class="post-list">')
        for p in by_year[year]:
            title = p["fm"].get("title", p["slug"])
            date  = p["fm"].get("date", "")
            date_display = date[5:] if len(date) >= 7 else date
            rows.append(
                f'<li>'
                f'<span class="post-date">{date_display}</span>'
                f'<span class="post-title"><a href="../{p["url"]}">{title}</a></span>'
                f'</li>'
            )
        rows.append("</ul></div>")

    body = "\n".join(rows)
    sidebar = build_sidebar(all_posts, pages, site_root="../")
    return html_shell(category, body, active="category", sidebar=sidebar)


def main():
    print("Loading Markdown files...")
    posts, pages = load_all()
    print(f"  {len(posts)} posts, {len(pages)} pages")

    SITE.mkdir(exist_ok=True)
    (SITE / "posts").mkdir(exist_ok=True)
    (SITE / "pages").mkdir(exist_ok=True)
    (SITE / "categories").mkdir(exist_ok=True)

    # Home feed
    (SITE / "index.html").write_text(build_feed(posts, pages), encoding="utf-8")
    print("  site/index.html")

    # Full archive
    (SITE / "archive.html").write_text(build_archive(posts, pages), encoding="utf-8")
    print("  site/archive.html")

    # Posts
    for item in posts:
        html = build_article(item, "post", posts, pages)
        out  = SITE / "posts" / f"{item['slug']}.html"
        out.write_text(html, encoding="utf-8")
        print(f"  site/posts/{item['slug']}.html")

    # Pages
    for item in pages:
        html = build_article(item, "page", posts, pages)
        out  = SITE / "pages" / f"{item['slug']}.html"
        out.write_text(html, encoding="utf-8")
        print(f"  site/pages/{item['slug']}.html")

    # Category index pages
    cat_map = defaultdict(list)
    for p in posts:
        for c in p["fm"].get("categories", []):
            if c.lower() != "uncategorized":
                cat_map[c].append(p)
    for cat, cat_posts in sorted(cat_map.items()):
        slug = slugify(cat)
        html = build_category_page(cat, cat_posts, posts, pages)
        out  = SITE / "categories" / f"{slug}.html"
        out.write_text(html, encoding="utf-8")
        print(f"  site/categories/{slug}.html")

    print(f"\nDone. Open site/index.html in a browser.")


if __name__ == "__main__":
    main()
