from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from flask_login import LoginManager

app = Flask(__name__) # 'from app import app' this is the second 'app' reference
app.config.from_object(Config) # updates config from Config object
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login' # such that force login page is set so protected features cannot be accessed by anons
# 'login' value is function name for login view

from app import routes, models