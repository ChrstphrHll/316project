from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse

from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

from .models.game import Game
from flask import current_app as app

from flask import Blueprint
bp = Blueprint('game', __name__, url_prefix="/games")

class Search(FlaskForm):
    search = StringField('search', validators=[DataRequired()])

@bp.route('/')
def games():
    form = Search()
    
    query = '''
SELECT gid, name, description, image_url, complexity, length, min_players, max_players
FROM Games
'''


    games_raw = app.db.execute(query)

    games = [Game(*game) for game in games_raw]

    if "search" in request.args:
        games = filter(lambda x: request.args.get("search").lower() in x.name.lower(), games)

    return render_template("game_search.html", games = games, form=form)

@bp.route('/<gid>')
def game(gid):
    query = '''
SELECT *
FROM Games
WHERE Games.gid = :gid
'''
    game_raw = app.db.execute(query, gid=gid)
    game = [Game(*game) for game in game_raw]

    return render_template("game.html", game = [] if len(game) == 0 else game[0])

