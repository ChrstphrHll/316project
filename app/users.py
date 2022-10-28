from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

from app.models.copy import Copy
from .models.user import User
from .models.recommendation import Recommendation
from .models.mechanic import Mechanic
from .models.collection import Collection
from .models.library import Library

from flask import Blueprint
bp = Blueprint('users', __name__)


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_auth(form.email.data, form.password.data)
        if user is None:
            flash('Invalid email or password')
            return redirect(url_for('users.login'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index.index')

        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(),
                                       EqualTo('password')])
    submit = SubmitField('Register')

    def validate_email(self, email):
        if User.email_exists(email.data):
            raise ValidationError('Already a user with this email.')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        if User.register(form.name.data,
                         form.email.data,
                         form.password.data):
            flash('Congratulations, you are now a registered user!')
            return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index.index'))


@bp.route('/users/<uid>/liked')
def likesgame(uid):
    # return all games this user likes
    liked_games = User.get_liked_games(uid)
    return render_template("likesgame.html", liked_games=liked_games)

@bp.route('/users/<uid>/recommended')
def recommended(uid):
    liked = Recommendation.get_base(uid)
    recs = []
    mechs = []
    for like in liked:
        liked_gid = like.gid
        mech = Mechanic.get(liked_gid)
        rec = Recommendation.get(uid, liked_gid)
        recs.append(rec)
        mechs.append(mech)
    return render_template('recommended.html', recommended=recs, liked=liked, mechs=mechs)


class CollectionSearch(FlaskForm):
    search = StringField('Search', validators=[DataRequired()])

class CollectionCreate(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Create')

@bp.route('/users/<uid>/collections', methods=['GET', 'POST'])
def collections(uid):
    collections = Collection.get_user_collections(uid)
    search_form = CollectionSearch()
    
    if "search" in request.args:
        collections = filter(lambda x : request.args.get("search").lower() in x.title.lower(), collections)

    create_form = CollectionCreate()
    print("here")
    if create_form.validate_on_submit():
        print("got here")
        collection = Collection.create(create_form.title.data, create_form.description.data, current_user.uid)
        if collection:
            return redirect(url_for('collection.collection', cid=collection.cid))

    return render_template('collections.html', collections=collections, form=search_form, create=create_form)

class LibrarySearch(FlaskForm):
    search = StringField('Search', validators=[DataRequired()])

@bp.route('/users/<uid>/libraries')
def libraries(uid):
    libraries = Library.get_user_libraries(uid)
    form = CollectionSearch()

    if "search" in request.args:
        libraries = filter(lambda x : request.args.get("search").lower() in x.title.lower(), libraries)

    return render_template('libraries.html', libraries=libraries, form=form)


class BorrowedSearch(FlaskForm):
    search = StringField('Search', validators=[DataRequired()])

@bp.route('/users/<uid>/borrowed')
def borrowed(uid):
    borrowed_copies = Copy.user_borrowed_copies(uid)
    form = BorrowedSearch()

    if "search" in request.args:
        borrowed_copies = filter(lambda x : request.args.get("search").lower() in x.title.lower(), borrowed_copies)

    return render_template('borrowed.html', copies=borrowed_copies, form=form)