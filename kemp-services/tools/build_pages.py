import re, os, sys, json, html
HERE=os.path.dirname(os.path.abspath(__file__))
ROOT=os.path.join(HERE,'..')
sys.path.insert(0,HERE)
import build_sqs as B

OUT=os.path.join(ROOT,'squarespace','pages'); os.makedirs(OUT,exist_ok=True)
PHONE='020 8983 8593'; TEL='tel:+442089838593'; EMAIL='info@kempservices.co.uk'
SITE='https://kempservices.co.uk'

ARROW='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m9 6 6 6-6 6"/></svg>'
PHONE_SVG='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.6a2 2 0 0 1-.5 2.1L8 9.7a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.8.3 1.7.5 2.6.7a2 2 0 0 1 1.7 2z"/></svg>'
MAIL_SVG='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="1"/><path d="M3 7l9 6 9-6"/></svg>'
BACK='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m15 6-6 6 6 6"/></svg>'

def U(id,w=1600): return f'https://images.unsplash.com/photo-{id}?w={w}&q=76&auto=format&fit=crop'

SERVICES={
 'contract-cleaning':('Contract cleaning','1718152421680-d1580e843cc9','Operative machine-cleaning a commercial floor','Bespoke and flexible contract cleaning services to office, retail and construction clients in London and across England.'),
 'office-cleaning':('Office cleaning','1577412647305-991150c7d163','Clean open-plan office floor','Our office cleaning team will work to reducing allergens, dust, and mould, which will make your team healthier and more productive.'),
 'construction-cleaning':('Construction cleaning','1768321903661-87da7d2962b0','Interior construction site with metal studs and exposed ceiling','We professionally clean buildings of all shapes and sizes for customers across the UK.'),
 'builders-clean':('Builders clean','1504297050568-910d24c426d3','Newly fitted-out office corridor after a builders clean','We provide high-quality, professional after builders cleans, at the end of any new building, refurbishment or renovation project.'),
 'welfare-area-cleaning':('Welfare area cleaning','1772209415876-76ea6cbc2f0c','Operatives working on the floor of a large empty building','We offer excellent and cost-effective welfare cleaning services. We can attend your premises as frequently as you need it; for contractors of all sizes.'),
 'property-management-cleaning':('Property management cleaning','1760160134936-14284be2a811','Balconies of a modern apartment building at dusk','We have been working in partnership with property management companies, private landlords and letting agents for over 30 years.'),
 'communal-block-cleaning':('Communal block cleaning','1635151925996-cf34cc3805d4','Long communal hallway with doors on both sides','We provide communal area cleaning services to housing associations, property management companies and residential associations.'),
 'pre-post-tenancy-cleans':('Pre and post tenancy cleans','1789352844327-765b16a51b9b','Empty carpeted living area opening into a kitchen','Book a pre/post-tenancy cleaning service to ensure all floors and surfaces are cleaned and the bathroom and kitchen sanitised.'),
 'carpet-floor-cleaning':('Carpet and floor cleaning','1742483359033-13315b247c74','Operative in protective clothing cleaning a carpet','We provide bespoke carpet cleaning services. Our carpet cleaners will take care of your flooring and have it looking like new in no time.'),
 'deep-cleaning':('Deep cleaning','1740657254989-42fe9c3b8cce','Gloved operative cleaning a hard floor','When the task has become overwhelming, it might be time to book us in for a deep clean. Some people opt for a deep clean before selling a property.'),
 'window-cleaning-london':('Window cleaning','1482449609509-eae2a7ea42b7','Window cleaner on a platform cleaning a large glass window','We provide a commercial window cleaning service throughout London and across the UK. We clean windows both internally and externally.'),
}
AREAS={'area-london':'London','contract-cleaning-essex':'Essex','area-kent':'Kent','area-surrey':'Surrey','area-middlesex':'Middlesex'}

IMAGES=[]
def img(id,alt,w=1600,lazy=True):
    IMAGES.append(U(id,w))
    lz=' loading="lazy"' if lazy else ''
    return f'<img src="{U(id,w)}" alt="{html.escape(alt)}"{lz}>'

# ---------- components ----------
def phero(h1,lede,photo,alt,crumb=None,wash=False,cta='Get a quote today'):
    c=f'<a class="crumb" href="{crumb[1]}">{BACK}{crumb[0]}</a>' if crumb else ''
    return f'''<section class="hero phero{' wash' if wash else ''}">
  {img(photo,alt,2000,lazy=False)}
  <div class="inner">
    <div class="copy">
      {c}
      <h1>{h1}</h1>
      <p>{lede}</p>
      <div class="actions">
        <a class="btn" href="/contact">{cta}</a>
        <a class="tel" href="{TEL}">{PHONE_SVG}{PHONE}</a>
      </div>
    </div>
  </div>
</section>'''

def P(paras):
    out=[]
    for i,p in enumerate(paras):
        cls=' class="lede"' if p.startswith('!') else ''
        out.append(f'<p{cls}>{p.lstrip("!")}</p>')
    return '\n'.join(out)

