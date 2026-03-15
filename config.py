import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

DATABASE = os.path.join(BASE_DIR, 'database', 'events.db')

SECRET_KEY = os.environ.get('SECRET_KEY', 'gerenciador-eventos-secret-change-in-production')

EVENTS_PER_PAGE = 9

CATEGORIES = [
    ('conferencia', 'Conferência', '#6366f1'),
    ('workshop', 'Workshop', '#8b5cf6'),
    ('meetup', 'Meetup', '#10b981'),
    ('webinar', 'Webinar', '#f59e0b'),
    ('social', 'Social', '#ec4899'),
    ('esportivo', 'Esportivo', '#ef4444'),
    ('cultural', 'Cultural', '#f97316'),
    ('show', 'Show/Festival', '#a855f7'),
    ('viagem', 'Viagem/Passeio', '#06b6d4'),
    ('festa', 'Festa/Celebração', '#e11d48'),
    ('outro', 'Outro', '#64748b'),
]

STATUSES = [
    ('planejado', 'Planejado', '#94a3b8'),
    ('confirmado', 'Confirmado', '#6366f1'),
    ('em_andamento', 'Em Andamento', '#10b981'),
    ('concluido', 'Concluído', '#64748b'),
    ('cancelado', 'Cancelado', '#ef4444'),
]

CATEGORY_DICT = {slug: (label, color) for slug, label, color in CATEGORIES}
STATUS_DICT = {slug: (label, color) for slug, label, color in STATUSES}
