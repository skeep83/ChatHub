from __future__ import annotations

from pathlib import Path


def main() -> None:
    site_dir = Path(__file__).resolve().parents[1] / 'output' / 'site'
    exported = 0
    for html_file in site_dir.glob('*.html'):
        if html_file.name == 'index.html':
            continue
        clean_path = site_dir / html_file.stem
        clean_path.write_text(html_file.read_text())
        exported += 1
    print(f'Exported {exported} clean-route files')


if __name__ == '__main__':
    main()
