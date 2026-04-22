from __future__ import annotations

import json
from pathlib import Path


def frontmatter(page: dict) -> str:
    lines = [
        '---',
        f'title: "{page["title"]}"',
        f'slug: "{page["slug"]}"',
        f'page_type: "{page["page_type"]}"',
        f'page_subtype: "{page.get("page_subtype", "general")}"',
        f'primary_keyword: "{page["primary_keyword"]}"',
        f'search_intent: "{page["search_intent"]}"',
        f'audience: "{page["audience"]}"',
        f'monetization_type: "{page["monetization_type"]}"',
        f'review_required: {str(page["review_required"]).lower()}',
        '---',
    ]
    return "\n".join(lines)


def best_of_sections(page: dict) -> list[str]:
    keyword = page['primary_keyword']
    audience = page['audience']
    subtype = page.get('page_subtype', 'crm')
    overview = f"The best choice for {keyword} should help {audience} make a shortlist quickly, not trap them in thin affiliate filler. The real goal is to find the cam site that best matches browsing style, private-show intent, and spending comfort."
    how_to_choose = 'Start by deciding whether you want mainstream room discovery, premium private-chat polish, mobile-friendly browsing, or more anonymous entry points. Then cut any site that serves a very different experience.'
    final_recommendation = 'The best option should be the one that feels easiest to use and closest to your actual chat intent, not just the one with the biggest name.'
    if subtype == 'fsm':
        overview = 'The best field service management stack for a small business should reduce quoting, scheduling, dispatch, invoicing, and communication friction without pushing the team into enterprise-style overhead.'
        how_to_choose = 'Start with field workflow first. If dispatch, scheduling, and technician coordination are core problems, prioritize FSM tools before broader CRM platforms.'
        final_recommendation = 'For most small teams, the best FSM choice is the one that keeps operations clear and adoptable, not the one with the deepest enterprise feature set.'
    elif subtype == 'invoicing':
        overview = 'The best invoicing software for a service business should help the team send invoices faster, get paid faster, and keep billing connected to estimates, jobs, and customer history.'
        how_to_choose = 'Decide whether invoicing is mainly part of field workflow or mainly part of accounting workflow. That choice should shape the shortlist.'
        final_recommendation = 'For most service businesses, the best invoicing setup is the one that reduces billing friction without disconnecting payments from the job workflow.'
    elif subtype == 'scheduling':
        overview = 'The best scheduling software for a service business should reduce missed appointments, simplify crew coordination, and make booking easier without creating admin sprawl.'
        how_to_choose = 'Prioritize scheduling clarity, dispatch ease, and communication flow before broader CRM extras.'
        final_recommendation = 'The right scheduling tool should make the calendar more reliable and the team easier to manage, not just add more software layers.'
    return [
        f"# {page['title']}",
        '',
        page['problem_statement'],
        '',
        '## Overview',
        overview,
        '',
        '## Who this is for',
        f"This page is for {audience} who want a practical shortlist instead of a bloated feature dump.",
        '',
        '## Key considerations',
        'Look at workflow fit first, then ease of adoption, pricing posture, and whether the tool solves the main operational bottleneck without adding unnecessary complexity.',
        '',
        '## Top picks',
        'The strongest shortlist should separate the safest all-round choice from the stronger second option and from heavier tools that only make sense in more complex environments.',
        '',
        '## Comparison table',
        'The comparison table should make it obvious which tool is best for simplicity, workflow depth, growth stage, and operational fit.',
        '',
        '## How to choose',
        how_to_choose,
        '',
        '## Final recommendation',
        final_recommendation,
        '',
        '## Call to action',
        page['call_to_action'],
        '',
    ]


def comparison_sections(page: dict) -> list[str]:
    keyword = page['primary_keyword']
    subtype = page.get('page_subtype', 'peer_fsm')
    overview = f"{keyword.title()} is not about who has the longest feature list. It is about which cam site gives you the better mix of discovery, private-show quality, room energy, and overall value."
    quick_verdict = 'A strong comparison should tell you quickly which option is better for mainstream browsing, which feels more premium, and whether either one is mismatched to the kind of session you actually want.'
    if subtype == 'simple_vs_complex':
        overview = f"{keyword.title()} is usually a decision between easier browsing and a more premium private-chat feel. Most users should treat this as an experience-fit test, not a feature-count contest."
        quick_verdict = 'The winning choice usually comes down to whether you want easier discovery now or a more premium room and payout feel.'
    elif subtype == 'crm_vs_fsm':
        overview = f"{keyword.title()} is often a comparison between broader discovery and a more private-session-focused path. These are not identical experiences, so the right choice depends on what you want to happen after the click."
        quick_verdict = 'The fastest good decision is figuring out whether your bigger priority is room variety or a more premium private-session feel.'
    return [
        f"# {page['title']}",
        '',
        page['problem_statement'],
        '',
        '## Overview',
        overview,
        '',
        '## Who this is for',
        f"This page is for {page['audience']} who want a fast answer on which site belongs on the shortlist and which one probably does not.",
        '',
        '## Key considerations',
        'The comparison should focus on room discovery, private-show feel, performer mix, pricing pressure, and how each site behaves once you move beyond casual browsing.',
        '',
        '## Quick verdict',
        quick_verdict,
        '',
        '## Feature comparison',
        'The feature comparison should focus on the actual browsing and chat experience, not generic checklist padding.',
        '',
        '## Pricing',
        'Pricing should be judged by token spend, premium feel, and how quickly each site pushes you toward paid interaction.',
        '',
        '## Best fit by scenario',
        'Different products win when the business priorities change, so the page should make those scenario boundaries obvious.',
        '',
        '## Call to action',
        page['call_to_action'],
        '',
    ]


