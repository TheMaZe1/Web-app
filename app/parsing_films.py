from app import kinopoisk_API
import requests
import json

headers = {'X-API-KEY': 'RXGPME8-S8Z4Z3G-KWW45VF-193ER0C'}
fields = ['id', 'rating.kp', 'type', 'name', 'description', 'poster.url', 'year', 'movieLength', 'ageRating']

def find_film_by_name(name):
    return requests.get('https://api.kinopoisk.dev/v1.3/movie', headers=headers, params={
        'name': name,
        'selectFields': fields
    }).json()

def find_film_by_id(id):
    return requests.get(f'https://api.kinopoisk.dev/v1.3/movie/{id}', headers=headers).json()
