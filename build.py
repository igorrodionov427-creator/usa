"""Build the static site: one fully translated page per language.

    python build.py

Reads _src/index.html (English source) and the dictionary in i18n.js, then writes
index.html (English) plus ru/ de/ fr/ es/ it/ pl/ sr/ pages, sitemap.xml, robots.txt and llms.txt.
Needs beautifulsoup4.
"""
import html
import json
import re
from pathlib import Path

from bs4 import BeautifulSoup, Comment, NavigableString

ROOT = Path(__file__).resolve().parent
BASE = 'https://apolline.site/'
OG_IMAGE = BASE + 'media/og.jpg'
LOCALES = {'en': 'en_US', 'ru': 'ru_RU', 'de': 'de_DE', 'fr': 'fr_FR', 'es': 'es_ES', 'it': 'it_IT', 'pl': 'pl_PL', 'sr': 'sr_RS'}
TELEGRAM = 'https://t.me/apollineAG'
BOT = 'https://t.me/ApollineAGbot'
WHATSAPP = 'https://wa.me/79670450339'
SOCIAL = [TELEGRAM, 'https://www.instagram.com/apollineag/']


def load_dict():
    js = (ROOT / 'i18n.js').read_text(encoding='utf-8')
    langs = json.loads(re.search(r'window\.LANGS = (\[.*?\]);', js).group(1).replace("'", '"'))
    body = re.search(r'window\.I18N_ROWS = \[\n(.*?)\n\];', js, re.S).group(1)
    rows = [json.loads(line.strip().rstrip(',')) for line in body.split('\n') if line.strip().startswith('[')]
    return langs, rows


def page_url(lang):
    return BASE if lang == 'en' else f'{BASE}{lang}/'


def norm(text):
    return re.sub(r'\s+', ' ', text).strip()


def build(lang, langs, rows, src):
    col = langs.index(lang)
    tr = {r[0]: r[col] for r in rows}
    t = lambda s: tr.get(s, s)
    soup = BeautifulSoup(src, 'html.parser')
    soup.html['lang'] = lang

    # visible text
    for node in list(soup.body.descendants):
        if not isinstance(node, NavigableString) or isinstance(node, Comment):
            continue
        if node.find_parent(['script', 'style', 'svg']):
            continue
        key = norm(str(node))
        if key in tr and tr[key] != key:
            lead, trail = re.match(r'^(\s*)[\s\S]*?(\s*)$', str(node)).groups()
            node.replace_with(NavigableString(lead + tr[key] + trail))
    for img in soup.find_all('img', alt=True):
        img['alt'] = t(img['alt'])

    title = t(norm(soup.title.string))
    soup.title.string = title
    desc_tag = soup.find('meta', attrs={'name': 'description'})
    desc = t(desc_tag['content'])
    desc_tag['content'] = desc

    # sub-pages live one folder down
    if lang != 'en':
        for tag in soup.find_all(src=True):
            if not re.match(r'^(https?:|data:|/|#|\.\./)', tag['src']):
                tag['src'] = '../' + tag['src']
        for tag in soup.find_all('a', href=True):
            if not re.match(r'^(https?:|mailto:|tel:|data:|/|#|\.\./)', tag['href']):
                tag['href'] = '../' + tag['href']

    # head: canonical, hreflang, social cards, structured data
    head = soup.head
    def add(name, attrs=None, **kw):
        head.append(soup.new_tag(name, attrs={**(attrs or {}), **kw}))
        head.append('\n')
    head.append('\n')
    add('link', rel='canonical', href=page_url(lang))
    for code in langs:
        add('link', rel='alternate', hreflang=code, href=page_url(code))
    add('link', rel='alternate', hreflang='x-default', href=page_url('en'))
    for prop, val in [('og:type', 'website'), ('og:site_name', 'Apolline'), ('og:title', title), ('og:description', desc),
                      ('og:url', page_url(lang)), ('og:image', OG_IMAGE), ('og:image:width', '1200'), ('og:image:height', '630'),
                      ('og:locale', LOCALES[lang])]:
        add('meta', property=prop, content=val)
    for alt in langs:
        if alt != lang:
            add('meta', property='og:locale:alternate', content=LOCALES[alt])
    for name, val in [('twitter:card', 'summary_large_image'), ('twitter:title', title), ('twitter:description', desc), ('twitter:image', OG_IMAGE)]:
        add('meta', {'name': name, 'content': val})

    services = [{'@type': 'Offer', 'itemOffered': {'@type': 'Service', 'name': norm(sv.h3.get_text()),
                 'description': ', '.join(norm(li.get_text()) for li in sv.find_all('li'))}}
                for sv in soup.select('#svc .sv')]
    faq = [{'@type': 'Question', 'name': norm(qa.button.get_text()),
            'acceptedAnswer': {'@type': 'Answer', 'text': norm(qa.p.get_text())}} for qa in soup.select('#qas .qa')]
    graph = [
        {'@type': 'ProfessionalService', '@id': BASE + '#org', 'name': 'Apolline', 'url': page_url(lang), 'image': OG_IMAGE,
         'logo': BASE + 'media/og.jpg', 'description': desc, 'areaServed': 'Worldwide', 'sameAs': SOCIAL,
         'availableLanguage': [LOCALES[c].replace('_', '-') for c in langs],
         'hasOfferCatalog': {'@type': 'OfferCatalog', 'name': t('Services'), 'itemListElement': services}},
        {'@type': 'WebSite', '@id': BASE + '#site', 'name': 'Apolline', 'url': BASE, 'inLanguage': LOCALES[lang].replace('_', '-'),
         'publisher': {'@id': BASE + '#org'}},
        {'@type': 'FAQPage', 'inLanguage': LOCALES[lang].replace('_', '-'), 'mainEntity': faq},
    ]
    ld = soup.new_tag('script', attrs={'type': 'application/ld+json'})
    ld.string = json.dumps({'@context': 'https://schema.org', '@graph': graph}, ensure_ascii=False)
    head.append(ld)
    head.append('\n')

    out = ROOT / ('index.html' if lang == 'en' else f'{lang}/index.html')
    out.parent.mkdir(exist_ok=True)
    out.write_text(str(soup), encoding='utf-8')
    return out


