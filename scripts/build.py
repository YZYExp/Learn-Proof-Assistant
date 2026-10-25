#!/usr/bin/env python3
"""Check sources and build merged Markdown and EPUB; never writes a website."""
import json,re,subprocess,zipfile,xml.etree.ElementTree as ET
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
manifest=json.loads((ROOT/'book.json').read_text())
out=ROOT/'build';out.mkdir(exist_ok=True)
parts=[];seen=set();images=set()
for chapter in manifest['chapters']:
 p=ROOT/chapter['source']
 text=p.read_text()
 assert text.startswith('# '),p
 assert chapter['id'] not in seen
 seen.add(chapter['id'])
 for target in re.findall(r'!\[[^\]]*\]\(([^)]+)\)',text):
  img=(p.parent/target).resolve()
  assert img.is_file(),(p,target)
  images.add(img)
 assert text.count('```')%2==0,p
 assert not re.search(r'\b(TODO|TBD)\b',text),p
 # Rebase local source paths for reading at project root.
 # Chapter and build directories are siblings, so relative image paths remain valid.
 parts.append(text)
for p in sorted((ROOT/'appendices').glob('*.md')):
 parts.append(p.read_text().replace('../assets/','assets/'))
for p in images: ET.parse(p)
merged=out/'Lean-Rocq-Complete.md'
merged.write_text('---\ntitle: "'+manifest['title']+'"\nlang: zh-CN\nauthor: "图解知识书系列"\n---\n\n'+ '\n\n'.join(parts))
subprocess.run(['pandoc',str(merged),'-o',str(out/'Lean-Rocq.epub'),'--toc','--toc-depth=2','--split-level=1','--resource-path='+str(out),'--css='+str(ROOT/'scripts/epub.css')],cwd=ROOT,check=True)
# Some Pandoc builds label plain SVG as .svgz; normalize extensions and references.
epub=out/'Lean-Rocq.epub'
normalized=out/'normalized.epub'
with zipfile.ZipFile(epub) as src, zipfile.ZipFile(normalized,'w') as dst:
 for item in src.infolist():
  data=src.read(item.filename)
  if item.filename.endswith(('.xhtml','.opf','.ncx','.xml')):
   data=data.replace(b'.svgz',b'.svg')
  item.filename=item.filename.replace('.svgz','.svg')
  dst.writestr(item,data)
normalized.replace(epub)
with zipfile.ZipFile(epub) as z:
 assert z.read('mimetype')==b'application/epub+zip'
 assert len([n for n in z.namelist() if n.endswith('.svg')])==len(images)
 for n in z.namelist():
  if n.endswith(('.xhtml','.opf','.xml')):ET.fromstring(z.read(n))
print(json.dumps({'chapters':len(seen),'illustrations':len(images),'merged_characters':len(merged.read_text()),'epub':'build/Lean-Rocq.epub'},ensure_ascii=False))
