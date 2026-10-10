"""Builds tools/embed/misbah-footer.html — the site footer as ONE self-contained file for a Wix "Embed HTML" element.
Icons are copied from index.html so they stay identical to the site; links are absolute and open in the whole page (target=_top)."""
import re, os
ROOT = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + '/../..') + '/'
src = open(ROOT + 'index.html', encoding='utf-8').read()
foot = src[src.index('<footer'):src.index('</footer>')]
foot = foot.replace('href="/articles"', 'href="https://article.misbah-inc.com/articles/"')
foot = foot.replace('href="/connect"', 'href="https://www.misbah-inc.com/connect"').replace('href="/about"', 'href="https://www.misbah-inc.com/about"')
foot = foot.replace('<a href=', '<a target="_top" href=').replace(' target="_blank" rel="noopener"', ' target="_blank" rel="noopener"')
foot = re.sub(r'<a target="_top" href=("[^"]*"[^>]*target="_blank")', r'<a href=\1', foot)   # external links keep their own target
foot = foot.replace('<footer class="site-footer" role="contentinfo">', '<footer class="site-footer" role="contentinfo">')
CSS = open(os.path.dirname(os.path.abspath(__file__)) + '/footer.css', encoding='utf-8').read()
html = f'''<!DOCTYPE html>
<html lang="en" dir="ltr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Misbah footer</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@600&family=Inter:wght@400;500&display=swap" rel="stylesheet">
<style>
{CSS}
</style>
</head>
<body>
{foot}</footer>
</body>
</html>
'''
open(os.path.dirname(os.path.abspath(__file__)) + '/misbah-footer.html', 'w', encoding='utf-8').write(html)
print(len(html), 'bytes')
