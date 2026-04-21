from __future__ import annotations

import json
from pathlib import Path


def main() -> None:
    base = Path(__file__).resolve().parents[1]
    site_dir = base / "output" / "site"
    files = []
    for path in sorted(site_dir.glob("*")):
        if path.is_file():
            files.append({"name": path.name, "size": path.stat().st_size})
    manifest = {
        "site_dir": str(site_dir),
        "artifact_count": len(files),
        "files": files,
        "deploy_target": "pending-domain",
        "recommended_first_hosting": "nginx or static file host",
    }
    out = base / "output" / "deploy_manifest.json"
    out.write_text(json.dumps(manifest, ensure_ascii=False, indent=2))
    print(f"Built {out}")


if __name__ == "__main__":
    main()
