from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse

from .models.game import Game
from flask import current_app as app

from flask import Blueprint
bp = Blueprint('game', __name__, url_prefix="/game")



@bp.route('/')
def games():
    cols = request.args.getlist('cols')
    dirs = request.args.getlist('dirs')
    
    query = '''
SELECT gid, name, description, image_url, complexity, length, min_players, max_players
FROM Games
'''
    games_raw = app.db.execute(query)

    games = [Game(*game) for game in games_raw]

    return render_template("game_search.html", games = games)

