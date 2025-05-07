from flask import Blueprint

game_bp = Blueprint('game_bp', __name__, template_folder='templates')

from . import routes