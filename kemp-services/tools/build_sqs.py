import re, base64, os, sys
HERE=os.path.dirname(os.path.abspath(__file__))
ROOT=os.path.join(HERE,'..')
src=open(os.path.join(ROOT,'hero.html')).read()
css=re.search(r'<style>(.*?)</style>',src,re.S).group(1)
body=re.search(r'<body>(.*)</body>',src,re.S).group(1)
logo='data:image/png;base64,'+base64.b64encode(open(os.path.join(ROOT,'ksl-logo.png'),'rb').read()).decode()

def strip_comments(t): return re.sub(r'/\*.*?\*/','',t,flags=re.S)
def strip_js_comments(t):
    t=re.sub(r'/\*.*?\*/','',t,flags=re.S)
    return re.sub(r'^\s*//.*$','',t,flags=re.M)
def tidy(t): return re.sub(r'\n\s*\n+','\n',t).strip()+'\n'

css=strip_comments(css)

def top_blocks(t):
    out=[];depth=0;buf=''
    for ch in t:
        buf+=ch
        if ch=='{':depth+=1
        elif ch=='}':
            depth-=1
            if depth==0: out.append(buf.strip()); buf=''
    return out

def prefix_selector(sel,root):
    parts=[]
    for s in sel.split(','):
        s=s.strip()
        if not s or s in('html','body','html,body'): continue
        if s.startswith('.js '): parts.append(root+'.js '+s[4:])
        elif s.startswith('.js.'): parts.append(root+s[3:])
        else: parts.append(root+' '+s)
    return ','.join(parts)

def prefix_rules(t,root,keep):
    out=[]
    for b in top_blocks(t):
        head,rest=b.split('{',1); rest=rest[:-1]; head=head.strip()
        if head.startswith('@keyframes'): out.append(b); continue
        if head.startswith('@media'):
            inner=prefix_rules(rest,root,keep)
            if inner.strip(): out.append(head+'{'+inner+'}')
            continue
        if head==':root': out.append(root+'{'+rest+'}'); continue
        if head=='html,body': continue
        if head=='body': out.append(root+'{'+rest+'}'); continue
        sels=[x.strip() for x in head.split(',')]
        sels=[x for x in sels if keep(x)]
        if not sels: continue
        out.append(prefix_selector(','.join(sels),root)+'{'+rest+'}')
    return '\n'.join(out)

hdr_keep=lambda s: s.startswith('.site-hdr') or s.startswith('.ntog') or s.startswith('.nbtn')
ftr_keep=lambda s: s.startswith('.site-ftr')
home_keep=lambda s: not(hdr_keep(s) or ftr_keep(s))

FONT="@import url('https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600;700&display=swap');"
def base_reset(root): return f"""{root},{root} *,{root} *::before,{root} *::after{{box-sizing:border-box;}}
{root} h1,{root} h2,{root} h3,{root} h4,{root} p,{root} ul,{root} ol,{root} li,{root} form{{margin:0;padding:0;font-family:inherit;}}
{root} a{{text-decoration:none;color:inherit;background:none;}}
{root} img{{display:block;max-width:100%;border:0;}}
{root} ul{{list-style:none;}}"""

OUT=os.path.join(ROOT,'squarespace')

# header
hdr_html=re.search(r'<header class="site-hdr">.*?</header>',body,re.S).group(0)
hdr_js=re.search(r'<script class="hdr-js">(.*?)</script>',body,re.S).group(1).replace('.site-hdr','.ksl-hdr')
hdr_html=hdr_html.replace('src="ksl-logo.png"',f'src="{logo}"').replace('<header class="site-hdr">','<header class="ksl-hdr">')
hdr_css=prefix_rules(css,'.ksl-hdr',hdr_keep).replace('.ksl-hdr .site-hdr','.ksl-hdr')
header=f"""<style>
{FONT}
#header,.header-announcement-bar-wrapper,.sqs-announcement-bar-dropzone{{display:none !important;}}
.ksl-hdr{{font-family:'Archivo',system-ui,sans-serif;-webkit-font-smoothing:antialiased;}}
{base_reset('.ksl-hdr')}
{hdr_css}
</style>
{hdr_html}
<script>
(function(){{
  var h=document.querySelector('.ksl-hdr');
  function place(){{
    if(h&&document.body&&document.body.firstElementChild!==h){{document.body.insertBefore(h,document.body.firstChild);}}
  }}
  if(document.readyState==='loading'){{document.addEventListener('DOMContentLoaded',place);}}else{{place();}}
}})();
{strip_js_comments(hdr_js).strip()}
</script>
"""
open(os.path.join(OUT,'header.html'),'w').write(tidy(header))

