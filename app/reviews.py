from flask import render_template, request, url_for, redirect
from flask_login import current_user

from .models.review import Review

from flask import Blueprint
bp = Blueprint('reviews', __name__)


@bp.route('/reviews', methods=['GET','POST'])
def getReview():
    if(request.method=='POST'):
        uid = request.form["nm"]
        return redirect(url_for("users.reviews",uid=uid))
    else:
        return render_template('reviewsIn.html')