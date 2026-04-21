from __future__ import annotations

import json
import re
from pathlib import Path


def detect_meta(text: str) -> tuple[str, str]:
    page_type = re.search(r'page_type: "([^"]+)"', text)
    subtype = re.search(r'page_subtype: "([^"]+)"', text)
    return (page_type.group(1) if page_type else 'general', subtype.group(1) if subtype else 'general')


def product_order(page_type: str, subtype: str) -> list[str]:
    if page_type == 'best_of' and subtype == 'crm':
        return ['Stripchat', 'Chaturbate', 'LiveJasmin', 'Flirt4Free']
    if page_type == 'comparison' and subtype == 'simple_vs_complex':
        return ['Chaturbate', 'LiveJasmin', 'Stripchat', 'Flirt4Free']
    if page_type == 'alternatives' and subtype == 'workflow_pain':
        return ['Stripchat', 'LiveJasmin', 'Chaturbate', 'Flirt4Free']
    return ['Stripchat', 'Chaturbate', 'LiveJasmin', 'Flirt4Free']


def cta_overrides(page_type: str, subtype: str) -> dict[str, str]:
    if page_type == 'best_of':
        return {
            'Stripchat': 'Try Stripchat if you want the broadest all-round cam discovery experience',
            'Chaturbate': 'Try Chaturbate if you want the biggest mainstream free-to-paid browsing funnel',
            'LiveJasmin': 'Try LiveJasmin if you care more about premium private chat than mass-market volume',
            'Flirt4Free': 'Try Flirt4Free if you want a private-session-first premium option',
        }
    if page_type == 'comparison' and subtype == 'simple_vs_complex':
        return {
            'Chaturbate': 'Try Chaturbate if you want easier discovery and a lighter mainstream entry point',
            'LiveJasmin': 'Try LiveJasmin if you want a more premium private-chat experience',
            'Stripchat': 'Try Stripchat if you want another high-volume comparison benchmark',
            'Flirt4Free': 'Try Flirt4Free if you want another premium private-session option',
        }
    if page_type == 'alternatives':
        return {
            'Stripchat': 'Try Stripchat if you want a stronger all-round alternative with broad model choice',
            'LiveJasmin': 'Try LiveJasmin if you want a more premium private-chat alternative',
            'Chaturbate': 'Try Chaturbate if you prefer mainstream discovery and public-room browsing',
            'Flirt4Free': 'Try Flirt4Free if you want a more premium private-show path',
        }
    return {}


def build_block(by_product: dict, page_type: str, subtype: str) -> str:
    lines = ['## Offers', '']
    overrides = cta_overrides(page_type, subtype)
    for product in product_order(page_type, subtype):
        item = by_product[product]
        cta = overrides.get(product, item['cta'])
        lines.append(f'- [{cta}]({item["placeholder_url"]})')
    lines.append('')
    return '\n'.join(lines)


def main() -> None:
    base = Path(__file__).resolve().parents[1]
    links = json.loads((base / 'data' / 'affiliate_placeholders.json').read_text())
    by_product = {item['product']: item for item in links}
    content_dir = base / 'output' / 'content'
    updated = 0
    for file in content_dir.glob('*.md'):
        text = file.read_text()
        page_type, subtype = detect_meta(text)
        block = build_block(by_product, page_type, subtype)
        if '## Offers' in text:
            text = re.sub(r'## Offers\n(?:.*\n)*?(?=\n## |\Z)', block + '\n', text, flags=re.MULTILINE)
        else:
            text += '\n' + block
        file.write_text(text)
        updated += 1
    print(f'Injected or refreshed offers in {updated} files')


if __name__ == '__main__':
    main()
