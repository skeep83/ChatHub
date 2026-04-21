from __future__ import annotations

from pathlib import Path

BASE_URL = 'https://servicehub.md/'


def main() -> None:
    site_dir = Path(__file__).resolve().parents[1] / 'output' / 'site'
    updated = 0
    for file in site_dir.glob('*.html'):
        if file.name.startswith('fo-verify'):
            continue
        slug = file.stem
        canonical = BASE_URL if slug == 'index' else f'{BASE_URL}{slug}'
        text = file.read_text()
        if 'rel="canonical"' in text:
            continue
        text = text.replace('</head>', f'<link rel="canonical" href="{canonical}">\n</head>')
        file.write_text(text)
        updated += 1
    print(f'Injected canonicals into {updated} pages')


if __name__ == '__main__':
    main()
