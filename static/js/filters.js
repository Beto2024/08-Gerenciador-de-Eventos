// filters.js – Lógica dos filtros dinâmicos

document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('filter-form');
  if (!form) return;

  // Submit form when selects change
  ['category-filter', 'status-filter'].forEach(id => {
    const el = document.getElementById(id);
    if (el) {
      el.addEventListener('change', () => {
        // Reset to page 1 on filter change
        const pageInput = form.querySelector('input[name="page"]');
        if (pageInput) pageInput.value = 1;
        form.submit();
      });
    }
  });

  // Clear all filters button
  const clearBtn = document.getElementById('clear-filters');
  if (clearBtn) {
    clearBtn.addEventListener('click', () => {
      window.location.href = window.location.pathname;
    });
  }
});
