from __future__ import annotations

import json
from pathlib import Path


def main() -> None:
    base = Path(__file__).resolve().parents[1]
    review_queue = json.loads((base / "output" / "review_queue.json").read_text())
    manifest = json.loads((base / "output" / "deploy_manifest.json").read_text())
    report = {
        "artifact_count": manifest["artifact_count"],
        "review_queue_count": len(review_queue),
        "public_ready": False,
        "blocking_items": [
            "domain not chosen",
            "commercial pages need review",
            "affiliate/lead integrations not wired",
            "analytics provider not connected",
        ],
    }
    out = base / "output" / "public_readiness_report.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2))
    print(f"Built {out}")


if __name__ == "__main__":
    main()
