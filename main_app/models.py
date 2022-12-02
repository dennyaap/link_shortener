from main_app.db_config import db
from main_app import login_manager

from flask_login import UserMixin

import hashlib, random


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)

    def find_user(login):
        return User.query.filter_by(login=login).first()
    def add_new_user(login, hash_password):
        new_user = User(login=login, password=hash_password)
        db.session.add(new_user)
        db.session.commit()
        return new_user

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

    def get_link(token):
        return Shortened_link.query.filter_by(token=token).first()

    def get_user_links(current_user_id):
        return Shortened_link.query.filter_by(user_id=current_user_id).all()
    
    def add_link(token, long_url, type_access, current_user_id):
        db.session.add(Shortened_link(token=token, long_url=long_url, type_access=type_access, user_id=current_user_id))
        db.session.commit()

    def check_link_access_type(shortened_link, current_user):
        link_access_type = shortened_link.access_type
        link_user_id = shortened_link.user_id

        if link_access_type == 'public':
            return
        if current_user.is_authenticated:
            if not (link_access_type == 'private' and link_user_id == current_user.id):
                return "You don't have access"
        else:
            return 'You are not authorized'
    def generate_token(long_url, min = 8, max = 12):
        return hashlib.md5(long_url.encode()).hexdigest()[:random.randint(min, max)]

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)