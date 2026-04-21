from __future__ import annotations

from pathlib import Path

BLOCK = """
## Site navigation
- [Home](/)
- [About DirtyChatHub](/about-dirtychathub)
- [Editorial Policy](/editorial-policy)
- [Contact](/contact)
"""


def main() -> None:
    content_dir = Path(__file__).resolve().parents[1] / 'output' / 'content'
    updated = 0
    for file in content_dir.glob('*.md'):
        text = file.read_text()
        if '## Site navigation' in text:
            text = text.split('## Site navigation')[0].rstrip() + '\n\n' + BLOCK
        else:
            text += '\n' + BLOCK
        file.write_text(text)
        updated += 1
    print(f'Refreshed site navigation on {updated} files')


if __name__ == '__main__':
    main()
