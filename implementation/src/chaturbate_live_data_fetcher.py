from __future__ import annotations

import json
import urllib.parse
import urllib.request
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
OUT = BASE / 'output' / 'chaturbate_live_rooms.json'
WM = 'aoQgT'
API = 'https://chaturbate.com/api/public/affiliates/onlinerooms/'


def fetch_rooms(limit: int = 24, genders: list[str] | None = None, tags: list[str] | None = None) -> dict:
    params: list[tuple[str, str]] = [
        ('wm', WM),
        ('client_ip', 'request_ip'),
        ('format', 'json'),
        ('limit', str(limit)),
        ('hd', 'true'),
    ]
    for gender in genders or ['f', 'c']:
        params.append(('gender', gender))
    for tag in tags or []:
        params.append(('tag', tag))
    url = API + '?' + urllib.parse.urlencode(params, doseq=True)
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.loads(resp.read().decode('utf-8', 'ignore'))


def normalize(data: dict) -> dict:
    rooms = []
    for item in data.get('results', []):
        rooms.append(
            {
                'username': item.get('username'),
                'display_name': item.get('display_name') or item.get('username'),
                'room_subject': item.get('room_subject', ''),
                'current_show': item.get('current_show', ''),
                'is_hd': item.get('is_hd', False),
                'num_users': item.get('num_users', 0),
                'num_followers': item.get('num_followers', 0),
                'tags': item.get('tags', []),
                'image_url': item.get('image_url_360x270') or item.get('image_url'),
                'chat_room_url': item.get('chat_room_url_revshare') or item.get('chat_room_url'),
            }
        )
    return {'count': data.get('count', len(rooms)), 'rooms': rooms}


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    data = fetch_rooms()
    normalized = normalize(data)
    OUT.write_text(json.dumps(normalized, ensure_ascii=False, indent=2))
    print(f"Saved {len(normalized['rooms'])} normalized Chaturbate rooms to {OUT}")


if __name__ == '__main__':
    main()
