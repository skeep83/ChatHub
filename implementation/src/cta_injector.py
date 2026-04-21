from __future__ import annotations

from pathlib import Path
import json


def main() -> None:
    base = Path(__file__).resolve().parents[1]
    mapping = json.loads((base / "output" / "monetization_map.json").read_text())
    content_dir = base / "output" / "content"
    by_slug = {item['slug']: item for item in mapping}
    updated = 0
    for file in content_dir.glob("*.md"):
        slug = file.stem
        strategy = by_slug.get(slug)
        if not strategy:
            continue
        text = file.read_text()
        if "## Conversion path" in text:
            continue
        text += "\n## Conversion path\n"
        if strategy["primary_strategy"] == "affiliate":
            text += "Readers on this page should be guided toward a shortlist, comparison decision, and a natural affiliate click or product evaluation next step.\n"
        else:
            text += "Readers on this page should be guided toward an email capture, internal comparison page, or follow-up resource.\n"
        if strategy["secondary_strategy"] == "lead_form":
            text += "A lead form can be added later for consultation or software matching offers.\n"
        file.write_text(text)
        updated += 1
    print(f"Injected CTA blocks into {updated} files")


if __name__ == "__main__":
    main()
