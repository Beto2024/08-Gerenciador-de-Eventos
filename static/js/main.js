// main.js – Scripts principais

document.addEventListener('DOMContentLoaded', () => {
  // Auto-dismiss flash messages after 4 seconds
  const flashes = document.querySelectorAll('.flash-message');
  flashes.forEach(el => {
    setTimeout(() => {
      el.style.transition = 'opacity 0.5s ease';
      el.style.opacity = '0';
      setTimeout(() => el.remove(), 500);
    }, 4000);
  });

  // Confirm delete buttons
  document.querySelectorAll('.confirm-delete').forEach(form => {
    form.addEventListener('submit', e => {
      if (!confirm('Tem certeza que deseja excluir este evento? Esta ação não pode ser desfeita.')) {
        e.preventDefault();
      }
    });
  });

  // Highlight active nav link
  const currentPath = window.location.pathname;
  document.querySelectorAll('.nav-link').forEach(link => {
    const href = link.getAttribute('href');
    if (href && (currentPath === href || (href !== '/' && currentPath.startsWith(href)))) {
      link.classList.add('nav-link-active');
    }
  });
});
