from __future__ import annotations

import json
from pathlib import Path


def main() -> None:
    suggestions = [
        {"domain": "fieldcrmguide.com", "angle": "review-focused brand", "strength": "clear niche signal"},
        {"domain": "servicestackcrm.com", "angle": "software stack positioning", "strength": "commercial tone"},
        {"domain": "smallservicecrm.com", "angle": "exact niche match", "strength": "very clear intent"},
        {"domain": "betterservicecrm.com", "angle": "comparison/recommendation", "strength": "brandable and broad enough"},
        {"domain": "servicetoolcompare.com", "angle": "comparison engine", "strength": "supports expansion later"},
    ]
    out = Path(__file__).resolve().parents[1] / "output" / "domain_strategy.json"
    out.write_text(json.dumps(suggestions, ensure_ascii=False, indent=2))
    print(f"Built {out}")


if __name__ == "__main__":
    main()
