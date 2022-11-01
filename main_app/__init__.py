from flask import Flask
from flask_login import LoginManager

import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

database_uri = os.getenv('DATABASE_URI')

server_url = os.getenv('SERVER_URL')

with app.app_context():
    login_manager = LoginManager(app)

    from main_app import models, routes

    from main_app.db_config import db
    db.create_all()

