// calendar.js – Lógica do calendário

document.addEventListener('DOMContentLoaded', () => {
  // Event tooltip / highlight on hover
  const calEvents = document.querySelectorAll('.calendar-event');
  calEvents.forEach(ev => {
    ev.addEventListener('mouseenter', () => {
      ev.style.opacity = '0.8';
    });
    ev.addEventListener('mouseleave', () => {
      ev.style.opacity = '1';
    });
  });
});
