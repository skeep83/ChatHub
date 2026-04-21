from __future__ import annotations

import json
from pathlib import Path
from site_settings import SITE_URL


def main() -> None:
    base = Path(__file__).resolve().parents[1]
    planned = json.loads((base / "output" / "planned_pages.json").read_text())
    metadata = []
    for page in planned:
        metadata.append(
            {
                "slug": page["slug"],
                "title": page["title"],
                "meta_title": page["title"],
                "meta_description": page["problem_statement"][:155],
                "canonical_url": f"{SITE_URL}/{page['slug']}",
                "robots": "index,follow",
            }
        )
    out = base / "output" / "metadata.json"
    out.write_text(json.dumps(metadata, ensure_ascii=False, indent=2))
    print(f"Built {out}")


if __name__ == "__main__":
    main()
