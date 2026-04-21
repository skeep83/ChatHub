from __future__ import annotations

import json
from pathlib import Path
from datetime import datetime, UTC


def main() -> None:
    base = Path(__file__).resolve().parents[1]
    planned = json.loads((base / "output" / "planned_pages.json").read_text())
    registry = []
    now = datetime.now(UTC).isoformat()
    for page in planned:
        registry.append(
            {
                "slug": page["slug"],
                "title": page["title"],
                "status": "draft",
                "review_required": page["review_required"],
                "last_generated_at": now,
                "publish_ready": False,
                "needs_refresh": False,
            }
        )
    out = base / "output" / "page_registry.json"
    out.write_text(json.dumps(registry, ensure_ascii=False, indent=2))
    print(f"Built {out}")


if __name__ == "__main__":
    main()
