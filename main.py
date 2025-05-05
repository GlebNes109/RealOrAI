from flask import render_template

from flask import Flask
from flask_wtf import CSRFProtect
from app.src.auth import auth_blueprint
from app.src.config import settings
from app.src.mainpage import home_blueprint
from app.src.repository.repository import Repository

app = Flask(__name__)
app.config['SECRET_KEY'] = settings.secret_key
CSRFProtect(app)

repository = Repository()

app.register_blueprint(auth_blueprint)
app.register_blueprint(home_blueprint)

if __name__ == '__main__':
    app.run(port=settings.server_port, host=settings.server_host)