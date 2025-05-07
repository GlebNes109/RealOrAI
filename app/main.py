from flask import Flask, send_from_directory
from flask_wtf import CSRFProtect
from cachetools import LRUCache

from app.src.blueprints.auth_bp import auth_bp
from app.src.config import settings
from app.src.blueprints.game_bp import game_bp
from app.src.blueprints.homepage_bp import home_bp
from app.src.database.repository import Repository

app = Flask(__name__)
app.config['SECRET_KEY'] = settings.secret_key
app.config['WTF_CSRF_ENABLED'] = True
csrf = CSRFProtect(app)
cache = LRUCache(maxsize=100)
repository = Repository()

app.register_blueprint(auth_bp)
app.register_blueprint(home_bp)
app.register_blueprint(game_bp)

@app.route('/user_data/<filename>')
def user_data(filename):
    return send_from_directory('static/user_data', filename)

"""@app.after_request
def add_csrf_token(response):
    response.headers['X-CSRF-Token'] = csrf.generate_csrf()
    return response"""

if __name__ == '__main__':
    app.run(port=settings.server_port, host=settings.server_host)