def sitemap(langs):
    alts = ''.join(f'\n    <xhtml:link rel="alternate" hreflang="{c}" href="{page_url(c)}"/>' for c in langs)
    alts += f'\n    <xhtml:link rel="alternate" hreflang="x-default" href="{page_url("en")}"/>'
    urls = ''.join(f'\n  <url>\n    <loc>{page_url(c)}</loc>{alts}\n  </url>' for c in langs)
    (ROOT / 'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
                                      'xmlns:xhtml="http://www.w3.org/1999/xhtml">' + urls + '\n</urlset>\n', encoding='utf-8')


def llms(src):
    soup = BeautifulSoup(src, 'html.parser')
    lines = ['# Apolline', '', f'> {norm(soup.find("meta", attrs={"name": "description"})["content"])}', '',
             'Apolline is a marketing and automation team for small businesses: social media, video, ads, marketplaces, '
             'outreach, bots, websites, documents, copywriting, design and AI tools. Clients work with us by chat, call or video. '
             'We can work for a percentage of sales: the client pays only after an order from a customer we brought.', '',
             '## Pages', ''] + [f'- [{c.upper()}]({page_url(c)})' for c in LOCALES] + ['', '## Services', '']
    for sv in soup.select('#svc .sv'):
        lines.append(f'- **{norm(sv.h3.get_text())}**: ' + ', '.join(norm(li.get_text()) for li in sv.find_all('li')))
    lines += ['', '## FAQ', '']
    for qa in soup.select('#qas .qa'):
        lines += [f'### {norm(qa.button.get_text())}', '', norm(qa.p.get_text()), '']
    lines += ['## Contact', '', f'- Telegram: {TELEGRAM}', f'- Request bot: {BOT}', f'- WhatsApp: {WHATSAPP}', '- Instagram, X, TikTok: @apollineag', '']
    (ROOT / 'llms.txt').write_text('\n'.join(lines), encoding='utf-8')


if __name__ == '__main__':
    langs, rows = load_dict()
    src = (ROOT / '_src' / 'index.html').read_text(encoding='utf-8')
    for code in langs:
        print('built', build(code, langs, rows, src).relative_to(ROOT))
    sitemap(langs)
    (ROOT / 'robots.txt').write_text(f'User-agent: *\nAllow: /\nDisallow: /_src/\n\nSitemap: {BASE}sitemap.xml\n', encoding='utf-8')
    llms(src)
    print('built sitemap.xml, robots.txt, llms.txt')
