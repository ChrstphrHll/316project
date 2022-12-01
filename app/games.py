from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse


from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

from .models.game import Game
from .models.user import User
from flask import current_app as app
from flask_login import current_user


from flask import Blueprint
bp = Blueprint('game', __name__, url_prefix="/games")

class Search(FlaskForm):
    search = StringField('search', validators=[DataRequired()])

@bp.route('/')
def games():
    form = Search()
    
    games = Game.get_all()

    if "search" in request.args:
        games = filter(lambda x: request.args.get("search").lower() in x.name.lower(), games)

    return render_template("game_search.html", games = games, form=form)

@bp.route('/<gid>', methods=['GET', 'POST'])
def game(gid):
    if request.method == 'POST':
        print(request.form)
        if "log_play" in request.form:
            if current_user.is_authenticated:
                User.increment_play_count(current_user.uid, gid)


    game = Game.get(gid)
    mechanics = Game.get_mechanics(gid)
    if current_user.is_authenticated:
        playCount = User.get_play_count(current_user.uid, gid)
        playCount = playCount if playCount else 0
    else:
        playCount = None
    return render_template("game.html", game=game, mechanics=mechanics, playCount=playCount)

