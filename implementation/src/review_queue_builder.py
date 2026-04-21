from __future__ import annotations

import json
from pathlib import Path


def main() -> None:
    base = Path(__file__).resolve().parents[1]
    registry = json.loads((base / "output" / "page_registry.json").read_text())
    queue = [item for item in registry if item["review_required"]]
    out = base / "output" / "review_queue.json"
    out.write_text(json.dumps(queue, ensure_ascii=False, indent=2))
    print(f"Built {out} with {len(queue)} pages")


if __name__ == "__main__":
    main()
