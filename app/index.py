from flask import render_template
from flask_login import current_user
import datetime

from .models.review import Review

from flask import Blueprint
bp = Blueprint('index', __name__)


@bp.route('/')
def index():
    return render_template('index.html')

