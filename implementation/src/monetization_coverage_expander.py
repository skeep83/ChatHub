from __future__ import annotations

import json
from pathlib import Path

NEW_LINKS = [
    {"product": "Zoho CRM", "placeholder_url": "https://www.zoho.com/crm/", "cta": "Explore Zoho CRM"},
    {"product": "monday.com", "placeholder_url": "https://monday.com/crm", "cta": "Explore monday CRM"},
    {"product": "Pipedrive", "placeholder_url": "https://www.pipedrive.com/", "cta": "Explore Pipedrive"}
]


def main() -> None:
    path = Path(__file__).resolve().parents[1] / 'data' / 'affiliate_placeholders.json'
    items = json.loads(path.read_text())
    existing = {item['product'] for item in items}
    for item in NEW_LINKS:
        if item['product'] not in existing:
            items.append(item)
    path.write_text(json.dumps(items, ensure_ascii=False, indent=2))
    print(f'Expanded monetization coverage to {len(items)} product links')


if __name__ == '__main__':
    main()
