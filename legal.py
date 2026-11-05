"""Legal pages for apolline.site: /privacy/, /terms/, /legal/ (English). Used by build.py.
Fill OPERATOR once the owner provides the details; empty fields are simply left out of the pages.
"""
import html
from pathlib import Path

import blog

ROOT = Path(__file__).resolve().parent
BASE = blog.BASE
UPDATED = '2026-11-05'
OPERATOR = {
    'name': '',        # legal name of the person or company running Apolline
    'address': '',     # postal address
    'email': 'apolline.agency@gmail.com',       # contact email for privacy requests
}
CONTACTS = [('Telegram', 'https://t.me/apollineAG', '@apollineAG'), ('Request bot', 'https://t.me/ApollineAGbot', '@ApollineAGbot'),
            ('WhatsApp', 'https://wa.me/79670450339', '+7 967 045-03-39'), ('Instagram', 'https://www.instagram.com/apollineag/', '@apollineag')]


def contact_list():
    items = ''.join(f'<li>{k}: <a href="{u}" target="_blank" rel="noopener">{html.escape(v)}</a></li>' for k, u, v in CONTACTS)
    if OPERATOR['email']:
        items = f'<li>Email: <a href="mailto:{OPERATOR["email"]}">{OPERATOR["email"]}</a></li>' + items
    return f'<ul>{items}</ul>'


def operator_block():
    lines = [f'<strong>{html.escape(OPERATOR["name"] or "Apolline")}</strong>']
    if OPERATOR['address']:
        lines.append(html.escape(OPERATOR['address']).replace('\n', '<br>'))
    return '<p>' + '<br>'.join(lines) + '</p>' + contact_list()


def privacy():
    return f"""
<p class="lead">This policy explains what personal data Apolline collects, why, and what rights you have. We keep it short because we collect very little.</p>
<h2>Who is responsible</h2>
{operator_block()}
<h2>This website</h2>
<p>apolline.site is a static website. It does <strong>not</strong> use analytics, advertising or tracking cookies, and it does not load fonts or scripts from third-party servers — everything is served from our own domain.</p>
<p>The only thing the site stores in your browser is a small note (in local storage, not a cookie) that you closed the privacy notice, so it does not show again. It never leaves your device.</p>
<p><strong>Hosting.</strong> The site is hosted by Cloudflare, Inc. (Cloudflare Pages). To deliver pages and protect against attacks, Cloudflare processes technical data such as your IP address, browser type and the time of the request in short-lived server logs. Legal basis: our legitimate interest in a secure, working website (Art. 6(1)(f) GDPR). Cloudflare is certified under the EU–US Data Privacy Framework.</p>
<h2>When you contact us</h2>
<p>You can reach us through Telegram, our Telegram request bot, WhatsApp or Instagram. When you do, we receive what you send: your name or username, phone number or account handle, and the content of your messages (for example, a description of your task).</p>
<ul>
<li><strong>Purpose:</strong> to answer you, prepare an offer and provide the services you ask for.</li>
<li><strong>Legal basis:</strong> steps before a contract and performing the contract (Art. 6(1)(b) GDPR); otherwise our legitimate interest in answering inquiries (Art. 6(1)(f) GDPR).</li>
<li><strong>Retention:</strong> as long as needed for the conversation and the project, and afterwards only as long as tax or accounting law requires. Inquiries that do not lead to a project are deleted within 24 months.</li>
<li><strong>Messengers:</strong> these services are run by Telegram FZ-LLC and Meta Platforms (WhatsApp, Instagram) under their own privacy policies. Data you send through them may be processed outside the EU.</li>
</ul>
<h2>If we contacted you first</h2>
<p>We sometimes write to businesses whose public contact details are listed online (for example on their website or map listing) to offer our services. We use only business contact data, only for that offer, and stop immediately if you ask. Reply "no" or "stop" in any channel and we will delete your details and not contact you again. Legal basis: legitimate interest (Art. 6(1)(f) GDPR).</p>
<h2>Who receives data</h2>
<p>We do not sell or rent personal data and do not share it for advertising. Data is shared only with the providers named above, with contractors who help deliver a project you ordered (bound to confidentiality), or where the law requires it.</p>
<h2>International transfers</h2>
<p>Some providers process data outside the EU/EEA or UK. Where this happens, transfers rely on adequacy decisions (such as the EU–US Data Privacy Framework) or the European Commission's Standard Contractual Clauses.</p>
<h2>Your rights</h2>
<p>Under the GDPR and UK GDPR you have the right to access your data, have it corrected or deleted, restrict or object to processing, and receive it in a portable format. Where processing is based on consent, you can withdraw it at any time. You can also complain to a data protection supervisory authority, in particular in the country where you live.</p>
<p><strong>California residents (CCPA/CPRA):</strong> you have the right to know what personal information we hold, to request deletion or correction, and not to be discriminated against for using these rights. We do not sell or share personal information as defined by the CCPA.</p>
<p>To use any of these rights, contact us through any of the channels above. We answer within one month.</p>
<h2>Children</h2>
<p>Our services are for businesses. We do not knowingly collect data from children under 16.</p>
<h2>Changes</h2>
<p>We update this policy when our practices change. The date below shows the latest version.</p>
<p class="upd">Last updated: {UPDATED}</p>"""


