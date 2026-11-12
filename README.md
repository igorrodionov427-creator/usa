# Apolline — marketing team for small businesses

Source of **[apolline.site](https://apolline.site)**: social media, short-form video, ads, chatbots and websites for small businesses in the US and Europe. One team instead of five contractors, fixed prices.

- Website: https://apolline.site
- Guides for small businesses: https://apolline.site/blog/
- Contact: apolline.agency@gmail.com · Telegram [@apollineAG](https://t.me/apollineAG)

## How the site is built

Static HTML, no framework. `_src/index.html` (English source) + `i18n.js` (8 languages) → `build.py` writes one page per language, the blog from `_src/blog/*.md`, legal pages, `sitemap.xml`, `robots.txt` and `llms.txt`. Hosted on Cloudflare Pages.

```bash
python build.py
```
