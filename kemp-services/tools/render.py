import sys, os, re, json, requests
from playwright.sync_api import sync_playwright
EXE="/opt/pw-browsers/chromium-1243/chrome-linux64/chrome"
UA="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"
sess=requests.Session(); sess.headers["User-Agent"]=UA
def handler(route, request):
    if request.url.startswith('file:'): return route.continue_()
    try:
        h={k:v for k,v in request.headers.items() if k.lower() not in ("host","content-length","accept-encoding")}
        r=sess.request(request.method, request.url, headers=h, data=request.post_data_buffer, timeout=40, allow_redirects=True)
        route.fulfill(status=r.status_code, headers={k:v for k,v in r.headers.items() if k.lower()=="content-type"}, body=r.content)
    except Exception: route.abort()

MOCK='''<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<style>body{margin:0;font-family:Georgia,serif} h1,h2,h3{font-family:Georgia;letter-spacing:.2em;margin:1em 0} p{margin:1em 0;line-height:2} a{text-decoration:underline;color:red} .page-section{padding:60px 0} .content-wrapper{max-width:1000px;margin:auto;padding:0 30px} .fluid-engine{display:grid;grid-template-columns:repeat(24,1fr)} .fe-block{grid-column:1/-1} .sqs-block{padding:17px} #header{height:100px;background:red} #footer-sections{height:100px;background:red}
.form-wrapper .field-list .field .field-element{background:#BFC5CC;border:0;border-radius:14px;padding:30px 20px;color:#000;font-family:Georgia}
.form-wrapper .field-list .title{color:#000;font-family:Georgia;font-size:22px;text-transform:uppercase}
.form-wrapper .form-button-wrapper .button{background:#ff0;color:#f0f;border-radius:40px;padding:30px 60px;font-size:30px}
</style>__HEAD__</head><body><div class="header-announcement-bar-wrapper"><header id="header">SQS HEADER</header></div><div id="siteWrapper"><main id="page"><section class="page-section"><div class="content-wrapper"><div class="content"><div class="fluid-engine"><div class="fe-block"><div class="sqs-block html-block"><div class="sqs-block-content">__PAGE__</div></div></div></div></div></div></section>__FORM__</main><footer id="footer-sections">SQS FOOTER</footer></div>__FOOT__</body></html>'''
FORM='''<section class="page-section" id="formsec"><div class="content-wrapper"><div class="content"><div class="fluid-engine"><div class="fe-block"><div class="sqs-block form-block sqs-block-form"><div class="sqs-block-content"><div class="form-wrapper"><div class="form-inner-wrapper"><form><div class="field-list clear">
<fieldset class="form-item fields name required"><div class="title">Name</div><div class="field first-name"><input class="field-element" type="text"><label class="caption"><span class="caption-text">First Name <span class="required">(required)</span></span></label></div><div class="field last-name"><input class="field-element" type="text"><label class="caption"><span class="caption-text">Last Name <span class="required">(required)</span></span></label></div></fieldset>
<div class="form-item field email required"><label class="title">Email <span class="required">(required)</span></label><input class="field-element" type="email"></div>
<div class="form-item field textarea required"><label class="title">Message <span class="required">(required)</span></label><textarea class="field-element" rows="4"></textarea></div>
</div><div class="form-button-wrapper"><input class="button sqs-system-button sqs-editable-button sqs-button-element--primary" type="submit" value="Submit"></div></form></div></div></div></div></div></div></div></div></section>'''

def build_mock(page_path, out_path, sqs_dir):
    h=open(os.path.join(sqs_dir,'header.html')).read(); f=open(os.path.join(sqs_dir,'footer.html')).read(); p=open(page_path).read()
    form=FORM if 'fslot' in p else ''
    open(out_path,'w').write(MOCK.replace('__HEAD__',h).replace('__PAGE__',p).replace('__FORM__',form).replace('__FOOT__',f))

def check(url, tag, outdir, shots=True):
    res={}
    with sync_playwright() as pw:
        b=pw.chromium.launch(executable_path=EXE,args=["--no-sandbox","--disable-dev-shm-usage"])
        for w,h,vp in [(1440,900,'d'),(390,844,'m')]:
            pg=b.new_page(viewport={"width":w,"height":h},user_agent=UA); pg.route("**/*",handler)
            pg.goto(url,wait_until="load",timeout=120000); pg.wait_for_timeout(1500)
            H=pg.evaluate("document.body.scrollHeight")
            for y in range(0,H,600): pg.evaluate(f"window.scrollTo(0,{y})"); pg.wait_for_timeout(80)
            pg.wait_for_timeout(1200); pg.evaluate("window.scrollTo(0,0)"); pg.wait_for_timeout(300)
            r=pg.evaluate("""(()=>{
              const small=[...document.querySelectorAll('a,button,label.nbtn,input[type=submit]')].filter(e=>!e.classList.contains('inl')).filter(e=>{const r=e.getBoundingClientRect();return r.width>0&&r.height>0&&(r.width<44||r.height<44)}).map(e=>(e.className||'')+':'+e.textContent.trim().slice(0,20)+' '+Math.round(e.getBoundingClientRect().width)+'x'+Math.round(e.getBoundingClientRect().height));
              const imgs=[...document.images].filter(i=>i.getBoundingClientRect().width>0).filter(i=>!i.complete||i.naturalWidth==0).map(i=>i.src.slice(0,80));
              const h1=document.querySelectorAll('h1').length;
              const hs=[...document.querySelectorAll('h1,h2,h3,h4')].map(h=>h.tagName+':'+h.textContent.trim().slice(0,50));
              const hidden=[...document.querySelectorAll('#header,#footer-sections')].map(e=>getComputedStyle(e).display);
              return {sw:document.documentElement.scrollWidth, small, imgs, h1, hs, hidden, formInSlot:!!document.querySelector('.fslot .sqs-block-form')};
            })()""")
            r['vw']=w; res[vp]=r
            if shots: pg.screenshot(path=os.path.join(outdir,f"{tag}_{vp}.png"),full_page=True)
            pg.close()
        b.close()
    return res

if __name__=="__main__":
    page=sys.argv[1]; tag=sys.argv[2]; outdir=sys.argv[3]
    sqs=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','squarespace')
    mock=os.path.join(outdir,f'mock_{tag}.html'); build_mock(page,mock,sqs)
    r=check('file://'+os.path.abspath(mock),tag,outdir,shots='--noshot' not in sys.argv)
    for vp in ('d','m'):
        x=r[vp]; print(tag,vp,'sw',x['sw'],'/',x['vw'],'h1',x['h1'],'small',x['small'],'imgs',x['imgs'],'hidden',x['hidden'],'form',x['formInSlot'])
    if '--headings' in sys.argv: print('\n'.join(r['d']['hs']))
