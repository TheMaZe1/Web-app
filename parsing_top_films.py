import requests
from bs4 import BeautifulSoup

from app import db, app
from app.models import Films, Actor, Director
from app.parsing_films import find_film_by_id, save_film

# with open('page2.html', 'r', encoding='utf-8') as f, open('id_films.txt', 'a', encoding='utf-8') as f2:
#     soup = BeautifulSoup(f.read(), 'html.parser')
#     tags = soup.find_all("a", {"class": "base-movie-main-info_link__YwtP1"})
#     for tag in tags:
#         f2.write(tag['href'].split('/')[2]+'\n')

with open('id_films.txt', 'r', encoding='utf-8') as f, app.app_context():
    for film_id in [line.rstrip() for line in f]:
        save_film(film_id)
        db.session.commit()

# with app.app_context():
#     film = Films.query.filter_by(id=1).first()
#     print(film.actors[0].name)


