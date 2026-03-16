import os
import calendar
from datetime import datetime, date

from flask import (
    Flask, render_template, request, redirect,
    url_for, flash, jsonify, abort
)

from config import (
    SECRET_KEY, EVENTS_PER_PAGE, CATEGORIES,
    STATUSES, CATEGORY_DICT, STATUS_DICT, DATABASE
)
from database.init_db import init_db
from models.event import (
    get_all_events, get_event_by_id, create_event,
    update_event, delete_event, get_events_for_month,
    get_dashboard_stats
)

app = Flask(__name__)
app.secret_key = SECRET_KEY

# Initialize database on startup
with app.app_context():
    init_db()

# ------------------------------------------------------------------
# Template context helpers
# ------------------------------------------------------------------

@app.context_processor
def inject_globals():
    return {
        'categories': CATEGORIES,
        'statuses': STATUSES,
        'category_dict': CATEGORY_DICT,
        'status_dict': STATUS_DICT,
        'today': date.today().isoformat(),
    }


@app.template_filter('format_date')
def format_date(value):
    if not value:
        return ''
    try:
        dt = datetime.strptime(str(value), '%Y-%m-%d')
        return dt.strftime('%d/%m/%Y')
    except Exception:
        return value


@app.template_filter('format_time')
def format_time(value):
    if not value:
        return ''
    try:
        return value[:5]
    except Exception:
        return value


# ------------------------------------------------------------------
# Dashboard
# ------------------------------------------------------------------

@app.route('/')
def index():
    stats = get_dashboard_stats()
    return render_template('index.html', stats=stats)


# ------------------------------------------------------------------
# Events CRUD
# ------------------------------------------------------------------

@app.route('/events')
def events_list():
    page = request.args.get('page', 1, type=int)
    filters = {
        'category': request.args.get('category', ''),
        'status': request.args.get('status', ''),
        'start_from': request.args.get('start_from', ''),
        'start_to': request.args.get('start_to', ''),
        'search': request.args.get('search', ''),
    }
    # Remove empty filters
    active_filters = {k: v for k, v in filters.items() if v}

    events, total = get_all_events(active_filters, page, EVENTS_PER_PAGE)
    total_pages = max(1, (total + EVENTS_PER_PAGE - 1) // EVENTS_PER_PAGE)

    return render_template(
        'events/list.html',
        events=events,
        page=page,
        total_pages=total_pages,
        total=total,
        filters=filters,
    )


@app.route('/events/create', methods=['GET', 'POST'])
def events_create():
    if request.method == 'POST':
        data = {
            'title': request.form.get('title', '').strip(),
            'description': request.form.get('description', '').strip(),
            'start_date': request.form.get('start_date', ''),
            'end_date': request.form.get('end_date', ''),
            'start_time': request.form.get('start_time', ''),
            'end_time': request.form.get('end_time', ''),
            'location': request.form.get('location', '').strip(),
            'category': request.form.get('category', 'outro'),
            'status': request.form.get('status', 'planejado'),
        }

        errors = []
        if not data['title']:
            errors.append('O título é obrigatório.')
        if not data['start_date']:
            errors.append('A data de início é obrigatória.')

        if errors:
            for err in errors:
                flash(err, 'error')
            return render_template('events/create.html', form_data=data)

        event_id = create_event(data)
        flash('Evento criado com sucesso!', 'success')
        return redirect(url_for('events_detail', event_id=event_id))

    return render_template('events/create.html', form_data={})


@app.route('/events/<int:event_id>')
def events_detail(event_id):
    event = get_event_by_id(event_id)
    if not event:
        abort(404)
    return render_template('events/detail.html', event=event)


@app.route('/events/<int:event_id>/edit', methods=['GET', 'POST'])
def events_edit(event_id):
    event = get_event_by_id(event_id)
    if not event:
        abort(404)

    if request.method == 'POST':
        data = {
            'title': request.form.get('title', '').strip(),
            'description': request.form.get('description', '').strip(),
            'start_date': request.form.get('start_date', ''),
            'end_date': request.form.get('end_date', ''),
            'start_time': request.form.get('start_time', ''),
            'end_time': request.form.get('end_time', ''),
            'location': request.form.get('location', '').strip(),
            'category': request.form.get('category', 'outro'),
            'status': request.form.get('status', 'planejado'),
        }

        errors = []
        if not data['title']:
            errors.append('O título é obrigatório.')
        if not data['start_date']:
            errors.append('A data de início é obrigatória.')

        if errors:
            for err in errors:
                flash(err, 'error')
            return render_template('events/edit.html', event={**event, **data})

        update_event(event_id, data)
        flash('Evento atualizado com sucesso!', 'success')
        return redirect(url_for('events_detail', event_id=event_id))

    return render_template('events/edit.html', event=event)


@app.route('/events/<int:event_id>/delete', methods=['POST'])
def events_delete(event_id):
    event = get_event_by_id(event_id)
    if not event:
        abort(404)
    delete_event(event_id)
    flash('Evento excluído com sucesso!', 'success')
    return redirect(url_for('events_list'))


# ------------------------------------------------------------------
# Calendar
# ------------------------------------------------------------------

@app.route('/calendar')
def calendar_view():
    today = date.today()
    return redirect(url_for('calendar_month', year=today.year, month=today.month))


@app.route('/calendar/<int:year>/<int:month>')
def calendar_month(year, month):
    if month < 1 or month > 12:
        abort(404)

    events = get_events_for_month(year, month)

    # Build a dict: day -> list of events
    events_by_day = {}
    for ev in events:
        day = int(ev['start_date'].split('-')[2])
        events_by_day.setdefault(day, []).append(ev)

    cal = calendar.monthcalendar(year, month)

    # Previous / next month
    if month == 1:
        prev_year, prev_month = year - 1, 12
    else:
        prev_year, prev_month = year, month - 1

    if month == 12:
        next_year, next_month = year + 1, 1
    else:
        next_year, next_month = year, month + 1

    month_name = [
        '', 'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
        'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'
    ][month]

    return render_template(
        'calendar/view.html',
        calendar=cal,
        events_by_day=events_by_day,
        year=year,
        month=month,
        month_name=month_name,
        prev_year=prev_year,
        prev_month=prev_month,
        next_year=next_year,
        next_month=next_month,
        today=date.today(),
    )


# ------------------------------------------------------------------
# API
# ------------------------------------------------------------------

@app.route('/api/events')
def api_events():
    filters = {
        'category': request.args.get('category', ''),
        'status': request.args.get('status', ''),
        'start_from': request.args.get('start_from', ''),
        'start_to': request.args.get('start_to', ''),
        'search': request.args.get('search', ''),
    }
    active_filters = {k: v for k, v in filters.items() if v}
    page = request.args.get('page', 1, type=int)
    events, total = get_all_events(active_filters, page, EVENTS_PER_PAGE)
    return jsonify({'events': events, 'total': total, 'page': page})


# ------------------------------------------------------------------
# Error handlers
# ------------------------------------------------------------------

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404


# ------------------------------------------------------------------
# Entry point
# ------------------------------------------------------------------

if __name__ == '__main__':
    from config import PORT
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(debug=debug, host='0.0.0.0', port=PORT)
