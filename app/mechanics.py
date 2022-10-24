from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse

from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

from .models.mechanic import Mechanic
from flask import current_app as app

mech = Blueprint('mechanics', __name__, url_prefix='/mechanics')
app.register(mech)

@bp.route('/')
def mechanics():
    mechs = Mechanic.get()
    return render_template('mechanics.html', mechanics=mechs)

@bp.route('/<name>/')
def games_with(name):
    mech_games = Mechanic.get_games(name)
    return render_template('game_with_mech.html', games=mech_games)

