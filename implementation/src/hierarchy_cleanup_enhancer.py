from __future__ import annotations

from pathlib import Path

TOP_PAGES = {
    'best-crm-for-small-service-business.md',
    'housecall-pro-vs-jobber.md',
    'jobber-alternatives.md',
    'jobber-pricing-review.md',
    'housecall-pro-review-for-small-business.md',
}

REMOVE_HEADINGS = [
    '## Editor note\nThis page should be reviewed before publication, especially if it carries affiliate links or product claims.\n',
]


def main() -> None:
    content_dir = Path(__file__).resolve().parents[1] / 'output' / 'content'
    updated = 0
    for filename in TOP_PAGES:
        path = content_dir / filename
        if not path.exists():
            continue
        text = path.read_text()
        before = text
        for block in REMOVE_HEADINGS:
            text = text.replace(block, '')
        text = text.replace('## Get help choosing\nIf you want help narrowing the shortlist for your business, use a simple lead form or contact flow here later.\n', '## Need help choosing\nIf your shortlist is still unclear, use the contact path on ServiceHub once the help workflow is fully enabled.\n')
        if text != before:
            path.write_text(text)
            updated += 1
    print(f'Cleaned hierarchy on {updated} top pages')


if __name__ == '__main__':
    main()
