from __future__ import annotations

from pathlib import Path

REWRITES = {
    'best-adult-video-chat-sites.md': {
        '## Overview\nThis page is designed to help users compare adult video chat options without wasting time on generic hype pages.\n': '## Overview\nMost users do not need a giant list of cam platforms. They need a shortlist that separates broad discovery sites from premium private-chat options and makes the fit obvious fast.\n',
        '## Final recommendation\nThe best option should match the user intent of the session, not just the biggest brand name.\n': '## Final recommendation\nFor most users, Stripchat and Chaturbate belong in the first shortlist. LiveJasmin and Flirt4Free become stronger when premium private-chat intent matters more than broad browsing.\n',
    },
    'best-private-cam-sites.md': {
        '## Overview\nThis page is designed to help users compare adult video chat options without wasting time on generic hype pages.\n': '## Overview\nPrivate cam buyers need a different shortlist than mainstream browsing users. This page should focus on platforms that make private sessions feel stronger, cleaner, and more intentional.\n',
    },
    'cam-site-alternatives-to-chaturbate.md': {
        '## Why people look for alternatives\nUsers usually look for alternatives when the experience feels too mainstream, too weak on private chat, or just mismatched to what they actually want.\n': '## Why people look for alternatives\nMost users look for alternatives to Chaturbate when they want a better private-chat experience, a different browsing feel, or a less mainstream platform mix.\n',
    },
}


def main() -> None:
    content_dir = Path(__file__).resolve().parents[1] / 'output' / 'content'
    updated = 0
    for filename, replacements in REWRITES.items():
        target = content_dir / filename
        if not target.exists():
            continue
        text = target.read_text()
        before = text
        for old, new in replacements.items():
            text = text.replace(old, new)
        if text != before:
            target.write_text(text)
            updated += 1
    print(f'Rewrote {updated} money pages')


if __name__ == '__main__':
    main()
