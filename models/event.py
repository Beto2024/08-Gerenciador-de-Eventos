import sqlite3
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import DATABASE


def get_db():
    """Retorna uma conexão com o banco de dados."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def get_all_events(filters=None, page=1, per_page=9):
    """Retorna eventos paginados com filtros opcionais."""
    conn = get_db()
    cursor = conn.cursor()

    query = "SELECT * FROM events WHERE 1=1"
    params = []

    if filters:
        if filters.get('category'):
            query += " AND category = ?"
            params.append(filters['category'])

        if filters.get('status'):
            query += " AND status = ?"
            params.append(filters['status'])

        if filters.get('start_from'):
            query += " AND start_date >= ?"
            params.append(filters['start_from'])

        if filters.get('start_to'):
            query += " AND start_date <= ?"
            params.append(filters['start_to'])

        if filters.get('search'):
            query += " AND (title LIKE ? OR description LIKE ?)"
            term = f"%{filters['search']}%"
            params.extend([term, term])

    count_query = query.replace("SELECT *", "SELECT COUNT(*)")
    cursor.execute(count_query, params)
    total = cursor.fetchone()[0]

    query += " ORDER BY start_date ASC, start_time ASC"
    query += " LIMIT ? OFFSET ?"
    params.extend([per_page, (page - 1) * per_page])

    cursor.execute(query, params)
    events = [dict(row) for row in cursor.fetchall()]
    conn.close()

    return events, total


def get_event_by_id(event_id):
    """Retorna um evento pelo ID."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM events WHERE id = ?", (event_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def create_event(data):
    """Cria um novo evento."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO events
           (title, description, start_date, end_date, start_time, end_time,
            location, category, status)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            data['title'],
            data.get('description', ''),
            data['start_date'],
            data.get('end_date') or None,
            data.get('start_time') or None,
            data.get('end_time') or None,
            data.get('location', ''),
            data['category'],
            data['status'],
        )
    )
    conn.commit()
    event_id = cursor.lastrowid
    conn.close()
    return event_id


def update_event(event_id, data):
    """Atualiza um evento existente."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        """UPDATE events SET
           title=?, description=?, start_date=?, end_date=?,
           start_time=?, end_time=?, location=?, category=?, status=?,
           updated_at=CURRENT_TIMESTAMP
           WHERE id=?""",
        (
            data['title'],
            data.get('description', ''),
            data['start_date'],
            data.get('end_date') or None,
            data.get('start_time') or None,
            data.get('end_time') or None,
            data.get('location', ''),
            data['category'],
            data['status'],
            event_id,
        )
    )
    conn.commit()
    conn.close()


def delete_event(event_id):
    """Remove um evento pelo ID."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM events WHERE id = ?", (event_id,))
    conn.commit()
    conn.close()


def get_events_for_month(year, month):
    """Retorna todos os eventos de um determinado mês/ano."""
    conn = get_db()
    cursor = conn.cursor()
    month_str = f"{year}-{month:02d}"
    cursor.execute(
        "SELECT * FROM events WHERE strftime('%Y-%m', start_date) = ? ORDER BY start_date, start_time",
        (month_str,)
    )
    events = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return events


def get_dashboard_stats():
    """Retorna estatísticas para o dashboard."""
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) as total FROM events")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM events WHERE start_date = date('now')")
    today = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM events WHERE start_date > date('now')"
    )
    upcoming = cursor.fetchone()[0]

    cursor.execute(
        """SELECT category, COUNT(*) as count FROM events
           GROUP BY category ORDER BY count DESC"""
    )
    by_category = [dict(row) for row in cursor.fetchall()]

    cursor.execute(
        """SELECT * FROM events WHERE start_date >= date('now')
           ORDER BY start_date ASC, start_time ASC LIMIT 5"""
    )
    next_events = [dict(row) for row in cursor.fetchall()]

    cursor.execute(
        "SELECT * FROM events WHERE start_date = date('now') ORDER BY start_time ASC"
    )
    today_events = [dict(row) for row in cursor.fetchall()]

    cursor.execute(
        """SELECT status, COUNT(*) as count FROM events
           GROUP BY status ORDER BY count DESC"""
    )
    by_status = [dict(row) for row in cursor.fetchall()]

    conn.close()
    return {
        'total': total,
        'today': today,
        'upcoming': upcoming,
        'by_category': by_category,
        'next_events': next_events,
        'today_events': today_events,
        'by_status': by_status,
    }
