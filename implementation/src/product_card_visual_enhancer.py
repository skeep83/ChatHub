from __future__ import annotations

from pathlib import Path


def main() -> None:
    content_dir = Path(__file__).resolve().parents[1] / 'output' / 'content'
    updated = 0
    for file in content_dir.glob('*.md'):
        text = file.read_text()
        if '## Product records' not in text:
            continue
        text = text.replace('## Product records', '## Product scorecards')
        text = text.replace('### Jobber record', '### Jobber scorecard')
        text = text.replace('### Housecall Pro record', '### Housecall Pro scorecard')
        text = text.replace('### ServiceTitan record', '### ServiceTitan scorecard')
        text = text.replace('### HubSpot record', '### HubSpot scorecard')
        file.write_text(text)
        updated += 1
    print(f'Reframed structured product records in {updated} files')


if __name__ == '__main__':
    main()
