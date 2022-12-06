from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse

import datetime
  
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.fields import StringField, PasswordField, SelectField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo


from .models.game import Game
from .models.user import User
from .models.recommendation import Recommendation
from .models.mechanic import Mechanic
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
    prev_search_string = ""

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
        prev_search_string = request.args.get("search")
    
    # if "mechanic" in request.args:
    #     games = filter(lambda x: request.args.get("mechanic"))

    # games = games[0 + (page * per_page): per_page + (page * per_page)]

    return render_template("game_pages/game_search.html", games = games, form=form, prev_search_string = prev_search_string, current_page = page, per_page = per_page, mechanic=mechanic)


class sumbitReview(FlaskForm):
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    rating = SelectField('Rating', validators=[DataRequired()], choices=[1,2,3,4,5])
    description = TextAreaField('Description', render_kw={"cols": 48, "rows": 4})
    submit = SubmitField('Submit')

@bp.route('/<gid>', methods=['GET', 'POST'])
def game(gid):

    
    if request.method == 'POST':
        if "log_play" in request.form:
            if current_user.is_authenticated:
                User.increment_play_count(current_user.uid, gid)
        elif "like" in request.form:
            if current_user.is_authenticated:
                User.toggle_like_game(current_user.uid, gid)
        elif "rating" in request.form:
            if current_user.is_authenticated:
                Review.create(current_user.uid, gid,request.form['rating'], 
                request.form['description'],  datetime.datetime.now())


    game = Game.get(gid)
    mechanics = Game.get_mechanics(gid)
    gameReviews = Review.get_top_5_game(gid)
    avgRating = Review.get_avg_rating(gid)
    if(avgRating):
        avgRating = round(avgRating, 2)

    sim_games = Recommendation.get_sim_games(gid)
    shared_mechs = Mechanic.get_shared_mechs_all(gid, sim_games)

    if current_user.is_authenticated:
        review_form = sumbitReview(User.get(current_user.uid))
        user = User.get(current_user.uid)
        playCount = User.get_play_count(current_user.uid, gid)
        playCount = playCount if playCount else 0
        likeStatus = User.check_likes(current_user.uid, gid)
        userReview = Review.get(gid, current_user.uid)
        
    else:
        userReview = []
        user = None
        review_form = None
        likeStatus = None

    return render_template("game_pages/game.html", game=game, mechanics=mechanics, sim_games=sim_games, shared_mechs=shared_mechs, 
    gameReviews=gameReviews, userReview=userReview, review_form=review_form, avgRating=avgRating, likeStatus=likeStatus)
