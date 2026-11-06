const search = document.querySelector('#search');
if (search) {
  const kind = document.querySelector('#kind');
  const status = document.querySelector('#status');
  const papers = [...document.querySelectorAll('#all-publications .paper')];
  function filter() {
    const query = search.value.trim().toLocaleLowerCase();
    let count = 0;
    for (const paper of papers) {
      const show = paper.textContent.toLocaleLowerCase().includes(query) && (kind.value === 'all' || kind.value === paper.dataset.kind) && (status.value === 'all' || status.value === paper.dataset.status);
      paper.hidden = !show;
      if (show) count++;
    }
    for (const group of document.querySelectorAll('.publication-group')) group.hidden = ![...group.querySelectorAll('.paper')].some(p => !p.hidden);
    document.querySelector('#result-count').textContent = document.documentElement.lang === 'zh-CN' ? `显示 ${count} / ${papers.length} 篇论文` : `Showing ${count} of ${papers.length} publications`;
    document.querySelector('#empty').hidden = count !== 0;
  }
  search.addEventListener('input', filter);
  kind.addEventListener('change', filter);
  status.addEventListener('change', filter);
  filter();
}
