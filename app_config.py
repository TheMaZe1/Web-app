import os


class Config:

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:LichKing536@localhost:5432/cinema_stats"
    FILMS_PER_PAGE = 10
