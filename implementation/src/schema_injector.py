from __future__ import annotations

import json
import re
from pathlib import Path

BASE_URL = 'https://dirtychathub.com'
WEBSITE_SCHEMA = {
    '@context': 'https://schema.org',
    '@type': 'WebSite',
    'name': 'DirtyChatHub',
    'url': BASE_URL,
}


def extract_title(text: str) -> str:
    match = re.search(r'<h1>(.*?)</h1>', text, re.S)
    return re.sub(r'<.*?>', '', match.group(1)).strip() if match else 'DirtyChatHub'


def extract_description(text: str) -> str:
    match = re.search(r'<meta name="description" content="(.*?)">', text, re.S)
    return match.group(1).strip() if match else 'Adult video chat reviews, comparisons, alternatives, and private cam guides.'


def page_schema(slug: str, title: str, description: str) -> dict:
    url = BASE_URL + ('/' if slug == 'index' else f'/{slug}')
    schema_type = 'CollectionPage' if slug == 'index' else 'Article'
    return {
        '@context': 'https://schema.org',
        '@type': schema_type,
        'headline': title,
        'name': title,
        'description': description,
        'url': url,
        'isPartOf': {'@type': 'WebSite', 'name': 'DirtyChatHub', 'url': BASE_URL},
        'about': 'Adult video chat and cam comparison guides',
    }


def breadcrumb_schema(slug: str, title: str) -> dict:
    item_list = [
        {'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': BASE_URL + '/'},
    ]
    if slug != 'index':
        item_list.append({'@type': 'ListItem', 'position': 2, 'name': title, 'item': BASE_URL + f'/{slug}'})
    return {
        '@context': 'https://schema.org',
        '@type': 'BreadcrumbList',
        'itemListElement': item_list,
    }


def main() -> None:
    site_dir = Path(__file__).resolve().parents[1] / 'output' / 'site'
    updated = 0
    for file in site_dir.glob('*.html'):
        if file.name.startswith('fo-verify'):
            continue
        text = file.read_text()
        slug = file.stem
        title = extract_title(text)
        description = extract_description(text)
        schemas = [WEBSITE_SCHEMA, page_schema(slug, title, description), breadcrumb_schema(slug, title)]
        schema_block = '<script type="application/ld+json">' + json.dumps(schemas, ensure_ascii=False) + '</script>'
        text = re.sub(r'<script type="application/ld\+json">.*?</script>', '', text, flags=re.S)
        text = text.replace('</head>', schema_block + '\n</head>')
        file.write_text(text)
        updated += 1
    print(f'Injected schema into {updated} pages')


if __name__ == '__main__':
    main()
