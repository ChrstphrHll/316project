from flask import render_template
from flask_login import current_user
import datetime

from .models.review import Review
from .models.game import Game

from flask import Blueprint
bp = Blueprint('index', __name__)


@bp.route('/')
def index():
    rand_game = Game.get_random()
    return render_template('index.html', rand_game=rand_game)

@bp.route('/404')
def notFound():
    return render_template('404.html')