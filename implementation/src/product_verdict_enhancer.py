from __future__ import annotations

import re
from pathlib import Path

DEFAULT_BLOCK = """
## Verdict snapshot
- Stripchat: strongest all-round fit for users who want broad model selection and mainstream cam discovery.
- Chaturbate: strong fit for users who prefer public-room browsing and a large free-to-paid funnel.
- LiveJasmin: better fit for buyers who care more about premium private chat than mass-market volume.
- Flirt4Free: strong premium alternative for users leaning toward private-session-first platforms.
"""

BEST_OF_BLOCK = """
## Verdict snapshot
- Stripchat: safest all-round shortlist choice for broad discovery and private-show flexibility.
- Chaturbate: strongest fit if mainstream browsing and sheer platform awareness matter most.
- LiveJasmin: stronger option if the buyer wants a more premium private-chat experience.
- Flirt4Free: useful premium alternative when private-session intent is stronger than discovery intent.
"""

COMPARISON_BLOCK = """
## Verdict snapshot
- Chaturbate: better fit when easier discovery and a mainstream browsing experience matter more.
- LiveJasmin: better fit when private premium experience matters more than mass-market scale.
- Stripchat: useful benchmark if the buyer still wants a broader all-round cam option in the shortlist.
- Flirt4Free: relevant for users still leaning toward premium private-session platforms.
"""

ALTERNATIVES_BLOCK = """
## Verdict snapshot
- Stripchat: strongest replacement if the goal is a broader all-round platform without overcomplicating the choice.
- LiveJasmin: stronger replacement when the user wants a more premium private-chat path.
- Chaturbate: strong replacement if mainstream browsing and public-room discovery are the priority.
- Flirt4Free: useful alternative for users who want another premium private-session route.
"""


def detect_meta(text: str) -> tuple[str, str]:
    page_type = re.search(r'page_type: "([^"]+)"', text)
    subtype = re.search(r'page_subtype: "([^"]+)"', text)
    return (page_type.group(1) if page_type else 'general', subtype.group(1) if subtype else 'general')


def verdict_block(page_type: str, subtype: str) -> str:
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
        block = verdict_block(page_type, subtype)
        if '## Verdict snapshot' in text:
            text = re.sub(r'## Verdict snapshot\n.*?(?=\n## )', block.rstrip() + '\n', text, flags=re.S)
            file.write_text(text)
            updated += 1
            continue
        if '## Recommended products' in text:
            text = text.replace('## Recommended products\n', block + '\n## Recommended products\n')
            file.write_text(text)
            updated += 1
    print(f'Updated verdict snapshots on {updated} files')


if __name__ == '__main__':
    main()
