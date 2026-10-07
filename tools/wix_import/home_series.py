import re,html
from build_kawthar import *   # re-runs the build (idempotent) and gives ART/S/ORD
def block(lang):
    L=S[lang]; a1=ART[(lang,1)]
    intro=next(b['x'] for b in a1['body'] if len(b['x'])>80 and not is_arabic_quote(b['x']))
    base=f'{PFX[lang]}/articles/{SLUG}/'
    return f'''<!-- ═══════════════════════════════════════
     NEW SERIES — Al-Kawthar (articles/al-kawthar/)
════════════════════════════════════════ -->
<section class="section kw-home" id="kawthar-series" aria-labelledby="kw-heading">
  <div class="container text-center">
    <span class="section-label">{L['new_series']}</span>
    <h2 class="section-title" id="kw-heading">{esc(L['series'])}</h2>
    <div class="divider" aria-hidden="true"><span class="divider-gem">◆</span></div>

    <article class="kw-home-card">
      <a href="{base}" tabindex="-1" aria-hidden="true"><img src="/images/kawthar/part1-{lang}.jpg" alt="" width="1400" height="483" loading="lazy" decoding="async"></a>
      <div class="kw-home-body">
        <span class="kw-series-chip" style="align-self:flex-start">{L['chip']}</span>
        <p>{esc(clip(intro, 260))}</p>
        <p><a href="{base}part-1/">{ORD[lang][1]}</a> &nbsp;·&nbsp; <a href="{base}part-2/">{ORD[lang][2]}</a></p>
        <a href="{base}" class="btn btn-gold">{L['view_series']}</a>
      </div>
    </article>
  </div>
</section>

'''
for lang in LANGS:
    path=ROOT+('index.html' if lang=='en' else f'{lang}/index.html')
    s=open(path,encoding='utf-8').read()
    s=re.sub(r'<!-- ═+\s*\n\s*NEW SERIES.*?</section>\s*','',s,flags=re.S)  # idempotent
    m=re.search(r'(<!--[^>]*?-->\s*)?<section class="section mourning-section"',s,re.S)
    # insert before the banner comment of the mourning section
    i=s.rfind('<!-- ═',0,m.start()+len(m.group(0))) if m.group(1) else m.start()
    s=s[:i]+block(lang)+s[i:]
    open(path,'w',encoding='utf-8').write(s)
    print(lang,'ok',len(s))
