import sys, os, json
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from render import *
ROOT=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')
sqs=os.path.join(ROOT,'squarespace'); pages=os.path.join(sqs,'pages')
out=sys.argv[1]; slugs=sys.argv[2:] or sorted(f[:-5] for f in os.listdir(pages) if f.endswith('.html'))
bad=0
for slug in slugs:
    mock=os.path.join(out,f'mock_{slug}.html'); build_mock(os.path.join(pages,slug+'.html'),mock,sqs)
    r=check('file://'+os.path.abspath(mock),slug,out,shots=True)
    for vp in ('d','m'):
        x=r[vp]; ok=(x['sw']<=x['vw'] and not x['small'] and not x['imgs'] and x['h1']==1 and x['hidden']==['none','none'])
        if not ok: bad+=1
        print(('OK ' if ok else 'BAD'),slug,vp,'sw',x['sw'],'h1',x['h1'],'small',x['small'],'imgs',x['imgs'],'form',x['formInSlot'])
    hs=r['d']['hs']; order_ok=True; last=1
    for h in hs:
        lvl=int(h[1]); 
        if lvl>last+1: order_ok=False
        last=lvl
    if not order_ok: print('   heading order problem:',hs)
print('bad',bad)
