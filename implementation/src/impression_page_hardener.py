from __future__ import annotations

from pathlib import Path

REPLACEMENTS = {
    'best-crm-for-pest-control-business.md': {
        '## Overview\nThis page is designed to help small service businesses compare CRM options without wasting time on generic software lists.\n': '## Overview\nPest control businesses need more than a generic CRM. They need a system that can handle repeat service, customer history, scheduling, routing logic, estimates, invoicing, and follow-up without turning the back office into a manual mess. This page focuses on that practical reality.\n',
    },
    'service-titan-alternatives-for-small-businesses.md': {
        '## Best alternatives\nAlternatives should be grouped by best fit, budget sensitivity, and operational complexity.\n': '## Best alternatives\nIf ServiceTitan feels too heavy, the best alternatives usually win by reducing complexity while still covering the workflows that matter most: quoting, dispatch, customer records, invoicing, and repeat service coordination.\n',
    },
}


def main() -> None:
    content_dir = Path(__file__).resolve().parents[1] / 'output' / 'content'
    updated = 0
    for filename, replacements in REPLACEMENTS.items():
        path = content_dir / filename
        if not path.exists():
            continue
        text = path.read_text()
        before = text
        for old, new in replacements.items():
            text = text.replace(old, new)
        if text != before:
            path.write_text(text)
            updated += 1
    print(f'Hardened {updated} impression-winning pages')


if __name__ == '__main__':
    main()
