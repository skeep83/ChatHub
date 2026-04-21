from __future__ import annotations

from pathlib import Path

ICONS = {
    'crm': '<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="title desc"><title>CRM icon</title><desc>Icon representing customer management software</desc><rect x="8" y="12" width="48" height="40" rx="12" fill="#6b8cff" fill-opacity="0.18"/><circle cx="24" cy="28" r="6" fill="#6b8cff"/><rect x="34" y="24" width="14" height="4" rx="2" fill="#7f5cff"/><rect x="34" y="32" width="10" height="4" rx="2" fill="#7f5cff"/></svg>',
    'compare': '<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="title desc"><title>Comparison icon</title><desc>Icon representing product comparison</desc><rect x="10" y="14" width="18" height="36" rx="8" fill="#6b8cff" fill-opacity="0.22"/><rect x="36" y="14" width="18" height="36" rx="8" fill="#7f5cff" fill-opacity="0.22"/><path d="M32 22v20" stroke="#536dfe" stroke-width="4" stroke-linecap="round"/></svg>',
    'money': '<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="title desc"><title>Monetization icon</title><desc>Icon representing monetization and offers</desc><rect x="10" y="18" width="44" height="28" rx="10" fill="#6b8cff" fill-opacity="0.18"/><circle cx="32" cy="32" r="9" fill="#7f5cff" fill-opacity="0.24"/><path d="M32 26v12M27 30h10M27 34h10" stroke="#536dfe" stroke-width="3" stroke-linecap="round"/></svg>',
    'trust': '<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="title desc"><title>Trust icon</title><desc>Icon representing trust and editorial reliability</desc><path d="M32 10l18 8v12c0 12-8 20-18 24-10-4-18-12-18-24V18l18-8z" fill="#6b8cff" fill-opacity="0.18"/><path d="M24 32l6 6 12-14" stroke="#536dfe" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/></svg>'
}


def main() -> None:
    out = Path(__file__).resolve().parents[1] / 'output' / 'site' / 'assets' / 'icons'
    out.mkdir(parents=True, exist_ok=True)
    for name, svg in ICONS.items():
        (out / f'{name}.svg').write_text(svg)
    print(f'Built {len(ICONS)} icon assets')


if __name__ == '__main__':
    main()
