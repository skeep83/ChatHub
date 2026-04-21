from __future__ import annotations

from pathlib import Path

REPLACEMENTS = {
    'housecall-pro-vs-jobber.md': {
        '## Comparison table\nThe practical comparison comes down to simplicity versus workflow depth. Jobber is usually easier to roll out and feels cleaner for smaller teams. Housecall Pro becomes more compelling when you need stronger communication loops, payments, and tighter job coordination.\n': '## Comparison table\nThe practical comparison comes down to operational shape. Jobber usually wins when the team wants simpler adoption and a cleaner path to quoting, scheduling, and invoicing. Housecall Pro becomes more appealing when communication, payments, dispatch coordination, and customer-facing workflow matter more across the full job cycle.\n',
        '## How to choose\nChoose based on company size, dispatch complexity, budget tolerance, and whether you need a field-service-first tool or a broader CRM.\n': '## How to choose\nIf your team values simplicity and wants faster adoption, Jobber is often the safer choice. If your operation already feels more coordination-heavy and customer communication is central to the workflow, Housecall Pro may justify the extra complexity. The right choice depends less on generic features and more on how your business actually runs jobs.\n',
    },
    'best-crm-for-small-service-business.md': {
        '## Quick verdict\nThis page should help a buyer narrow the shortlist fast, not just learn vocabulary.\n': '## Quick verdict\nIf you run a small service business, the smartest path is usually to shortlist one field-service-first platform and one broader CRM, then eliminate whichever one clearly mismatches your workflow. The mistake is choosing based on feature noise instead of the real operational bottleneck.\n',
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
    print(f'Manually upgraded {updated} priority pages in round 2')


if __name__ == '__main__':
    main()
