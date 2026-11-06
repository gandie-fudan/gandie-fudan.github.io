"""Check generated pages and content before every GitHub Pages deployment."""
import json,re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse,unquote
R=Path(__file__).resolve().parent
D=json.loads((R/'content.json').read_text(encoding='utf-8'))
class Page(HTMLParser):
 def __init__(self):super().__init__();self.ids=[];self.links=[];self.records=[];self.current=None
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id' in a:self.ids.append(a['id'])
  for key in ['href','src']:
   if key in a:self.links.append(a[key])
  if 'data-year' in a:self.records.append((a['data-status'],int(a['data-year'])))
pages={}
for f in (R/'dist').glob('*.html'):
 s=f.read_text(encoding='utf-8');p=Page();p.feed(s);pages[f.name]=p
 assert len(p.ids)==len(set(p.ids)),f'Duplicate IDs in {f.name}'
 assert '021-65647856' not in s and 'Handan' not in s and 'cv-llt.pdf' not in s
 expected=len(D['publications']) if f.name.startswith('publications') else sum(bool(x.get('selected')) for x in D['publications']) if f.name.startswith('index') else 0
 assert len(p.records)==expected,f'Publication count differs: {f.name}'
 for status in {x[0] for x in p.records}:
  years=[x[1] for x in p.records if x[0]==status]
  assert years==sorted(years,reverse=True),f'Incorrect chronological order in {f.name}'
assert len(pages)==16,'Expected 8 pages in each language'
for name,p in pages.items():
 for href in p.links:
  u=urlparse(href)
  if u.scheme:assert u.scheme in ['https','http','mailto'];continue
  path=unquote(u.path)
  target=(R/'dist'/path).resolve() if path else R/'dist'/name
  assert target.is_relative_to(R/'dist') and target.is_file(),f'Broken local link: {name}: {href}'
  if u.fragment:assert u.fragment in pages[target.name].ids,f'Broken anchor: {href}'
print(f'PASS: {len(pages)} pages; all assets, navigation and language links; publication counts and descending years; privacy checks.')
