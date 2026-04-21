from __future__ import annotations

from pathlib import Path

RELATED_DEFAULT = [
    ('housecall-pro-vs-jobber', 'Compare Jobber and Housecall Pro'),
    ('jobber-alternatives', 'See Jobber alternatives'),
    ('crm-for-plumbers', 'Understand CRM for plumbers'),
    ('crm-for-electricians', 'Understand CRM for electricians'),
]

CATEGORY_MAP = {
    'best-crm-for-': [
        ('best-crm-for-small-service-business', 'See the main CRM guide for small service businesses'),
        ('housecall-pro-vs-jobber', 'Compare two of the most common field-service options'),
        ('jobber-alternatives', 'See lighter and broader Jobber alternatives'),
    ],
    'best-field-service-management-software': [
        ('best-dispatch-software-for-small-service-business', 'Compare dispatch-first software options'),
        ('fieldpulse-vs-jobber', 'Compare FieldPulse and Jobber'),
        ('workiz-vs-jobber', 'Compare Workiz and Jobber'),
    ],
    'best-invoicing-software': [
        ('best-crm-for-small-service-business', 'See the main CRM guide for service businesses'),
        ('jobber-pricing-review', 'Review Jobber pricing and fit'),
        ('housecall-pro-pricing-vs-jobber-pricing', 'Compare two common pricing paths'),
    ],
    'vs': [
        ('best-crm-for-small-service-business', 'Go back to the main CRM shortlist'),
        ('service-titan-alternatives-for-small-businesses', 'See lighter alternatives for smaller teams'),
        ('best-field-service-management-software-for-small-business', 'Compare broader field service software options'),
    ],
    'alternatives': [
        ('best-crm-for-small-service-business', 'See the main CRM shortlist'),
        ('housecall-pro-vs-jobber', 'Compare two top field-service tools directly'),
        ('best-field-service-management-software-for-small-business', 'Expand the shortlist to broader FSM tools'),
    ],
}


def related_links(slug: str) -> list[tuple[str, str]]:
    for key, links in CATEGORY_MAP.items():
        if key in slug:
            return links
    return RELATED_DEFAULT


def main() -> None:
    content_dir = Path(__file__).resolve().parents[1] / 'output' / 'content'
    updated = 0
    for file in content_dir.glob('*.md'):
        text = file.read_text()
        slug = file.stem
        if '## Related guides' in text:
            text = text.split('## Related guides')[0].rstrip() + '\n'
        lines = ['## Related guides']
        seen = set()
        for target_slug, label in related_links(slug):
            if target_slug == slug or target_slug in seen:
                continue
            seen.add(target_slug)
            lines.append(f'- [{label}](/{target_slug})')
        text += '\n' + '\n'.join(lines) + '\n'
        file.write_text(text)
        updated += 1
    print(f'Refreshed internal link blocks on {updated} files')


if __name__ == '__main__':
    main()
