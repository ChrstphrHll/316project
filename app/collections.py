from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

from .models.collection import Collection
from flask import current_app as app

from flask import Blueprint
bp = Blueprint('collections', __name__, url_prefix='/collections')

class Search(FlaskForm):
    search = StringField('Search', validators=[DataRequired()])

@bp.route('/')
def collections():
    form = Search()

    collections = Collection.get_all()
    
    if "search" in request.args:
        collections = filter(lambda x : request.args.get("search").lower() in x.title.lower(), collections)

    return render_template('collections.html', collections=collections, form=form)

@bp.route('/<cid>')
def collection(cid):
    collection = Collection.get(cid)
    games = Collection.get_games(cid)
    return render_template("collection.html", collection=collection, games=games)
