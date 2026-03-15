import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

DATABASE = os.path.join(BASE_DIR, 'database', 'events.db')

SECRET_KEY = os.environ.get('SECRET_KEY', 'gerenciador-eventos-secret-change-in-production')

EVENTS_PER_PAGE = 9

CATEGORIES = [
    ('conferencia', 'Conferência', '#5a9fcf'),
    ('workshop', 'Workshop', '#9a7ec8'),
    ('meetup', 'Meetup', '#4fb896'),
    ('webinar', 'Webinar', '#e0a642'),
    ('social', 'Social', '#d47fa8'),
    ('esportivo', 'Esportivo', '#e07a5f'),
    ('cultural', 'Cultural', '#d48f50'),
    ('show', 'Show/Festival', '#a07ad4'),
    ('viagem', 'Viagem/Passeio', '#4ab8c4'),
    ('festa', 'Festa/Celebração', '#e06b80'),
    ('outro', 'Outro', '#8a8279'),
]

STATUSES = [
    ('planejado', 'Planejado', '#a09890'),
    ('confirmado', 'Confirmado', '#2e9e8f'),
    ('em_andamento', 'Em Andamento', '#4fb896'),
    ('concluido', 'Concluído', '#8a8279'),
    ('cancelado', 'Cancelado', '#d96a5a'),
]

CATEGORY_DICT = {slug: (label, color) for slug, label, color in CATEGORIES}
STATUS_DICT = {slug: (label, color) for slug, label, color in STATUSES}
