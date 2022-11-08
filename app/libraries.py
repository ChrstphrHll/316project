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
from .models.copy import Copy

from flask import Blueprint
bp = Blueprint('library', __name__, url_prefix='/libraries')

class Search(FlaskForm):
    search = StringField('Search', validators=[DataRequired()])

@bp.route('/')
def libraries():
    form = Search()

    libraries = Library.get_all()
    
    if "search" in request.args:
        libraries = filter(lambda x : request.args.get("search").lower() in x.title.lower(), libraries)
        
    return render_template('libraries.html', libraries=libraries, form=form)

class Create(FlaskForm):
    comment = StringField('Comment', validators=[DataRequired()])
    gid = StringField('Game ID', validators=[DataRequired()])
    borrower = StringField('Borrower ID', validators=[])
    submit = SubmitField('Create')

@bp.route('/<lid>', methods=["GET", "POST"])
def library(lid):
    library = Library.get(lid)
    copies = Library.get_copies(lid)

    create_form = Create() if current_user.is_authenticated and current_user.uid == int(library.owner.uid) else None

    if create_form and create_form.validate_on_submit():
        copy = Copy.create(create_form.gid.data, create_form.comment.data, lid, create_form.borrower.data)
        if copy:
            return redirect(url_for('library.library', lid=lid))

    return render_template("library.html", library=library, copies=copies, create=create_form)

@bp.route('/<lid>/checkout/<cpid>', methods=["GET", "POST"])
def checkout(lid, cpid):
    Copy.checkout_copy(cpid, current_user.uid)

    return redirect(url_for('library.library', lid=lid))

@bp.route('/<lid>/return/<cpid>', methods=["GET", "POST"])
def return_copy(cpid):
    Copy.return_copy(cpid, current_user.uid)

    return redirect(url_for('users.borrowed'))
