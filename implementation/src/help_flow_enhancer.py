from __future__ import annotations

from pathlib import Path

TOP_PAGES = {
    'best-crm-for-small-service-business.md',
    'housecall-pro-vs-jobber.md',
    'jobber-alternatives.md',
    'jobber-pricing-review.md',
    'housecall-pro-review-for-small-business.md',
}

HELP_BLOCK = """
## Need help choosing
If you are comparing 2 to 4 tools and still feel uncertain, use the contact page and describe your business size, workflow, and priorities. ServiceHub should evolve toward shortlist guidance, not only static content.
"""


def main() -> None:
    content_dir = Path(__file__).resolve().parents[1] / 'output' / 'content'
    updated = 0
    for filename in TOP_PAGES:
        path = content_dir / filename
        if not path.exists():
            continue
        text = path.read_text()
        text = text.replace('## Get help choosing\nIf you want help narrowing the shortlist for your business, use a simple lead form or contact flow here later.\n', '')
        if '## Need help choosing' not in text:
            text += '\n' + HELP_BLOCK
        path.write_text(text)
        updated += 1
    print(f'Enhanced help flow on {updated} top pages')


if __name__ == '__main__':
    main()
