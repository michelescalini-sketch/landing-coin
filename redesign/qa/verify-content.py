from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse,unquote
from collections import Counter
import json,xml.etree.ElementTree as ET,re,zipfile
BASE=Path(__file__).resolve().parents[2]/'docs';pages={};errors=[]
VOID={'meta','link','img','input','br','hr','source','area','base','embed','param','track','wbr'}
class Parser(HTMLParser):
 def __init__(self):super().__init__();self.nodes=[];self.stack=[];self.errors=[]
 def handle_starttag(self,t,a):
  self.nodes.append((t,dict(a)))
  if t not in VOID:self.stack.append(t)
 def handle_endtag(self,t):
  if not self.stack or self.stack[-1]!=t:self.errors.append((t,self.stack[-3:]))
  else:self.stack.pop()
 def handle_startendtag(self,t,a):self.nodes.append((t,dict(a)))
titles=[];descriptions=[]
manifest=json.loads((BASE.parent/'redesign/source-manifest.json').read_text())
redirects=set(manifest['redirects'])
for f in sorted(f for f in BASE.rglob('*.html') if f.relative_to(BASE).as_posix() not in redirects):
 source=f.read_text();p=Parser();p.feed(source);ids=[a['id']for t,a in p.nodes if'id'in a]
 assert not p.errors and not p.stack,(f.name,p.errors,p.stack)
 assert len(ids)==len(set(ids)),(f.name,'duplicate IDs')
 assert sum(t=='h1'for t,a in p.nodes)==1,(f.name,'H1')
 assert 'LandingCoinFun'not in source and 'X · suspended'not in source,(f.name,'old social account')
 assert 'https://x.com/LandingCoin2026'in source and 'https://www.linkedin.com/company/146683351'in source
 titles.append(re.search(r'<title>(.*?)</title>',source,re.S)[1]);descriptions.append(next(a['content']for t,a in p.nodes if t=='meta'and a.get('name')=='description'))
 for data in re.findall(r'<script type="application/ld\+json">(.*?)</script>',source,re.S):json.loads(data)
 for t,a in p.nodes:
  for key in ['aria-controls','aria-labelledby']:
   assert all(x in ids for x in a.get(key,'').split()),(f.name,key)
  if a.get('target')=='_blank':assert 'noopener'in a.get('rel','')
 pages[f.resolve()]=(p,ids)
assert len(titles)==len(set(titles)),'Duplicate titles'
assert len(descriptions)==len(set(descriptions)),'Duplicate descriptions'
for f,(p,ids)in pages.items():
 for t,a in p.nodes:
  for key in ['href','src','poster']:
   raw=a.get(key,'');u=urlparse(raw)
   if not raw or u.scheme or u.netloc:continue
   path=unquote(u.path);target=(BASE/path.lstrip('/') if path.startswith('/')else f.parent/path).resolve()if path else f
   if path.endswith('/')or target.is_dir():target=target/'index.html'
   assert target.exists(),(f.name,raw)
   if u.fragment:
    if target.suffix=='.html':assert u.fragment in pages[target.resolve()][1],(f.name,raw)
    if target.suffix=='.svg':assert any(x.get('id')==u.fragment for x in ET.parse(target).iter()),(f.name,raw)
for f in BASE.glob('*.css'):
 source=f.read_text();assert source.count('{')==source.count('}'),f.name
 for raw in re.findall(r'url\([\'"]?([^\'"\)]+)',source):
  if not raw.startswith(('data:','https:')):assert (f.parent/raw).exists(),(f.name,raw)
for f in BASE.rglob('*.xml'):ET.parse(f)
with zipfile.ZipFile(BASE/'assets/LANDING-media-kit.zip')as z:assert z.testzip()is None
faq=(BASE/'faq.html').read_text();data=json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>',faq,re.S)[1]);schema=next(x for x in data['@graph']if 'FAQPage' in (x['@type'] if isinstance(x['@type'],list) else [x['@type']]));assert len(schema['mainEntity'])==17
for item in schema['mainEntity']:assert item['name']in faq and item['acceptedAnswer']['text'].replace('’','’')in __import__('html').unescape(faq)
for name in ['privacy.html','cookie-policy.html','terms-of-service.html']:
 source=(BASE/name).read_text()
 assert 'CURRENT POLICY'in source
 assert 'PREPARED FOR FINAL OWNER REVIEW'not in source
 assert 'Source required.'not in source
assert 'DESIGN EXAMPLE / 001'not in(BASE/'index.html').read_text(),'No simulated public Wall posts'
print(f'PASS: {len(pages)} production HTML pages, unique metadata, internal links/assets/anchors, ARIA, schemas, 17 visible FAQ answers, sitemap/RSS, media ZIP, official socials and three current legal policy pages.')
