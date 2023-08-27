import requests
from bs4 import BeautifulSoup

from app import db, app
from app.models import Films
from app.parsing_films import find_film_by_id

# with open('page2.html', 'r', encoding='utf-8') as f, open('id_films.txt', 'a', encoding='utf-8') as f2:
#     soup = BeautifulSoup(f.read(), 'html.parser')
#     tags = soup.find_all("a", {"class": "base-movie-main-info_link__YwtP1"})
#     for tag in tags:
#         f2.write(tag['href'].split('/')[2]+'\n')

with open('id_films.txt', 'r', encoding='utf-8') as f, app.app_context():
    for film_id in [line.rstrip() for line in f]:
        film = Films.query.filter_by(id=film_id).first()
        if not film:
            film_js = find_film_by_id(film_id)
            film = Films(
                id=int(film_js['id']),
                rating=float(film_js['rating']['kp']),
                type=film_js['type'],
                name=film_js['name'],
                description=film_js['description'],
                poster=film_js['poster']['url'],
                year=film_js['year'],
                movieLength=film_js['movieLength'],
                ageRating=film_js['ageRating'],
                genres=[genre['name'] for genre in film_js['genres']],
                actors=[actor['name'] for actor in film_js['persons'] if actor['profession'] == 'актеры'],
                directors=[director['name'] for director in film_js['persons'] if director['profession'] == 'режиссеры']
            )
            db.session.add(film)
            db.session.commit()
