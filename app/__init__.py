from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap5

from app_config import Config

app = Flask(__name__, static_folder='static')
app.config.from_object(Config())
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
bootstrap = Bootstrap5(app)
kinopoisk_API = 'RXGPME8-S8Z4Z3G-KWW45VF-193ER0C'


from app import routes, models

