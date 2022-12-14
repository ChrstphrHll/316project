from crypt import methods
from ssl import create_default_context
from venv import create
from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user
from werkzeug.urls import url_parse
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

from .models.collection import Collection
from .models.game import Game
from flask import current_app as app
from flask import Blueprint

bp = Blueprint('collection', __name__, url_prefix='/collections')

class Search(FlaskForm):
    search = StringField('Search', validators=[DataRequired()])

@bp.route('/')
def collections():
    form = Search()
    prev_search_string = ""

    collections = Collection.get_all()
    
    if "search" in request.args:
        collections = filter(lambda x : request.args.get("search").lower() in x.title.lower(), collections)
        prev_search_string = request.args.get("search")

    return render_template('collections.html', collections=collections, form=form, prev_search_string = prev_search_string)

class Create(FlaskForm):
    gamename = StringField('Game Name', validators=[DataRequired()], render_kw={"list": "game_list"})
    submit = SubmitField('Create')

class Delete(FlaskForm):
    delete = SubmitField('Delete Collection')

@bp.route('/<cid>', methods=["GET", "POST", "DELETE"])
def collection(cid):
    collection = Collection.get(cid)
    games = Collection.get_games(cid)
    all_games = Game.get_all()
    collection_games = Collection.get_games(cid)
    creator = Collection.get_creator(cid)
    edit_permissions = current_user.is_authenticated and current_user.uid == int(collection.creator.uid)
    likeStatus = False

    create_form = None
    delete_form = None
    remove_form = None

    if request.method == 'POST' and current_user.is_authenticated:
        if "like" in request.form:
            Collection.toggle_like_collection(current_user.uid, cid)

    if current_user.is_authenticated:
        likeStatus = Collection.get_liked_status(current_user.uid, cid)

    if current_user.is_authenticated and current_user.uid == int(collection.creator.uid):
        create_form = Create()
        delete_form = Delete()

    if create_form and create_form.validate_on_submit():
        name = create_form.gamename.data

        if(name):
            game = Game.get_by_name(name)
            if game:
                if Collection.add_game(cid, game.gid):
                    return redirect(url_for('collection.collection', cid=cid))
    
    if request.method == "POST" and "delete_id" in request.form and current_user.uid == int(collection.creator.uid):
        remove_id = Game.get(request.form['delete_id'])

        if remove_id:
            res = Collection.remove_game(cid, remove_id.gid)
            if res:
                return redirect(url_for('collection.collection', cid=cid))

    if delete_form and delete_form.validate_on_submit() and "delete" in request.form:
        res = Collection.delete(cid)
        if res:
            return redirect(url_for('users.collections', uid=creator.uid))

    return render_template("collection.html", edit_permissions=edit_permissions, collection=collection, collection_games=collection_games, games=games, all_games=all_games, create=create_form, delete=delete_form, remove=remove_form, likeStatus=likeStatus)
