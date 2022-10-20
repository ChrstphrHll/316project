from flask import render_template, request, url_for, redirect
from flask_login import current_user

from .models.review import Review

from flask import Blueprint
bp = Blueprint('reviews', __name__)


@bp.route('/reviews', methods=['GET','POST'])
def getReview():
    if(request.method=='POST'):
        user = request.form["nm"]
        return redirect(url_for("reviews.showReview",usr=user))
    else: 
        return render_template('reviewsIn.html')

@bp.route('/reviews/<usr>', methods=['GET', 'POST'])
def showReview(usr):
    reviews = Review.get_top_5(int(usr))
    return render_template('reviews.html', review_history=reviews)