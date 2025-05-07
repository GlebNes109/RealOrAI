from flask import render_template, flash, session, redirect, url_for

from . import auth_bp
from app.src.blueprints.auth_bp.forms import LoginForm, RegisterForm
from app.src.database.repository import Repository

repository = Repository()

@auth_bp.route('/signin', methods=['GET', 'POST'])
def signin():
    form = LoginForm()
    if form.validate_on_submit():
        login = form.login.data
        password = form.password.data
        user = repository.get_user(login, password)
        if user:
            session['user_id'] = user.id
            return redirect(url_for('home_bp.home'))
        else:
            pass
    return render_template('signin.html', form=form)

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        res = repository.add_user(username, password)
        if not res:
            flash('Пользователь с таким логином уже существует', 'danger')
        # return redirect(url_for('login'))
    return render_template('signup.html', form=form)

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash("Вы вышли из аккаунта", "info")
    return redirect(url_for('auth_bp.signin'))