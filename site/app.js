'use strict';
const details = document.querySelector('aside details');
if (details && matchMedia('(max-width:720px)').matches) details.open = false;
const search = document.querySelector('#search');
if (search) {
  const grid = document.querySelector('#chapter-grid');
  const results = document.querySelector('#results');
  const status = document.querySelector('#search-status');
  let indexPromise;
  let generation = 0;
  search.addEventListener('input', async () => {
    const current = ++generation;
    const query = search.value.trim().toLocaleLowerCase();
    results.replaceChildren();
    grid.hidden = Boolean(query);
    if (!query) { status.textContent = ''; return; }
    try {
      indexPromise ||= fetch(new URL('search.json', document.querySelector('script[src$="app.js"]').src)).then(r => {
        if (!r.ok) throw new Error('Search unavailable');
        return r.json();
      }).catch(error => { indexPromise = null; throw error; });
      const index = await indexPromise;
      if (current !== generation) return;
      const matches = index.filter(item => (item.title + ' ' + item.text).toLocaleLowerCase().includes(query));
      status.textContent = `找到 ${matches.length} 个相关章节`;
      matches.forEach(item => {
        const a = document.createElement('a');
        a.href = item.url;
        const title = document.createElement('strong'); title.textContent = item.title;
        const excerpt = document.createElement('p');
        const at = Math.max(0, item.text.toLocaleLowerCase().indexOf(query) - 30);
        excerpt.textContent = '…' + item.text.slice(at, at + 150) + '…';
        a.append(title, excerpt); results.append(a);
      });
    } catch (_) {
      if (current === generation) { status.textContent = '搜索暂不可用，请使用下方目录。'; grid.hidden = false; }
    }
  });
}
