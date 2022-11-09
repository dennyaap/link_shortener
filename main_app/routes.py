from main_app import app, server_url
from main_app.models import Shortened_link, User
from main_app.db_config import db

import hashlib, random

from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html', isAuth=current_user.is_authenticated)

@app.route('/<token>', methods=['GET', 'POST'])
def redirect_page(token):
    shortened_link = Shortened_link.query.filter_by(token=token).first()
    
    if shortened_link is None:
        return 'No such links'

    return redirect(shortened_link.long_url)


@app.route('/main', methods=['GET'])
@login_required
def main():
    data = dict()

    data['server_url'] = server_url
    data['shortened_links'] = Shortened_link.query.filter_by(user_id=current_user.id).all()
    data['access_types'] = ['public', 'auth', 'private']

    return render_template('main.html', data=data)

@app.route('/add_link', methods=['POST'])
@login_required
def add_link():
    long_url = request.form['long_url']
    pseudonym = request.form['pseudonym']
    type_access = request.form['type_access']

    if pseudonym:
        token = pseudonym
    else:
        token = hashlib.md5(long_url.encode()).hexdigest()[:random.randint(8,12)]

    user_id = current_user.id

    flash('Please fill in the long url')
    db.session.add(Shortened_link(token, long_url, type_access, user_id))
    db.session.commit()

    return redirect(url_for('main'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_anonymous:
        next_page = request.args.get('next')

        if next_page is None:
            next_page = url_for('main')

        if request.method == 'POST':
            login = request.form['login']
            password = request.form['password']

            if login and password:
                user = User.query.filter_by(login=login).first()

                if user and check_password_hash(user.password, password):
                    login_user(user)

                    return redirect(next_page)
                else:
                    flash('Incorrect login or password')
            else:
                flash('Please fill in your login and password')

        return render_template('login.html')
    else:
        return redirect(url_for('main'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']

        if not (login or password):
            flash('Please, fill all field')
        else:
            hash_password = generate_password_hash(password)
            new_user = User(login=login, password=hash_password)
            db.session.add(new_user)
            db.session.commit()

            login_user(new_user)

            return redirect(url_for('main'))

    return render_template('register.html')


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    
    return redirect(url_for('index'))

@app.after_request
def redirect_to_signin(response):
    if response.status_code == 401:
        return redirect(url_for('login') + '?next=' + request.url)
    
    return response