# footer
ftr_html=re.search(r'<footer class="site-ftr">.*?</footer>',body,re.S).group(0)
ftr_html=ftr_html.replace('src="ksl-logo.png"',f'src="{logo}"').replace('<footer class="site-ftr">','<footer class="ksl-ftr">')
ftr_css=prefix_rules(css,'.ksl-ftr',ftr_keep).replace('.ksl-ftr .site-ftr','.ksl-ftr')
footer=f"""<style>
{FONT}
#footer-sections,footer.sections{{display:none !important;}}
.ksl-ftr{{font-family:'Archivo',system-ui,sans-serif;-webkit-font-smoothing:antialiased;}}
{base_reset('.ksl-ftr')}
{ftr_css}
</style>
{ftr_html}
"""
open(os.path.join(OUT,'footer.html'),'w').write(tidy(footer))

# homepage
home_html=re.sub(r'<header class="site-hdr">.*?</header>\n<script class="hdr-js">.*?</script>','',body,flags=re.S)
home_html=re.sub(r'<footer class="site-ftr">.*?</footer>','',home_html,flags=re.S)
script=re.search(r'<script>(.*?)</script>',home_html,re.S).group(1)
home_html=re.sub(r'<script>.*?</script>','',home_html,flags=re.S)
home_html=re.sub(r'<!--.*?-->','',home_html,flags=re.S)
script=strip_js_comments(script).replace("document.documentElement.classList.add('js');","document.querySelector('.ksl-home').classList.add('js');")
home_css=prefix_rules(css,'.ksl-home',home_keep)
SQS_FIX="""#page .page-section:has(.ksl-home){padding:0 !important;min-height:0 !important;}
#page .page-section:has(.ksl-home) .content-wrapper{padding:0 !important;max-width:none !important;width:100% !important;}
#page .page-section:has(.ksl-home) .content{width:100% !important;max-width:none !important;}
#page .page-section:has(.ksl-home) .fluid-engine{display:block !important;grid-template-columns:none !important;}
#page .page-section:has(.ksl-home) .fe-block{position:static !important;width:100% !important;}
#page .page-section:has(.ksl-home) .sqs-block{padding:0 !important;}
#page .page-section:has(.ksl-home) .sqs-block-content{width:100% !important;}
body{overflow-x:clip;}"""
FORM_JS="""(function(){
  var slot=document.querySelector('.ksl-home .fslot');
  if(!slot) return;
  function grab(){
    var forms=document.querySelectorAll('.sqs-block-form');
    for(var i=0;i<forms.length;i++){
      var f=forms[i];
      if(slot.contains(f)) continue;
      var sec=f.closest('.page-section');
      slot.appendChild(f);
      slot.classList.add('has-form');
      if(sec && !sec.contains(slot)) sec.style.display='none';
      return true;
    }
    return false;
  }
  if(grab()) return;
  var mo=new MutationObserver(function(){ if(grab()) mo.disconnect(); });
  mo.observe(document.documentElement,{childList:true,subtree:true});
  document.addEventListener('DOMContentLoaded',grab);
  window.addEventListener('load',function(){ grab(); mo.disconnect(); });
})();"""
HOME_LD='{"@context":"https://schema.org","@type":"LocalBusiness","name":"Kemp Services Ltd","alternateName":"KSL Commercial Cleaning","url":"https://kempservices.co.uk/","telephone":"+442089838593","email":"info@kempservices.co.uk","address":{"@type":"PostalAddress","streetAddress":"Number One, 1 Vicarage Lane","addressLocality":"Stratford, London","postalCode":"E15 4HF","addressCountry":"GB"},"openingHoursSpecification":{"@type":"OpeningHoursSpecification","dayOfWeek":["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],"opens":"07:30","closes":"19:30"},"areaServed":["London","Essex","Kent","Surrey","Middlesex","Hertfordshire"],"sameAs":["https://www.facebook.com/kempservices","https://www.linkedin.com/company/kempservicesltd","https://www.instagram.com/kempservicesltd"]}'
home=f"""<style>
{FONT}
{SQS_FIX}
.ksl-home{{font-family:'Archivo',system-ui,sans-serif;background:#0D1D27;-webkit-font-smoothing:antialiased;}}
{base_reset('.ksl-home')}
{home_css}
</style>
<div class="ksl-home">
{home_html.strip()}
</div>
<script type="application/ld+json">
{HOME_LD}
</script>
<script>
{script.strip()}
{FORM_JS}
</script>
"""
open(os.path.join(OUT,'homepage.html'),'w').write(tidy(home))

# standalone form css
start=css.index('.fslot .sqs-block-form{')
end=css.index('@media (max-width:900px){\n  .contact{padding:72px 0;}')
fcss=css[start:end].replace('.fslot .sqs-block-form','.sqs-block-form')
open(os.path.join(OUT,'form.css'),'w').write(FONT+"\n.sqs-block-form{font-family:'Archivo',system-ui,sans-serif;}\n"+fcss.strip()+'\n')

for f in ['header','footer','homepage']:
    t=open(os.path.join(OUT,f+'.html')).read(); print(f,len(t),t.count('{'),t.count('}'),'comments',t.count('/*')+t.count('<!--'))
