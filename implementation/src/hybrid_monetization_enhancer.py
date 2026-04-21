from __future__ import annotations

from pathlib import Path


def inject_hybrid_blocks(text: str) -> str:
    if "## Get help choosing" not in text:
        text += "\n## Get help choosing\nIf you want help narrowing the shortlist for your business, use a simple lead form or contact flow here later.\n"
    if "## Affiliate disclosure" not in text:
        text += "\n## Affiliate disclosure\nSome links on this site may later become affiliate links. Recommendations should stay based on fit, not only payout.\n"
    return text


def main() -> None:
    content_dir = Path(__file__).resolve().parents[1] / "output" / "content"
    updated = 0
    for file in content_dir.glob("*.md"):
        text = file.read_text()
        if "## Get help choosing" in text and "## Affiliate disclosure" in text:
            continue
        file.write_text(inject_hybrid_blocks(text))
        updated += 1
    print(f"Enhanced {updated} files for hybrid monetization")


if __name__ == "__main__":
    main()
