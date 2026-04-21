from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import List


@dataclass
class ContentPage:
    slug: str
    title: str
    page_type: str
    primary_keyword: str
    search_intent: str
    audience: str
    problem_statement: str
    recommended_products: List[str] = field(default_factory=list)
    source_urls: List[str] = field(default_factory=list)
    outline: List[str] = field(default_factory=list)
    faq: List[str] = field(default_factory=list)
    call_to_action: str = ""
    monetization_type: str = "affiliate"
    review_required: bool = True

    def to_dict(self) -> dict:
        return asdict(self)
