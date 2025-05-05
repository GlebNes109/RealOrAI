from flask import session, render_template, redirect, url_for

from app.src.mainpage import home_blueprint


@home_blueprint.route('/home')
def home():
    if 'login' in session:
        login = session['login']
        return render_template('homepage.html', login=login)
    return redirect(url_for('auth.signin'))