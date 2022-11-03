from flask import render_template, redirect, url_for, flash, request, Blueprint
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from .models.mechanic import Mechanic
bp = Blueprint('mechanic', __name__, url_prefix="/mechanics")

class SearchForm(FlaskForm):
    search = StringField('Search', validators=[DataRequired()])

@bp.route('/')
def mechanics():
    form = SearchForm()
    mechs = Mechanic.get_all()
    if form.validate_on_submit:
        return redirect(url_for('mechanics.mech_search', mech=mechs))

@bp.route('/<mech>')
def mech_search():
    form = SearchForm()
    mechs = Mechanic.get_all()
    if form.validate_on_submit:
        return redirect(url_for('login'))
    return render_template('mechanics.html', mechs=mechs)