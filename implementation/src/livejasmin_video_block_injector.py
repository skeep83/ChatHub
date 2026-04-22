from __future__ import annotations

import json
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
DATA = BASE / 'output' / 'livejasmin_videos.json'
TARGETS = {
    'best-private-cam-sites.md': 'Premium LiveJasmin picks right now',
    'flirt4free-vs-livejasmin.md': 'LiveJasmin featured videos right now',
}


def build_block(label: str, videos: list[dict]) -> str:
    lines = [f'## {label}', '<!-- livejasmin-video-grid -->', '']
    for item in videos[:6]:
        tags = '|'.join(item.get('tags', [])[:4])
        parts = [
            item.get('title', ''),
            item.get('target_url', ''),
            item.get('thumb_image', ''),
            str(item.get('duration', 0)),
            item.get('quality', '') or 'sd',
            'hd' if item.get('is_hd') else 'standard',
            tags,
            item.get('uploader', 'LiveJasmin'),
        ]
        lines.append('LJ-VIDEO-CARD::' + '||'.join(parts))
    lines.append('')
    return '\n'.join(lines)


def main() -> None:
    if not DATA.exists():
        print('No LiveJasmin snapshot found, skipping injection')
        return
    data = json.loads(DATA.read_text())
    videos = data.get('videos', [])
    content_dir = BASE / 'output' / 'content'
    updated = 0
    for filename, label in TARGETS.items():
        target = content_dir / filename
        if not target.exists():
            continue
        text = target.read_text()
        block = build_block(label, videos)
        marker = f'## {label}'
        if marker in text:
            text = text.split(marker)[0].rstrip() + '\n\n' + block + '\n'
        else:
            text += '\n' + block + '\n'
        target.write_text(text)
        updated += 1
    print(f'Injected LiveJasmin video blocks into {updated} files')


if __name__ == '__main__':
    main()
