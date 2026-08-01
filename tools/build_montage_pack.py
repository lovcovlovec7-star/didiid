#!/usr/bin/env python3
import csv,hashlib,html,json,re,shutil,subprocess,urllib.parse,zipfile
from pathlib import Path
import requests
from bs4 import BeautifulSoup

R=Path.cwd(); W=R/'_work'; D=W/'downloads'; X=W/'extract'; P=W/'МОНТАЖНЫЙ_SFX_ПАК_RU'
A=P/'01_ЗВУКИ_WAV'; C=P/'02_КАТАЛОГ_И_ПОИСК'; Q=P/'03_БЫСТРЫЕ_ПОДБОРКИ'; L=P/'04_ИСТОЧНИКИ_И_ЛИЦЕНЗИИ'; O=P/'05_ОФОРМЛЕНИЕ_PLAYEROK'; OUT=R/'dist'
UA={'User-Agent':'Mozilla/5.0 MontagePackBuilder/1.0'}
SRC=[
('interface-sounds','Kenney Interface Sounds','03_КЛИКИ_ИНТЕРФЕЙС_UI'),
('ui-audio','Kenney UI Audio','03_КЛИКИ_ИНТЕРФЕЙС_UI'),
('impact-sounds','Kenney Impact Sounds','02_УДАРЫ_ИМПАКТЫ'),
('digital-audio','Kenney Digital Audio','05_ГЛИТЧ_ЦИФРА_ТЕХНО'),
('sci-fi-sounds','Kenney Sci-Fi Sounds','06_SCI_FI_ТЕХНОЛОГИИ'),
('rpg-audio','Kenney RPG Audio','07_ИГРОВЫЕ_БОЕВЫЕ'),
('foley-sounds','Kenney Foley Sounds','08_FOLEY_ПРЕДМЕТЫ_ШАГИ'),
('retro-sounds-1','Kenney Retro Sounds 1','09_РЕТРО_АРКАДА'),
('retro-sounds-2','Kenney Retro Sounds 2','09_РЕТРО_АРКАДА'),
('casino-audio','Kenney Casino Audio','11_КАЗИНО_НАГРАДЫ'),
('synth-voice-1','Kenney Synth Voice 1','10_ГОЛОСА_РОБОТЫ_СИГНАЛЫ'),
('synth-voice-2','Kenney Synth Voice 2','10_ГОЛОСА_РОБОТЫ_СИГНАЛЫ')]
CATS=['01_ПЕРЕХОДЫ_ВУШИ_СВИПЫ','02_УДАРЫ_ИМПАКТЫ','03_КЛИКИ_ИНТЕРФЕЙС_UI','04_КАМЕРА_ФОТО_МЕХАНИЗМЫ','05_ГЛИТЧ_ЦИФРА_ТЕХНО','06_SCI_FI_ТЕХНОЛОГИИ','07_ИГРОВЫЕ_БОЕВЫЕ','08_FOLEY_ПРЕДМЕТЫ_ШАГИ','09_РЕТРО_АРКАДА','10_ГОЛОСА_РОБОТЫ_СИГНАЛЫ','11_КАЗИНО_НАГРАДЫ','12_РАЗНОЕ']
EXT={'.wav','.ogg','.mp3','.flac','.aif','.aiff','.m4a'}

def cmd(a,cap=False):
 print('+',' '.join(map(str,a)),flush=True)
 return subprocess.run(a,text=True,stdout=subprocess.PIPE if cap else None,stderr=subprocess.PIPE if cap else None)
def clean(s):
 s=re.sub(r'[^0-9A-Za-zА-Яа-яЁё_-]+','_',s.replace(' ','_')); return re.sub(r'_+','_',s).strip('_')[:90] or 'sound'
