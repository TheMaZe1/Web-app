import urllib
from urllib import parse


from app import app, db
from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Films, Actor, Director

from app.forms import LoginForm, RegistrationForm, addFilm
from app.parsing_films import find_film_by_name, find_film_by_id, save_film


@app.route('/', methods=['POST', 'GET'])
@app.route('/index', methods=['POST', 'GET'])
def index():
    if not current_user.is_anonymous:
        films_top = Films.query.order_by(Films.rating.desc()).limit(4)
        form = addFilm()
        if form.validate_on_submit():
            films_js = find_film_by_name(form.namefilm.data)
            films = []
            for film_js in films_js['docs']:
                films.append(Films(
                    id=int(film_js['id']),
                    rating=float(film_js['rating']['kp']),
                    type=film_js['type'],
                    name=film_js['name'],
                    description=film_js['description'],
                    poster=film_js['poster']['url'] if 'poster' in film_js else None,
                    year=film_js['year'],
                    movieLength=film_js['movieLength'],
                    ageRating=film_js['ageRating']
                ))

            return render_template('index.html', form=form, films=films)
        else:
            return render_template('index.html', form=form, films_top=films_top)
    else:
        return render_template('index.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return render_template(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        print(user.check_password(form.password.data))
        if user is None or not user.check_password(form.password.data):
            flash("Wrong login or password")
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or parse.urlsplit(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/user/<username>', methods=['POST', 'GET'])
@login_required
def user(username):
    page = request.args.get('page',1,type=int)
    user = User.query.filter_by(username=username).first_or_404()
    films = user.films
    films_pagination = user.films.paginate(page=page, per_page=app.config['FILMS_PER_PAGE'], error_out=False)
    top_actors = {}
    top_directors = {}
    top_years = {}
    top_genres = {}
    for film in films:
        for actor in film.actors:
            top_actors[actor.id] = top_actors.get(actor.id, 0) + 1
        for director in film.directors:
            top_directors[director.id] = top_directors.get(director.id, 0) + 1
        genre = film.genres[0]
        top_genres[genre] = top_genres.get(genre, 0) + 1
        top_years[film.year] = top_years.get(film.year, 0) + 1
    top_actors = sorted(top_actors, key=lambda x: top_actors[x], reverse=True)
    top_directors = sorted(top_directors, key=lambda x: top_directors[x], reverse=True)
    count = user.films.count()
    return render_template('user.html', user=user, films=films_pagination,
                           top_actors=Actor.query.filter_by(id=int(top_actors[0])).first() if top_actors else None,
                           top_directors=Director.query.filter_by(id=int(top_directors[0])).first() if top_directors else None,
                           top_genres=sorted(top_genres, key=lambda x: top_genres[x], reverse=True),
                           top_years=sorted(top_years, key=lambda x: top_years[x], reverse=True),
                           pagination=films_pagination, count=count
    )


@app.route('/addfilm/<film_id>', methods=['POST', 'GET'])
@login_required
def addfilm(film_id):
    film = Films.query.filter_by(id=film_id).first()
    if not film:
        save_film(id)
    if film not in current_user.films:
        current_user.viewed(film)
        db.session.commit()
    next_page = request.args.get('next')
    if not next_page:
        next_page = url_for('index')
    return redirect(next_page)

@app.route('/removefilm/<film_id>', methods=['POST', 'GET'])
@login_required
def remove_film(film_id):
    film = Films.query.filter_by(id=film_id).first()
    current_user.unseen(film)
    db.session.commit()
    next_page = request.args.get('next')
    if not next_page:
        next_page = url_for('index')
    return redirect(next_page)

@app.route('/top_100')
def top_100():
    page = request.args.get('page',1,type=int)
    films_top = Films.query.order_by(Films.rating.desc())
    films_top = films_top.paginate(page=page, per_page=app.config['FILMS_PER_PAGE'], error_out=False)
    return render_template('top_films.html', films_top=films_top, count=100)

@app.route('/film/<film_id>')
def film(film_id):
    film = Films.query.filter_by(id=film_id).first()
    if not film:
        save_film(film_id)
        film = Films.query.filter_by(id=film_id).first()
    actors = []
    for actor in film.actors:
        actors.append((actor, film.get_role(actor)[2]))
    return render_template('film.html', film=film, actors=actors, directors=film.directors)