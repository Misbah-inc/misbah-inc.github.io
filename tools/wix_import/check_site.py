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
        body=re.search(r'<div class="art-body">(.*?)</section>',s,re.S).group(1)
        if re.search(r'Updated:|Checking Your',body): iss.append('wix leftover')
        if iss: bad+=1; print('XX',f,iss)
print(n,'pages checked,',bad,'with issues')
