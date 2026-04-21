from __future__ import annotations

from pathlib import Path


BADGES = (
    '<div class="hero-badges">'
    '<span class="badge"><img src="assets/icons/crm.svg" alt="CRM icon" class="badge-icon"> CRM</span>'
    '<span class="badge"><img src="assets/icons/compare.svg" alt="Comparison icon" class="badge-icon"> Comparison</span>'
    '<span class="badge"><img src="assets/icons/money.svg" alt="Offers icon" class="badge-icon"> Offers</span>'
    '</div>'
)

INDEX_BADGES = (
    '<div class="hero-badges">'
    '<span class="badge"><img src="assets/icons/trust.svg" alt="Trust icon" class="badge-icon"> Trusted guides</span>'
    '<span class="badge"><img src="assets/icons/compare.svg" alt="Comparison icon" class="badge-icon"> Comparisons</span>'
    '<span class="badge"><img src="assets/icons/money.svg" alt="Offers icon" class="badge-icon"> Offers</span>'
    '</div>'
)

CSS = '''
.hero-badges{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:14px}
.badge{display:inline-flex;align-items:center;gap:8px;padding:8px 12px;border-radius:999px;background:rgba(255,255,255,.78);box-shadow:var(--shadow-soft);font-size:.86rem;font-weight:700;color:#30415c}
.badge-icon{width:18px;height:18px;display:block}
.hero-visual{padding:12px}
.hero-visual img{width:100%;height:320px;object-fit:cover;border-radius:20px;display:block;background:linear-gradient(135deg,rgba(107,140,255,.16),rgba(127,92,255,.1))}
'''


def inject_once(text: str, marker: str, insert: str) -> str:
    if insert in text:
        return text
    return text.replace(marker, marker + insert, 1)


def main() -> None:
    site_dir = Path(__file__).resolve().parents[1] / 'output' / 'site'
    updated = 0
    for path in site_dir.glob('*.html'):
        text = path.read_text()
        before = text
        if path.name == 'index.html':
            text = inject_once(text, '<section class="hero">', INDEX_BADGES)
        else:
            text = inject_once(text, '<div class="hero-copy">', BADGES)
        if CSS not in text:
            text = text.replace('</style>', CSS + '\n</style>')
        path.write_text(text)
        if text != before:
            updated += 1
    print(f'Enhanced hero graphics on {updated} pages')


if __name__ == '__main__':
    main()
