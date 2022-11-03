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
    
    games = Game.get_all()

    if "search" in request.args:
        games = filter(lambda x: request.args.get("search").lower() in x.name.lower(), games)

    return render_template("game_search.html", games = games, form=form)

@bp.route('/<gid>')
def game(gid):
    game = Game.get(gid)
    return render_template("game.html", game=game)

