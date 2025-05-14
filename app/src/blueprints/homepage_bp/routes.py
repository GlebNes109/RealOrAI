from flask import session, render_template, redirect, url_for

from app.src.database.repository import Repository
from app.src.blueprints.homepage_bp import home_bp

repository = Repository()

@home_bp.route('/home')
def home():
    if 'user_id' in session:
        user_id = session['user_id']
        user_db = repository.get_user_by_id(user_id)
        if not user_db:
            return redirect(url_for('auth_bp.signin'))
        limit = 10
        scoreboard = repository.get_scoreboard(user_id, limit)
        print(scoreboard)
        return render_template('homepage.html', login=user_db.login, scoreboard=scoreboard)
    return redirect(url_for('auth_bp.signin'))