from __future__ import annotations

from pathlib import Path

REPLACEMENTS = {
    'Draft notes for: Overview.': 'This page is designed to help users compare adult video chat options without wasting time on generic hype pages.',
    'Draft notes for: Top picks.': 'The strongest shortlist should separate broad discovery platforms from premium private-chat options instead of pretending every site solves the same need.',
    'Draft notes for: Comparison table.': 'The practical comparison should make it obvious which platform is better for mainstream browsing, premium private-chat intent, and safer all-round fit.',
    'Draft notes for: How to choose.': 'Choose based on whether you want broad discovery, premium private chat, or the strongest all-round fit without overpaying for the wrong experience.',
    'Draft notes for: Final recommendation.': 'The best option should match the user intent of the session, not just the biggest brand name.',
    'Draft notes for: Quick verdict.': 'The goal is to narrow the shortlist fast and show what kind of user each platform actually fits.',
    'Draft notes for: Feature comparison.': 'The comparison should focus on private chat quality, browsing style, mainstream reach, and how strong the premium experience feels.',
    'Draft notes for: Pricing.': 'Pricing should be judged by the kind of experience the user wants, not just the headline spending model.',
    'Draft notes for: Best fit by scenario.': 'Different cam platforms win for different user intent, so the page should make those boundaries obvious.',
    'Draft notes for: Why people look for alternatives.': 'Users usually look for alternatives when the experience feels too mainstream, too weak on private chat, or just mismatched to what they actually want.',
    'Draft notes for: Best alternatives.': 'The strongest alternatives should be grouped by mainstream discovery fit, premium private-chat fit, and overall shortlist safety.',
    'Draft notes for: How to switch.': 'Switching only makes sense if the next platform clearly fits the user intent better than the current one.',
    'Draft notes for: Why this niche needs a CRM.': 'This page should explain why a specific adult video chat intent or sub-niche changes which platforms actually fit best.',
    'Draft notes for: Top options.': 'The shortlist should prioritize the platforms that best match the page-specific intent instead of repeating generic rankings.',
    'Draft notes for: Implementation tips.': 'Keep the guidance practical and focused on choosing the right kind of experience rather than overexplaining platform basics.',
    'Draft notes for: Recommendation.': 'The recommendation should be clear about which platform category fits the page intent best.',
}


def main() -> None:
    content_dir = Path(__file__).resolve().parents[1] / 'output' / 'content'
    updated = 0
    for file in content_dir.glob('*.md'):
        text = file.read_text()
        before = text
        for old, new in REPLACEMENTS.items():
            text = text.replace(old, new)
        if text != before:
            file.write_text(text)
            updated += 1
    print(f'Refined {updated} content files')


if __name__ == '__main__':
    main()
