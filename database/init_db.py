import sqlite3
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import DATABASE

CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    start_date DATE NOT NULL,
    end_date DATE,
    start_time TIME,
    end_time TIME,
    location TEXT,
    category TEXT NOT NULL DEFAULT 'outro',
    status TEXT NOT NULL DEFAULT 'planejado',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

SEED_EVENTS = [
    (
        'PyCon Brasil 2026',
        'A maior conferência de Python do Brasil. Palestras, workshops e networking com desenvolvedores de todo o país.',
        '2026-03-20', '2026-03-22', '09:00', '18:00',
        'Centro de Convenções Frei Caneca, São Paulo - SP',
        'conferencia', 'confirmado'
    ),
    (
        'Workshop de Flask e APIs REST',
        'Workshop prático sobre criação de APIs REST com Flask, SQLAlchemy e boas práticas de desenvolvimento.',
        '2026-03-18', '2026-03-18', '14:00', '17:00',
        'Online - Google Meet',
        'workshop', 'confirmado'
    ),
    (
        'Meetup Python SP - Março',
        'Encontro mensal da comunidade Python de São Paulo. Talks sobre machine learning e automação.',
        '2026-03-25', '2026-03-25', '19:00', '22:00',
        'Google Brasil, São Paulo - SP',
        'meetup', 'planejado'
    ),
    (
        'Webinar: Introdução ao FastAPI',
        'Webinar gratuito sobre FastAPI, o framework moderno para criação de APIs em Python.',
        '2026-03-28', '2026-03-28', '20:00', '21:30',
        'Online - YouTube Live',
        'webinar', 'planejado'
    ),
    (
        'Hackathon de Inteligência Artificial',
        '48 horas de desafios de IA. Equipes de até 4 pessoas. Prêmios para os 3 primeiros lugares.',
        '2026-04-04', '2026-04-06', '08:00', '20:00',
        'Campus Party Brasil, São Paulo - SP',
        'conferencia', 'planejado'
    ),
    (
        'Workshop: Docker e Kubernetes na Prática',
        'Aprenda a containerizar aplicações e orquestrar com Kubernetes em ambiente de produção.',
        '2026-04-10', '2026-04-11', '09:00', '17:00',
        'Alura, São Paulo - SP',
        'workshop', 'planejado'
    ),
    (
        'JS Conf Brasil 2026',
        'Conferência nacional de JavaScript. Front-end, Node.js, TypeScript e as últimas tendências do ecossistema JS.',
        '2026-04-15', '2026-04-17', '09:00', '19:00',
        'Hotel Maksoud Plaza, São Paulo - SP',
        'conferencia', 'planejado'
    ),
    (
        'Corrida Tech 5K',
        'Corrida solidária organizada pela comunidade tech. Percurso de 5km pelo Parque Ibirapuera.',
        '2026-04-19', '2026-04-19', '07:00', '10:00',
        'Parque Ibirapuera, São Paulo - SP',
        'esportivo', 'planejado'
    ),
    (
        'Show de Rock Beneficente',
        'Show beneficente com bandas locais. Renda revertida para projetos de inclusão digital.',
        '2026-03-29', '2026-03-29', '19:00', '23:00',
        'Audio Club, São Paulo - SP',
        'cultural', 'confirmado'
    ),
    (
        'Meetup UX/UI Design',
        'Encontro para designers e desenvolvedores front-end. Tema: Design Systems e acessibilidade.',
        '2026-04-02', '2026-04-02', '18:30', '21:00',
        'WeWork Paulista, São Paulo - SP',
        'meetup', 'planejado'
    ),
    (
        'Webinar: Segurança em Aplicações Web',
        'Como proteger suas aplicações contra OWASP Top 10. Exemplos práticos com Python e Flask.',
        '2026-04-08', '2026-04-08', '19:00', '20:30',
        'Online - Zoom',
        'webinar', 'planejado'
    ),
    (
        'Confraternização da Equipe Dev',
        'Happy hour e jantar de integração da equipe de desenvolvimento. Celebrando os resultados do Q1 2026.',
        '2026-03-27', '2026-03-27', '19:00', '23:00',
        'Restaurante Spot, São Paulo - SP',
        'social', 'confirmado'
    ),
    (
        'DevFest São Paulo 2026',
        'Google Developer Festival com palestras sobre Android, Flutter, Firebase, Google Cloud e muito mais.',
        '2026-05-02', '2026-05-03', '09:00', '18:00',
        'FIAP, São Paulo - SP',
        'conferencia', 'planejado'
    ),
    (
        'Workshop de Tailwind CSS',
        'Aprenda a criar interfaces modernas com Tailwind CSS. Do básico ao avançado com projetos reais.',
        '2026-03-16', '2026-03-16', '09:00', '13:00',
        'Online - Discord',
        'workshop', 'em_andamento'
    ),
    (
        'Expo Tech 2026',
        'Exposição de tecnologia com demos de produtos inovadores, startups e grandes empresas de tecnologia.',
        '2026-02-14', '2026-02-16', '10:00', '20:00',
        'Expo Center Norte, São Paulo - SP',
        'conferencia', 'concluido'
    ),
]


def init_db():
    """Inicializa o banco de dados e insere dados de seed."""
    os.makedirs(os.path.dirname(DATABASE), exist_ok=True)
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(CREATE_TABLE)

    cursor.execute("SELECT COUNT(*) FROM events")
    count = cursor.fetchone()[0]

    if count == 0:
        cursor.executemany(
            """INSERT INTO events
               (title, description, start_date, end_date, start_time, end_time,
                location, category, status)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            SEED_EVENTS
        )
        print(f"[DB] {len(SEED_EVENTS)} eventos de exemplo inseridos.")

    conn.commit()
    conn.close()
    print(f"[DB] Banco de dados inicializado em: {DATABASE}")


if __name__ == '__main__':
    init_db()