def zipurl(page):
 t=requests.get(page,headers=UA,timeout=45).text; b=BeautifulSoup(t,'html.parser'); u=[]
 for tag in b.find_all(True):
  for v in tag.attrs.values():
   for z in (v if isinstance(v,list) else [v]):
    if isinstance(z,str) and '.zip' in z.lower(): u.append(urllib.parse.urljoin(page,html.unescape(z).replace('\\/','/')))
 for pat in [r'https?://[^"\'<>\s]+?\.zip(?:\?[^"\'<>\s]*)?',r'/media/pages/assets/[^"\'<>\s]+?\.zip(?:\?[^"\'<>\s]*)?']:
  u += [urllib.parse.urljoin(page,x) for x in re.findall(pat,t,re.I)]
 for x in sorted(set(u),key=lambda x:(0 if 'kenney.nl/media/' in x else 1,len(x))):
  try:
   r=requests.get(x,headers=UA,timeout=60,stream=True); first=next(r.iter_content(8),b'')
   if r.ok and (first.startswith(b'PK') or 'zip' in r.headers.get('content-type','').lower()): return r.url
  except Exception: pass
 raise RuntimeError('ZIP не найден')
def category(default,name):
 s=name.lower(); rules=[
 ('01_ПЕРЕХОДЫ_ВУШИ_СВИПЫ',['whoosh','woosh','swoosh','sweep','swipe','transition','flyby','passby','riser']),
 ('04_КАМЕРА_ФОТО_МЕХАНИЗМЫ',['camera','shutter','photo','mechanic','machine','gear','lever','clock']),
 ('02_УДАРЫ_ИМПАКТЫ',['impact','hit','slam','thud','punch','kick','crash','break','explosion','boom']),
 ('03_КЛИКИ_ИНТЕРФЕЙС_UI',['click','button','tap','select','confirm','cancel','toggle','menu','notification']),
 ('08_FOLEY_ПРЕДМЕТЫ_ШАГИ',['foot','step','door','paper','cloth','wood','metal','glass','water','stone','drop']),
 ('10_ГОЛОСА_РОБОТЫ_СИГНАЛЫ',['voice','synth','robot','speech','alarm','signal','beep']),
 ('11_КАЗИНО_НАГРАДЫ',['coin','card','dice','chip','casino','win','jackpot','reward'])]
 for c,ws in rules:
  if any(w in s for w in ws): return c
 return default
def duration(p):
 z=cmd(['ffprobe','-v','error','-show_entries','format=duration','-of','default=nw=1:nk=1',str(p)],True)
 try:return float(z.stdout.strip())
 except:return 0
def wav(src,dst):
 dst.parent.mkdir(parents=True,exist_ok=True)
 z=cmd(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(src),'-vn','-ar','48000','-c:a','pcm_s16le',str(dst)],True)
 return z.returncode==0 and dst.exists() and dst.stat().st_size>100
def choose(root):
 p=[x for x in root.rglob('*') if x.is_file() and x.suffix.lower() in EXT]; g={}; pri={'.wav':0,'.flac':1,'.aiff':2,'.aif':2,'.ogg':3,'.mp3':4,'.m4a':5}
 for x in p:g.setdefault(str(x.relative_to(root).with_suffix('')).lower(),[]).append(x)
 return [sorted(v,key=lambda x:pri.get(x.suffix.lower(),9))[0] for v in g.values()]
def hh(p):
 q=hashlib.sha256()
 with p.open('rb') as f:
  for x in iter(lambda:f.read(1048576),b''):q.update(x)
 return q.hexdigest()

for z in [W,OUT]:
 if z.exists():shutil.rmtree(z)
