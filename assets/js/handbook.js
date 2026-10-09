/* Progressive enhancement: document navigation remains usable without JavaScript. */
(() => {
  const article = document.querySelector('.handbook-article');
  if (!article) return;
  const headings = [...article.querySelectorAll('h2[id]')];
  if (headings.length < 2) return;
  const details = document.createElement('details');
  details.className = 'handbook-toc';
  details.open = window.matchMedia('(min-width: 641px)').matches;
  const summary = document.createElement('summary');
  summary.textContent = `本页目录 · ${headings.length} 节`;
  const nav = document.createElement('nav');
  nav.setAttribute('aria-label', '本页目录');
  const list = document.createElement('ol');
  headings.forEach(heading => {
    const item = document.createElement('li');
    const link = document.createElement('a');
    link.href = '#' + encodeURIComponent(heading.id);
    link.textContent = heading.textContent;
    item.append(link);
    list.append(item);
  });
  nav.append(list);
  details.append(summary, nav);
  headings[0].before(details);
})();
