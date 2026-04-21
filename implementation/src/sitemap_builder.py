from __future__ import annotations

import json
from pathlib import Path
from site_settings import SITE_URL


def main() -> None:
    base = Path(__file__).resolve().parents[1]
    planned = json.loads((base / "output" / "planned_pages.json").read_text())
    lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    lines.append(f"  <url><loc>{SITE_URL}/</loc></url>")
    for page in planned:
        lines.append(f"  <url><loc>{SITE_URL}/{page['slug']}</loc></url>")
    lines.append('</urlset>')
    out = base / "output" / "site" / "sitemap.xml"
    out.write_text("\n".join(lines) + "\n")
    print(f"Built {out}")


if __name__ == "__main__":
    main()
