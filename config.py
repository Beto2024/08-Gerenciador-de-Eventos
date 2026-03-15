import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

DATABASE = os.path.join(BASE_DIR, 'database', 'events.db')

SECRET_KEY = os.environ.get('SECRET_KEY', 'gerenciador-eventos-secret-change-in-production')

EVENTS_PER_PAGE = 9

CATEGORIES = [
    ('conferencia', 'Conferência', '#3b82f6'),
    ('workshop', 'Workshop', '#8b5cf6'),
    ('meetup', 'Meetup', '#10b981'),
    ('webinar', 'Webinar', '#f59e0b'),
    ('social', 'Social', '#ec4899'),
    ('esportivo', 'Esportivo', '#ef4444'),
    ('cultural', 'Cultural', '#f97316'),
    ('show', 'Show/Festival', '#a855f7'),
    ('viagem', 'Viagem/Passeio', '#06b6d4'),
    ('festa', 'Festa/Celebração', '#f43f5e'),
    ('outro', 'Outro', '#6b7280'),
]

STATUSES = [
    ('planejado', 'Planejado', '#94a3b8'),
    ('confirmado', 'Confirmado', '#3b82f6'),
    ('em_andamento', 'Em Andamento', '#10b981'),
    ('concluido', 'Concluído', '#6b7280'),
    ('cancelado', 'Cancelado', '#ef4444'),
]

CATEGORY_DICT = {slug: (label, color) for slug, label, color in CATEGORIES}
STATUS_DICT = {slug: (label, color) for slug, label, color in STATUSES}
