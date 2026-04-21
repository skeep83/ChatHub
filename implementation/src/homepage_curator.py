from __future__ import annotations

import json
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
OUT = BASE / 'output' / 'homepage_sections.json'

DATA = {
    'featured_money_pages': [
        {'slug': 'best-adult-video-chat-sites', 'label': 'Best Adult Video Chat Sites'},
        {'slug': 'best-private-cam-sites', 'label': 'Best Private Cam Sites'},
        {'slug': 'stripchat-vs-chaturbate', 'label': 'Stripchat vs Chaturbate'},
        {'slug': 'cam-site-alternatives-to-chaturbate', 'label': 'Cam Site Alternatives to Chaturbate'},
    ],
    'trust_pages': [
        {'slug': 'about-dirtychathub', 'label': 'About DirtyChatHub'},
        {'slug': 'editorial-policy', 'label': 'Editorial Policy'},
        {'slug': 'contact', 'label': 'Contact'},
    ],
    'clusters': [
        {'name': 'Best-of Guides', 'items': ['best-adult-video-chat-sites', 'best-private-cam-sites', 'best-adult-cam-sites-for-private-shows']},
        {'name': 'Comparisons and Alternatives', 'items': ['stripchat-vs-chaturbate', 'flirt4free-vs-livejasmin', 'cam-site-alternatives-to-chaturbate']},
        {'name': 'Intent Pages', 'items': ['best-anonymous-adult-video-chat', 'best-mobile-cam-sites', 'private-adult-video-chat-for-couples']},
    ]
}


def main() -> None:
    OUT.write_text(json.dumps(DATA, ensure_ascii=False, indent=2))
    print(f'Built homepage curation data at {OUT}')


if __name__ == '__main__':
    main()
