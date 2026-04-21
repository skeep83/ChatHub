from __future__ import annotations

import html
import re
from pathlib import Path
import json

from analytics_settings import GA4_MEASUREMENT_ID
from site_settings import SITE_NAME, SITE_TAGLINE, SITE_URL

FLEXOFFERS_VERIFY = '9e1d32fb-49d8-48e6-a930-ba97187d23da'
SKIMLINKS_SNIPPET = '<script type="text/javascript" src="https://s.skimresources.com/js/301862X1789840.skimlinks.js"></script>'


def meta_description(text: str, fallback: str) -> str:
    source = re.sub(r"\s+", " ", (text or fallback or "")).strip()
    if len(source) <= 155:
        return source
    shortened = source[:152].rsplit(" ", 1)[0].rstrip(" ,.;:-")
    return shortened + "..."


def parse_markdown_sections(text: str) -> tuple[str, list[tuple[str, list[str]]]]:
    lines = text.splitlines()
    title = "Untitled"
    sections: list[tuple[str, list[str]]] = []
    current_heading = None
    current_body: list[str] = []
    in_frontmatter = False
    for line in lines:
        if line.strip() == "---":
            in_frontmatter = not in_frontmatter
            continue
        if in_frontmatter:
            continue
        if line.startswith("# "):
            title = line[2:].strip()
        elif line.startswith("## "):
            if current_heading is not None:
                sections.append((current_heading, current_body[:]))
            current_heading = line[3:].strip()
            current_body = []
        elif current_heading is not None:
            current_body.append(line)
    if current_heading is not None:
        sections.append((current_heading, current_body[:]))
    return title, sections


def slug_to_label(slug: str) -> str:
    return slug.replace("-", " ").title()


def ga4_snippet() -> str:
    if not GA4_MEASUREMENT_ID:
        return ""
    return f"""
  <script async src=\"https://www.googletagmanager.com/gtag/js?id={GA4_MEASUREMENT_ID}\"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', '{GA4_MEASUREMENT_ID}');
  </script>"""


def normalize_internal_href(href: str) -> str:
    if href == "index.html":
        return "/"
    if href.endswith(".html"):
        return "/" + href[:-5]
    return href


def render_inline(text: str) -> str:
    escaped = html.escape(text)
    escaped = re.sub(r"\[(.*?)\]\((https?://[^\)]+)\)", r'<a href="\2" target="_blank" rel="nofollow noopener">\1</a>', escaped)
    escaped = re.sub(r"\[(.*?)\]\(([^\)]+\.html)\)", lambda m: f'<a href="{normalize_internal_href(m.group(2))}">{m.group(1)}</a>', escaped)
    return escaped


def render_line(line: str) -> str:
    if not line.strip():
        return ""
    if line.startswith("### "):
        return f"<h3>{html.escape(line[4:].strip())}</h3>"
    if line.startswith("- "):
        return f"<li>{render_inline(line[2:].strip())}</li>"
    return f"<p>{render_inline(line)}</p>"


def classify_section(heading: str) -> str:
    name = heading.lower()
    if heading == "Offers":
        return "offer"
    if "recommended products" in name or "top picks" in name:
        return "products"
    if "product scorecards" in name:
        return "scorecards"
    if "comparison" in name:
        return "comparison"
    if "final recommendation" in name or "call to action" in name:
        return "highlight"
    return "default"


def render_product_cards(lines: list[str]) -> str:
    cards: list[str] = []
    current_title: str | None = None
    current_lines: list[str] = []
    for line in lines + ["### __END__"]:
        if line.startswith("### "):
            if current_title is not None:
                body = "".join(render_line(x) for x in current_lines if x.strip())
                cards.append(f"<article class='product-card'><h3>{html.escape(current_title)}</h3><div class='product-body'>{body}</div></article>")
            current_title = line[4:].strip()
            current_lines = []
        else:
            current_lines.append(line)
    return "<div class='product-grid'>" + "".join(cards) + "</div>"


def render_section(heading: str, lines: list[str]) -> str:
    section_type = classify_section(heading)
    classes = {
        "offer": "panel panel-accent",
        "products": "panel panel-soft",
        "scorecards": "panel panel-soft",
        "comparison": "panel panel-soft",
        "highlight": "panel panel-accent",
        "default": "panel",
    }
    if section_type in {"products", "scorecards"}:
        return f"<section class='{classes[section_type]}'><h2>{html.escape(heading)}</h2>{render_product_cards(lines)}</section>"

    body: list[str] = []
    list_buffer: list[str] = []
    for line in lines:
        rendered = render_line(line)
        if not rendered:
            if list_buffer:
                body.append("<ul class='soft-list'>" + "".join(list_buffer) + "</ul>")
                list_buffer = []
            continue
        if rendered.startswith("<li>"):
            list_buffer.append(rendered)
        else:
            if list_buffer:
                body.append("<ul class='soft-list'>" + "".join(list_buffer) + "</ul>")
                list_buffer = []
            body.append(rendered)
    if list_buffer:
        body.append("<ul class='soft-list'>" + "".join(list_buffer) + "</ul>")

    return f"<section class='{classes[section_type]}'><h2>{html.escape(heading)}</h2>{''.join(body)}</section>"


