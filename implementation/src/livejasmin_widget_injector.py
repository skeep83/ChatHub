from __future__ import annotations

from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
TARGETS = {
    'best-private-cam-sites.md': ('LiveJasmin live preview', 'dch_private_cam_widget'),
    'flirt4free-vs-livejasmin.md': ('LiveJasmin live preview', 'dch_lj_compare_widget'),
    'best-adult-video-chat-sites.md': ('LiveJasmin featured preview', 'dch_best_video_chat_widget'),
}


def build_block(label: str, sub_aff_id: str) -> str:
    embed = (
        '<div class="lj-widget-shell">\n'
        '  <div id="object_container_' + sub_aff_id + '" class="lj-widget-frame"></div>\n'
        '  <script src="https://ecdwm.com/embed/lf?'
        'c=object_container_' + sub_aff_id +
        '&site=jasmin&cobrandId=&psid=Skeepy83&pstool=202_1&psprogram=pps&campaign_id=&category=girl'
        '&forcedPerformers[]=&vp[showChat]=&vp[chatAutoHide]=&vp[showCallToAction]=&vp[showPerformerName]=&vp[showPerformerStatus]=&ms_notrack=1'
        '&subAffId=' + sub_aff_id + '"></script>'
    )
    return f"## {label}\n\n<!-- livejasmin-widget -->\n{embed}\n"


def main() -> None:
    content_dir = BASE / 'output' / 'content'
    updated = 0
    for filename, (label, sub_aff_id) in TARGETS.items():
        path = content_dir / filename
        if not path.exists():
            continue
        text = path.read_text()
        block = build_block(label, sub_aff_id)
        marker = f'## {label}'
        if marker in text:
            text = text.split(marker)[0].rstrip() + '\n\n' + block + '\n'
        else:
            text += '\n' + block + '\n'
        path.write_text(text)
        updated += 1
    print(f'Injected LiveJasmin widgets into {updated} files')


if __name__ == '__main__':
    main()
