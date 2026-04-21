from __future__ import annotations

from pathlib import Path


def main() -> None:
    site_dir = Path(__file__).resolve().parents[1] / 'output' / 'site'
    redirects_path = site_dir / '_redirects'
    lines = ['# Canonical redirect hints', '/index.html / 301']
    for file in site_dir.glob('*.html'):
        if file.name == 'index.html':
            continue
        lines.append(f'/{file.name} /{file.stem} 301')
    redirects_path.write_text('\n'.join(lines) + '\n')
    print(f'Wrote redirects file to {redirects_path}')


if __name__ == '__main__':
    main()
