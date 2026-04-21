from __future__ import annotations

from pathlib import Path


def main() -> None:
    content_dir = Path(__file__).resolve().parents[1] / 'output' / 'content'
    updated = 0
    for file in content_dir.glob('*.md'):
        text = file.read_text()
        before = text
        text = text.replace('\n\n\n', '\n\n')
        text = text.replace('## Get help choosing\nIf you want help narrowing the shortlist for your business, use a simple lead form or contact flow here later.\n\n## Need help choosing', '## Need help choosing')
        if text != before:
            file.write_text(text)
            updated += 1
    print(f'Final cleanup adjusted {updated} files')


if __name__ == '__main__':
    main()
