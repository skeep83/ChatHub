from __future__ import annotations

import json
import re
from pathlib import Path


def detect_meta(text: str) -> tuple[str, str]:
    page_type = re.search(r'page_type: "([^"]+)"', text)
    subtype = re.search(r'page_subtype: "([^"]+)"', text)
    return (page_type.group(1) if page_type else 'general', subtype.group(1) if subtype else 'general')


def record_order(page_type: str, subtype: str) -> list[str]:
    if page_type == 'comparison' and subtype == 'simple_vs_complex':
        return ['Chaturbate', 'LiveJasmin', 'Stripchat', 'Flirt4Free']
    if page_type == 'alternatives':
        return ['Stripchat', 'LiveJasmin', 'Chaturbate', 'Flirt4Free']
    return ['Stripchat', 'Chaturbate', 'LiveJasmin', 'Flirt4Free']


def main() -> None:
    base = Path(__file__).resolve().parents[1]
    verdicts = json.loads((base / 'data' / 'product_verdicts_adult_video_chat.json').read_text())
    by_name = {item['name']: item for item in verdicts}
    content_dir = base / 'output' / 'content'
    updated = 0
    for file in content_dir.glob('*.md'):
        text = file.read_text()
        page_type, subtype = detect_meta(text)
        names = record_order(page_type, subtype)
        lines = ['## Product records', '']
        for name in names:
            item = by_name[name]
            lines.append(f"### {name} record")
            lines.append(f"- Best fit: {item['best_fit']}")
            lines.append(f"- Adoption score: {item['adoption_score']}/10")
            lines.append(f"- Discovery score: {item['workflow_depth_score']}/10")
            lines.append(f"- Brand strength score: {item['marketing_score']}/10")
            lines.append(f"- Complexity: {item['complexity']}")
            lines.append(f"- Verdict: {item['verdict']}")
            lines.append('')
        block = '\n'.join(lines)
        if '## Product records' in text:
            text = re.sub(r'## Product records\n.*?(?=\n## )', block + '\n', text, flags=re.S)
        elif '## Recommended products' in text:
            text = text.replace('## Recommended products\n', block + '\n## Recommended products\n')
        else:
            continue
        file.write_text(text)
        updated += 1
    print(f'Updated structured product records on {updated} files')


if __name__ == '__main__':
    main()
