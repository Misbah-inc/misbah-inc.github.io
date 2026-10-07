import json,subprocess,time,os,sys
alts=json.load(open('alts.json'))
want=['morning-and-evening-mourning','morning-and-evening-mourning-1']
for w in want:
    for l,u in sorted(alts[w].items()):
        f=f'posts2/{w[:60]}-{l}.html'
        if os.path.exists(f) and os.path.getsize(f)>200000 and 'Checking Your Request' not in open(f,encoding='utf-8',errors='replace').read(4000): continue
        for attempt in range(6):
            subprocess.run(['curl','-sL','-A','Mozilla/5.0','-o',f,u],timeout=120)
            t=open(f,encoding='utf-8',errors='replace').read()
            if 'Checking Your Request' not in t[:5000] and len(t)>200000: print('ok',f,flush=True); break
            wait=20*(attempt+1); print('blocked, wait',wait,f,flush=True); time.sleep(wait)
        time.sleep(4)
print('ALL DONE',flush=True)
