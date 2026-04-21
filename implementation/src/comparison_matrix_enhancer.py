from __future__ import annotations

from pathlib import Path

MATRIX = """
## Comparison matrix
- Broad discovery and mainstream reach: Chaturbate > Stripchat > LiveJasmin > Flirt4Free
- Premium private-chat feel: LiveJasmin > Flirt4Free > Stripchat > Chaturbate
- All-round shortlist safety: Stripchat > Chaturbate > LiveJasmin > Flirt4Free
- Private-session intent fit: LiveJasmin > Flirt4Free > Stripchat > Chaturbate
"""


def main() -> None:
    content_dir = Path(__file__).resolve().parents[1] / 'output' / 'content'
    updated = 0
    for file in content_dir.glob('*.md'):
        text = file.read_text()
        if '## Comparison matrix' in text:
            text = text.split('## Comparison matrix')[0] + MATRIX + '\n' + text.split('## Comparison matrix', 1)[1].split('\n## ', 1)[-1] if '\n## ' in text.split('## Comparison matrix', 1)[1] else text
            file.write_text(text)
            updated += 1
            continue
        if '## Comparison summary' in text:
            text = text.replace('## Comparison table\n', MATRIX + '\n## Comparison table\n')
            file.write_text(text)
            updated += 1
    print(f'Added comparison matrices to {updated} files')


if __name__ == '__main__':
    main()
