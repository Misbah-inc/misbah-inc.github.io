import re,json,glob,os,sys
os.chdir(os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + '/../..'))
cat=json.load(open(os.path.dirname(os.path.abspath(__file__)) + '/catalog.json'))
bad=0; n=0
for slug,c in cat.items():
    for l in c['langs']:
        f=('' if l=='en' else l+'/')+f'articles/{slug}/index.html'
        s=open(f,encoding='utf-8').read(); n+=1
        iss=[]
        m=re.search(r'<html lang="(\w+)" dir="(\w+)"',s)
        if m.group(1)!=l or m.group(2)!=('ltr' if l=='en' else 'rtl'): iss.append('lang/dir')
        t=re.search(r'<title>(.*?)</title>',s,re.S).group(1); d=re.search(r'name="description" content="([^"]*)"',s).group(1)
        if len(t)>75: iss.append(f'title{len(t)}')
        if not 40<len(d)<=175: iss.append(f'desc{len(d)}')
        can=re.search(r'rel="canonical"\s+href="([^"]+)"',s).group(1)
        if can!=f'https://article.misbah-inc.com{"/"+l if l!="en" else ""}/articles/{slug}/': iss.append('canonical')
        hl=re.findall(r'hreflang="([\w-]+)"\s+href="([^"]+)"',s)
        if {x for x,_ in hl}!=set(c['langs'])|{'x-default'}: iss.append(f'hreflang {sorted({x for x,_ in hl})}')
        try: json.loads(re.search(r'application/ld\+json">(.*?)</script>',s,re.S).group(1))
        except Exception as e: iss.append('jsonld')
        if len(re.findall(r'<h1',s))!=1: iss.append('h1')
        for i in re.findall(r'<img[^>]*>',s):
            if 'alt=' not in i: iss.append('noalt')
            m2=re.search(r'src="(/images/[^"]+)"',i)
            if m2 and not os.path.exists(m2.group(1)[1:]): iss.append('missing '+m2.group(1))
        og=re.search(r'og:image"\s+content="https://article.misbah-inc.com([^"]+)"',s)
        if not og or not os.path.exists(og.group(1)[1:]): iss.append('og missing')
        bm=re.search(r'<div class="art-body">(.*?)</section>',s,re.S)
        if bm and re.search(r'Updated:|Checking Your',bm.group(1)): iss.append('wix leftover')
        if not bm and c.get('kind')!='series': iss.append('no body')
        if iss: bad+=1; print('XX',f,iss)
# header: language links must stay inside their language and every page needs the theme button
import glob as _g
hb=0
for hf in _g.glob('**/*.html', recursive=True):
    if hf.startswith(('tools/','assets/','node_modules/')) or '/work/' in hf: continue
    s=open(hf,encoding='utf-8').read(); m=re.search(r'<header class="site-header">.*?</header>',s,re.S)
    if not m: continue
    links=dict((l,h) for h,l in re.findall(r'<a href="([^"]+)" hreflang="(\w+)"(?: class="active")?>[A-Z]{2}</a>',m.group(0)))
    okl=all((links.get(l,'').startswith('/'+l+'/') if l!='en' else not re.match(r'/(ar|fa|ur)/',links.get('en','/'))) for l in ('en','ar','fa','ur')) and 'rabi_al_awwal' not in ''.join(links.values()) or 'rabi_al_awwal' in hf
    if not okl or 'theme-toggle' not in m.group(0): hb+=1; print('XX header',hf)
print(n,'pages checked,',bad,'with issues;',hb,'headers wrong')
