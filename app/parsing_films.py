from app import kinopoisk_API, db
import requests
import json

from app.models import Films, Actor, Director

headers = {'X-API-KEY': 'RXGPME8-S8Z4Z3G-KWW45VF-193ER0C'}
fields = ['id', 'rating.kp', 'type', 'name', 'description', 'poster.url', 'year', 'movieLength', 'ageRating']

def find_film_by_name(name):
    return requests.get('https://api.kinopoisk.dev/v1.3/movie', headers=headers, params={
        'name': name,
        'selectFields': fields
    }).json()

def find_film_by_id(id):
    return requests.get(f'https://api.kinopoisk.dev/v1.3/movie/{id}', headers=headers).json()

def save_film(film_id):
    film_js = find_film_by_id(film_id)
    film = Films(
        id=int(film_js['id']),
        rating=float(film_js['rating']['kp']),
        type=film_js['type'],
        name=film_js['name'],
        description=film_js['description'],
        poster=film_js['poster']['url'] if 'poster' in film_js else None,
        year=film_js['year'],
        movieLength=film_js['movieLength'],
        ageRating=film_js['ageRating'],
        genres=[genre['name'] for genre in film_js['genres']]
    )
    db.session.add(film)
    db.session.commit()
    directors = []
    for actor in film_js['persons']:
        if actor['profession'] == 'актеры':
            if not Actor.query.filter_by(id=actor['id']).first():
                db.session.add(Actor(id=actor['id'],
                                     name=actor['name'],
                                     photo=actor['photo']
                                     ))
        if actor['profession'] == 'режиссеры':
            director = Director.query.filter_by(id=actor['id']).first()
            if not director:
                director = Director(id=actor['id'],
                                    name=actor['name'],
                                    photo=actor['photo']
                                    )
                db.session.add(director)
            film.directors.append(director)
    film.add_actor([actor for actor in film_js['persons'] if actor['profession'] == 'актеры'])
    db.session.commit()