def terms():
    return f"""
<p class="lead">These terms apply to the use of apolline.site and to working with Apolline.</p>
<h2>About us</h2>
{operator_block()}
<h2>Information on this website</h2>
<p>The content of this website, including blog articles, is general information about our services and marketing. It is not a binding offer and not legal, tax or financial advice. Price ranges and examples are indicative.</p>
<h2>Working together</h2>
<ul>
<li>Every project starts with a discussion of the task. The scope, deadlines, price and payment model (fixed fee, monthly fee or a percentage of sales) are agreed individually in writing — in a message, an offer or a contract — before work begins.</li>
<li>For pay-for-results projects, how sales are attributed, the percentage, and when it is paid are agreed in advance. If no orders come from our work, no fee for results is due.</li>
<li>You confirm that materials you give us (texts, photos, logos, account access) are yours to use, and that the products and services we promote are legal.</li>
<li>Unless agreed otherwise, after full payment you receive the rights to use the final materials we create for you. We may show non-confidential results in our portfolio unless you ask us not to.</li>
</ul>
<h2>Third-party platforms</h2>
<p>Social networks, marketplaces, ad platforms and messengers are run by third parties with their own rules. We cannot guarantee their availability, reach, ranking or decisions such as account restrictions, and are not responsible for changes they make.</p>
<h2>Liability</h2>
<p>We do our work with care. To the extent permitted by law, our liability is limited to the fees paid for the specific service in question, and we are not liable for indirect losses such as lost profit. Nothing in these terms limits liability that cannot be limited by law, including for intent or gross negligence, or your statutory rights as a consumer.</p>
<h2>Links</h2>
<p>This site links to external websites. We are not responsible for their content.</p>
<h2>Changes</h2>
<p>We may update these terms. The version valid at the time an agreement is made applies to that agreement.</p>
<p class="upd">Last updated: {UPDATED}</p>"""


def notice():
    return f"""
<h2>Operator</h2>
{operator_block()}
<h2>Responsible for content</h2>
<p>{html.escape(OPERATOR['name'] or 'Apolline')}, contact as above.</p>
<h2>Liability for content and links</h2>
<p>We create the content of this website carefully but cannot guarantee that it is complete, correct and up to date. External links lead to content of third parties, for which their operators are responsible; we checked them when linking and will remove any link to unlawful content as soon as we become aware of it.</p>
<h2>Copyright</h2>
<p>Texts, designs, videos and graphics on this website are protected by copyright. Please ask before reusing them.</p>
<h2>Dispute resolution</h2>
<p>We are not obliged or willing to take part in dispute resolution proceedings before a consumer arbitration board.</p>
<p class="upd">Last updated: {UPDATED}</p>"""


PAGES = [('privacy', 'Privacy Policy', 'How Apolline handles personal data: no tracking cookies, what we process when you contact us, and your rights under GDPR, UK GDPR and CCPA.', privacy),
         ('terms', 'Terms of Service', 'Terms for using apolline.site and working with Apolline: offers, payment models, rights to materials and liability.', terms),
         ('legal', 'Legal Notice', 'Legal notice (imprint) for apolline.site: operator, contact and liability information.', notice)]


def build_legal():
    urls = []
    for slug, title, desc, fn in PAGES:
        url = f'{BASE}{slug}/'
        body = f"""<main class="wrap"><div class="crumbs"><a href="/">Home</a> / {title}</div>
<article><h1>{title}</h1>{fn()}</article></main>"""
        d = ROOT / slug
        d.mkdir(exist_ok=True)
        (d / 'index.html').write_text(blog.page(f'{title} | Apolline', desc, url, body, None, og_type='website')
                                      .replace('</style>', '.upd{color:var(--grey);font-size:14px;margin-top:40px}</style>'), encoding='utf-8')
        urls.append(url)
        print('built', f'{slug}/index.html')
    return urls
