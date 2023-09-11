from flask_login import UserMixin

from app import db, login
from sqlalchemy_utils import ScalarListType

from werkzeug.security import generate_password_hash, check_password_hash

user_film = db.Table('user_films', db.Model.metadata,
                       db.Column('user_id', db.Integer(), db.ForeignKey("users.id")),
                       db.Column('film_id', db.Integer(), db.ForeignKey("films.id"))
                       )

actor_film = db.Table('actor_films', db.Model.metadata,
                       db.Column('actor_id', db.Integer(), db.ForeignKey("actors.id")),
                       db.Column('film_id', db.Integer(), db.ForeignKey("films.id")),
                       db.Column('role', db.String())
                       )

director_film = db.Table('director_films', db.Model.metadata,
                       db.Column('director_id', db.Integer(), db.ForeignKey("directors.id")),
                       db.Column('film_id', db.Integer(), db.ForeignKey("films.id")),
                       )

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    films = db.relationship('Films', secondary=user_film,
                            primaryjoin=(user_film.c.user_id == id),
                            backref='users', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def viewed(self, film):
        if not self.is_viewed(film):
            self.films.append(film)

    def unseen(self, film):
        if self.is_viewed(film):
            self.films.remove(film)

    def is_viewed(self, film):
        return self.films.filter(user_film.c.film_id == film.id).count() > 0



    def __repr__(self):
        return '<User {}>'.format(self.username)


class Films(db.Model):
    __tablename__ = 'films'
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Float())
    type = db.Column(db.String())
    name = db.Column(db.String(128), index=True)
    description = db.Column(db.String())
    poster = db.Column(db.String())
    year = db.Column(db.Integer())
    movieLength = db.Column(db.Integer())
    ageRating = db.Column(db.Integer())
    genres = db.Column(ScalarListType())
    actors = db.relationship('Actor', secondary=actor_film,
                            backref='films', lazy='dynamic')
    directors = db.relationship('Director', secondary=director_film,
                            backref='films', lazy='dynamic')

    def add_actor(self, actors):
        for actor in actors:
            c = actor_film.insert().values(actor_id=actor['id'], film_id=self.id, role=actor['description'])
            db.session.execute(c)

    def get_role(self, actor):
        return db.session.execute(actor_film.select().where(actor_film.c.film_id==self.id, actor_film.c.actor_id==actor.id)).first()
class Actor(db.Model):
    __tablename__ = 'actors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), index=True, unique=True)
    photo = db.Column(db.String(), index=True, unique=True)

class Director(db.Model):
    __tablename__ = 'directors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), index=True, unique=True)
    photo = db.Column(db.String(), index=True, unique=True)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))