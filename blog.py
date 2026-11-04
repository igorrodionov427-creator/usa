"""Blog for apolline.site: English articles from _src/blog/*.md → blog/<slug>/index.html + blog/index.html + 404.html.
Used by build.py. Markdown subset: ## / ### headings, paragraphs, - and 1. lists, | tables |, > quotes, **bold**, [links](url).
"""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BASE = 'https://apolline.site/'
OG_IMAGE = BASE + 'media/og.jpg'
TELEGRAM, BOT, WHATSAPP, INSTAGRAM = ('https://t.me/apollineAG', 'https://t.me/ApollineAGbot?start=blog',
                                      'https://wa.me/79670450339', 'https://www.instagram.com/apollineag/')


def inline(t):
    t = html.escape(t, quote=False)
    t = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', t)
    def link(m):
        text, url = m.group(1), m.group(2)
        ext = url.startswith('http')
        return f'<a href="{html.escape(url)}"' + (' target="_blank" rel="noopener"' if ext else '') + f'>{text}</a>'
    return re.sub(r'\[([^\]]+)\]\(([^)]+)\)', link, t)


def md(text):
    out, lines, i = [], text.strip().split('\n'), 0
    while i < len(lines):
        ln = lines[i].rstrip()
        if not ln.strip():
            i += 1
            continue
        if ln.startswith('### '):
            out.append(f'<h3>{inline(ln[4:])}</h3>')
        elif ln.startswith('## '):
            hid = re.sub(r'[^a-z0-9]+', '-', ln[3:].lower()).strip('-')
            out.append(f'<h2 id="{hid}">{inline(ln[3:])}</h2>')
        elif ln.startswith('|'):
            rows = []
            while i < len(lines) and lines[i].startswith('|'):
                rows.append([c.strip() for c in lines[i].strip().strip('|').split('|')])
                i += 1
            head, body = rows[0], [r for r in rows[1:] if not set(''.join(r)) <= set('-: ')]
            out.append('<div class="tbl"><table><thead><tr>' + ''.join(f'<th>{inline(c)}</th>' for c in head) + '</tr></thead><tbody>'
                       + ''.join('<tr>' + ''.join(f'<td>{inline(c)}</td>' for c in r) + '</tr>' for r in body) + '</tbody></table></div>')
            continue
        elif ln.startswith('> '):
            q = []
            while i < len(lines) and lines[i].startswith('> '):
                q.append(lines[i][2:])
                i += 1
            out.append(f'<blockquote>{inline(" ".join(q))}</blockquote>')
            continue
        elif re.match(r'^(- |\d+\. )', ln):
            tag = 'ol' if ln[0].isdigit() else 'ul'
            items = []
            while i < len(lines) and re.match(r'^(- |\d+\. )', lines[i]):
                items.append(re.sub(r'^(- |\d+\. )', '', lines[i]))
                i += 1
            out.append(f'<{tag}>' + ''.join(f'<li>{inline(x)}</li>' for x in items) + f'</{tag}>')
            continue
        else:
            para = [ln]
            while i + 1 < len(lines) and lines[i + 1].strip() and not re.match(r'^(#|- |\d+\. |\||> )', lines[i + 1]):
                i += 1
                para.append(lines[i].rstrip())
            out.append(f'<p>{inline(" ".join(para))}</p>')
        i += 1
    return '\n'.join(out)