def two(heading,paras,side='',white=True,id=''):
    return f'''<section class="sec {'white' if white else 'navy'}"{f' id="{id}"' if id else ''}>
  <div class="w two">
    <div class="side"><h2>{heading}</h2>{side}</div>
    <div class="text">{P(paras)}</div>
  </div>
</section>'''

def rows(heading,intro,items,white=True,plain=False,cols=False,after=''):
    if plain: lis='\n'.join(f'<li>{t}</li>' for t in items)
    else: lis='\n'.join(f'<li><div><h3>{h}</h3><p>{p}</p></div></li>' for h,p in items)
    cls='rows'+(' plain' if plain else '')+(' cols' if cols else '')
    return f'''<section class="sec {'white' if white else 'navy'}">
  <div class="w">
    <h2>{heading}</h2>
    {('<p class="lede" style="margin-top:22px;max-width:64ch">'+intro+'</p>') if intro else ''}
    <ul class="{cls}" style="margin-top:40px">{lis}</ul>
    {after}
  </div>
</section>'''

def facts(items):
    lis='\n'.join(f'<li><span class="big">{b}</span><p>{p}</p></li>' for b,p in items)
    return f'<section class="facts"><div class="w"><ul>{lis}</ul></div></section>'

def split(heading,paras,photo,alt,rev=False,buttons=(),white=True):
    btns=''.join(f'<a class="{cls}" href="{href}">{label}{ARROW}</a>' for label,href,cls in buttons)
    return f'''<section class="sec {'white' if white else 'navy'}">
  <div class="w split{' rev' if rev else ''}">
    <div class="pic">{img(photo,alt,1200)}</div>
    <div class="text"><h2>{heading}</h2><div style="margin-top:22px">{P(paras)}</div>{btns}</div>
  </div>
</section>'''

def scard(slug,w=900):
    name,pid,alt,_=SERVICES[slug]
    return f'<a class="scard" href="/{slug}">{img(pid,alt,w)}<h3>{name}{ARROW}</h3></a>'

def related(slugs,heading='Related services',intro='',four=False,extra=''):
    cards='\n'.join(scard(s) for s in slugs)
    return f'''<section class="related">
  <div class="w">
    <div class="head"><h2 style="padding-top:28px;position:relative;margin:0;font-size:clamp(1.8rem,1.3rem + 1.6vw,2.6rem);font-weight:500;line-height:1.12;letter-spacing:-.03em;color:var(--navy)">{heading}</h2>{('<p>'+intro+'</p>') if intro else ''}<a class="more" href="/our-services">All our services{ARROW}</a></div>
    <div class="grid{' four' if four else ''}">{cards}</div>
    {extra}
  </div>
</section>'''

def hublist(heading,intro,items,white=True,id=''):
    lis=[]
    for i,it in enumerate(items,1):
        if isinstance(it,str):
            name,pid,alt,desc=SERVICES[it]; href='/'+it; sub=False
        else:
            name,href,pid,alt,desc,sub=it
        pl=f'<span class="plabel">Part of {sub}</span>' if sub else ''
        lis.append(f'<li><a href="{href}"><span class="n">{i:02d}</span><span class="pic">{img(pid,alt,600)}</span><span>{pl}<h3>{name}</h3><p>{desc}</p></span><span class="arr">{ARROW}</span></a></li>')
    return f'''<section class="sec {'white' if white else 'navy'}"{f' id="{id}"' if id else ''}>
  <div class="w">
    <h2>{heading}</h2>
    {('<p class="lede" style="margin-top:22px;max-width:64ch">'+intro+'</p>') if intro else ''}
    <ol class="hublist" style="margin-top:40px">{''.join(lis)}</ol>
  </div>
</section>'''

def compact(featured,white=True):
    rest=[k for k in SERVICES if k not in featured]
    lis=''.join(f'<li><a href="/{k}">{SERVICES[k][0]}</a></li>' for k in rest)
    return f'<div class="compact"><p>Everything else we offer:</p><ul>{lis}</ul></div>'

def towns(heading,intro,names,white=True):
    lis=''.join(f'<li>{n}</li>' for n in names)
    return f'''<section class="sec {'white' if white else 'navy'}">
  <div class="w">
    <h2>{heading}</h2>
    {('<p class="lede" style="margin-top:22px;max-width:64ch">'+intro+'</p>') if intro else ''}
    <div class="towns"><ul>{lis}</ul></div>
  </div>
</section>'''

def band(h2,p,label='Get a quote today'):
    return f'''<section class="sec band">
  <div class="w">
    <div><h2>{h2}</h2><p>{p}</p></div>
    <div class="cta"><a class="btn-dark" href="/contact">{label}{ARROW}</a><a class="tel" href="{TEL}">{PHONE_SVG}{PHONE}</a></div>
  </div>
</section>'''

