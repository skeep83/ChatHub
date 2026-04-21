from __future__ import annotations

import json
from pathlib import Path
from datetime import datetime, UTC


def main() -> None:
    base = Path(__file__).resolve().parents[1]
    planned = json.loads((base / "output" / "planned_pages.json").read_text())
    now = datetime.now(UTC).isoformat()
    rows = []
    for page in planned:
        rows.append(
            {
                "slug": page["slug"],
                "page_type": page["page_type"],
                "sessions": 0,
                "organic_clicks": 0,
                "conversion_events": 0,
                "affiliate_clicks": 0,
                "last_checked_at": now,
            }
        )
    out = base / "output" / "analytics_registry.json"
    out.write_text(json.dumps(rows, ensure_ascii=False, indent=2))
    print(f"Built {out}")


if __name__ == "__main__":
    main()
