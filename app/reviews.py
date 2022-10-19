from flask import render_template, request
from flask_login import current_user

from .models.review import Review

from flask import Blueprint
bp = Blueprint('reviews', __name__)


@bp.route('/reviews', methods=['GET'])
def feedback():
    reviews = Review.get_top_5(int(request.args.get("uid")))
    return render_template('reviews.html', review_history=reviews)