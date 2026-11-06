"""Generate a bilingual GitHub Pages site using Python's standard library."""
import html,json,shutil
from pathlib import Path
from urllib.parse import urlparse
ROOT=Path(__file__).resolve().parent
DATA=json.loads((ROOT/'content.json').read_text(encoding='utf-8'))
OUT=ROOT/'dist'
OUT.mkdir(exist_ok=True)
esc=lambda x:html.escape(str(x),quote=True)
PAGES={'index':('简介','About'),'experience':('经历','Experience'),'publications':('论文','Publications'),'projects':('项目','Projects'),'patents':('专利','Patents'),'honors':('荣誉','Honors'),'teaching':('教学','Teaching'),'service':('服务','Service')}
pubs=sorted(DATA['publications'],key=lambda p:-p['year'])
assert len({p['id'] for p in pubs})==len(pubs),'Publication IDs must be unique'
assert all(p['status'] in ['published','accepted','review','preprint','unspecified'] for p in pubs)
photo=DATA.get('photo','')
if photo:
 resolved=(ROOT/photo).resolve()
 assert resolved.is_relative_to(ROOT/'assets') and resolved.is_file(),'Photo must exist inside assets/'
for lang in ['zh','en']:
 zh=lang=='zh'
 def t(a,b):return a if zh else b
 def url(page,language=None):return page+('' if (language or lang)=='zh' else '-en')+'.html'
 def rows(key):
  return '<div class="timeline">'+''.join('<article class="timeline-row"><p class="date">'+esc(p['date'])+(t('至今','present') if p['date'].endswith('–') else '')+'</p><div>'+('<span class="badge">'+esc(p['role'][lang])+'</span> ' if 'role' in p else '')+esc(p[lang])+'</div></article>' for p in DATA[key])+'</div>'
 status={'preprint':t('预印本','Preprints'),'published':t('已发表','Published'),'accepted':t('已录用','Accepted'),'review':t('在审','Under review'),'unspecified':t('预印本／在审栏目，具体状态未注明','Preprint / under-review section; exact status unspecified')}
 def paper(p):
  links=''
  for link in p.get('links',[]):
   assert urlparse(link['url']).scheme in ['https','http'],'Paper links must use HTTPS or HTTP'
   links+=f'<a class="paper-link" href="{esc(link["url"])}">{esc(link["label"])} ↗</a>'
  title=esc(p['title'])
  target=p.get("publisher_url") or next((x["url"] for x in p.get("links",[]) if x["label"] in ["DOI","arXiv"]),None) or next((x["url"] for x in p.get("links",[])),None)
  if target:
   assert urlparse(target).scheme in ["https","http"]
   title=f'<a href="{esc(target)}">{title}</a>'
  kind={'journal':t('期刊','Journal'),'conference':t('会议','Conference'),'preprint':t('预印本','Preprint')}[p['kind']]
  authors=esc(p['authors']).replace('D. Gan','<strong>D. Gan</strong>').replace('甘叠','<strong>甘叠</strong>')
  return f'<article class="paper" data-year="{p["year"]}" data-status="{p["status"]}" data-kind="{p["kind"]}"><div class="paper-year">{p["year"]}</div><div class="paper-content"><div class="paper-meta">{kind}<span> / </span>{status[p["status"]]}</div><h3 lang="en">{title}</h3><p class="authors" lang="en">{authors}</p><p class="venue" lang="en">{esc(p["venue"])}</p>{links}</div></article>'
 def heading(title,note=''):
  return f'<div class="page-heading"><h1>{title}</h1>{"<p>"+note+"</p>" if note else ""}</div>'
 scholar=f'<a href="{esc(DATA["scholar"])}">Google Scholar ↗</a>' if DATA.get('scholar') else ''
 contact=f'<div class="contact-strip"><div><strong>{esc(DATA["affiliation"][lang])}</strong><p>{t("中国 · 上海","Shanghai, China")}</p></div><a href="mailto:{esc(DATA["email"])}">{esc(DATA["email"])} ↗</a>{scholar}</div>'
 portrait=f'<img class="portrait" src="{esc(photo)}" alt="{esc(DATA["name"][lang])}" width="876" height="1208" fetchpriority="high">' if photo else ''
 home=f'<section class="profile" aria-labelledby="name">{portrait}<div class="profile-copy"><h1 id="name">{esc(DATA["name"][lang])}<span>{t("Die Gan","甘叠")}</span></h1><p class="role">{esc(DATA["role"][lang])}</p><p class="affiliation">{esc(DATA["affiliation"][lang])}</p><p>{t("中国 · 上海","Shanghai, China")}</p><p class="profile-mail"><span>{t("邮箱：","Email: ")}</span><a href="mailto:{esc(DATA["email"])}">{esc(DATA["email"])}</a></p><div class="profile-links">{scholar}<a href="{url("publications")}">{t("论文列表","Publications")}</a></div></div></section>'
 bio=esc(DATA['bio'][lang])
 for phrase in DATA.get('bio_emphasis',{}).get(lang,[]):bio=bio.replace(esc(phrase),'<strong>'+esc(phrase)+'</strong>')
 home+=f'<section class="biography"><h2>{t("个人简介","Brief biography")}</h2><p>{bio}</p>'
 home+=f'<p>{esc(DATA["biography_background"][lang])} <a href="{url("experience")}">{t("详细经历","Full background")} →</a></p></section>'
 home+='<section class="research" aria-labelledby="research-title"><h2 id="research-title">'+t('研究方向','Research interests')+'</h2><div class="research-overview"><ul class="research-list">'+''.join(f'<li><strong>{esc(r[lang][0])}</strong><span>{esc(r[lang][1])}</span></li>' for r in DATA['research'])+'</ul>'
 home+=f'<figure class="network-figure"><p class="figure-title">{t("从观测到辨识","From observations to identification")}</p><img src="assets/research-map.svg" alt="{t("分布式节点协同观测与参数估计的概念示意图","Conceptual illustration of networked observations and parameter estimation")}" width="480" height="340"><figcaption>{t("随机系统 · 分布式学习 · 自适应估计","Stochastic systems · Distributed learning · Adaptive estimation")}</figcaption></figure></div></section>'
 if DATA.get('exploration'):
  ex=DATA['exploration']
  home+=f'<section class="future-research" aria-labelledby="future-title"><h2 id="future-title">{t("未来研究：","Future research: ")}{esc(ex["title"][lang])}</h2><p class="future-intro">{esc(ex["intro"][lang])}</p><div class="future-layout"><figure class="hand-figure"><img src="assets/hand-study.svg" alt="{t("灵巧手关节、输入、观测与在线参数估计的概念示意图","Conceptual sketch of hand joints, inputs, observations and online parameter estimation")}" width="440" height="400" loading="lazy"><figcaption>{t("灵巧手系统辨识概念图","Dexterous-hand system identification concept")}</figcaption><p class="figure-note">{t("输入 u(t) → 观测 y(t) → 参数估计 θ̂(t)","Input u(t) → observations y(t) → parameter estimates θ̂(t)")}</p></figure><div class="research-agenda">'+''.join(f'<article><p class="agenda-number">0{i+1}</p><div><h3>{esc(q[lang][0])}</h3><p>{esc(q[lang][1])}</p></div></article>' for i,q in enumerate(ex['questions']))+'</div></div>'
  if ex.get('approach'):home+=f'<div class="research-approach"><h3>{t("拟开展的研究路径","Proposed research approach")}</h3><p>{esc(ex["approach"][lang])}</p></div>'
  home+=f'<p class="concept-note">{t("以上为拟开展的研究方向；图示用于说明研究思路。","These are prospective research directions; the diagrams illustrate research concepts.")}</p></section>'
 options=lambda pairs:''.join(f'<option value="{k}">{esc(v)}</option>' for k,v in pairs)
 filters=f'<div class="filters"><label for="search">{t("搜索论文","Search publications")}<input id="search" type="search" placeholder="{t("题名、作者、年份…","Title, author, year…")}"></label><label for="kind">{t("类型","Type")}<select id="kind">'+options([('all',t('全部类型','All types')),('journal',t('期刊','Journal')),('conference',t('会议','Conference')),('preprint',t('预印本','Preprint'))])+f'</select></label><label for="status">{t("状态","Status")}<select id="status">'+options([('all',t('全部状态','All statuses'))]+list(status.items()))+'</select></label></div><p id="result-count" role="status" aria-live="polite"></p>'
 publications=heading(t('研究论文','Publications'),t('随机系统、自适应辨识与分布式学习。','Stochastic systems, adaptive identification and distributed learning.'))+f'<p class="editorial-note">{t("* 表示通信作者","* Corresponding author.")}</p><p class="scholar-note">{scholar} · {t("最近核对","Last checked")}: {esc(DATA["publications_verified_on"])}</p><div class="jump-links">'+''.join(f'<a href="#{s}">{status[s]} <span>{sum(p["status"]==s for p in pubs)}</span></a>' for s in ['published','accepted','review','preprint'])+'</div>'+filters+'<div id="all-publications">'
 for state in ['published','accepted','review','preprint','unspecified']:
  group=[p for p in pubs if p['status']==state]
  if group:publications+=f'<section class="publication-group" id="{state}"><h2>{status[state]}</h2>'+''.join(paper(p) for p in group)+'</section>'
 publications+='</div><p id="empty" hidden>'+t('没有匹配的论文。请调整关键词或筛选条件。','No matching publications. Try another keyword or filter.')+'</p>'
 patents=heading(t('专利','Patents'))+'<div class="timeline">'+''.join(f'<article class="timeline-row"><p class="date">{esc(p["date"])}</p><div><span class="badge">{t("审查中","Under examination") if "Under Examination" in p["text"] else t("已授权","Granted")}</span><p lang="en">{esc(p["text"])}</p></div></article>' for p in sorted(DATA['patents'],key=lambda p:p['date'],reverse=True))+'</div>'
 projects=heading(t('科研项目','Research support'),t('以下项目均在简历中列为主持（PI），日期为项目起止时间。','All projects below are listed as PI in the CV. Dates indicate project periods.'))+rows('projects')
 teaching=heading(t('教学工作','Teaching'),t('课程教学与学生指导。','Courses and student mentoring.'))+rows('teaching')+f'<section class="mentoring"><h2>{t("教学与指导成果","Student mentoring")}</h2><p>{esc(DATA["mentoring"][lang])}</p></section>'
 experience=heading(t('教育与工作经历','Experience & education'))+f'<section><h2>{t("工作经历","Appointments")}</h2>'+rows('work')+f'</section><section class="spaced"><h2>{t("教育背景","Education")}</h2>'+rows('education')+'</section>'
 honors=heading(t('荣誉与奖励','Honors & awards'))+rows('honors')
 service=heading(t('学术服务','Professional service'))+rows('service')
 for page,body in dict(index=home,experience=experience,publications=publications,projects=projects,patents=patents,honors=honors,teaching=teaching,service=service).items():
  nav=''.join(f'<a href="{url(k)}" {"aria-current=page" if k==page else ""}>{v[0 if zh else 1]}</a>' for k,v in PAGES.items())
  title=esc(DATA['name'][lang])+' · '+PAGES[page][0 if zh else 1]+' | '+t('复旦大学','Fudan University')
  doc=f'''<!doctype html>
<html lang="{'zh-CN' if zh else 'en'}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title}</title><meta name="description" content="{esc(DATA['bio'][lang])}"><meta name="color-scheme" content="light"><link rel="icon" href="assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="assets/style.css"><link rel="alternate" hreflang="zh-CN" href="{url(page,'zh')}"><link rel="alternate" hreflang="en" href="{url(page,'en')}"><script src="assets/site.js" defer></script></head><body><a class="skip" href="#main">{t('跳转至正文','Skip to content')}</a><header><div class="header-inner"><a class="brand" href="{url('index')}">{esc(DATA['name'][lang])}<span>{t(' / Die Gan',' / 甘叠')}</span></a><nav aria-label="{t('主导航','Main navigation')}">{nav}</nav><a class="language" href="{url(page,'en' if zh else 'zh')}" lang="{'en' if zh else 'zh-CN'}">{t('EN','中文')}</a></div></header><main id="main" class="{page}">{body}</main><footer>{contact}<div class="footer-bottom"><span>© {esc(DATA['name'][lang])} · {t('学术个人主页','Academic website')}</span><a href="#main">{t('返回顶部','Back to top')} ↑</a></div></footer></body></html>'''
  (OUT/url(page)).write_text(doc,encoding='utf-8')
shutil.copytree(ROOT/'assets',OUT/'assets',dirs_exist_ok=True)
(OUT/'.nojekyll').touch()
print(f'Built {len(PAGES)*2} bilingual pages; {len(pubs)} publications; {len(DATA["projects"])} projects.')
