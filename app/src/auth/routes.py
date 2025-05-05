from flask import render_template, flash, session

from . import auth_blueprint
from app.src.auth.forms import LoginForm, RegisterForm
from app.src.repository.repository import Repository

repository = Repository()

@auth_blueprint.route('/signin', methods=['GET', 'POST'])
def signin():
    form = LoginForm()
    if form.validate_on_submit():
        login = form.login.data
        password = form.password.data
        if repository.check_user(login, password):
            session['login'] = login
            # залогинился, что дальше
        else:
            pass
    return render_template('signin.html', form=form)

@auth_blueprint.route('/signup', methods=['GET', 'POST'])
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