def use_case_sections(page: dict) -> list[str]:
    keyword = page['primary_keyword']
    return [
        f"# {page['title']}",
        '',
        page['problem_statement'],
        '',
        '## Overview',
        f"The best answer for {keyword} depends on the trade workflow, not just generic CRM features. The right software should reduce admin drag and support the way this business type actually books, schedules, follows up, and gets paid.",
        '',
        '## Who this is for',
        f"This page is for {page['audience']} who need software that fits the realities of their trade instead of a vague all-purpose tool.",
        '',
        '## Key considerations',
        'The most important factors are quoting, scheduling, follow-up, invoicing, repeat work, and how easy the system is for a small team to adopt consistently.',
        '',
        '## Why this niche needs a CRM',
        'This trade-specific page should explain the workflow pressure points that make dedicated software useful instead of treating every service business as identical.',
        '',
        '## Top options',
        'The shortlist should prioritize tools that fit the trade-specific workflow first and only then consider broader CRM flexibility.',
        '',
        '## Implementation tips',
        'The best tool still fails if setup is messy, so implementation guidance should stay practical and adoption-focused.',
        '',
        '## Recommendation',
        'The best choice should be the one that matches how the crew already works while reducing missed follow-up and admin friction.',
        '',
        '## Call to action',
        page['call_to_action'],
        '',
    ]


def alternatives_sections(page: dict) -> list[str]:
    keyword = page['primary_keyword']
    subtype = page.get('page_subtype', 'workflow_pain')
    overview = f"People searching {keyword} are usually not asking for random substitutions. They want to know which replacement fits better if the original tool feels too expensive, too heavy, or just mismatched to the workflow."
    why_alt = 'Most buyers switch when they hit pricing pressure, missing workflow depth, or a mismatch between the software and the way the team actually operates day to day.'
    if subtype == 'pricing_pain':
        overview = f"People searching {keyword} are usually trying to escape cost pressure without breaking the rest of their workflow. The best alternative is not just cheaper. It has to stay operationally usable."
        why_alt = 'Pricing-driven switching usually happens when the tool still works, but the economics no longer feel justified for the team size or revenue stage.'
    return [
        f"# {page['title']}",
        '',
        page['problem_statement'],
        '',
        '## Overview',
        overview,
        '',
        '## Why people look for alternatives',
        why_alt,
        '',
        '## Best alternatives to consider',
        'The shortlist should separate lighter, simpler options from broader or more operationally complex platforms.',
        '',
        '## How to compare alternatives',
        'Compare alternatives by what problem they solve better, not by counting features in a vacuum.',
        '',
        '## Final recommendation',
        'The best alternative is the one that fixes the current pain point without adding a worse one elsewhere in the workflow.',
        '',
        '## Call to action',
        page['call_to_action'],
        '',
    ]


def default_sections(page: dict) -> list[str]:
    sections = [f"# {page['title']}", '', page['problem_statement'], '']
    for item in page['outline']:
        sections.append(f'## {item}')
        sections.append(f'Draft notes for: {item}.')
        sections.append('')
    sections.append('## Call to action')
    sections.append(page['call_to_action'])
    sections.append('')
    return sections


def body(page: dict) -> str:
    page_type = page['page_type']
    if page_type == 'best_of':
        return '\n'.join(best_of_sections(page))
    if page_type == 'comparison':
        return '\n'.join(comparison_sections(page))
    if page_type == 'use_case':
        return '\n'.join(use_case_sections(page))
    if page_type == 'alternatives':
        return '\n'.join(alternatives_sections(page))
    return '\n'.join(default_sections(page))


def main() -> None:
    base = Path(__file__).resolve().parents[1]
    planned = json.loads((base / 'output' / 'planned_pages.json').read_text())
    out_dir = base / 'output' / 'content'
    out_dir.mkdir(parents=True, exist_ok=True)
    for page in planned:
        content = frontmatter(page) + '\n\n' + body(page)
        (out_dir / f"{page['slug']}.md").write_text(content)
    print(f'Generated {len(planned)} markdown files in {out_dir}')


if __name__ == '__main__':
    main()
