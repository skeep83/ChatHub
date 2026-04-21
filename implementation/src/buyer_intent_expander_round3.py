from __future__ import annotations

import json
from pathlib import Path

NEW_TOPICS = [
    {"keyword": "jobber vs service titan", "page_type": "comparison", "audience": "buyers comparing simple vs complex service software", "intent": "commercial"},
    {"keyword": "housecall pro alternatives", "page_type": "alternatives", "audience": "buyers considering alternatives to Housecall Pro", "intent": "commercial"},
    {"keyword": "best crm for garage door business", "page_type": "use_case", "audience": "garage door business owners", "intent": "commercial"},
    {"keyword": "best crm for landscaping business", "page_type": "use_case", "audience": "landscaping business owners", "intent": "commercial"},
    {"keyword": "hubspot vs jobber", "page_type": "comparison", "audience": "buyers comparing broad CRM vs field-service-first tool", "intent": "commercial"},
    {"keyword": "best crm for pressure washing business", "page_type": "use_case", "audience": "pressure washing business owners", "intent": "commercial"},
    {"keyword": "is housecall pro worth it", "page_type": "review", "audience": "buyers evaluating Housecall Pro value", "intent": "commercial"},
    {"keyword": "is jobber worth it", "page_type": "review", "audience": "buyers evaluating Jobber value", "intent": "commercial"}
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
