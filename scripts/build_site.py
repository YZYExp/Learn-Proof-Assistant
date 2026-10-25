#!/usr/bin/env python3
"""Build and validate a static reading site without the book export toolchain."""
import argparse, html, json, re, shutil
from pathlib import Path
from urllib.parse import urlsplit, unquote
from html.parser import HTMLParser
import markdown
ROOT=Path(__file__).resolve().parents[1]

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--base-path',default='/');args=ap.parse_args()
 base='/'+args.base_path.strip('/')+'/' if args.base_path.strip('/') else '/'
 if not re.fullmatch(r'/[A-Za-z0-9_/-]*',base):raise ValueError('Invalid base path')
 book=json.loads((ROOT/'book.json').read_text());out=ROOT/'build/site'
 if out.exists():shutil.rmtree(out)
 out.mkdir(parents=True)
 chapters=book['chapters']+book.get('appendices',[])
 routes={c['source']:c['slug']+'.html' for c in chapters}
 routes.update({'README.md':'index.html','VERIFICATION.md':'verification.html','references/README.md':'references.html'})
 pages=chapters+[{'source':'VERIFICATION.md','title':'检查状态','slug':'verification'},{'source':'references/README.md','title':'资料索引','slug':'references'}]
 def esc(x):return html.escape(str(x),quote=True)
 def url(path):return base+path
 def nav(active):
  links=[]
  for i,c in enumerate(chapters,1):
   current='aria-current="page"' if c['slug']==active else ''
   links.append(f'<a {current} href="{url(c["slug"]+".html")}"><span>{i:02}</span>{esc(c["title"])}</a>')
  return ''.join(links)
 def shell(title,body,active=''):
  return f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="{esc(book['description'])}"><title>{esc(title)} · 证明有据</title><link rel="stylesheet" href="{url('static/style.css')}"><script defer src="{url('static/app.js')}"></script></head><body><a class="skip" href="#main">跳到正文</a><header class="top"><a class="brand" href="{base}">∴ <strong>证明有据</strong><small>Lean × Rocq</small></a><nav aria-label="辅助导航"><a href="{base}#catalog">目录</a><a href="{url('references.html')}">资料</a><a href="{url('downloads/Lean-Rocq.epub')}">EPUB ↓</a><a href="https://github.com/YZYExp/Learn-Proof-Assistant">GitHub ↗</a></nav></header><div class="layout"><aside><details open><summary>阅读目录</summary><nav aria-label="章节目录">{nav(active)}</nav><a class="status-link" href="{url('verification.html')}">示例代码检查状态 ↗</a></details></aside><main id="main">{body}</main></div><footer>证明有据 · 从陈述到证据，从概念到实践。<a href="{url('verification.html')}">检查状态</a></footer></body></html>'''
 def rewrite(content,source):
  def replace(m):
   attr,quote,target=m.groups();v=html.unescape(target);u=urlsplit(v)
   if u.scheme or u.netloc or v.startswith(('#','data:')):return m.group(0)
   target_path=(ROOT/Path(source).parent/unquote(u.path)).resolve()
   try:rel=target_path.relative_to(ROOT).as_posix()
   except ValueError:raise ValueError('Link escapes source root: '+v)
   if not target_path.is_file():raise ValueError(f'Missing source link: {source}: {v}')
   dest=routes.get(rel,rel)
   return f'{attr}={quote}{esc(url(dest)+("#"+u.fragment if u.fragment else ""))}{quote}'
  return re.sub(r'(href|src)=([\"\x27])([^\"\x27]*)\2',replace,content)
 def render(source):
  txt=(ROOT/source).read_text()
  converted=markdown.markdown(txt,extensions=['fenced_code','tables','toc','sane_lists'])
  return rewrite(converted,source),txt
 index=[]
 for i,p in enumerate(pages):
  content,txt=render(p['source']);slug=p['slug']
  prev=chapters[i-1] if 0<i<len(chapters) else None
  nxt=chapters[i+1] if i+1<len(chapters) else None
  links='<nav class="pager" aria-label="前后章">'
  links+=f'<a href="{url(prev["slug"]+".html")}">← {esc(prev["title"])}</a>' if prev else f'<a href="{base}">← 首页</a>'
  if nxt:links+=f'<a href="{url(nxt["slug"]+".html")}">{esc(nxt["title"])} →</a>'
  links+='</nav>'
  body=f'<div class="eyebrow">{("第 "+str(i+1)+" 章") if i<12 else "阅读资料"} / LEAN × ROCQ</div><article>{content}</article>{links}'
  (out/(slug+'.html')).write_text(shell(p['title'],body,slug))
  index.append({'title':p['title'],'url':url(slug+'.html'),'text':re.sub(r'\s+',' ',re.sub(r'<[^>]+>',' ',content))})
 cards=''.join(f'<a class="chapter-card" href="{url(c["slug"]+".html")}"><span>{i:02}</span><h3>{esc(c["title"])}</h3><p>{esc(["概念与观察","动手构造证据","规格与证明工程"][min((i-1)//4,2)]) if i<=12 else "辅助阅读"} →</p></a>' for i,c in enumerate(chapters,1))
 body=f'''<section class="hero"><div class="eyebrow">一本关于形式化证明的图解入门书</div><h1>让每一步推理，<br>都有据可查。</h1><p class="lead">用 Lean 与 Rocq 研究同一个问题：怎样把一个精确的陈述，变成机器能够检查的证明。</p><div class="actions"><a class="primary" href="{url(chapters[0]['slug']+'.html')}">开始阅读 →</a><a href="{url('downloads/Lean-Rocq.epub')}">下载 EPUB ↓</a></div><div class="stats"><span><b>12</b> 个主题章节</span><span><b>12</b> 幅教学图解</span><span><b>2</b> 种证明语言</span></div></section><section class="feature"><div><div class="eyebrow">从一个小证明开始</div><h2>相同的逻辑，<br>两种表达。</h2><p>把 P 与 Q 的证据拆开，再组合成 Q 与 P。先理解证据的结构，再认识具体策略。</p><a href="{url('first-proofs.html')}">进入双语言实作 →</a></div><img src="{url('assets/images/fig-05.svg')}" alt="合取交换的证据路线：拆开 P 和 Q，再按相反顺序组合" width="960" height="640"></section><section class="routes"><h2>选择你的阅读路线</h2><p><b>理解概念：</b>先读 1—3 章，再看规格与真实项目。<br><b>动手证明：</b>依次完成 5—8 章的双语言示例与练习。<br><b>走向工程：</b>重点阅读 9—12 章的规格、库与可复现方法。</p><p class="note">示例代码已静态审阅，尚未在 Lean / Rocq 工具链中实际编译。<a href="{url('verification.html')}">查看检查记录</a>。</p></section><section id="catalog"><div class="catalog-head"><h2>全书目录</h2><label>搜索书中内容<input type="search" id="search" placeholder="例如：归纳、规格、重写" autocomplete="off"></label></div><p id="search-status" role="status"></p><div id="results" class="search-results"></div><div id="chapter-grid" class="chapter-grid">{cards}</div></section>'''
 (out/'index.html').write_text(shell(book['title'],body))
 (out/'static').mkdir()
 for name in ['style.css','app.js']:shutil.copy2(ROOT/'site'/name,out/'static'/name)
 shutil.copytree(ROOT/'assets',out/'assets')
 shutil.copytree(ROOT/'examples',out/'examples')
 (out/'downloads').mkdir();epub=ROOT/'downloads/Lean-Rocq.epub'
 if not epub.is_file():raise ValueError('EPUB download missing')
 shutil.copy2(epub,out/'downloads'/epub.name)
 (out/'static/search.json').write_text(json.dumps(index,ensure_ascii=False))
 (out/'.nojekyll').touch()
 validate(out,base)
 print(f'Built {len(pages)+1} pages; local links and resources validated: {out}')

def validate(out,base):
 class Links(HTMLParser):
  def __init__(self):super().__init__();self.targets=[];self.ids=set()
  def handle_starttag(self,tag,attrs):
   a=dict(attrs)
   if 'id' in a:self.ids.add(a['id'])
   for k in ['href','src']:
    if k in a:self.targets.append(a[k])
 parsed={}
 for p in out.glob('*.html'):
  parser=Links();parser.feed(p.read_text());parsed[p]=parser
 for p,parser in parsed.items():
  for target in parser.targets:
   u=urlsplit(target)
   if u.scheme or u.netloc:continue
   if u.path:
    if not u.path.startswith(base):raise ValueError(f'Wrong base path: {target}')
    file=out/unquote(u.path[len(base):]);file=file/'index.html' if file.is_dir() else file
   else:file=p
   if not file.is_file():raise ValueError(f'Broken link in {p.name}: {target}')
   if u.fragment and file in parsed and unquote(u.fragment) not in parsed[file].ids:raise ValueError(f'Broken fragment: {target}')

if __name__=='__main__':main()
