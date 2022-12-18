from main_app import app, server_url
from main_app.models import Shortened_link, User
from main_app.db_config import db

from flask import render_template, redirect, url_for, request, flash, session
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html', isAuth=current_user.is_authenticated)

@app.route('/s/<token>', methods=['GET'])
def redirect_page(token):
    shortened_link = Shortened_link.get_link(token)
    
    if shortened_link is None:
        flash('No such link')

        return render_template('index.html')
    else:
        error = Shortened_link.check_link_access_type(shortened_link, current_user)

        if not error:
            Shortened_link.update_count_link_redirects(token=token, count=1)
            return redirect(shortened_link.long_url)
        else:
            flash(error)
            return render_template('error.html')

@app.route('/main', methods=['GET'])
@login_required
def main():
    data = dict()

    data['server_url'] = server_url
    data['shortened_links'] = Shortened_link.get_user_links(current_user_id=current_user.id)

    return render_template('main.html', data=data)

@app.route('/add_link', methods=['POST'])
@login_required
def add_link():
    long_url = request.form['long_url']
    pseudonym = request.form['pseudonym']
    type_access = request.form['type_access']

    if long_url:
        token = Shortened_link.generate_token(long_url)

        while Shortened_link.get_link(token):
            token = Shortened_link.generate_token(long_url)

        Shortened_link.add_link(token=token, long_url=long_url, type_access=type_access, current_user_id=current_user.id, count_redirects=0, pseudonym=pseudonym)    
    else:
        flash('Please fill in the long url')

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
                user = User.find_user(login)

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

            login_user(User.add_new_user(login, hash_password))

            return redirect(url_for('main'))

    return render_template('register.html')


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    
    return redirect(url_for('index'))

@app.route('/edit/<token>', methods=['GET', 'POST'])
@login_required
def edit(token):
    data = dict()
    data['shortened_link'] = Shortened_link.get_link(token)
    data['access_types'] = ['public', 'auth', 'private']

    if request.method == 'POST':
        pseudonym = request.form['pseudonym']
        access_type = request.form['current_type_access']

        Shortened_link.edit_link(token=token, pseudonym=pseudonym, access_type=access_type)

        print('dfgdfgdfgdf')

        return redirect(url_for('main'))
    return render_template('edit.html', data=data)

@app.after_request
def redirect_to_signin(response):
    if response.status_code == 401:
        return redirect(url_for('login') + '?next=' + request.url)
    
    return response