for z in [D,X,A,C,Q,L,O,OUT]:z.mkdir(parents=True,exist_ok=True)
for z in CATS:(A/z).mkdir(exist_ok=True)
rows=[]; seen=set(); ok=[]; bad=[]; n=1
for slug,title,default in SRC:
 page=f'https://kenney.nl/assets/{slug}'
 try:
  print('\n==',title,'=='); u=zipurl(page); arc=D/f'{slug}.zip'
  with requests.get(u,headers=UA,timeout=180,stream=True) as r:
   r.raise_for_status()
   with arc.open('wb') as f:
    for b in r.iter_content(1048576):
     if b:f.write(b)
  root=X/slug;root.mkdir();zipfile.ZipFile(arc).extractall(root)
  lic=L/slug;lic.mkdir()
  for x in root.rglob('*'):
   if x.is_file() and any(k in x.name.lower() for k in ['license','licence','credit','readme','attribution']) and x.stat().st_size<2000000:
    try:shutil.copy2(x,lic/clean(x.name))
    except:pass
  add=0
  for i,s in enumerate(choose(root),1):
   dur=duration(s)
   if dur<=.01 or dur>180:continue
   cat=category(default,s.name); tmp=W/'tmp'/f'{slug}_{i:04d}_{clean(s.stem)}.wav'
   if not wav(s,tmp):continue
   d=hh(tmp)
   if d in seen:tmp.unlink();continue
   seen.add(d); name=f'{n:04d}_{clean(slug)}_{clean(s.stem)}.wav'; dst=A/cat/name;shutil.move(tmp,dst)
   rows.append({'№':n,'Категория':cat,'Название':clean(s.stem).replace('_',' '),'Длительность':f'{dur:.2f}','Источник':title,'Путь':dst.relative_to(P).as_posix()});n+=1;add+=1
  ok.append((title,page,u,add))
 except Exception as e:
  print('FAILED',title,e);bad.append((title,str(e)))
if len(rows)<250 or len(ok)<5:raise SystemExit(f'Недостаточно материалов: {len(rows)} файлов, {len(ok)} источников')
rows.sort(key=lambda r:(CATS.index(r['Категория']),r['Название'].lower()))
for i,r in enumerate(rows,1):r['№']=i
for z in CATS:
 p=A/z
 if p.exists() and not any(p.iterdir()):p.rmdir()
with (C/'СПИСОК_ВСЕХ_ЗВУКОВ.csv').open('w',newline='',encoding='utf-8-sig') as f:
 w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
data=[{'c':r['Категория'],'n':r['Название'],'d':r['Длительность'],'s':r['Источник'],'u':urllib.parse.quote('../../'+r['Путь'],safe='/._-')} for r in rows]
opts=''.join(f'<option>{html.escape(x)}</option>' for x in CATS if any(r['Категория']==x for r in rows))
page=f'''<!doctype html><meta charset="utf-8"><title>Каталог SFX</title><style>body{{margin:0;background:#090a0e;color:#fff;font:15px Arial}}header{{position:sticky;top:0;padding:20px;background:#090a0eee}}input,select{{padding:12px;margin:4px;background:#151821;color:#fff;border:1px solid #333;border-radius:10px}}main{{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:10px;padding:20px}}article{{padding:14px;background:#12151c;border:1px solid #292e3a;border-radius:14px}}audio{{width:100%}}small{{color:#a9b2c3}}</style><header><h1>Монтажный SFX-пак</h1><input id=q placeholder="Поиск по названию"><select id=c><option value="">Все категории</option>{opts}</select><b id=k></b></header><main id=g></main><script>const a={json.dumps(data,ensure_ascii=False)},g=document.querySelector('#g'),q=document.querySelector('#q'),c=document.querySelector('#c'),k=document.querySelector('#k');function r(){{let x=q.value.toLowerCase(),v=a.filter(z=>(!c.value||z.c==c.value)&&(!x||(z.n+' '+z.c+' '+z.s).toLowerCase().includes(x)));k.textContent=' Найдено: '+v.length;g.innerHTML=v.map(z=>`<article><b>${{z.n}}</b><br><small>${{z.c}} • ${{z.d}} сек.</small><audio controls preload=none src="${{z.u}}"></audio></article>`).join('')}}q.oninput=c.onchange=r;r()</script>'''
(C/'ОТКРЫТЬ_КАТАЛОГ.html').write_text(page,encoding='utf-8')
sets={'01_SHORTS_REELS':['01_ПЕРЕХОДЫ_ВУШИ_СВИПЫ','02_УДАРЫ_ИМПАКТЫ','03_КЛИКИ_ИНТЕРФЕЙС_UI'],'02_ИГРОВАЯ_НАРЕЗКА':['07_ИГРОВЫЕ_БОЕВЫЕ','09_РЕТРО_АРКАДА'],'03_ТЕХНО_ГЛИТЧ':['05_ГЛИТЧ_ЦИФРА_ТЕХНО','06_SCI_FI_ТЕХНОЛОГИИ'],'04_МЕМНЫЙ_МОНТАЖ':['10_ГОЛОСА_РОБОТЫ_СИГНАЛЫ','11_КАЗИНО_НАГРАДЫ']}
for fn,cs in sets.items():
 v=[r for r in rows if r['Категория'] in cs][:90]; (Q/f'{fn}.m3u8').write_text('#EXTM3U\n'+'\n'.join('../'+r['Путь'] for r in v)+'\n',encoding='utf-8')
