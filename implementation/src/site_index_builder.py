from __future__ import annotations

import json
from pathlib import Path


def main() -> None:
    base = Path(__file__).resolve().parents[1]
    pages = json.loads((base / "output" / "planned_pages.json").read_text())
    out = base / "output" / "site_index.md"
    lines = ["# Site Index", ""]
    for page in pages:
        lines.append(f"- [{page['title']}](content/{page['slug']}.md) — {page['page_type']}")
    out.write_text("\n".join(lines) + "\n")
    print(f"Built {out}")


if __name__ == "__main__":
    main()
