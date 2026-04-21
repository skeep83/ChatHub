from __future__ import annotations

from pathlib import Path

FAQ_BLOCK = """
## FAQ
### Is a field-service CRM always better than a general CRM?
Not always. It depends on whether your daily bottleneck is field operations or sales and marketing workflow.

### What is the biggest mistake small service businesses make when choosing software?
Choosing based on generic feature lists instead of matching the tool to scheduling, quoting, dispatch, invoicing, and follow-up needs.

### Should a small team choose the most powerful platform available?
Usually no. A smaller team often benefits more from faster adoption and operational clarity than from maximum feature depth.
"""


def main() -> None:
    content_dir = Path(__file__).resolve().parents[1] / 'output' / 'content'
    updated = 0
    for file in content_dir.glob('*.md'):
        text = file.read_text()
        if '## FAQ' in text:
            continue
        text += '\n' + FAQ_BLOCK
        file.write_text(text)
        updated += 1
    print(f'Added FAQ blocks to {updated} files')


if __name__ == '__main__':
    main()
