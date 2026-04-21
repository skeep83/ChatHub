from __future__ import annotations

import json
from pathlib import Path

NEW_TOPICS = [
    {"keyword": "best crm for roofing companies", "page_type": "use_case", "audience": "roofing company owners", "intent": "commercial"},
    {"keyword": "best crm for cleaning business", "page_type": "use_case", "audience": "cleaning business owners", "intent": "commercial"},
    {"keyword": "housecall pro pricing vs jobber pricing", "page_type": "comparison", "audience": "buyers comparing cost and fit", "intent": "commercial"},
    {"keyword": "service titan alternatives for small businesses", "page_type": "alternatives", "audience": "smaller teams seeking lighter options", "intent": "commercial"},
    {"keyword": "best dispatch software for small service business", "page_type": "best_of", "audience": "operators comparing dispatch tools", "intent": "commercial"}
]


def main() -> None:
    base = Path(__file__).resolve().parents[1]
    seed_path = base / "data" / "topic_seed_crm_small_service_businesses.json"
    current = json.loads(seed_path.read_text())
    existing = {item['keyword'] for item in current}
    for item in NEW_TOPICS:
        if item['keyword'] not in existing:
            current.append(item)
    seed_path.write_text(json.dumps(current, ensure_ascii=False, indent=2))
    print(f"Expanded topic seed to {len(current)} entries")


if __name__ == "__main__":
    main()
