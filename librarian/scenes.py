from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from librarian.auth import login_required
from librarian.db import get_db

# @TODO Somehow make url_prefix '/scene'.
bp = Blueprint('scenes', __name__)


@bp.route('/')
@login_required
def index():
    db = get_db()
    scenes = db.execute(
        'SELECT s.id, title, body, created, user_id, username, participants, location, music, dramatic_poles, emotional_requests'
        ' FROM scene s JOIN user u ON s.user_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('scenes/index.html', scenes=scenes)

# @TODO Save and continue editing button.
@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        participants = request.form['participants']
        location = request.form['location']
        music = request.form['music']
        dramatic_poles = request.form['dramatic_poles']
        emotional_requests = request.form['emotional_requests']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO scene (title, body, user_id, participants, location, music, dramatic_poles, emotional_requests)'
                ' VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                (title, body, g.user['id'], participants, location, music, dramatic_poles, emotional_requests)
            )
            db.commit()
            return redirect(url_for('scenes.index'))

    return render_template('scenes/create.html')


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    scene = get_post(id, False)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        participants = request.form['participants']
        location = request.form['location']
        music = request.form['music']
        dramatic_poles = request.form['dramatic_poles']
        emotional_requests = request.form['emotional_requests']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE scene SET title = ?, body = ?, participants = ?, '
                'location = ?, music = ?, dramatic_poles = ?, emotional_requests = ?'
                ' WHERE id = ?',
                (title, body, participants, location, music, dramatic_poles, emotional_requests, id)
            )
            db.commit()
            return redirect(url_for('scenes.index'))

    return render_template('scenes/update.html', scene=scene)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM scene WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('scenes.index'))


def get_post(id, check_author=True):
    scene = get_db().execute(
        'SELECT s.id, title, body, created, user_id, username, participants, location, music, dramatic_poles, emotional_requests'
        ' FROM scene s JOIN user u ON s.user_id = u.id'
        ' WHERE s.id = ?',
        (id,)
    ).fetchone()

    if scene is None:
        abort(404, f"Scene id {id} doesn't exist.")

    if check_author and scene['user_id'] != g.user['id']:
        abort(403)

    return scene
