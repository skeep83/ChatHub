from __future__ import annotations

import json
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
DATA = BASE / 'output' / 'chaturbate_live_rooms.json'
TARGETS = {
    'best-adult-video-chat-sites.md': 'Live rooms worth checking right now',
    'best-private-cam-sites.md': 'Live private-chat leaning rooms right now',
    'best-anonymous-adult-video-chat.md': 'Live rooms to explore right now',
}


def build_block(label: str, rooms: list[dict]) -> str:
    lines = [f'## {label}', '<!-- chaturbate-live-grid -->', '']
    for room in rooms[:6]:
        tags = '|'.join(room.get('tags', [])[:4])
        subject = (room.get('room_subject') or '').replace('\n', ' ').strip()
        parts = [
            room.get('display_name') or room.get('username') or '',
            room.get('chat_room_url') or '',
            room.get('image_url') or '',
            str(room.get('num_users', 0)),
            str(room.get('num_followers', 0)),
            room.get('current_show') or 'public',
            tags,
            subject,
        ]
        lines.append('CB-LIVE-CARD::' + '||'.join(parts))
    lines.append('')
    return '\n'.join(lines)


def main() -> None:
    if not DATA.exists():
        print('No Chaturbate live room snapshot found, skipping injection')
        return
    data = json.loads(DATA.read_text())
    rooms = data.get('rooms', [])
    content_dir = BASE / 'output' / 'content'
    updated = 0
    for filename, label in TARGETS.items():
        target = content_dir / filename
        if not target.exists():
            continue
        text = target.read_text()
        block = build_block(label, rooms)
        marker = f'## {label}'
        if marker in text:
            text = text.split(marker)[0].rstrip() + '\n\n' + block + '\n'
        else:
            text += '\n' + block + '\n'
        target.write_text(text)
        updated += 1
    print(f'Injected Chaturbate live blocks into {updated} files')


if __name__ == '__main__':
    main()
