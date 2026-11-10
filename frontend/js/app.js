document.addEventListener('DOMContentLoaded', () => {
  // Année du pied de page
  const year = document.getElementById('year');
  if (year) year.textContent = new Date().getFullYear();

  // Menu mobile
  const toggle = document.querySelector('.menu-toggle');
  if (toggle) {
    toggle.addEventListener('click', () => {
      document.querySelector('.topbar').classList.toggle('menu-open');
    });
  }

  // Recherche et filtre du catalogue
  const search = document.getElementById('courseSearch');
  const category = document.getElementById('courseCategory');

  function filterCourses() {
    if (!search || !category) return;
    const q = search.value.toLocaleLowerCase('fr');
    const c = category.value;
    let shown = 0;
    document.querySelectorAll('.course-card').forEach(card => {
      const matchText = card.textContent.toLocaleLowerCase('fr').includes(q);
      const matchCategory = c === 'all' || card.dataset.category === c;
      card.hidden = !(matchText && matchCategory);
      if (!card.hidden) shown++;
    });
    const empty = document.getElementById('emptyState');
    if (empty) empty.hidden = shown !== 0;
  }

  if (search) search.addEventListener('input', filterCourses);
  if (category) category.addEventListener('change', filterCourses);
});
