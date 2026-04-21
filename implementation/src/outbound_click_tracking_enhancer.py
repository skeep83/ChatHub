from __future__ import annotations

from pathlib import Path

TRACKER = """
<script>
document.addEventListener('click', function (event) {
  const link = event.target.closest('a');
  if (!link) return;
  const href = link.getAttribute('href') || '';
  if (!href.startsWith('http')) return;
  if (typeof gtag === 'function') {
    gtag('event', 'affiliate_click', {
      link_url: href,
      link_text: (link.textContent || '').trim(),
      page_path: window.location.pathname
    });
  }
});
</script>
"""


def main() -> None:
    site_dir = Path(__file__).resolve().parents[1] / 'output' / 'site'
    updated = 0
    for file in site_dir.glob('*.html'):
        if file.name.startswith('fo-verify'):
            continue
        text = file.read_text()
        if 'affiliate_click' in text:
            continue
        text = text.replace('</body>', TRACKER + '\n</body>')
        file.write_text(text)
        updated += 1
    print(f'Added outbound click tracking to {updated} pages')


if __name__ == '__main__':
    main()
