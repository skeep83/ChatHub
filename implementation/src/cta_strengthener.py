from __future__ import annotations

from pathlib import Path

TOP_PAGES = {
    'best-crm-for-small-service-business.md',
    'housecall-pro-vs-jobber.md',
    'jobber-alternatives.md',
    'jobber-pricing-review.md',
    'housecall-pro-review-for-small-business.md',
}


def main() -> None:
    content_dir = Path(__file__).resolve().parents[1] / 'output' / 'content'
    updated = 0
    for filename in TOP_PAGES:
        path = content_dir / filename
        if not path.exists():
            continue
        text = path.read_text()
        before = text
        text = text.replace('## Call to action\nSee the recommended tools and compare the best fit for your business.\n', '## Call to action\nShortlist the 1 to 2 tools that best match your workflow first, then use the offer block only after eliminating the obvious poor fits. Good software decisions usually come from narrowing choices, not clicking the first CTA.\n')
        if text != before:
            path.write_text(text)
            updated += 1
    print(f'Strengthened CTA language on {updated} top pages')


if __name__ == '__main__':
    main()
