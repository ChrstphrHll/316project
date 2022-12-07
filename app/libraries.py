from crypt import methods
from ssl import create_default_context
from venv import create
from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user
from werkzeug.urls import url_parse
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

from .models.library import Library
from .models.game import Game
from .models.copy import Copy
from .models.user import User

from flask import Blueprint
bp = Blueprint('library', __name__, url_prefix='/libraries')

class Search(FlaskForm):
    search = StringField('Search', validators=[DataRequired()])

@bp.route('/')
def libraries():
    form = Search()
    prev_search_string = ""

    libraries = Library.get_all()
    
    if "search" in request.args:
        libraries = filter(lambda x : request.args.get("search").lower() in x.title.lower(), libraries)
        prev_search_string = request.args.get("search")
        
    return render_template('libraries.html', libraries=libraries, form=form, prev_search_string = prev_search_string)

class Create(FlaskForm):
    comment = StringField('Comment')
    gamename = StringField('Game Name', validators=[DataRequired()], render_kw={"list": "game_list"})
    borrower  = StringField('Borrower Name', render_kw={"list": "user_list"})
    submit = SubmitField('Create')

@bp.route('/<lid>', methods=["GET", "POST"])
def library(lid):
    library = Library.get(lid)
    copies = Library.get_copies(lid)
    all_games = Game.get_all()
    all_users = User.get_all()

    create_form = Create() if current_user.is_authenticated and current_user.uid == int(library.owner.uid) else None

    if create_form and create_form.validate_on_submit():
        name = create_form.gamename.data
        borrowername = create_form.borrower.data if create_form.borrower.data else ""
        comment = create_form.comment.data if create_form.comment.data else ""

        if(name):
            game = Game.get_by_name(name)
            if(game):
                borrower = User.get_by_name(borrowername)
                borrower_id = borrower.uid if borrower else None 

                if Copy.create(game.gid, comment, lid, borrower_id):
                    return redirect(url_for('library.library', lid=lid))

    return render_template("library.html", library=library, copies=copies, create=create_form, user=current_user, all_games=all_games, all_users=all_users)

@bp.route('/<lid>/checkout/<cpid>', methods=["GET", "POST"])
def checkout(lid, cpid):
    res = Copy.checkout_copy(cpid, current_user.uid)

    if res:
        return redirect(url_for('library.library', lid=lid))

@bp.route('/return/<cpid>', methods=["GET", "POST"])
def return_copy(cpid):
    borrower = Copy.checked_out_by(cpid)

    if borrower.uid == current_user.uid or str(cpid) in list(map(lambda copy: str(copy.cpid), Copy.user_owned_copies(current_user.uid))):
        res = Copy.return_copy(cpid, borrower.uid)

    return redirect(request.referrer)
