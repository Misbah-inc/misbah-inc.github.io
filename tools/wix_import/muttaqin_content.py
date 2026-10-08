"""Sermon of Muttaqin: turn the YouTube descriptions (muttaqin_src/<video id>.txt) into body blocks.

The text is the channel's own description of each video, kept word for word. Only social furniture is
removed (emoji bullets, hashtags, separators, markdown asterisks, the ༺《N》༻ counter). Where the description
carries the same passage twice (a rough draft followed by a clean version — parts 12 and 13) the rougher
copy is dropped and the clean one kept; DROP lists exactly which lines.
"""
import os, re

HERE = os.path.dirname(os.path.abspath(__file__)) + '/'
# part number -> (video id, published, short title for <title>, YouTube title)
PARTS = {
 1: ('vFym-FULM3M', '2026-06-16', 'Correct and Upright Speech', 'Their Speech is Correct and Upright'),
 2: ('blkOqLuTxN0', '2026-06-20', 'Moderation in Dress and Conduct', 'Their Manner of Dress, Conduct, and Way of Life is based upon Moderation'),
 3: ('8WQiSwcS4eM', '2026-06-27', 'They Walk with Humility', 'They walk with humility'),
 4: ('5sowLYMOCjc', '2026-07-15', 'They Lower Their Gaze', 'They restrain their eye from which Allah has made unlawful'),
 5: ('vXiBLyQPd74', '2026-07-17', 'Hearing Devoted to Beneficial Knowledge', 'They devote their hearing to knowledge that benefits them'),
 6: ('TtmHI9YpZK0', '2026-07-22', 'The Same in Hardship and Ease', 'They remain the same during trials and hardships as times of comfort and ease'),
 7: ('vtnAT2dlhP4', '2026-08-19', 'They Long to Meet Their Lord', 'They long to see their beloved'),
 8: ('f7XqvGWwmMQ', '2026-08-25', 'The Creator Is Great in Their Souls', 'Creator is great within their soul and everything else is small'),
 9: ('Fy1KnlanhOE', '2026-09-01', 'People of Certainty', 'They are people of certainty'),
 10: ('3fjpR0Regqg', '2026-09-08', 'Hearts Filled with Sorrow', 'Their hearts are filled with sorrow'),
 11: ('MN8yhHgQf3E', '2026-09-15', 'People Are Safe from Their Harm', 'People are secure from their harm'),
 12: ('IaXhLHzHS1E', '2026-09-22', 'Lean and Slender Bodies', 'They possess lean bodies and slender'),
 13: ('4m8l1m1da2M', '2026-09-29', 'Few and Modest Needs', 'Their needs are few and modest'),
 14: ('56EvctLGXeo', '2026-10-06', 'Chaste, Pure Souls', 'Their souls are chaste, pure, and guarded from sin'),
}

DROP = {   # line prefixes (after cleaning) to leave out — see the module note
 12: ['A group set out following the Commander of the Faithful', 'God Almighty says: {Their mark', 'Also, the news of the arrival'],
 13: ['"When I was thirteen years old, my grandfather', '«Abu Muhammad (peace be upon him) informed me', '«To this very moment, no one but you'],
}
POEM = {12: ['The mark of God’s servants', 'How wondrous are they']}   # two-line verses: keep the line break
SUB = {3: ['They Walk with Humility']}   # lines that are sub-headings

BULLET = re.compile(r'^[\s⚜️🔸▪️▫️◾️🔳📙📓📔✨️•]+')
SEP = re.compile(r'^[\s⸻➖\-—_▪️◾️🔸▫️️]*$')
ARABIC = re.compile(r'[؀-ۿ]')
LATIN = re.compile(r'[A-Za-z]')
CHAR = re.compile(r'^The (\w+) [Cc]haracteristic')
REFHEAD = re.compile(r'^(References?:?|Sources?:?)$')


def is_arabic(t):
    a = len(ARABIC.findall(t)); l = len(LATIN.findall(t))
    return a > 0 and a > 2 * l


def parse(n):
    vid = PARTS[n][0]
    raw = open(HERE + f'muttaqin_src/{vid}.txt', encoding='utf-8').read()
    raw = raw.replace(' Bishr ibn Sulayman recounts:', '\nBishr ibn Sulayman recounts:')   # two sentences glued on one line in the source
    out, refs = [], []
    in_refs = False
    for block in re.split(r'\n\s*\n', raw):
        lines = []
        for ln in block.split('\n'):
            ln = ln.strip()
            if not ln or ln.startswith('༺') or ln.startswith('#') or SEP.match(ln): continue
            ref_mark = ln[:1] in '📙📓📔'
            emph = ln.startswith('⚜')
            ln = BULLET.sub('', ln).strip()
            ln = re.sub(r'\*+', '', ln)
            if not ln: continue
            if any(ln.startswith(d) for d in DROP.get(n, [])): continue
            lines.append((ln, ref_mark, emph))
        cur = []   # merged paragraphs of this block
        block_refs = False
        for ln, ref_mark, emph in lines:
            if REFHEAD.match(ln) or re.match(r'^(References?|Sources?):?$', re.sub(r'^[^\w]+', '', ln)):
                in_refs = True; continue
            if ref_mark or block_refs:
                block_refs = True
                body = re.sub(r'^Reference:?\s*', '', ln)
                if body: refs.append(body)
                continue
            if in_refs:
                refs.append(ln); continue
            if CHAR.match(ln):
                cur.append(('H', ln)); continue
            if is_arabic(ln):
                cur.append(('A', ln)); continue
            if emph or any(ln.startswith(s) for s in SUB.get(n, [])):
                cur.append(('S', ln)); continue
            if cur and cur[-1][0] == 'P':
                prev = cur[-1][1]
                if any(ln.startswith(p) for p in POEM.get(n, [])) or any(prev.startswith(p) for p in POEM.get(n, [])):
                    cur[-1] = ('P', prev + '\n' + ln); continue
                if not re.search(r'[:”»"]$', prev) and not re.match(r'^[“«"‘]', ln):
                    cur[-1] = ('P', prev + ' ' + ln); continue
            cur.append(('P', ln))
        out.extend(cur)
    # ⚜ lines in English are the characteristic itself: make them sub-headings
    return out, refs


if __name__ == '__main__':
    import sys
    for n in PARTS:
        if len(sys.argv) > 1 and str(n) != sys.argv[1]: continue
        b, r = parse(n)
        print(f'=== part {n}')
        for k, t in b: print(f'[{k}]', t)
        print('[refs]', r)
