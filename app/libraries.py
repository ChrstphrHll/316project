from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

from .models.library import Library
from flask import current_app as app

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

@bp.route('/<lid>')
def library(lid):
    library = Library.get(lid)
    copies = Library.get_copies(lid)
    return render_template("library.html", library=library, copies=copies)
