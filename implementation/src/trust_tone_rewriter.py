from __future__ import annotations

from pathlib import Path

REPLACEMENTS = {
    'DirtyChatHub publishes adult video chat buying guides, comparisons, and alternatives for users who want a faster path to the right platform.': 'DirtyChatHub is a focused adult video chat review and comparison publication. It exists to help users evaluate cam and private-chat platforms with clearer judgment and less empty promo noise.',
    'If you need to reach DirtyChatHub about a guide, correction, or commercial issue, use this page as the current contact point.': 'If you need to contact DirtyChatHub about a guide, correction, or commercial issue, use this page as the current contact route.',
    'DirtyChatHub aims to publish commercially aware but still useful adult video chat comparisons.': 'DirtyChatHub aims to publish commercially aware but genuinely useful adult video chat comparisons and alternatives.',
}


def main() -> None:
    content_dir = Path(__file__).resolve().parents[1] / 'output' / 'content'
    updated = 0
    for file in content_dir.glob('*.md'):
        text = file.read_text()
        before = text
        for old, new in REPLACEMENTS.items():
            text = text.replace(old, new)
        if text != before:
            file.write_text(text)
            updated += 1
    print(f'Rewrote trust tone in {updated} files')


if __name__ == '__main__':
    main()
