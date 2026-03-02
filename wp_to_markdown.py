#!/usr/bin/env python3
"""
WordPress WXR XML → Markdown converter for parizek.com blog backup.

Usage:
    python3 wp_to_markdown.py [--xml PATH] [--out DIR] [--comments-xml PATH]

Defaults:
    --xml      parizekcom.wordpress.com-2020-07-16-21_34_50/parizekcom.wordpress.2020-07-16.001.xml
    --out      output/
    --comments-xml  parizekcom.wordpress.2016-06-08.xml  (richer comment archive)
"""

import argparse
import os
import re
import sys
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

import html2text

# ---------------------------------------------------------------------------
# XML namespaces used in WXR files
# ---------------------------------------------------------------------------
NS = {
    "content": "http://purl.org/rss/1.0/modules/content/",
    "dc":      "http://purl.org/dc/elements/1.1/",
    "wp":      "http://wordpress.org/export/1.2/",
    "excerpt": "http://wordpress.org/export/1.2/excerpt/",
}


def tx(element, tag):
    """Return text of a child tag (with namespace), or ''."""
    child = element.find(tag, NS)
    if child is not None and child.text:
        return child.text.strip()
    return ""


def cdata(element, tag):
    """Return text of a CDATA child (html2text-friendly)."""
    child = element.find(tag, NS)
    if child is not None and child.text:
        return child.text
    return ""


def html_to_md(html: str) -> str:
    h = html2text.HTML2Text()
    h.ignore_links = False
    h.ignore_images = False
    h.body_width = 0          # don't hard-wrap lines
    h.protect_links = True
    h.unicode_snob = True
    h.images_to_alt = False
    return h.handle(html).strip()


def slugify(title: str) -> str:
    """Create a filesystem-safe slug from a title."""
    s = title.lower()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"[\s_]+", "-", s)
    s = re.sub(r"-+", "-", s).strip("-")
    return s[:80]  # cap length


def yaml_str(s: str) -> str:
    """Quote a string for YAML front matter if it contains special chars."""
    if any(c in s for c in ':#{}[]|>&*!,?'):
        return '"' + s.replace('"', '\\"') + '"'
    return s


def format_comments(comments: list) -> str:
    if not comments:
        return ""
    lines = ["\n---\n\n## Comments\n"]
    for c in sorted(comments, key=lambda x: x["date"]):
        lines.append(
            f"**{c['author']}** — {c['date']}\n\n{c['content']}\n"
        )
    return "\n".join(lines)


def parse_xml(path: str) -> list:
    """Parse a WXR file and return a list of item dicts."""
    tree = ET.parse(path)
    root = tree.getroot()
    channel = root.find("channel")
    items = []

    for item in channel.findall("item"):
        post_type = tx(item, "wp:post_type")
        if post_type not in ("post", "page"):
            continue

        status = tx(item, "wp:status")
        if status not in ("publish", "draft", "private"):
            continue

        title    = item.findtext("title") or ""
        link     = item.findtext("link") or ""
        pub_date = item.findtext("pubDate") or ""
        author   = tx(item, "dc:creator")
        content  = cdata(item, "content:encoded")
        excerpt  = cdata(item, "excerpt:encoded")
        post_id  = tx(item, "wp:post_id")
        slug     = tx(item, "wp:post_name") or slugify(title)

        # Date parsing
        try:
            dt = datetime.strptime(pub_date[:25], "%a, %d %b %Y %H:%M:%S")
            date_str = dt.strftime("%Y-%m-%d")
        except Exception:
            date_str = tx(item, "wp:post_date")[:10] or "0000-00-00"

        # Categories and tags
        categories = []
        tags = []
        for cat in item.findall("category"):
            domain = cat.get("domain", "")
            name = cat.text or ""
            if domain == "category":
                categories.append(name)
            elif domain == "post_tag":
                tags.append(name)

        # Comments
        comments = []
        for comment in item.findall("wp:comment", NS):
            c_status = tx(comment, "wp:comment_approved")
            if c_status != "1":
                continue
            c_author  = tx(comment, "wp:comment_author")
            c_date    = tx(comment, "wp:comment_date")
            c_content = tx(comment, "wp:comment_content")
            if c_content:
                comments.append({
                    "author":  c_author or "Anonymous",
                    "date":    c_date,
                    "content": c_content,
                })

        items.append({
            "id":         post_id,
            "type":       post_type,
            "status":     status,
            "title":      title,
            "slug":       slug,
            "date":       date_str,
            "author":     author,
            "link":       link,
            "categories": categories,
            "tags":       tags,
            "content":    content,
            "excerpt":    excerpt,
            "comments":   comments,
        })

    return items


