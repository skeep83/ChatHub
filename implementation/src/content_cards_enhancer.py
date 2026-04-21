from __future__ import annotations

import re
from pathlib import Path


def detect_meta(text: str) -> tuple[str, str]:
    page_type = re.search(r'page_type: "([^"]+)"', text)
    subtype = re.search(r'page_subtype: "([^"]+)"', text)
    return (page_type.group(1) if page_type else 'general', subtype.group(1) if subtype else 'general')


def quick_verdict(page_type: str, subtype: str) -> str:
    if page_type == 'best_of':
        return 'Most buyers should shortlist Stripchat and Chaturbate first, then keep LiveJasmin and Flirt4Free for more premium private-chat intent.'
    if page_type == 'comparison':
        return 'This comparison is mainly about mainstream discovery versus premium private-chat fit, not just which site is bigger.'
    if page_type == 'alternatives':
        return 'The best alternative is the one that fixes the experience mismatch without pushing the buyer into a weaker offer style.'
    return 'This page should help a buyer narrow the shortlist fast, not just browse names.'


def decision_shortcuts(page_type: str, subtype: str) -> list[str]:
    if page_type == 'best_of':
        return [
            'Choose Stripchat if you want the safest all-round shortlist option.',
            'Choose Chaturbate if mainstream discovery and public-room browsing matter more.',
            'Choose LiveJasmin or Flirt4Free if premium private-chat intent matters more than broad browsing.',
        ]
    if page_type == 'comparison':
        return [
            'Choose the mainstream platform if discovery volume and easier browsing matter most.',
            'Choose the premium platform if private-chat quality matters more than mass-market scale.',
            'Use Stripchat or Flirt4Free as secondary benchmarks if you want to widen the shortlist intelligently.',
        ]
    if page_type == 'alternatives':
        return [
            'Switch to Stripchat if you want the strongest all-round replacement.',
            'Switch to LiveJasmin if you want a more premium private-chat direction.',
            'Do not switch just to land on another site with the same mismatch in a different wrapper.',
        ]
    return [
        'Prioritize all-round fit first, then decide whether mainstream discovery or premium private-chat matters more.',
        'Do not mistake brand size for the best fit.',
        'Eliminate options that do not match the user intent of the page.',
    ]


def main() -> None:
    content_dir = Path(__file__).resolve().parents[1] / 'output' / 'content'
    updated = 0
    for file in content_dir.glob('*.md'):
        text = file.read_text()
        page_type, subtype = detect_meta(text)
        qv = '## Quick verdict\n' + quick_verdict(page_type, subtype) + '\n'
        ds_lines = ['## Decision shortcuts'] + [f'- {line}' for line in decision_shortcuts(page_type, subtype)]
        ds = '\n'.join(ds_lines) + '\n'
        if '## Quick verdict' in text:
            text = re.sub(r'## Quick verdict\n.*?(?=\n## )', qv, text, flags=re.S)
        else:
            text = text.replace('## Call to action\n', qv + '\n## Call to action\n')
        if '## Decision shortcuts' in text:
            text = re.sub(r'## Decision shortcuts\n.*?(?=\n## |\Z)', ds, text, flags=re.S)
        else:
            text += '\n' + ds
        file.write_text(text)
        updated += 1
    print(f'Enhanced decision content in {updated} files')


if __name__ == '__main__':
    main()
