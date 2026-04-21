from __future__ import annotations

from pathlib import Path

PAGES = {
    'about-dirtychathub.md': """# About DirtyChatHub

DirtyChatHub publishes adult video chat buying guides, comparisons, and alternatives for users who want a faster path to the right platform.

## What DirtyChatHub covers
- adult video chat sites
- private cam platforms
- comparison pages
- alternatives pages
- intent-specific cam and chat recommendations

## Goal
The goal is simple: help users compare adult video chat platforms without relying on empty hype or random affiliate clutter.
""",
    'contact.md': """# Contact

If you need to reach DirtyChatHub about a guide, correction, or commercial issue, use this page as the current contact point.

## What to contact us about
- factual corrections
- broken links
- partnership or affiliate issues
- content questions
""",
    'editorial-policy.md': """# Editorial Policy

DirtyChatHub aims to publish commercially aware but still useful adult video chat comparisons.

## Principles
- prioritize fit over hype
- separate comparison logic from pure ad copy
- keep affiliate incentives from overriding the core recommendation
- update pages when offers, brands, or platform fit meaningfully change
""",
}


def main() -> None:
    content_dir = Path(__file__).resolve().parents[1] / 'output' / 'content'
    content_dir.mkdir(parents=True, exist_ok=True)
    for filename, body in PAGES.items():
        (content_dir / filename).write_text(body + '\n')
    print(f'Built {len(PAGES)} trust pages')


if __name__ == '__main__':
    main()
