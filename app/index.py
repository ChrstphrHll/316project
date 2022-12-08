from flask import render_template
from flask_login import current_user
import datetime

from .models.review import Review
from .models.game import Game
from .models.user import User
from .models.recommendation import Recommendation

from flask import Blueprint
bp = Blueprint('index', __name__)


@bp.route('/')
def index():
    rand_game = Game.get_random()
    sim_games = Recommendation.get_sim_games(rand_game.gid)
    rec_collections = Recommendation.get_sim_coll(Recommendation.get_pop_mech(current_user.uid).mech_name)
    return render_template('index.html', rand_game=rand_game, sim_games=sim_games, rec_collections=rec_collections)

@bp.route('/404')
def notFound():
    return render_template('404.html')