from __future__ import annotations

from pathlib import Path


def main() -> None:
    site_dir = Path(__file__).resolve().parents[1] / 'output' / 'site'
    updated = 0
    for path in site_dir.glob('*.html'):
        text = path.read_text()
        before = text
        text = text.replace("<article class='product-card'><h3>", "<article class='product-card'><div class='card-icon-wrap'><img src=\"assets/icons/crm.svg\" alt=\"CRM icon\" class=\"card-icon\"></div><h3>")
        if '.card-icon' not in text:
            text = text.replace('</style>', '.card-icon-wrap{margin-bottom:10px}.card-icon{width:28px;height:28px;display:block}\n</style>')
        if text != before:
            path.write_text(text)
            updated += 1
    print(f'Injected card icons into {updated} pages')


if __name__ == '__main__':
    main()
