from __future__ import annotations

import json
from pathlib import Path


def main() -> None:
    base = Path(__file__).resolve().parents[1]
    planned = json.loads((base / "output" / "planned_pages.json").read_text())
    mapping = []
    for page in planned:
        strategy = "affiliate" if page["search_intent"] == "commercial" else "email_capture"
        mapping.append(
            {
                "slug": page["slug"],
                "primary_strategy": strategy,
                "secondary_strategy": "lead_form" if page["search_intent"] == "commercial" else "none",
                "cta": page["call_to_action"],
            }
        )
    out = base / "output" / "monetization_map.json"
    out.write_text(json.dumps(mapping, ensure_ascii=False, indent=2))
    print(f"Built {out}")


if __name__ == "__main__":
    main()
