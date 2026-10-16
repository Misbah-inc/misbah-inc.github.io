"""Biography of Lady Khadijah, chapter 1 — laid out like the Rabi' al-Awwal article: a contents box, numbered section headings, the
Arabic quotations in their own boxes with footnote numbers that link to a collapsible Sources list at the end.

The page already exists (build_khadijah.py made it from the channel posts); this script rewrites only the body of
lady-khadijah-biography/1 in each language, in place, from the same posts (work/tg/scan-<lang>.json). Text is word for word:
the 🌳 lines become the section headings (their trailing colon dropped), 💫 lines are paragraphs, ❝…❞ lines are quotation boxes,
(1) / (2) … become footnote links, and the 📚 blocks become the Sources list. Idempotent.
usage: python3 build_khadijah_ch1.py
"""
import os as _os
HERE = _os.path.dirname(_os.path.abspath(__file__)) + '/'
import json, os, re, sys, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_kawthar import PFX, ROOT
import build_khadijah as K

LANGS4 = ['en', 'ar', 'fa', 'ur']
SER = 'lady-khadijah-biography'
UI = {'en': ('In this chapter', 'Sources'), 'ar': ('في هذا الفصل', 'المصادر'), 'fa': ('در این فصل', 'منابع'), 'ur': ('اس باب میں', 'حوالہ جات')}
ROMAN = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X']
ESC = lambda t: html.escape(t, quote=False)
NUM = re.compile(r'^(\d+)\s*[.\-–۔]\s*(.*)$')
FOOT = re.compile(r'\((\d+)\)')


def numeral(n, lang):
    if lang == 'en': return ROMAN[n - 1]
    return K.num(n, lang)


def parse(text):
    """-> chapter subtitle, sections [{title, items:[('p'|'q', text, group)]}], groups {g: [(n, text)]}"""
    sections, groups, sub = [], {}, ''
    cur, g, in_src, last_n = None, 0, False, None
    for raw in text.split('\n'):
        l = raw.strip()
        if not l:
            if in_src: g += 1; in_src = False          # a blank line ends a 📚 block: the next block of footnotes is a new group
            continue
        if l.startswith('#') or l.startswith('@') or re.match(r'^[\s✦━❁🌸─]*$', l): continue
        if l.startswith('🌸'): continue
        if not sub and not l.startswith(('🌳', '💫', '❝', '📚')) and sections == []:
            sub = l; continue
        if l.startswith('🌳'):
            cur = dict(title=re.sub(r'[:：]\s*$', '', l[1:].strip()), items=[]); sections.append(cur); continue
        if l.startswith('📚'):
            in_src = True; groups.setdefault(g, [])
            l = l[1:].strip()
        if in_src:
            m = NUM.match(l)
            if m: groups[g].append([int(m.group(1)), m.group(2)])
            elif groups[g]: groups[g][-1][1] += ' ' + l          # a wrapped line of the previous source
            continue
        if cur is None: continue
        if l.startswith('💫'): cur['items'].append(('p', l[1:].strip(), g))
        elif l.startswith('❝'): cur['items'].append(('q', l, g))
        else: cur['items'].append(('p', l, g))
    return sub, sections, groups


def sup(text, g):
    return FOOT.sub(lambda m: f'<sup class="bio-ref"><a href="#src-{g}-{m.group(1)}">[{m.group(1)}]</a></sup>', ESC(text))


def body(lang, text):
    toc_h, src_h = UI[lang]
    sub, sections, groups = parse(text)
    toc = ''.join(f'<li><a href="#sec{i}">{ESC(s["title"])}</a></li>' for i, s in enumerate(sections, 1))
    out = [f'<nav class="bio-toc" aria-label="{toc_h}"><div class="bio-toc-heading">{toc_h}</div><ol>{toc}</ol></nav>']
    for i, s in enumerate(sections, 1):
        out.append(f'<div class="bio-part-label" id="sec{i}"><span class="bio-part-num">{numeral(i, lang)}</span><h2 class="bio-part-title">{ESC(s["title"])}</h2></div>')
        for k, t, g in s['items']:
            if k == 'q':
                quote = t.replace('❝', '').replace('❞', ' ')
                out.append(f'<div class="quran-verse"><span class="quran-ar" lang="ar" dir="rtl">❝{sup(quote.strip(), g)}❞</span></div>')
            else:
                out.append(f'<p>{sup(t, g)}</p>')
    if groups:
        lists = ''
        for g, items in sorted(groups.items()):
            # which sections cite this group (their numerals label the list)
            idx = [i for i, s in enumerate(sections, 1) if any(gg == g for _, _, gg in s['items'])]
            label = numeral(idx[0], lang) + ('–' + numeral(idx[-1], lang) if len(idx) > 1 else '') if idx else ''
            lis = ''.join(f'<li id="src-{g}-{n}" value="{n}">{ESC(t)}</li>' for n, t in items)
            lists += f'<div class="bio-src-group"><div class="bio-src-label">{label}</div><ol>{lis}</ol></div>'
        out.append(f'<div class="bio-sources"><button type="button" class="bio-sources-btn" aria-expanded="false" aria-controls="bio-src-body"><span>{src_h}</span><span class="bio-sources-chevron" aria-hidden="true">▾</span></button>'
                   f'<div class="bio-sources-body" id="bio-src-body">{lists}</div></div>')
    return sub, '\n        '.join(out)


def main(dry=False):
    for lang in LANGS4:
        pid = K.POSTS[SER][lang][0]
        text = K.SCAN[lang][pid]['text']
        sub, html_body = body(lang, text)
        path = ROOT + f"{PFX[lang].lstrip('/')}{'/' if PFX[lang] else ''}articles/{SER}/1/index.html"
        if dry: print(lang, sub, '\n', html_body[:600]); continue
        s = open(path, encoding='utf-8').read()
        m = re.search(r'(<section class="art-part">\s*<div class="art-body">)(.*?)(\s*</div>\s*</section>)', s, re.S)
        assert m, path
        s = s[:m.start()] + m.group(1) + '\n\n        <div class="bio-ch">\n        ' + html_body + '\n        </div>\n' + m.group(3) + s[m.end():]
        open(path, 'w', encoding='utf-8').write(s)
        print(lang, 'rewritten', len(html_body))


if __name__ == '__main__':
    main('--dry' in sys.argv)
