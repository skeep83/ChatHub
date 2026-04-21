from __future__ import annotations

import re
from pathlib import Path

DEFAULT_BLOCK = """
## Comparison summary
- Best if you want broad model discovery and a strong all-round cam option: Stripchat.
- Best if you prefer mainstream public-room browsing: Chaturbate.
- Best if you want a more premium private-chat experience: LiveJasmin.
- Best if you want another premium private-session benchmark: Flirt4Free.
"""

BEST_OF_BLOCK = """
## Comparison summary
- Best if you want the safest all-round adult video chat shortlist: Stripchat.
- Best if discovery and public-room browsing matter most: Chaturbate.
- Best if premium private-chat quality matters more than mass-market scale: LiveJasmin.
- Best if you want another premium private-session option in the shortlist: Flirt4Free.
"""

COMPARISON_BLOCK = """
## Comparison summary
- Best if you want easier mainstream discovery and public-room browsing: Chaturbate.
- Best if you want a more premium private-chat experience: LiveJasmin.
- Best if you want a broader all-round benchmark in the same shortlist: Stripchat.
- Best if you want another premium private-session comparison point: Flirt4Free.
"""

ALTERNATIVES_BLOCK = """
## Comparison summary
- Best if you want the strongest all-round replacement: Stripchat.
- Best if you want a more premium private-chat replacement: LiveJasmin.
- Best if you still want mainstream browsing and broad discovery: Chaturbate.
- Best if you want another premium private-session path: Flirt4Free.
"""


def detect_meta(text: str) -> tuple[str, str]:
    page_type = re.search(r'page_type: "([^"]+)"', text)
    subtype = re.search(r'page_subtype: "([^"]+)"', text)
    return (page_type.group(1) if page_type else 'general', subtype.group(1) if subtype else 'general')


def block_for(page_type: str, subtype: str) -> str:
    if page_type == 'best_of':
        return BEST_OF_BLOCK
    if page_type == 'comparison':
        return COMPARISON_BLOCK
    if page_type == 'alternatives':
        return ALTERNATIVES_BLOCK
    return DEFAULT_BLOCK


def main() -> None:
    content_dir = Path(__file__).resolve().parents[1] / 'output' / 'content'
    updated = 0
    for file in content_dir.glob('*.md'):
        text = file.read_text()
        page_type, subtype = detect_meta(text)
        block = block_for(page_type, subtype)
        if '## Comparison summary' in text:
            text = re.sub(r'## Comparison summary\n.*?(?=\n## )', block.rstrip() + '\n', text, flags=re.S)
        elif '## Comparison table' in text:
            text = text.replace('## Comparison table\n', block + '\n## Comparison table\n')
        else:
            continue
        file.write_text(text)
        updated += 1
    print(f'Updated comparison summaries on {updated} files')


if __name__ == '__main__':
    main()