def render_page(title: str, sections: list[tuple[str, list[str]]]) -> str:
    summary = ""
    if sections and sections[0][1]:
        summary = next((line for line in sections[0][1] if line.strip()), "")
    hero = f"""
    <section class=\"hero-shell\">
      <div class=\"hero-copy\">
        <div class=\"eyebrow\">DirtyChatHub • 2026 comparison guide</div>
        <h1>{html.escape(title)}</h1>
        <p class=\"hero-summary\">{render_inline(summary)}</p>
        <div class=\"hero-actions\">
          <a class=\"button button-primary\" href=\"#offers\">View offers</a>
          <a class=\"button button-secondary\" href=\"/\">Explore guides</a>
        </div>
      </div>
      <aside class=\"hero-card\">
        <div class=\"metric\"><span>Focus</span><strong>Commercial intent</strong></div>
        <div class=\"metric\"><span>Site</span><strong>{html.escape(SITE_NAME)}</strong></div>
        <div class=\"metric\"><span>Audience</span><strong>Adult video chat buyers</strong></div>
      </aside>
    </section>
    """

    rendered_sections = []
    for heading, lines in sections:
        section_html = render_section(heading, lines)
        if heading == "Offers":
            section_html = section_html.replace("<section", "<section id='offers'", 1)
        rendered_sections.append(section_html)

    page_description = meta_description(summary, SITE_TAGLINE)
    return f"""<!doctype html>
<html lang=\"en\">
<head>
  <meta charset=\"utf-8\">
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
  <meta name=\"theme-color\" content=\"#e9eef7\">
  <meta name=\"description\" content=\"{html.escape(page_description)}\">
  <meta name=\"fo-verify\" content=\"{FLEXOFFERS_VERIFY}\">
  <title>{html.escape(title)} | {html.escape(SITE_NAME)}</title>
  <style>
    :root {{
      --bg: #e9eef7;
      --bg-2: #f4f7fb;
      --surface: rgba(255,255,255,0.58);
      --surface-strong: rgba(255,255,255,0.82);
      --text: #152033;
      --muted: #60708a;
      --accent: #5b7cff;
      --accent-2: #7f5cff;
      --shadow-soft: 14px 14px 30px rgba(163,177,198,0.34), -12px -12px 28px rgba(255,255,255,0.9);
      --shadow-inset: inset 6px 6px 12px rgba(163,177,198,0.22), inset -6px -6px 12px rgba(255,255,255,0.85);
      --border: rgba(255,255,255,0.55);
      --radius-xl: 28px;
      --radius-lg: 22px;
      --radius-md: 16px;
    }}
    * {{ box-sizing: border-box; }}
    html {{ scroll-behavior: smooth; }}
    body {{
      margin: 0;
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      color: var(--text);
      background:
        radial-gradient(circle at top left, rgba(115,145,255,0.22), transparent 28%),
        radial-gradient(circle at top right, rgba(127,92,255,0.18), transparent 24%),
        linear-gradient(180deg, var(--bg-2), var(--bg));
      min-height: 100vh;
      line-height: 1.65;
    }}
    a {{ color: var(--accent); text-decoration: none; }}
    a:hover {{ text-decoration: underline; }}
    .shell {{ max-width: 1120px; margin: 0 auto; padding: 28px 18px 60px; }}
    .topbar {{
      display: flex; justify-content: space-between; align-items: center; gap: 16px;
      padding: 14px 18px; margin-bottom: 26px; border-radius: var(--radius-lg);
      background: var(--surface); border: 1px solid var(--border); box-shadow: var(--shadow-soft); backdrop-filter: blur(14px) saturate(130%);
    }}
    .brand strong {{ display:block; font-size:1rem; }}
    .brand span, .topnav a {{ color: var(--muted); font-size: 0.95rem; }}
    .topnav {{ display:flex; gap:14px; flex-wrap: wrap; }}
    .hero-shell {{
      display:grid; grid-template-columns: 1.5fr .9fr; gap: 22px; margin-bottom: 26px;
    }}
    .hero-copy, .hero-card, .panel, .footer-card {{
      background: var(--surface); border: 1px solid var(--border); box-shadow: var(--shadow-soft); backdrop-filter: blur(14px) saturate(130%);
    }}
    .hero-copy {{ padding: 34px; border-radius: 34px; }}
    .hero-card {{ padding: 24px; border-radius: 28px; display:flex; flex-direction:column; gap:14px; justify-content:center; }}
    .eyebrow {{ color: var(--accent-2); font-weight: 700; letter-spacing: .04em; text-transform: uppercase; font-size: .78rem; }}
    h1 {{ font-size: clamp(2rem, 4vw, 3.5rem); line-height: 1.02; margin: 14px 0 18px; letter-spacing: -0.04em; }}
    h2 {{ margin: 0 0 16px; font-size: 1.35rem; letter-spacing: -0.02em; }}
    h3 {{ margin: 18px 0 8px; font-size: 1.02rem; }}
    .hero-summary {{ color: var(--muted); font-size: 1.05rem; max-width: 62ch; }}
    .hero-actions {{ display:flex; gap:12px; flex-wrap:wrap; margin-top: 24px; }}
    .button {{
      display:inline-flex; align-items:center; justify-content:center; padding: 12px 18px; border-radius: 999px; font-weight: 700;
      border: 1px solid rgba(255,255,255,0.7); box-shadow: var(--shadow-soft); text-decoration:none;
    }}
    .button-primary {{ background: linear-gradient(135deg, #6b8cff, #7f5cff); color: white; }}
    .button-secondary {{ background: rgba(255,255,255,0.7); color: var(--text); }}
    .metric {{ padding: 16px 18px; border-radius: 20px; background: var(--surface-strong); box-shadow: var(--shadow-inset); }}
    .metric span {{ display:block; font-size:.76rem; text-transform: uppercase; letter-spacing:.05em; color: var(--muted); margin-bottom: 6px; }}
    .metric strong {{ font-size:1rem; }}
    .content-grid {{ display:grid; grid-template-columns: minmax(0, 1fr) 300px; gap: 22px; }}
    .main-col {{ display:flex; flex-direction:column; gap: 18px; }}
    .sidebar {{ display:flex; flex-direction:column; gap: 18px; }}
    .panel {{ padding: 24px; border-radius: 24px; }}
    .panel-soft {{ background: rgba(255,255,255,0.67); }}
    .panel-accent {{ background: linear-gradient(145deg, rgba(107,140,255,0.16), rgba(255,255,255,0.7)); }}
    p {{ margin: 0 0 10px; color: #22314b; }}
    .soft-list {{ margin: 0; padding-left: 20px; color: #22314b; }}
    .soft-list li {{ margin-bottom: 8px; }}
    .footer-card {{ margin-top: 24px; padding: 18px 22px; border-radius: 22px; display:flex; justify-content:space-between; gap:16px; flex-wrap:wrap; color: var(--muted); }}
    .product-grid {{ display:grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap:16px; }}
    .product-card {{ padding: 18px; border-radius: 20px; background: rgba(255,255,255,0.74); box-shadow: var(--shadow-inset); }}
    .product-card h3 {{ margin-top:0; margin-bottom:12px; }}
    .product-body p {{ margin-bottom:8px; }}
    .site-index {{ display:grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 18px; margin-top: 22px; }}
    .index-card {{ padding: 18px; border-radius: 20px; background: var(--surface); border:1px solid var(--border); box-shadow: var(--shadow-soft); backdrop-filter: blur(14px) saturate(130%); }}
    @media (max-width: 920px) {{
      .hero-shell, .content-grid {{ grid-template-columns: 1fr; }}
      .shell {{ padding: 18px 14px 42px; }}
      .hero-copy {{ padding: 24px; }}
    }}
  </style>
  {ga4_snippet()}
</head>
<body>
{SKIMLINKS_SNIPPET}
  <div class="shell">
    <header class="topbar">
      <div class="brand">
        <strong>{html.escape(SITE_NAME)}</strong>
        <span>{html.escape(SITE_TAGLINE)}</span>
      </div>
      <nav class="topnav">
        <a href="/">Guides</a>
        <a href="{html.escape(SITE_URL)}">Live site</a>
      </nav>
    </header>
    {hero}
    <div class="content-grid">
      <main class="main-col">
        {''.join(rendered_sections)}
      </main>
      <aside class="sidebar">
        <section class="panel panel-soft">
          <h2>How to use this page</h2>
          <p>Start with the overview, scan the recommended platforms, then use the offer block only after the fit is clear.</p>
        </section>
        <section class="panel panel-accent">
          <h2>Design direction</h2>
          <p>Use the page to separate mainstream discovery platforms from premium private-chat options instead of clicking the first brand you recognize.</p>
        </section>
      </aside>
    </div>
    <footer class="footer-card">
      <div>Built for adult video chat comparison research.</div>
      <div><a href="/">Browse all guides</a></div>
    </footer>
  </div>
</body>
</html>"""


