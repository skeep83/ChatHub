from __future__ import annotations

import json
from pathlib import Path


def relevant_products(page: dict, products: list[dict]) -> list[dict]:
    page_type = page.get('page_type', 'general')
    subtype = page.get('page_subtype', 'general')
    default = ['Stripchat', 'Chaturbate', 'LiveJasmin', 'Flirt4Free']
    if page_type == 'best_of' and subtype == 'invoicing':
        order = ['Stripchat', 'LiveJasmin', 'Chaturbate', 'Flirt4Free']
    elif page_type == 'comparison' and subtype == 'crm_vs_fsm':
        order = ['Stripchat', 'Chaturbate', 'LiveJasmin', 'Flirt4Free']
    elif page_type == 'comparison' and subtype == 'simple_vs_complex':
        order = ['Chaturbate', 'LiveJasmin', 'Stripchat', 'Flirt4Free']
    elif page_type == 'alternatives' and subtype == 'workflow_pain':
        order = ['Stripchat', 'LiveJasmin', 'Chaturbate', 'Flirt4Free']
    else:
        order = default
    by_name = {product['name']: product for product in products}
    return [by_name[name] for name in order if name in by_name]


def best_for_text(product: dict, page_type: str, subtype: str) -> str:
    if page_type == 'best_of' and subtype == 'fsm':
        mapping = {
            'Jobber': 'small field-service teams that want the safest all-round operating fit',
            'Housecall Pro': 'growing service teams that need stronger communication and dispatch coordination',
            'ServiceTitan': 'larger service operations with much heavier workflow depth',
            'HubSpot': 'businesses where pipeline and marketing matter more than field execution',
        }
        return mapping.get(product['name'], ', '.join(product['best_for']))
    if page_type == 'best_of' and subtype == 'invoicing':
        mapping = {
            'Jobber': 'service businesses that want invoicing tied directly to jobs and estimates',
            'Housecall Pro': 'teams that need payments and customer communication tightly connected to field workflow',
            'ServiceTitan': 'larger operations with heavier billing and operational complexity',
            'HubSpot': 'teams where revenue pipeline matters more than invoicing workflow itself',
        }
        return mapping.get(product['name'], ', '.join(product['best_for']))
    if page_type == 'comparison' and subtype == 'crm_vs_fsm':
        mapping = {
            'Jobber': 'teams whose bottleneck is field execution, scheduling, and invoicing',
            'HubSpot': 'teams whose bottleneck is lead management and pipeline automation',
            'Housecall Pro': 'buyers who still want a field-service-first comparison benchmark',
            'ServiceTitan': 'operations already large enough to justify much heavier control',
        }
        return mapping.get(product['name'], ', '.join(product['best_for']))
    return ', '.join(product['best_for'])


def strengths_text(product: dict, page_type: str, subtype: str) -> str:
    if page_type == 'comparison' and subtype == 'simple_vs_complex':
        mapping = {
            'Jobber': 'cleaner adoption, faster setup, simpler day-to-day execution',
            'ServiceTitan': 'deep workflow control, reporting, enterprise-style process depth',
            'Housecall Pro': 'middle-ground dispatch, payments, and communication flow',
            'HubSpot': 'CRM pipeline visibility, automation, broader marketing flexibility',
        }
        return mapping.get(product['name'], ', '.join(product['strengths']))
    if page_type == 'alternatives' and subtype == 'workflow_pain':
        mapping = {
            'Housecall Pro': 'stronger communication, dispatch flow, and customer interaction workflow',
            'Jobber': 'simple operations coverage with lighter adoption burden',
            'ServiceTitan': 'deeper process control for teams that have outgrown lighter tools',
            'HubSpot': 'pipeline automation and broader CRM flexibility outside field execution',
        }
        return mapping.get(product['name'], ', '.join(product['strengths']))
    return ', '.join(product['strengths'])


def weaknesses_text(product: dict, page_type: str, subtype: str) -> str:
    if page_type == 'best_of' and subtype == 'fsm':
        mapping = {
            'Jobber': 'can feel limiting if the team later needs heavier operational depth',
            'Housecall Pro': 'can feel like more system than a very small team wants',
            'ServiceTitan': 'too much complexity for many small operators',
            'HubSpot': 'not built around technician-first workflow',
        }
        return mapping.get(product['name'], ', '.join(product['weaknesses']))
    if page_type == 'best_of' and subtype == 'invoicing':
        mapping = {
            'Jobber': 'less appealing if accounting is the main problem instead of job-linked billing',
            'Housecall Pro': 'may be more field-workflow-heavy than finance-first buyers want',
            'ServiceTitan': 'overkill for most small-business invoicing needs',
            'HubSpot': 'weak fit if billing execution matters more than sales pipeline',
        }
        return mapping.get(product['name'], ', '.join(product['weaknesses']))
    return ', '.join(product['weaknesses'])


def pricing_text(product: dict, page_type: str, subtype: str) -> str:
    if page_type == 'comparison' and subtype == 'simple_vs_complex' and product['name'] == 'ServiceTitan':
        return 'custom pricing, usually only worth it when the complexity budget is already justified'
    return product['pricing_note']


def enrich_markdown(page: dict, products: list[dict]) -> str:
    chosen = relevant_products(page, products)
    page_type = page.get('page_type', 'general')
    subtype = page.get('page_subtype', 'general')
    lines = []
    lines.append('## Recommended products')
    for product in chosen:
        lines.append(f"### {product['name']}")
        lines.append(f"- Best for: {best_for_text(product, page_type, subtype)}")
        lines.append(f"- Strengths: {strengths_text(product, page_type, subtype)}")
        lines.append(f"- Weaknesses: {weaknesses_text(product, page_type, subtype)}")
        lines.append(f"- Pricing note: {pricing_text(product, page_type, subtype)}")
        lines.append(f"- Source: {product['source_url']}")
        lines.append('')
    lines.append('## Editor note')
    lines.append('This page should be reviewed before publication, especially if it carries affiliate links or product claims.')
    lines.append('')
    return '\n'.join(lines)


def main() -> None:
    base = Path(__file__).resolve().parents[1]
    pages = json.loads((base / 'output' / 'planned_pages.json').read_text())
    products = json.loads((base / 'data' / 'products_adult_video_chat.json').read_text())
    content_dir = base / 'output' / 'content'
    for page in pages:
        target = content_dir / f"{page['slug']}.md"
        text = target.read_text()
        block = enrich_markdown(page, products)
        if '## Recommended products' in text:
            text = text.split('## Recommended products')[0].rstrip() + '\n\n' + block
        else:
            text += '\n' + block
        target.write_text(text)
    print(f'Enriched {len(pages)} content files')


if __name__ == '__main__':
    main()
