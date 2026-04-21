from __future__ import annotations

import json
from pathlib import Path

NEW_TOPICS = [
    {"keyword": "best crm for hvac companies", "page_type": "use_case", "audience": "hvac business owners", "intent": "commercial"},
    {"keyword": "best crm for pest control business", "page_type": "use_case", "audience": "pest control business owners", "intent": "commercial"},
    {"keyword": "jobber pricing review", "page_type": "pricing", "audience": "buyers evaluating Jobber cost and value", "intent": "commercial"},
    {"keyword": "housecall pro review for small business", "page_type": "review", "audience": "small service teams evaluating Housecall Pro", "intent": "commercial"},
    {"keyword": "best crm for appliance repair business", "page_type": "use_case", "audience": "appliance repair business owners", "intent": "commercial"},
    {"keyword": "hubspot for home service business", "page_type": "use_case", "audience": "service businesses considering HubSpot", "intent": "commercial"}
]


def main() -> None:
    base = Path(__file__).resolve().parents[1]
    seed_path = base / 'data' / 'topic_seed_crm_small_service_businesses.json'
    current = json.loads(seed_path.read_text())
    existing = {item['keyword'] for item in current}
    for item in NEW_TOPICS:
        if item['keyword'] not in existing:
            current.append(item)
    seed_path.write_text(json.dumps(current, ensure_ascii=False, indent=2))
    print(f'Expanded topic seed to {len(current)} entries')


if __name__ == '__main__':
    main()