def render_index(pages: list[tuple[str, str]]) -> str:
    base = Path(__file__).resolve().parents[1]
    curated_path = base / 'output' / 'homepage_sections.json'
    curated = json.loads(curated_path.read_text()) if curated_path.exists() else {}
    title_map = {slug: title for slug, title in pages}

    def card(slug: str, label: str | None = None) -> str:
        shown = label or title_map.get(slug, slug_to_label(slug))
        return f"<a class='index-card' href='/{slug}'><strong>{html.escape(shown)}</strong><p>{html.escape(slug_to_label(slug))}</p></a>"

    featured = ''.join(card(item['slug'], item.get('label')) for item in curated.get('featured_money_pages', []))
    trust = ''.join(card(item['slug'], item.get('label')) for item in curated.get('trust_pages', []))
    clusters = []
    for cluster in curated.get('clusters', []):
        items = ''.join(f"<li><a href='/{slug}'>{html.escape(title_map.get(slug, slug_to_label(slug)))}</a></li>" for slug in cluster.get('items', []))
        clusters.append(f"<div class='cluster-card'><strong>{html.escape(cluster['name'])}</strong><ul>{items}</ul></div>")
    latest = ''.join(card(slug, title) for slug, title in pages[:12])
    homepage_description = meta_description(
        'Compare adult video chat sites, private cam platforms, alternatives, and premium live chat options with clearer buyer guides.',
        SITE_TAGLINE,
    )
    return f"""<!doctype html>
<html lang=\"en\">
<head>
  <meta charset=\"utf-8\">
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
  <meta name=\"description\" content=\"{html.escape(homepage_description)}\">
  <title>Best Adult Video Chat Sites and Private Cam Guides | {html.escape(SITE_NAME)}</title>
  <style>
    body {{ margin:0; font-family: Inter, ui-sans-serif, system-ui, sans-serif; background: linear-gradient(180deg, #f3f6fb, #e8edf6); color:#152033; }}
    .shell {{ max-width: 1120px; margin:0 auto; padding: 28px 18px 60px; }}
    .hero, .index-card, .cluster-card {{ background: rgba(255,255,255,0.65); border:1px solid rgba(255,255,255,.65); box-shadow: 14px 14px 30px rgba(163,177,198,.34), -12px -12px 28px rgba(255,255,255,.9); backdrop-filter: blur(14px) saturate(130%); }}
    .hero {{ border-radius: 30px; padding: 34px; margin-bottom:22px; }}
    h1 {{ font-size: clamp(2.2rem, 4vw, 4rem); margin: 0 0 12px; letter-spacing: -.04em; }}
    h2 {{ margin: 28px 0 14px; font-size: 1.4rem; }}
    p {{ color:#5d6d88; line-height:1.65; }}
    .grid {{ display:grid; grid-template-columns: repeat(auto-fit, minmax(240px,1fr)); gap:18px; margin-top:10px; }}
    .index-card, .cluster-card {{ display:block; padding:20px; border-radius:22px; color:inherit; text-decoration:none; }}
    .index-card strong, .cluster-card strong {{ display:block; margin-bottom: 8px; font-size: 1.05rem; }}
    .cluster-card ul {{ margin: 10px 0 0; padding-left: 18px; color:#5d6d88; }}
  </style>
  {ga4_snippet()}
</head>
<body>
{SKIMLINKS_SNIPPET}
  <div class="shell">
    <section class="hero">
      <div style="font-size:.8rem;text-transform:uppercase;letter-spacing:.05em;color:#7f5cff;font-weight:700;">DirtyChatHub</div>
      <h1>{html.escape(SITE_NAME)}</h1>
      <p>{html.escape(SITE_TAGLINE)}. Built to help users compare adult video chat sites faster, with clearer comparisons, alternatives, and private-chat buying guidance.</p>
    </section>
    <h2>Featured buying guides</h2>
    <section class="grid">{featured}</section>
    <h2>Trust and editorial pages</h2>
    <section class="grid">{trust}</section>
    <h2>Core topic clusters</h2>
    <section class="grid">{''.join(clusters)}</section>
    <h2>More guides</h2>
    <section class="grid">{latest}</section>
  </div>
</body>
</html>"""


def main() -> None:
    base = Path(__file__).resolve().parents[1]
    content_dir = base / "output" / "content"
    site_dir = base / "output" / "site"
    site_dir.mkdir(parents=True, exist_ok=True)
    pages = []
    for md_file in sorted(content_dir.glob("*.md")):
        text = md_file.read_text()
        title, sections = parse_markdown_sections(text)
        slug = md_file.stem
        html_page = render_page(title, sections)
        (site_dir / f"{slug}.html").write_text(html_page)
        pages.append((slug, title))
    (site_dir / "index.html").write_text(render_index(pages))
    print(f"Built HTML site in {site_dir}")


if __name__ == "__main__":
    main()
