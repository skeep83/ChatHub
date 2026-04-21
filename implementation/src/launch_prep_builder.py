from __future__ import annotations

import json
from pathlib import Path


def main() -> None:
    checklist = {
        "must_do_before_launch": [
            "pick domain",
            "replace example.com in site builders",
            "review top 5 commercial pages",
            "add at least one monetization destination",
            "configure nginx and static deploy",
            "verify site on public URL",
            "connect analytics",
        ],
        "nice_to_have": [
            "brand styling pass",
            "logo and simple design layer",
            "email capture flow",
            "search console submission",
        ],
    }
    out = Path(__file__).resolve().parents[1] / "output" / "launch_prep.json"
    out.write_text(json.dumps(checklist, ensure_ascii=False, indent=2))
    print(f"Built {out}")


if __name__ == "__main__":
    main()