src=['ИСТОЧНИКИ И ЛИЦЕНЗИИ','','Все включённые библиотеки взяты с официального сайта Kenney и помечены там лицензией Creative Commons CC0 1.0.','https://creativecommons.org/publicdomain/zero/1.0/','']
for t,p,u,a in ok:src += [t,f'Страница: {p}',f'Архив: {u}',f'Добавлено: {a}','']
if bad:src += ['НЕ ВКЛЮЧЕНО:']+[f'{t}: {e}' for t,e in bad]
(L/'ИСТОЧНИКИ_И_ЛИЦЕНЗИИ.txt').write_text('\n'.join(src),encoding='utf-8')
cnt=len(rows)
(P/'ОТКРОЙ_МЕНЯ.txt').write_text(f'''МОНТАЖНЫЙ SFX-ПАК RU

Внутри: {cnt} уникальных WAV 48 kHz.

Звуки: 01_ЗВУКИ_WAV
Каталог с поиском: 02_КАТАЛОГ_И_ПОИСК/ОТКРЫТЬ_КАТАЛОГ.html
Быстрые подборки: 03_БЫСТРЫЕ_ПОДБОРКИ
Лицензии: 04_ИСТОЧНИКИ_И_ЛИЦЕНЗИИ

Никаких EXE, BAT и установщиков.
''',encoding='utf-8')
(O/'НАЗВАНИЕ_ТОВАРА.txt').write_text(f'🔥 {cnt}+ ЗВУКОВ ДЛЯ МОНТАЖА | WAV + РУССКИЙ КАТАЛОГ | АВТОВЫДАЧА\n',encoding='utf-8')
(O/'ОПИСАНИЕ_ТОВАРА.txt').write_text(f'''🔥 МОЩНЫЙ SFX-ПАК ДЛЯ МОНТАЖА — {cnt} УНИКАЛЬНЫХ ЗВУКОВ

Архив очищен от точных дублей, приведён к WAV 48 kHz и разложен по понятным русским категориям.

ВНУТРИ:
• {cnt} готовых звуков WAV;
• русские папки;
• HTML-каталог с поиском и прослушиванием;
• быстрые подборки для Shorts/Reels, игр, техно и мемного монтажа;
• таблица файлов, источники и лицензии.

Подходит для CapCut, Premiere Pro, After Effects, DaVinci Resolve, Vegas Pro, Filmora и других редакторов.

✅ Без EXE, BAT и взломанных плагинов.
✅ Официальные CC0-библиотеки Kenney.
⚡ Автовыдача сразу после оплаты.
''',encoding='utf-8')
shutil.make_archive(str(OUT/'МОНТАЖНЫЙ_SFX_ПАК_RU'),'zip',root_dir=W,base_dir=P.name)
print('DONE',cnt,'sounds',len(ok),'sources',len(bad),'failed')
