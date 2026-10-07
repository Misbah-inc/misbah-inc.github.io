import re,html
from html.parser import HTMLParser
class P(HTMLParser):
    def __init__(s):
        super().__init__(convert_charrefs=True); s.blocks=[]; s.cur=None; s.depth=0; s.inart=False
    def handle_starttag(s,tag,a):
        a=dict(a)
        if tag=='article': s.inart=True
        if not s.inart: return
        if tag in('h1','h2','h3','h4','h5','h6','p','li','blockquote'):
            s.cur={'t':tag,'x':'','cls':a.get('class','')}
        if tag=='img' and a.get('src'): s.blocks.append({'t':'img','x':a['src']})
        if tag=='ol' or tag=='ul': s.blocks.append({'t':'list-'+tag,'x':''})
        if tag=='br' and s.cur is not None: s.cur['x']+='\n'
    def handle_endtag(s,tag):
        if tag=='article': s.inart=False
        if s.cur and tag==s.cur['t']:
            s.cur['x']=re.sub(r'[ \t]+',' ',s.cur['x']).strip()
            if s.cur['x']: s.blocks.append(s.cur)
            s.cur=None
    def handle_data(s,d):
        if s.inart and s.cur is not None: s.cur['x']+=d
def parse(f):
    p=P(); p.feed(open(f,encoding='utf-8').read()); return p.blocks
if __name__=='__main__':
    import sys
    for b in parse(sys.argv[1]): print(b['t'],'|',b['x'][:110].replace('\n','⏎'))
