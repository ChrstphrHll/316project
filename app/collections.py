import string
from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

from .models.collection import Collection

from flask import Blueprint
bp = Blueprint('collections', __name__, url_prefix='/collections')

@bp.route('/', methods=['GET'])
def collections():
    collection_list = Collection.get_all()
    print(str(current_user.uid))
    return render_template('collections.html', collections=collection_list)