def merge_comments(primary: list, secondary: list) -> list:
    """Add comments from secondary into primary items by slug match."""
    sec_by_slug = {i["slug"]: i for i in secondary}
    for item in primary:
        if not item["comments"] and item["slug"] in sec_by_slug:
            item["comments"] = sec_by_slug[item["slug"]]["comments"]
    return primary


def write_item(item: dict, out_dir: Path):
    subdir = out_dir / (item["type"] + "s")  # posts/ or pages/
    subdir.mkdir(parents=True, exist_ok=True)

    if item["type"] == "post":
        filename = f"{item['date']}-{item['slug']}.md"
    else:
        filename = f"{item['slug']}.md"

    md_content = html_to_md(item["content"]) if item["content"] else ""
    comments_block = format_comments(item["comments"])

    # YAML front matter
    fm_lines = ["---"]
    fm_lines.append(f"title: {yaml_str(item['title'])}")
    fm_lines.append(f"date: {item['date']}")
    if item["author"]:
        fm_lines.append(f"author: {item['author']}")
    if item["status"] != "publish":
        fm_lines.append(f"status: {item['status']}")
    if item["categories"]:
        fm_lines.append("categories:")
        for c in item["categories"]:
            fm_lines.append(f"  - {yaml_str(c)}")
    if item["tags"]:
        fm_lines.append("tags:")
        for t in item["tags"]:
            fm_lines.append(f"  - {yaml_str(t)}")
    if item["link"]:
        fm_lines.append(f"original_url: {item['link']}")
    fm_lines.append("---")
    front_matter = "\n".join(fm_lines)

    body = f"{front_matter}\n\n# {item['title']}\n\n{md_content}"
    if comments_block:
        body += comments_block

    filepath = subdir / filename
    filepath.write_text(body, encoding="utf-8")
    return filepath


def main():
    base = Path(__file__).parent
    default_xml = str(base / "parizekcom.wordpress.com-2020-07-16-21_34_50" / "parizekcom.wordpress.2020-07-16.001.xml")
    default_comments_xml = str(base / "parizekcom.wordpress.2016-06-08.xml")
    default_out = str(base / "output")

    parser = argparse.ArgumentParser(description="Convert WordPress WXR XML to Markdown files.")
    parser.add_argument("--xml",          default=default_xml,          help="Primary WXR export XML")
    parser.add_argument("--comments-xml", default=default_comments_xml, help="Secondary XML for comments (optional)")
    parser.add_argument("--out",          default=default_out,          help="Output directory")
    args = parser.parse_args()

    print(f"Parsing primary XML:  {args.xml}")
    primary = parse_xml(args.xml)
    print(f"  Found {len(primary)} items (posts + pages)")

    secondary = []
    if args.comments_xml and os.path.exists(args.comments_xml):
        print(f"Parsing comments XML: {args.comments_xml}")
        secondary = parse_xml(args.comments_xml)
        print(f"  Found {len(secondary)} items for comment merging")
        primary = merge_comments(primary, secondary)

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    posts_written = 0
    pages_written = 0
    for item in primary:
        path = write_item(item, out_dir)
        if item["type"] == "post":
            posts_written += 1
        else:
            pages_written += 1
        print(f"  {'POST' if item['type']=='post' else 'PAGE'}  {path.relative_to(base)}")

    print(f"\nDone. {posts_written} posts + {pages_written} pages written to {out_dir}/")


if __name__ == "__main__":
    main()
