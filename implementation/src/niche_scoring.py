from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import List
import json
from pathlib import Path


@dataclass
class NicheCandidate:
    name: str
    demand: int
    monetization: int
    freshness: int
    data_availability: int
    serp_weakness: int
    trust_barrier: int

    def score(self) -> float:
        return (
            self.demand * 0.25
            + self.monetization * 0.25
            + self.freshness * 0.15
            + self.data_availability * 0.15
            + self.serp_weakness * 0.15
            + (10 - self.trust_barrier) * 0.05
        )


def default_candidates() -> List[NicheCandidate]:
    return [
        NicheCandidate("AI tools for lawyers", 7, 8, 6, 7, 6, 6),
        NicheCandidate("AI tools for real estate agents", 8, 8, 7, 7, 6, 5),
        NicheCandidate("VPNs for remote workers", 8, 9, 5, 6, 4, 7),
        NicheCandidate("Appointment software for clinics", 7, 9, 7, 7, 5, 7),
        NicheCandidate("Email tools for creators", 7, 8, 6, 8, 6, 5),
        NicheCandidate("AI note takers for sales teams", 8, 8, 7, 8, 6, 5),
        NicheCandidate("Proposal software for freelancers", 6, 8, 5, 7, 7, 4),
        NicheCandidate("Password managers for families", 7, 8, 4, 6, 5, 7),
        NicheCandidate("CRM tools for small service businesses", 8, 9, 7, 8, 5, 6),
        NicheCandidate("Website chatbots for local businesses", 7, 8, 7, 7, 6, 5),
    ]


def rank_candidates(candidates: List[NicheCandidate]) -> list[dict]:
    ranked = sorted(candidates, key=lambda item: item.score(), reverse=True)
    return [{**asdict(item), "score": round(item.score(), 2)} for item in ranked]


def main() -> None:
    output_dir = Path(__file__).resolve().parents[1] / "output"
    output_dir.mkdir(parents=True, exist_ok=True)
    ranked = rank_candidates(default_candidates())
    out = output_dir / "niche_scores.json"
    out.write_text(json.dumps(ranked, ensure_ascii=False, indent=2))
    for row in ranked:
        print(f"{row['score']:>4}  {row['name']}")
    print(f"\nSaved to {out}")


if __name__ == "__main__":
    main()
