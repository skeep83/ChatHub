from __future__ import annotations

import json
import re
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit


def detect_meta(text: str) -> tuple[str, str, str]:
    page_type = re.search(r'page_type: "([^"]+)"', text)
    subtype = re.search(r'page_subtype: "([^"]+)"', text)
    slug = re.search(r'slug: "([^"]+)"', text)
    return (
        page_type.group(1) if page_type else 'general',
        subtype.group(1) if subtype else 'general',
        slug.group(1) if slug else 'general',
    )


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


def tracked_chaturbate_link(slug: str, page_type: str) -> str:
    if page_type == 'best_of' and 'private' in slug:
        base = 'https://chaturbate.com/in/?tour=dU9X&campaign=aoQgT&track=default&signup_notice=1'
    elif 'anonymous' in slug:
        base = 'https://chaturbate.com/in/?tour=IGtl&campaign=aoQgT&track=default'
    elif 'couple' in slug:
        base = 'https://chaturbate.com/in/?tour=0G9g&campaign=aoQgT&track=default'
    elif 'trans' in slug:
        base = 'https://chaturbate.com/in/?tour=khMd&campaign=aoQgT&track=default'
    else:
        base = 'https://chaturbate.com/in/?tour=grq0&campaign=aoQgT&track=default'

    track = f"skeepy83_{slug.replace('-', '_')[:40]}"
    parts = urlsplit(base)
    query = dict(parse_qsl(parts.query, keep_blank_values=True))
    query['track'] = track
    return urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(query), parts.fragment))


def build_block(by_product: dict, page_type: str, subtype: str, slug: str) -> str:
    lines = ['## Offers', '']
    overrides = cta_overrides(page_type, subtype)
    for product in product_order(page_type, subtype):
        item = by_product[product].copy()
        if product == 'Chaturbate':
            item['placeholder_url'] = tracked_chaturbate_link(slug, page_type)
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
        page_type, subtype, slug = detect_meta(text)
        block = build_block(by_product, page_type, subtype, slug)
        if '## Offers' in text:
            text = re.sub(r'## Offers\n(?:.*\n)*?(?=\n## |\Z)', block + '\n', text, flags=re.MULTILINE)
        else:
            text += '\n' + block
        file.write_text(text)
        updated += 1
    print(f'Injected or refreshed offers in {updated} files')


if __name__ == '__main__':
    main()
