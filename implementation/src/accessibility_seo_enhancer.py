from __future__ import annotations

from pathlib import Path


VERIFY_TAG = '<meta name="fo-verify" content="9e1d32fb-49d8-48e6-a930-ba97187d23da">'


def main() -> None:
    site_dir = Path(__file__).resolve().parents[1] / 'output' / 'site'
    updated = 0
    for file in site_dir.glob('*.html'):
        if file.name.startswith('fo-verify'):
            continue
        text = file.read_text()
        before = text
        text = text.replace('<html lang="en">', '<html lang="en"><!-- enhanced -->')
        text = text.replace('<body>', '<body><a href="#main-content" class="skip-link">Skip to content</a>')
        text = text.replace('<main class="main-col">', '<main id="main-content" class="main-col" role="main">')
        text = text.replace('<nav class="topnav">', '<nav class="topnav" aria-label="Primary">')
        text = text.replace('<section class="grid">', '<section class="grid" aria-label="Guide links">', 1)
        if 'name="fo-verify"' not in text:
            text = text.replace('</head>', f'  {VERIFY_TAG}\n</head>')
        if '.skip-link' not in text:
            text = text.replace('</style>', '.skip-link{position:absolute;left:-9999px;top:auto;width:1px;height:1px;overflow:hidden}.skip-link:focus{left:16px;top:16px;width:auto;height:auto;padding:10px 14px;background:#fff;color:#111;border-radius:10px;z-index:9999;box-shadow:0 4px 18px rgba(0,0,0,.15)}\n</style>')
        if text != before:
            file.write_text(text)
            updated += 1
    print(f'Applied accessibility/SEO enhancements to {updated} pages')


if __name__ == '__main__':
    main()
