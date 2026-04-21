from __future__ import annotations

from pathlib import Path


def main() -> None:
    path = Path(__file__).resolve().parents[1] / 'output' / 'homepage_sections.json'
    if not path.exists():
        print('Homepage sections file not found')
        return
    print('Homepage conversion layer uses curated homepage_sections.json and html_builder rendering')


if __name__ == '__main__':
    main()
