from __future__ import annotations

import json
from pathlib import Path


def slugify(value: str) -> str:
    return (
        value.lower()
        .replace(' vs ', '-vs-')
        .replace(' ', '-')
        .replace('/', '-')
        .replace('?', '')
    )


def page_title(keyword: str, page_type: str) -> str:
    if page_type == 'best_of':
        return keyword.title() + ' in 2026'
    if page_type == 'comparison':
        return keyword.title() + ': Which Is Better?'
    if page_type == 'alternatives':
        return keyword.title().replace('Alternatives', 'Alternatives to Consider')
    return keyword.title()


def detect_subtype(keyword: str, page_type: str) -> str:
    k = keyword.lower()
    if page_type == 'best_of':
        if 'field service management' in k or 'dispatch' in k:
            return 'fsm'
        if 'invoicing' in k or 'invoice' in k or 'billing' in k:
            return 'invoicing'
        if 'scheduling' in k or 'appointment' in k or 'booking' in k:
            return 'scheduling'
        return 'crm'
    if page_type == 'comparison':
        if 'hubspot' in k:
            return 'crm_vs_fsm'
        if 'servicetitan' in k or 'service titan' in k:
            return 'simple_vs_complex'
        return 'peer_fsm'
    if page_type == 'alternatives':
        if 'pricing' in k or 'cheap' in k or 'affordable' in k:
            return 'pricing_pain'
        return 'workflow_pain'
    if page_type == 'use_case':
        return 'trade_specific'
    return 'general'


def make_outline(page_type: str) -> list[str]:
    common = ['Overview', 'Who this is for', 'Key considerations']
    variants = {
        'best_of': ['Top picks', 'Comparison table', 'How to choose', 'Final recommendation'],
        'comparison': ['Quick verdict', 'Feature comparison', 'Pricing', 'Best fit by scenario'],
        'use_case': ['Why this niche needs a CRM', 'Top options', 'Implementation tips', 'Recommendation'],
        'alternatives': ['Why people look for alternatives', 'Best alternatives', 'How to switch'],
        'faq': ['Short answer', 'Detailed explanation', 'Common questions'],
    }
    return common + variants.get(page_type, ['Recommendation'])


def default_cta(page_type: str, subtype: str) -> str:
    if page_type == 'best_of' and subtype == 'fsm':
        return 'Compare the strongest field-service-first tools first and eliminate heavier options that do not fit your current team size.'
    if page_type == 'best_of' and subtype == 'invoicing':
        return 'Compare the tools that keep invoicing connected to estimates, jobs, and payments before adding separate finance complexity.'
    if page_type == 'comparison' and subtype == 'simple_vs_complex':
        return 'Decide whether you need simpler adoption or deeper operational control before keeping both tools in the shortlist.'
    if page_type == 'comparison' and subtype == 'crm_vs_fsm':
        return 'Choose whether your main bottleneck is field execution or sales pipeline before treating both tools as direct substitutes.'
    if page_type == 'alternatives' and subtype == 'pricing_pain':
        return 'Focus on the alternatives that reduce cost without creating a worse workflow problem somewhere else.'
    if page_type == 'alternatives' and subtype == 'workflow_pain':
        return 'Focus on the alternatives that fix the operational mismatch without adding new complexity the team does not need.'
    return 'See the recommended tools and compare the best fit for your business.'


def main() -> None:
    base = Path(__file__).resolve().parents[1]
    seeds = json.loads((base / 'data' / 'topic_seed_adult_video_chat.json').read_text())
    pages = []
    for item in seeds:
        subtype = detect_subtype(item['keyword'], item['page_type'])
        pages.append(
            {
                'slug': slugify(item['keyword']),
                'title': page_title(item['keyword'], item['page_type']),
                'page_type': item['page_type'],
                'page_subtype': subtype,
                'primary_keyword': item['keyword'],
                'search_intent': item['intent'],
                'audience': item['audience'],
                'problem_statement': f"Users searching for '{item['keyword']}' need a fast, trustworthy answer with actionable recommendations.",
                'recommended_products': [],
                'source_urls': [],
                'outline': make_outline(item['page_type']),
                'faq': [],
                'call_to_action': default_cta(item['page_type'], subtype),
                'monetization_type': 'affiliate',
                'review_required': item['intent'] == 'commercial',
            }
        )
    out = base / 'output' / 'planned_pages.json'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(pages, ensure_ascii=False, indent=2))
    print(f'Planned {len(pages)} pages -> {out}')


if __name__ == '__main__':
    main()
