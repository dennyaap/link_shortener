from main_app.db_config import db
from main_app import login_manager

from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)

class Shortened_link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(255), nullable=False, unique=True)
    long_url = db.Column(db.String(255), nullable=False)
    access_type = db.Column(db.String(15), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, token, long_url, type_access, user_id):
        self.token = token
        self.long_url = long_url
        self.access_type = type_access
        self.user_id = user_id

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)