def contact(h2='Get a quote today.',intro='Tell us about your premises and what you need cleaned, and we will come back to you with a quote.',extra=''):
    return f'''<section class="contact" id="contact" aria-labelledby="contact-heading">
  <div class="cw">
    <div>
      <h2 id="contact-heading">{h2}</h2>
      <p class="cintro">{intro}</p>
      <ul class="cdetails">
        <li><a href="{TEL}">{PHONE_SVG}{PHONE}</a></li>
        <li><a href="mailto:{EMAIL}">{MAIL_SVG}{EMAIL}</a></li>
      </ul>
      {extra}
    </div>
    <div class="fslot">
      <form class="fallback" action="#" method="post">
        <div class="two">
          <label class="field"><span>Name</span><input type="text" name="name" autocomplete="name" required></label>
          <label class="field"><span>Company</span><input type="text" name="company" autocomplete="organization"></label>
        </div>
        <div class="two">
          <label class="field"><span>Email</span><input type="email" name="email" autocomplete="email" required></label>
          <label class="field"><span>Phone</span><input type="tel" name="phone" autocomplete="tel"></label>
        </div>
        <label class="field"><span>Tell us about your premises</span><textarea name="message" rows="5"></textarea></label>
        <button class="send" type="submit">Send enquiry</button>
      </form>
    </div>
  </div>
</section>'''

def guar():
    m=re.search(r'<section class="guar".*?</section>',B.body,re.S).group(0)
    IMAGES.append('https://images.unsplash.com/photo-1669101602108-fa5ba89507ee?w=2000&q=72&auto=format&fit=crop')
    return m

def quote():
    return '''<div class="quote"><blockquote><p>I am writing to thank you very much indeed for the cleaning service provided. Neli, who came to clean our kitchen after some nasty building work, was punctual, fast, thorough and highly skilled. I am very grateful indeed! I hope that Neli will be suitably awarded and made aware of our comments.</p></blockquote><cite>Silvia, customer</cite></div>'''

def ld_service(name,desc,slug,area=None):
    d={"@context":"https://schema.org","@type":"Service","name":name,"serviceType":name,"description":desc,"url":f"{SITE}/{slug}","provider":{"@type":"LocalBusiness","name":"Kemp Services Ltd","telephone":"+442089838593","url":SITE+"/"},"areaServed":area or ["London","Essex","Kent","Surrey","Middlesex","Hertfordshire"]}
    return json.dumps(d,ensure_ascii=False)

# ---------- page assembly ----------
PAGES_CSS=open(os.path.join(HERE,'pages.css')).read()
HOME_CSS=B.prefix_rules(B.css,'.ksl-home',B.home_keep)
PAGE_CSS=B.prefix_rules(B.strip_comments(PAGES_CSS),'.ksl-home',lambda s:True)
REVEAL=B.strip_js_comments(re.search(r'<script>(.*?)</script>',B.body,re.S).group(1)).replace("document.documentElement.classList.add('js');","document.querySelector('.ksl-home').classList.add('js');").strip()

SEO=[]
def page(slug,title,meta,sections,ld=None,needs_guar=False,needs_form=False):
    IMAGES.clear()
    html_sections='\n'.join(sections)
    scripts=[]
    if needs_guar: scripts.append(REVEAL)
    if needs_form: scripts.append(B.FORM_JS)
    if ld: ldtag=f'<script type="application/ld+json">\n{ld}\n</script>\n'
    else: ldtag=''
    out=f"""<style>
{B.FONT}
{B.SQS_FIX}
.ksl-home{{font-family:'Archivo',system-ui,sans-serif;background:#fff;-webkit-font-smoothing:antialiased;}}
{B.base_reset('.ksl-home')}
{HOME_CSS}
{PAGE_CSS}
</style>
<div class="ksl-home">
{html_sections}
</div>
{ldtag}{('<script>'+chr(10)+chr(10).join(scripts)+chr(10)+'</script>') if scripts else ''}
"""
    out=B.tidy(out)
    assert out.count('/*')==0 and out.count('<!--')==0
    open(os.path.join(OUT,slug+'.html'),'w').write(out)
    assert len(title)<=60, (slug,len(title)); assert len(meta)<=155,(slug,len(meta))
    SEO.append((slug,title,meta,list(dict.fromkeys(IMAGES))))
    print(slug,len(out),'{',out.count('{'),'}',out.count('}'))

import content
content.build(globals())

with open(os.path.join(ROOT,'squarespace','seo.md'),'w') as f:
    f.write('# KSL page SEO\n\nOne row per page. Titles are under 60 characters and descriptions under 155. Image URLs are the stock photos currently in each page, listed so they can be swapped for client photography.\n\n')
    f.write('| Slug | Title | Meta description | Images |\n|---|---|---|---|\n')
    for slug,t,m,ims in SEO:
        f.write(f'| /{slug} | {t} | {m} | '+'<br>'.join(ims)+' |\n')
print('pages',len(SEO))
