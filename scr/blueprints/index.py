
from datetime import date
from uuid import uuid4

from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for
)
from werkzeug.security import (
    check_password_hash,
    generate_password_hash
)

from ..structs.album import Album

from .auth import login_required
from ..controllers.db import get_db

bp = Blueprint('index', __name__, url_prefix='/index')

@bp.route('/')
@login_required
def main():
    db = get_db()

    g.last_album = db.execute(
        f"SELECT * FROM {g.user['username']}_ALBUM ORDER BY DT_INSERTED DESC LIMIT 1"
    ).fetchone()

    g.last_single = db.execute(
        f"SELECT * FROM {g.user['username']}_SINGLE ORDER BY DT_INSERTED DESC LIMIT 1"
    ).fetchone()

    g.top5_album = db.execute(
        f"SELECT * FROM {g.user['username']}_ALBUM ORDER BY RATING DESC LIMIT 5"
    ).fetchall()

    g.top5_album = db.execute(
        f"SELECT * FROM {g.user['username']}_SINGLE ORDER BY RATING DESC LIMIT 5"
    ).fetchall()

    return render_template('main.html')


@bp.route('/album')
@login_required
def album():
    db = get_db()

    g.albums = db.execute(
        f"SELECT * FROM {g.user['username']}_ALBUM"
    ).fetchall()

    return render_template('album.html')


@bp.route('/album/create', methods=('GET', 'POST'))
@login_required
def create_album():
    if request.method == 'POST':
        error = None

        id = uuid4().__str__()
        title = request.form['title']
        artists = request.form['artists'] 
        genre = request.form['genre']
        subgenre = request.form['subgenre']
        rating = float(request.form['rating'])
        n_tracks = int(request.form['n_tracks'])
        length = float(request.form['length'])
        dt_release = request.form['dt_release']
        dt_inserted = date.today().isoformat()

        print(type(id))
        print(type(title))
        print(type(artists))
        print(type(genre))
        print(type(subgenre))
        print(type(rating))
        print(type(n_tracks))
        print(type(length))
        print(type(dt_release))
        print(type(dt_inserted))

        if not title and artists and genre and subgenre and rating and n_tracks and length and dt_release:
            error = "All fields are required, fill them properly, please..."

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                f"""INSERT INTO {g.user['username']}_ALBUM (ID, TITLE, ARTISTS, GENRE,
                SUBGENRE, RATING, N_TRACKS, LENGTH, DT_RELEASE, DT_INSERTED) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (id, title, artists, genre, subgenre, rating, n_tracks, length, dt_release, dt_inserted)
            )
            db.commit()
            return redirect(url_for('index.album'))


    return render_template('create_album.html')