def load_posts():
    posts = []
    for f in sorted((ROOT / '_src' / 'blog').glob('*.md')):
        raw = f.read_text(encoding='utf-8')
        fm, body = re.match(r'^---\n(.*?)\n---\n(.*)$', raw, re.S).groups()
        meta = dict(line.split(': ', 1) for line in fm.split('\n') if ': ' in line)
        words = len(re.sub(r'[#|*\-\[\]()>]', ' ', body).split())
        posts.append({**meta, 'slug': f.stem, 'body': body, 'html': md(body), 'minutes': max(3, round(words / 220)),
                      'url': f'{BASE}blog/{f.stem}/', 'lead': re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', body.strip().split('\n\n')[0])})
    order = ['social-media-management-cost', 'pay-for-performance-marketing', 'short-form-video-for-small-business',
             'outsource-social-media-vs-in-house', 'social-media-content-calendar', 'chatbot-for-small-business',
             'cold-outreach-small-business', 'marketplace-listing-optimization']
    return sorted(posts, key=lambda p: order.index(p['slug']) if p['slug'] in order else 99)


CSS = """
:root{--bg:#000;--ink:#f4f4f4;--mute:#a9a9a9;--grey:#6f6f6f;--hair:rgba(255,255,255,.14);--paper:#dadada;--ui:'Inter Tight',system-ui,sans-serif;--disp:'Archivo','Inter Tight',sans-serif}
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%;scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--ink);font:400 18px/1.7 var(--ui);-webkit-font-smoothing:antialiased}
a{color:inherit}
.wrap{width:min(760px,100% - 32px);margin:0 auto}.wide{width:min(1180px,100% - 32px);margin:0 auto}
.top{position:sticky;top:0;z-index:5;background:rgba(0,0,0,.82);backdrop-filter:blur(12px);border-bottom:1px solid var(--hair)}
.top .wide{display:flex;align-items:center;justify-content:space-between;gap:16px;height:64px}
.logo{display:flex;align-items:center;gap:10px;text-decoration:none;font:600 18px/1 var(--disp);font-stretch:125%;font-variation-settings:'wdth' 125}
.logo i{width:28px;height:28px;border-radius:8px;background:var(--ink);color:#000;display:grid;place-items:center;font:700 14px/1 var(--ui);font-style:normal}
.top nav{display:flex;gap:22px;align-items:center;font:500 14px/1 var(--ui)}
.top nav a{text-decoration:none;color:var(--mute)}.top nav a:hover,.top nav a.on{color:var(--ink)}
.btn{display:inline-flex;align-items:center;gap:8px;height:42px;padding:0 18px;border-radius:999px;background:var(--ink);color:#000!important;text-decoration:none;font:600 14px/1 var(--ui)}
@media(max-width:640px){.top nav .hide{display:none}}
.crumbs{font:500 13px/1.4 var(--ui);color:var(--grey);margin:42px 0 18px}.crumbs a{text-decoration:none}.crumbs a:hover{color:var(--ink)}
.meta{display:flex;gap:10px;flex-wrap:wrap;font:600 12px/1 var(--disp);font-stretch:125%;font-variation-settings:'wdth' 125;letter-spacing:.06em;text-transform:uppercase;color:var(--grey);margin-bottom:18px}
.meta span+span:before{content:'·';margin-right:10px}
h1{margin:0 0 26px;font:640 clamp(34px,5.4vw,58px)/1.02 var(--disp);font-stretch:104%;font-variation-settings:'wdth' 104;letter-spacing:-.04em}
article{padding-bottom:30px}
article h2{margin:54px 0 14px;font:640 clamp(24px,3vw,32px)/1.15 var(--disp);font-stretch:104%;font-variation-settings:'wdth' 104;letter-spacing:-.03em;scroll-margin-top:84px}
article h3{margin:34px 0 8px;font:600 21px/1.3 var(--ui)}
article p,article li{color:#dcdcdc}article p{margin:0 0 18px}
article ul,article ol{padding-left:22px;margin:0 0 20px}article li{margin-bottom:8px}
article strong{color:var(--ink)}
article a{color:var(--ink);text-decoration-color:rgba(255,255,255,.4);text-underline-offset:3px}
article a:hover{text-decoration-color:var(--ink)}
blockquote{margin:22px 0;padding:18px 22px;border-left:3px solid var(--ink);background:#111;border-radius:0 14px 14px 0;color:#dcdcdc;font-size:17px}
.tbl{overflow-x:auto;margin:22px 0 26px;border:1px solid var(--hair);border-radius:16px}
table{border-collapse:collapse;width:100%;font-size:15px;line-height:1.45}
th,td{text-align:left;padding:12px 14px;border-bottom:1px solid var(--hair);vertical-align:top}
th{font:600 12px/1.3 var(--disp);font-stretch:125%;font-variation-settings:'wdth' 125;letter-spacing:.05em;text-transform:uppercase;color:var(--mute);background:#0c0c0c}
tr:last-child td{border-bottom:0}
.lead{font-size:21px;line-height:1.55;color:var(--ink)}
.cta{margin:46px 0 10px;background:var(--paper);color:#111;border-radius:24px;padding:30px}
.cta h2{margin:0 0 8px;font:640 30px/1.05 var(--disp);font-stretch:104%;font-variation-settings:'wdth' 104;letter-spacing:-.03em;color:#111}
.cta p{color:#333;margin:0 0 18px;font-size:16px}
.cta .row{display:flex;gap:10px;flex-wrap:wrap}
.cta a{display:inline-flex;align-items:center;height:44px;padding:0 18px;border-radius:999px;background:#111;color:#f4f4f4;text-decoration:none;font:600 14px/1 var(--ui)}
.cta a.l{background:#fff;color:#111}
.related{border-top:1px solid var(--hair);margin-top:50px;padding:40px 0 10px}
.related h2,.list-h{font:600 12px/1 var(--disp);font-stretch:125%;font-variation-settings:'wdth' 125;letter-spacing:.06em;text-transform:uppercase;color:var(--grey);margin:0 0 18px}
.cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:14px}
.card{display:flex;flex-direction:column;gap:10px;padding:22px;border:1px solid var(--hair);border-radius:20px;text-decoration:none;transition:border-color .3s,background .3s;min-height:200px}
.card:hover{border-color:rgba(255,255,255,.4);background:#0b0b0b}
.card .t{font:600 20px/1.25 var(--ui);color:var(--ink)}
.card .d{font-size:15px;line-height:1.5;color:var(--mute);flex:1}
.card .m{font:600 11px/1 var(--disp);font-stretch:125%;font-variation-settings:'wdth' 125;letter-spacing:.06em;text-transform:uppercase;color:var(--grey)}
.hero-b{padding:70px 0 40px}.hero-b p{font-size:20px;color:var(--mute);max-width:640px;margin:0}
footer{border-top:1px solid var(--hair);margin-top:60px;padding:30px 0 50px;font:500 14px/1.6 var(--ui);color:var(--grey)}
footer .wide{display:flex;justify-content:space-between;gap:20px;flex-wrap:wrap}footer a{text-decoration:none}footer a:hover{color:var(--ink)}
footer nav{display:flex;gap:18px;flex-wrap:wrap}
"""


def page(title, desc, canonical, body, ld, og_type='article', robots=None):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
{f'<meta name="robots" content="{robots}">' if robots else ''}
<link rel="canonical" href="{canonical}">
<link rel="icon" href="/favicon.ico" sizes="48x48"><link rel="icon" href="/favicon.svg" type="image/svg+xml"><link rel="apple-touch-icon" href="/apple-touch-icon.png">
<meta property="og:type" content="{og_type}"><meta property="og:site_name" content="Apolline"><meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}"><meta property="og:url" content="{canonical}"><meta property="og:image" content="{OG_IMAGE}">
<meta property="og:locale" content="en_US"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{html.escape(title)}">
<meta name="twitter:description" content="{html.escape(desc)}"><meta name="twitter:image" content="{OG_IMAGE}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@400..700&family=Archivo:wdth,wght@100..125,500..800&display=swap" rel="stylesheet">
<style>{CSS}</style>
{f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>' if ld else ''}
</head>
<body>
<header class="top"><div class="wide"><a class="logo" href="/"><i>A</i>APOLLINE</a>
<nav><a class="hide" href="/#services">Services</a><a class="hide" href="/#pay">Pay for results</a><a href="/blog/"{' class="on"' if '/blog/' in canonical else ''}>Blog</a><a class="btn" href="/#contact">Message us ↗</a></nav></div></header>
{body}
<footer><div class="wide"><span>© 2026 Apolline · social media, video, ads, outreach, bots and websites for small businesses</span>
<nav><a href="/">Home</a><a href="/#services">Services</a><a href="/blog/">Blog</a><a href="{TELEGRAM}" target="_blank" rel="noopener">Telegram</a><a href="{WHATSAPP}" target="_blank" rel="noopener">WhatsApp</a><a href="{INSTAGRAM}" target="_blank" rel="noopener">Instagram</a></nav></div></footer>
</body>
</html>
"""


def card(p):
    return (f'<a class="card" href="/blog/{p["slug"]}/"><span class="m">{html.escape(p["tag"])} · {p["minutes"]} min read</span>'
            f'<span class="t">{html.escape(p["h1"])}</span><span class="d">{html.escape(p["description"])}</span></a>')


CTA = f"""<section class="cta"><h2>Hand this task to us.</h2>
<p>Social media, video, ads, outreach, bots and websites — one team instead of five contractors. For suitable projects we work for a percentage of sales: no orders, no fee.</p>
<div class="row"><a href="{TELEGRAM}" target="_blank" rel="noopener">Telegram @apollineAG</a><a class="l" href="{WHATSAPP}" target="_blank" rel="noopener">WhatsApp</a><a class="l" href="{BOT}" target="_blank" rel="noopener">Request bot</a></div></section>"""

ORG = {'@type': 'Organization', '@id': BASE + '#org', 'name': 'Apolline', 'url': BASE, 'logo': BASE + 'apple-touch-icon.png'}


def build_blog():
    posts = load_posts()
    out = ROOT / 'blog'
    out.mkdir(exist_ok=True)
    for p in posts:
        others = [x for x in posts if x['slug'] != p['slug']][:3]
        body = f"""<main class="wrap"><div class="crumbs"><a href="/">Home</a> / <a href="/blog/">Blog</a></div>
<article><div class="meta"><span>{html.escape(p['tag'])}</span><span>{p['minutes']} min read</span><span><time datetime="{p['date']}">{p['date']}</time></span></div>
<h1>{html.escape(p['h1'])}</h1>
{p['html'].replace('<p>', '<p class="lead">', 1)}
{CTA}
</article></main>
<section class="related wide"><h2>Keep reading</h2><div class="cards">{''.join(card(x) for x in others)}</div></section>"""
        ld = {'@context': 'https://schema.org', '@graph': [
            {'@type': 'BlogPosting', '@id': p['url'] + '#post', 'headline': p['h1'][:110], 'name': p['title'], 'description': p['description'],
             'datePublished': p['date'], 'dateModified': p['date'], 'inLanguage': 'en-US', 'mainEntityOfPage': p['url'], 'url': p['url'],
             'image': OG_IMAGE, 'wordCount': len(p['body'].split()), 'articleSection': p['tag'], 'author': ORG, 'publisher': ORG},
            {'@type': 'BreadcrumbList', 'itemListElement': [
                {'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': BASE},
                {'@type': 'ListItem', 'position': 2, 'name': 'Blog', 'item': BASE + 'blog/'},
                {'@type': 'ListItem', 'position': 3, 'name': p['h1'], 'item': p['url']}]}]}
        d = out / p['slug']
        d.mkdir(exist_ok=True)
        (d / 'index.html').write_text(page(p['title'] + ' | Apolline', p['description'], p['url'], body, ld), encoding='utf-8')
        print('built', f'blog/{p["slug"]}/index.html')

    body = f"""<main class="wide"><section class="hero-b"><div class="crumbs" style="margin-top:0"><a href="/">Home</a> / Blog</div>
<h1>Guides for small businesses.</h1><p>Practical, no-fluff guides on social media, short-form video, chatbots, outreach, marketplaces and paying for marketing results — from the Apolline team.</p></section>
<div class="cards">{''.join(card(p) for p in posts)}</div>
{CTA.replace('class="cta"', 'class="cta" style="margin-top:60px"')}</main>"""
    ld = {'@context': 'https://schema.org', '@graph': [
        {'@type': 'Blog', '@id': BASE + 'blog/#blog', 'name': 'Apolline Blog', 'url': BASE + 'blog/', 'inLanguage': 'en-US', 'publisher': ORG,
         'blogPost': [{'@type': 'BlogPosting', 'headline': p['h1'], 'url': p['url'], 'datePublished': p['date']} for p in posts]},
        {'@type': 'BreadcrumbList', 'itemListElement': [{'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': BASE},
                                                        {'@type': 'ListItem', 'position': 2, 'name': 'Blog', 'item': BASE + 'blog/'}]}]}
    (out / 'index.html').write_text(page('Blog — Social Media & Marketing Guides for Small Business | Apolline',
                                         'Practical guides for small businesses: social media pricing, short-form video, chatbots, cold outreach, marketplaces and pay-for-performance marketing.',
                                         BASE + 'blog/', body, ld, og_type='website'), encoding='utf-8')
    print('built blog/index.html')

    body = f"""<main class="wrap" style="padding:90px 0 40px"><div class="meta"><span>Error 404</span></div><h1>This page doesn't exist.</h1>
<p style="color:var(--mute)">The link may be old or mistyped. Try the homepage or one of our guides.</p>
<p style="margin-top:26px"><a class="btn" href="/">Go to homepage</a></p>
<section class="related" style="border:0;padding-top:30px"><h2>Popular guides</h2><div class="cards">{''.join(card(p) for p in posts[:3])}</div></section></main>"""
    (ROOT / '404.html').write_text(page('Page not found | Apolline', 'This page does not exist.', BASE, body, None, og_type='website', robots='noindex'), encoding='utf-8')
    print('built 404.html')
    return posts
