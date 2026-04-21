from __future__ import annotations

import json
from pathlib import Path


def main() -> None:
    base = Path(__file__).resolve().parents[1]
    products = json.loads((base / "data" / "products_crm_small_service_businesses.json").read_text())
    out_dir = base / "output" / "product_fact_sheets"
    out_dir.mkdir(parents=True, exist_ok=True)
    for product in products:
        lines = [
            f"# {product['name']}",
            "",
            f"- Category: {product['category']}",
            f"- Best for: {', '.join(product['best_for'])}",
            f"- Strengths: {', '.join(product['strengths'])}",
            f"- Weaknesses: {', '.join(product['weaknesses'])}",
            f"- Pricing note: {product['pricing_note']}",
            f"- Source: {product['source_url']}",
            "",
        ]
        (out_dir / f"{product['name'].lower().replace(' ', '-')}.md").write_text("\n".join(lines))
    print(f"Built fact sheets in {out_dir}")


if __name__ == "__main__":
    main()
