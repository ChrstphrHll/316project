from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse


from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.fields import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo


from .models.game import Game
from .models.user import User
from .models.review import Review
from flask import current_app as app
from flask_login import current_user

from math import ceil

from flask import Blueprint
bp = Blueprint('game', __name__, url_prefix="/games")

class Search(FlaskForm):
    search = StringField('search', validators=[DataRequired()])

@bp.route('/')
def games():
    form = Search()

    page = int(request.args.get('page') or 0) 
    per_page = int(request.args.get('per_page') or 10)
    mechanic = request.args.get('mechanic') or None

    try:
        games = Game.get_some(page=page, per_page=per_page, mechanic=mechanic)
    except:
        return redirect(url_for('index.notFound'))

    max_page = ceil(len(games)/per_page)


    if "search" in request.args:
        games = filter(lambda x: request.args.get("search").lower() in x.name.lower(), games)
    
    # if "mechanic" in request.args:
    #     games = filter(lambda x: request.args.get("mechanic"))

    # games = games[0 + (page * per_page): per_page + (page * per_page)]

    return render_template("game_pages/game_search.html", games = games, form=form, current_page = page, per_page = per_page, mechanic=mechanic)


class sumbitReview(FlaskForm):
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    rating = StringField('Rating', validators=[DataRequired()], render_kw={"size": 32})
    description = TextAreaField('Description', render_kw={"cols": 48, "rows": 4})
    submit = SubmitField('Save Changes')

@bp.route('/<gid>', methods=['GET', 'POST'])
def game(gid):

    
    if request.method == 'POST':
        print(request.form)
        if "log_play" in request.form:
            if current_user.is_authenticated:
                User.increment_play_count(current_user.uid, gid)


    game = Game.get(gid)
    mechanics = Game.get_mechanics(gid)
    gameReviews = Review.get_top_5_game(gid)
    if current_user.is_authenticated:
        review_form = sumbitReview(User.get(current_user.uid))
        user = User.get(current_user.uid)
        playCount = User.get_play_count(current_user.uid, gid)
        playCount = playCount if playCount else 0
        userReview = Review.get(current_user.uid, gid)
        
    else:
        playCount = None
        userReview = []
        user = None

