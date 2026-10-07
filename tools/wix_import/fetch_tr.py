import json,subprocess,time,os,sys
alts=json.load(open('alts.json'))
want=['the-virtues-of-the-ziarat-lady-fatimah-ma-soumah-p','hadrat-abdul-azim-hasani-p','the-month-of-rabi-al-akhir','supplications-of-salawat','the-letter-of-imam-ja-far-al-sadiq-p-to-the-shia-s','the-recognition-of-imam-sadiq-p-the-blessed-title-al-sadiq','the-blessed-marriage-of-lady-khadijah-p-and-the-holy-prophet-p','30-name-and-title-of-the-messenger-of-god-p-in-the-verses-of-the-holy-qur-an']
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
