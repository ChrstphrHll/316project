from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse

from .models.game import Game

from flask import Blueprint
bp = Blueprint('game', __name__, url_prefix="/game")

@bp.route('/')
def likesgame():
    # return all games this user likes
    games = [{"gid": 1, "name": "Fantasy Realms"}]
    return render_template("game_search.html", games = games)