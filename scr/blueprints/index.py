
import json
from datetime import date
from io import BytesIO
from uuid import uuid4

from flask import (
    Blueprint,
    flash,
    jsonify,
    g,
    redirect,
    render_template,
    request,
    send_file,
    url_for
)

from .auth import login_required
from ..controllers.db import get_db

bp = Blueprint('index', __name__, url_prefix='/index')

@bp.route('/')
@login_required
def main():
    db = get_db()

    g.last_album = db.execute(
        f"SELECT * FROM {g.user['username']}_ALBUM WHERE ROWID = (SELECT MAX(ROWID) FROM {g.user['username']}_ALBUM)"
    ).fetchone()

    g.last_single = db.execute(
        f"SELECT * FROM {g.user['username']}_SINGLE WHERE ROWID = (SELECT MAX(ROWID) FROM {g.user['username']}_SINGLE)"
    ).fetchone()

    g.top5_album = db.execute(
        f"SELECT * FROM {g.user['username']}_ALBUM ORDER BY RATING DESC LIMIT 5"
    ).fetchall()

    g.top5_single = db.execute(
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


@bp.route('/album/<id>/update', methods=('GET', 'POST'))
@login_required
def update_album(id):

    db = get_db()
    album = db.execute(f"SELECT * FROM {g.user['username']}_ALBUM WHERE id = '{id}'").fetchone()

    if request.method == 'POST':
        error = None

        title = request.form['title']
        artists = request.form['artists'] 
        genre = request.form['genre']
        subgenre = request.form['subgenre']
        rating = float(request.form['rating'])
        n_tracks = int(request.form['n_tracks'])
        length = float(request.form['length'])
        dt_release = request.form['dt_release']

        if not title and artists and genre and subgenre and rating and n_tracks and length and dt_release:
            error = "All fields are required, fill them properly, please..."

        if error is not None:
            flash(error)
        else:
            db.execute(
                f"""UPDATE {g.user['username']}_ALBUM SET TITLE = ?, ARTISTS = ?,
                GENRE = ?, SUBGENRE = ?, RATING = ?, N_TRACKS = ?, LENGTH = ?, 
                DT_RELEASE = ?
                WHERE id = ?
                """,
                (title, artists, genre, subgenre, rating, n_tracks, length, dt_release, id)
            )
            db.commit()
            return redirect(url_for('index.album'))

    return render_template('update_album.html', album=album)


@bp.route('/album/<id>/delete', methods=('POST',))
@login_required
def delete_album(id):
    db = get_db()
    db.execute(f"DELETE FROM {g.user['username']}_ALBUM WHERE id = ?", (id,))
    db.commit()
    return redirect(url_for('index.album'))


@bp.route('/single')
@login_required
def single():
    db = get_db()

    g.singles = db.execute(
        f"SELECT * FROM {g.user['username']}_SINGLE"
    ).fetchall()

    return render_template('single.html')


@bp.route('/single/create', methods=('GET', 'POST'))
@login_required
def create_single():
    if request.method == 'POST':
        error = None

        id = uuid4().__str__()
        title = request.form['title']
        artists = request.form['artists'] 
        genre = request.form['genre']
        subgenre = request.form['subgenre']
        rating = float(request.form['rating'])
        length = float(request.form['length'])
        dt_release = request.form['dt_release']
        dt_inserted = date.today().isoformat()

        if not title and artists and genre and subgenre and rating and length and dt_release:
            error = "All fields are required, fill them properly, please..."

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                f"""INSERT INTO {g.user['username']}_SINGLE (ID, TITLE, ARTISTS, GENRE,
                SUBGENRE, RATING, LENGTH, DT_RELEASE, DT_INSERTED) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (id, title, artists, genre, subgenre, rating, length, dt_release, dt_inserted)
            )
            db.commit()
            return redirect(url_for('index.single'))

    return render_template('create_single.html')


@bp.route('/single/<id>/update', methods=('GET', 'POST'))
@login_required
def update_single(id):

    db = get_db()
    single = db.execute(f"SELECT * FROM {g.user['username']}_SINGLE WHERE id = '{id}'").fetchone()

    if request.method == 'POST':
        error = None

        title = request.form['title']
        artists = request.form['artists'] 
        genre = request.form['genre']
        subgenre = request.form['subgenre']
        rating = float(request.form['rating'])
        length = float(request.form['length'])
        dt_release = request.form['dt_release']

        if not title and artists and genre and subgenre and rating and length and dt_release:
            error = "All fields are required, fill them properly, please..."

        if error is not None:
            flash(error)
        else:
            db.execute(
                f"""UPDATE {g.user['username']}_SINGLE SET TITLE = ?, ARTISTS = ?,
                GENRE = ?, SUBGENRE = ?, RATING = ?, LENGTH = ?, DT_RELEASE = ?
                WHERE id = ?
                """,
                (title, artists, genre, subgenre, rating, length, dt_release, id)
            )
            db.commit()
            return redirect(url_for('index.single'))

    return render_template('update_single.html', single=single)


@bp.route('/single/<id>/delete', methods=('POST',))
@login_required
def delete_single(id):
    db = get_db()
    db.execute(f"DELETE FROM {g.user['username']}_SINGLE WHERE id = ?", (id,))
    db.commit()
    return redirect(url_for('index.single'))



@bp.route('/analytics')
@login_required
def analytics():
    db = get_db()

    g.count_singles = db.execute(
        f"""SELECT GENRE, COUNT(*) AS QTT
        FROM {g.user['username']}_SINGLE
        GROUP BY GENRE
        ORDER BY GENRE;"""
    ).fetchall()

    g.count_albums = db.execute(
        f"""SELECT GENRE, COUNT(*) AS QTT
        FROM {g.user['username']}_ALBUM
        GROUP BY GENRE
        ORDER BY GENRE;"""
    ).fetchall()

    x = []
    y = []
    for row in g.count_albums:
        x.append(row['GENRE'])
        y.append(row['QTT'])

    g.count_albums = [x, y]

    x = []
    y = []
    for row in g.count_singles:
        x.append(row['GENRE'])
        y.append(row['QTT'])

    g.count_singles = [x, y]
    
    return render_template('analytics.html')


def fetch_singles_data(username):
    db = get_db()
    singles = db.execute(f"SELECT * FROM {username}_SINGLE").fetchall()

    singles_list = []
    for single in singles:
        single_dict = {
            'ID': single['ID'],
            'TITLE': single['TITLE'],
            'ARTISTS': single['ARTISTS'],
            'GENRE': single['GENRE'],
            'SUBGENRE': single['SUBGENRE'],
            'RATING': single['RATING'],
            'LENGTH': single['LENGTH'],
            'DT_RELEASE': single['DT_RELEASE'],
            'DT_INSERTED': single['DT_INSERTED']
        }
        singles_list.append(single_dict)

    return singles_list


@bp.route('/download_singles')
def download_singles():
    singles_data = fetch_singles_data(g.user['username'])

    singles_json = json.dumps(singles_data, indent=4)

    json_file = BytesIO()
    json_file.write(singles_json.encode('utf-8'))
    json_file.seek(0)

    return send_file(
        json_file,
        as_attachment=True,
        download_name="singles_data.json",
        mimetype="application/json"
    )

def fetch_albums_data(username):
    db = get_db()
    albums = db.execute(f"SELECT * FROM {username}_ALBUM").fetchall()

    albums_list = []
    for album in albums:
        album_dict = {
            'ID': album['ID'],
            'TITLE': album['TITLE'],
            'ARTISTS': album['ARTISTS'],
            'GENRE': album['GENRE'],
            'SUBGENRE': album['SUBGENRE'],
            'RATING': album['RATING'],
            'N_TRACKS': album['N_TRACKS'],
            'LENGTH': album['LENGTH'],
            'DT_RELEASE': album['DT_RELEASE'],
            'DT_INSERTED': album['DT_INSERTED']
        }
        albums_list.append(album_dict)

    return albums_list


@bp.route('/download_albums')
def download_albums():
    albums_data = fetch_albums_data(g.user['username'])

    albums_json = json.dumps(albums_data, indent=4)

    json_file = BytesIO()
    json_file.write(albums_json.encode('utf-8'))
    json_file.seek(0)

    return send_file(
        json_file,
        as_attachment=True,
        download_name="albums_data.json",
        mimetype="application/json"
    )
