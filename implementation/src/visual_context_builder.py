from __future__ import annotations

from pathlib import Path

SVG_TEMPLATE = '''<svg viewBox="0 0 640 320" role="img" aria-labelledby="title desc" xmlns="http://www.w3.org/2000/svg">
  <title>{title}</title>
  <desc>{desc}</desc>
  <defs>
    <linearGradient id="bg" x1="0" x2="1">
      <stop offset="0%" stop-color="#6b8cff" stop-opacity="0.16"/>
      <stop offset="100%" stop-color="#7f5cff" stop-opacity="0.10"/>
    </linearGradient>
  </defs>
  <rect x="0" y="0" width="640" height="320" rx="28" fill="url(#bg)"/>
  <rect x="44" y="46" width="210" height="228" rx="22" fill="#ffffff" fill-opacity="0.82"/>
  <rect x="282" y="78" width="314" height="40" rx="16" fill="#ffffff" fill-opacity="0.70"/>
  <rect x="282" y="136" width="260" height="28" rx="14" fill="#ffffff" fill-opacity="0.58"/>
  <rect x="282" y="182" width="220" height="28" rx="14" fill="#ffffff" fill-opacity="0.52"/>
  <rect x="282" y="228" width="180" height="28" rx="14" fill="#6b8cff" fill-opacity="0.32"/>
  <circle cx="118" cy="112" r="34" fill="#6b8cff" fill-opacity="0.25"/>
  <rect x="92" y="168" width="112" height="18" rx="9" fill="#7f5cff" fill-opacity="0.26"/>
  <rect x="78" y="202" width="144" height="16" rx="8" fill="#6b8cff" fill-opacity="0.18"/>
</svg>'''


def label_for_slug(slug: str) -> tuple[str, str]:
    title = slug.replace('-', ' ').title() + ' illustration'
    desc = f'Contextual abstract illustration supporting the topic {slug.replace('-', ' ')}.'
    return title, desc


def main() -> None:
    site_dir = Path(__file__).resolve().parents[1] / 'output' / 'site'
    assets_dir = site_dir / 'assets' / 'visuals'
    assets_dir.mkdir(parents=True, exist_ok=True)
    created = 0
    for html_file in site_dir.glob('*.html'):
        slug = html_file.stem
        if slug == 'index':
            continue
        title, desc = label_for_slug(slug)
        svg = SVG_TEMPLATE.format(title=title, desc=desc)
        (assets_dir / f'{slug}.svg').write_text(svg)
        created += 1
    print(f'Built {created} contextual visuals')


if __name__ == '__main__':
    main()
