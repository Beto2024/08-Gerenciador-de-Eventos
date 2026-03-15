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
        'Carnatal 2026',
        'O maior carnaval fora de época do Brasil. Três dias de festa com os melhores artistas do axé, forró e pagode nas ruas de Natal.',
        '2026-06-11', '2026-06-14', '18:00', '04:00',
        'Parque de Exposições, Natal - RN',
        'festa', 'confirmado'
    ),
    (
        'Réveillon de Ponta Negra',
        'Festa de Ano Novo na praia mais famosa de Natal, com show pirotécnico, atrações musicais ao vivo e muito forró na areia.',
        '2026-02-28', '2026-02-28', '20:00', '04:00',
        'Praia de Ponta Negra, Natal - RN',
        'festa', 'confirmado'
    ),
    (
        'Circuito de Surf de Pipa',
        'Etapa nordestina do campeonato brasileiro de surf. Ondas perfeitas e competição de alto nível na praia mais bonita do RN.',
        '2026-03-06', '2026-03-08', '07:00', '17:00',
        'Praia da Pipa, Tibau do Sul - RN',
        'esportivo', 'confirmado'
    ),
    (
        'Show: Alceu Valença na Arena das Dunas',
        'Show imperdível do rei do frevo e da música pernambucana na moderna arena multiuso de Natal.',
        '2026-03-21', '2026-03-21', '20:00', '23:30',
        'Arena das Dunas, Natal - RN',
        'show', 'confirmado'
    ),
    (
        'Passeio de Buggy pelas Dunas',
        'Aventura de buggy pelas dunas do litoral norte do RN, saindo de Genipabu até Maracajaú. Inclui parada nas lagoas e morro do careca.',
        '2026-04-04', '2026-04-05', '08:00', '17:00',
        'Dunas de Genipabu, Extremoz - RN',
        'viagem', 'planejado'
    ),
    (
        'São João de Caruaru 2026',
        'O maior São João do mundo! Quadrilhas, forró pé de serra, comidas típicas e toda a magia do maior arraial do Brasil.',
        '2026-06-10', '2026-06-24', '18:00', '02:00',
        'Pátio de Eventos Luiz Gonzaga, Caruaru - PE',
        'festa', 'confirmado'
    ),
    (
        'Rock in Rio 2026',
        'O maior festival de música do mundo retorna ao Rio de Janeiro com lineup internacional de peso. Sete dias de rock, pop e muito mais.',
        '2026-07-11', '2026-07-19', '14:00', '02:00',
        'Cidade do Rock, Rio de Janeiro - RJ',
        'show', 'confirmado'
    ),
    (
        'Carnaval de Salvador 2026',
        'O maior carnaval de rua do planeta. Circuitos Osmar, Dodô e Batatinha com trios elétricos e mais de 2 milhões de foliões.',
        '2026-02-14', '2026-02-21', '14:00', '04:00',
        'Circuito Osmar (Campo Grande), Salvador - BA',
        'festa', 'confirmado'
    ),
    (
        'Maratona de Natal',
        'Corrida de rua com percurso de 42km pela orla de Natal, passando por Ponta Negra, Areia Preta e a Via Costeira.',
        '2026-04-19', '2026-04-19', '05:30', '12:00',
        'Via Costeira, Natal - RN',
        'esportivo', 'planejado'
    ),
    (
        'Exposição Fotográfica: Nordeste Vivo',
        'Mostra fotográfica que retrata a cultura, o povo e as paisagens do Nordeste brasileiro. Com obras de fotógrafos locais e nacionais.',
        '2026-05-02', '2026-05-31', '09:00', '18:00',
        'Centro Cultural do Brasil, Natal - RN',
        'cultural', 'planejado'
    ),
    (
        'Festival Literário de Paraty (FLIP)',
        'Um dos maiores festivais literários do mundo. Debates, lançamentos e encontros com grandes nomes da literatura nacional e internacional.',
        '2026-07-01', '2026-07-05', '10:00', '22:00',
        'Centro Histórico de Paraty, Paraty - RJ',
        'cultural', 'planejado'
    ),
    (
        'Passeio a Fernando de Noronha',
        'Viagem ao paraíso ecológico de Fernando de Noronha. Snorkeling, mergulho, caminhadas e contato com a natureza preservada.',
        '2026-05-09', '2026-05-13', '07:00', '20:00',
        'Fernando de Noronha - PE',
        'viagem', 'planejado'
    ),
    (
        'Python Nordeste 2026',
        'A maior conferência regional de Python do Nordeste. Palestras, workshops e hackathon para devs de todos os níveis.',
        '2026-06-06', '2026-06-07', '09:00', '18:00',
        'Universidade Federal do RN (UFRN), Natal - RN',
        'conferencia', 'planejado'
    ),
    (
        'Clássico ABC x América no Frasqueirão',
        'Derby potiguar entre ABC e América-RN no estádio Juvenal Lamartine. Rivalidade histórica que divide a capital.',
        '2026-03-29', '2026-03-29', '16:00', '18:00',
        'Estádio Juvenal Lamartine (Frasqueirão), Natal - RN',
        'esportivo', 'confirmado'
    ),
    (
        'Happy Hour DevNatal',
        'Confraternização da comunidade de desenvolvimento de software de Natal. Networking, bate-papo e cerveja artesanal.',
        '2026-04-24', '2026-04-24', '18:00', '22:00',
        'Taproom Cervejaria Artesanal, Natal - RN',
        'social', 'planejado'
    ),
    (
        'Carnaval de Olinda 2026',
        'Carnaval histórico nas ladeiras de Olinda. Os gigantes de Olinda, frevo nas ruas e uma das festas mais tradicionais do Brasil.',
        '2026-02-14', '2026-02-17', '08:00', '02:00',
        'Centro Histórico de Olinda - PE',
        'festa', 'confirmado'
    ),
    (
        'Workshop de Fotografia nas Dunas',
        'Workshop prático de fotografia de paisagem e natureza nas deslumbrantes dunas da costa norte do RN.',
        '2026-04-11', '2026-04-12', '06:00', '12:00',
        'Dunas de Natal, Natal - RN',
        'workshop', 'planejado'
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
