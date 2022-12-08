from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse

import datetime
  
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.fields import StringField, PasswordField, SelectField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo


from .models.game import Game
from .models.mechanic import Mechanic
from .models.user import User
from .models.recommendation import Recommendation
from .models.mechanic import Mechanic
from .models.review import Review
from flask import current_app as app
from flask_login import current_user


from flask import Blueprint
bp = Blueprint('game', __name__, url_prefix="/games")

class Search(FlaskForm):
    search = StringField('Name:', validators=[])
    mechname = StringField('Mechanic:', validators=[], render_kw={"list": "mech_list"})
    submit = SubmitField('Create')

@bp.route('/')
def games():
    form = Search()


    page = int(request.args.get('page') or 0) 
    per_page = int(request.args.get('per_page') or 12)
    mechanic = request.args.get('mechanic') or None
    search = request.args.get('search') or None

    try:
        games = Game.get_some(page=page, per_page=per_page, mechanic=mechanic, search=search)
        mechanics = Mechanic.get_all()
    except:
        return redirect(url_for('index.notFound'))


    if search:
        search = search.lower()
    
    return render_template("game_pages/game_search.html", games=games, mechanics=mechanics, form=form, current_page = page, per_page = per_page, mechanic=mechanic, search=search)


class sumbitReview(FlaskForm):
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    rating = SelectField('Rating', validators=[DataRequired()], choices=[1,2,3,4,5])
    description = TextAreaField('Description', render_kw={"cols": 48, "rows": 4})
    submit = SubmitField('Submit')

@bp.route('/<gid>', methods=['GET', 'POST'])
def game(gid):

    
    if request.method == 'POST' and current_user.is_authenticated:
        if "log_play" in request.form:
                User.increment_play_count(current_user.uid, gid)
        elif "like" in request.form:
                User.toggle_like_game(current_user.uid, gid)
        elif "rating" in request.form:
                Review.create(current_user.uid, gid,request.form['rating'], 
                request.form['description'],  datetime.datetime.now())
        elif "deleteReview" in request.form:
            Review.delete(current_user.uid, gid)


    game = Game.get(gid)
    mechanics = Game.get_mechanics(gid)
    gameReviews = Review.get_top_5_game(gid)
    avgRating = Review.get_avg_rating(gid)
    if(avgRating):
        avgRating = str(round(avgRating, 2)) + "/5"

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
    gameReviews=gameReviews, userReview=userReview, review_form=review_form, avgRating=avgRating, likeStatus=likeStatus, playCount=playCount)
