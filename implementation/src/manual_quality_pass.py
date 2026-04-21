from __future__ import annotations

from pathlib import Path

REWRITES = {
    '## Overview\nThis page is designed to help small service businesses compare CRM options without wasting time on generic software lists.\n': '## Overview\nThis page is designed to help users compare adult video chat options without wasting time on generic affiliate clutter or weak comparison copy.\n',
    '## Who this is for\nIt is for owners and operators who need quoting, scheduling, invoicing, customer follow-up, and basic pipeline visibility in one place.\n': '## Who this is for\nThis page is for users who want a faster path to the right adult video chat platform, whether they care most about mainstream browsing, premium private chat, or a safer all-round option.\n',
    '## How to choose\nChoose based on company size, dispatch complexity, budget tolerance, and whether you need a field-service-first tool or a broader CRM.\n': '## How to choose\nChoose based on whether you want broad model discovery, a more premium private-chat experience, or the strongest all-round fit without landing on a mismatched platform.\n',
    '## Comparison table\nA comparison table should highlight best fit, strengths, weaknesses, and pricing posture for each tool.\n': '## Comparison table\nA useful comparison should make it obvious which platform is stronger for mainstream discovery, premium private chat, and private-session-first intent.\n',
}


def main() -> None:
    content_dir = Path(__file__).resolve().parents[1] / 'output' / 'content'
    updated = 0
    for file in content_dir.glob('*.md'):
        text = file.read_text()
        before = text
        for old, new in REWRITES.items():
            text = text.replace(old, new)
        if text != before:
            file.write_text(text)
            updated += 1
    print(f'Applied manual quality pass to {updated} files')


if __name__ == '__main__':
    main()
