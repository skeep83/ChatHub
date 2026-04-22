from __future__ import annotations

import json
import urllib.parse
import urllib.request
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
OUT = BASE / 'output' / 'livejasmin_videos.json'
API = 'https://atwmcd.com/api/video-promotion/v1/list'
PSID = 'Skeepy83'
ACCESS_KEY = '4fd3ee2080af4020773f3ea847329855'
PSTOOL = '421_1'


def fetch_videos(limit: int = 12, orientation: str = 'straight') -> dict:
    params = {
        'psid': PSID,
        'pstool': PSTOOL,
        'accessKey': ACCESS_KEY,
        'ms_notrack': '1',
        'program': 'vpapi',
        'campaign_id': '135006',
        'site': 'jasmin',
        'sexualOrientation': orientation,
        'limit': str(limit),
        'primaryColor': '#8AC437',
        'labelColor': '#212121',
        'clientIp': 'request_ip',
    }
    url = API + '?' + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=25) as resp:
        return json.loads(resp.read().decode('utf-8', 'ignore'))


def normalize_url(url: str) -> str:
    if not url:
        return ''
    if url.startswith('//'):
        return 'https:' + url
    return url


def normalize(data: dict) -> dict:
    source = data.get('data') or {}
    videos = []
    for item in source.get('videos', []):
        previews = [normalize_url(x) for x in item.get('previewImages', []) if x]
        videos.append(
            {
                'id': item.get('id'),
                'title': item.get('title', ''),
                'duration': item.get('duration', 0),
                'tags': item.get('tags', []),
                'profile_image': normalize_url(item.get('profileImage', '')),
                'cover_image': normalize_url(item.get('coverImage', '')),
                'preview_images': previews,
                'thumb_image': previews[0] if previews else normalize_url(item.get('profileImage', '')),
                'target_url': normalize_url(item.get('targetUrl', '')),
                'details_url': normalize_url(item.get('detailsUrl', '')),
                'quality': item.get('quality', ''),
                'is_hd': item.get('isHd', False),
                'uploader': item.get('uploader', ''),
                'uploader_link': normalize_url(item.get('uploaderLink', '')),
            }
        )
    return {
        'success': data.get('success', False),
        'status': data.get('status', ''),
        'count': len(videos),
        'videos': videos,
    }


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    data = fetch_videos()
    normalized = normalize(data)
    OUT.write_text(json.dumps(normalized, ensure_ascii=False, indent=2))
    if not normalized['videos']:
        print(f"LiveJasmin API returned no videos, status={normalized['status']}")
    else:
        print(f"Saved {len(normalized['videos'])} normalized LiveJasmin videos to {OUT}")


if __name__ == '__main__':
    main()
