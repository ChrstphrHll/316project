from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, HiddenField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

from .models.copy import Copy
from .models.user import User
from .models.recommendation import Recommendation
from .models.mechanic import Mechanic

from .models.collection import Collection
from .models.library import Library
from .models.review import Review


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
    name = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(),
                                       EqualTo('password')])
    submit = SubmitField('Register')

    def validate_name(self, name_field):
        if User.username_exists(name_field.data):
            raise ValidationError("Already a user with this username")

    def validate_email(self, email_field):
        if User.email_exists(email_field.data):
            raise ValidationError('Already a user with this email')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        if User.register(form.name.data,
                         form.email.data,
                         form.password.data):
            user = User.get_by_auth(form.email.data, form.password.data)
            if user: # should always be true
                login_user(user)
                return redirect(url_for('users.profile', uid=user.uid))
    return render_template('register.html', title='Register', form=form)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index.index'))



class Search(FlaskForm):
    search = StringField('search', validators=[DataRequired()])

@bp.route('/users', methods=['GET','POST'])
def user_search():
    search_form = Search()
    prev_search_string = ""
    users = User.get_all()

    if "search" in request.args:
        users = filter(lambda x: request.args.get("search").lower() in x.name.lower(), users)
        prev_search_string = request.args.get("search")

    return render_template("user_pages/user_search.html", users=users, search_form=search_form, prev_search_string=prev_search_string)


class EditUserInfo(FlaskForm):
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    name = StringField('Username', validators=[DataRequired()], render_kw={"size": 32})
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"size": 32})
    about = TextAreaField('About', render_kw={"cols": 48, "rows": 4})
    password = PasswordField('New Password', validators=[EqualTo('repeat_password', message='Passwords must match')])
    repeat_password = PasswordField('Repeat Password')
    submit = SubmitField('Save Changes')

    def validate_name(self, name_field):
        if name_field.data != self.user.name and User.username_exists(name_field.data):
            raise ValidationError("Another user has this username already")

    def validate_email(self, email_field):
        if email_field.data != self.user.email and User.email_exists(email_field.data):
            raise ValidationError("Another user has this email already")

class ProfilePic(FlaskForm):
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
    image_url = HiddenField('image_url')
    submit = SubmitField('Save')
    valid_urls = ["https://cdn.pixabay.com/photo/2012/02/28/00/49/snow-17854_1280.jpg",
                    "https://cdn.pixabay.com/photo/2020/04/08/06/58/elephant-5015980__480.jpg",
                    "https://cdn.pixabay.com/photo/2018/07/22/21/12/panda-3555554_1280.jpg",
                    "https://cdn.pixabay.com/photo/2016/02/15/00/04/penguin-1200535__480.jpg",
                    "https://cdn.pixabay.com/photo/2014/08/24/19/10/clownfish-426567__480.jpg"]
    def validate_image_url(self, image_url_field):
        if not image_url_field.data in ProfilePic.valid_urls:
            raise ValidationError("Invalid profile pic URL")


@bp.route('/users/<uid>', methods=['GET','POST'])
def profile(uid):
    if not User.get(uid):
        return redirect(url_for("index.notFound"))
    
    user = User.get(uid)
    edit_info_form = EditUserInfo(user)
    profile_pic_form = ProfilePic(User.get(uid))
    designed_games = user.get_designed_games()
    
    if request.method == 'POST':
        if edit_info_form.validate_on_submit():
            User.get(uid).update_information(edit_info_form.data) # filters these to only use the relevant ones
            return redirect(url_for('users.profile', uid=uid))
        if profile_pic_form.validate_on_submit():
            User.get(uid).update_profile_pic(profile_pic_form.image_url.data)
            return redirect(url_for('users.profile', uid=uid))

    return render_template("user_pages/user_profile.html", user=User.get(uid), designed_games=designed_games, edit_info_form=edit_info_form, pic_form=profile_pic_form)


@bp.route('/users/<uid>/liked')
def liked(uid):
    if not User.get(uid):
        return redirect(url_for("index.notFound"))
    
    # return all games this user likes
    liked_games = User.get_liked_games(uid)
    return render_template("user_pages/liked.html", user=User.get(uid), liked_games=liked_games)

@bp.route('/users/<uid>/recommended')
def recommended(uid):
    liked = User.get_liked_games(uid)
    if len(liked) == 0:
        pop_games = Recommendation.get_pop_games()
        pop_coll = Recommendation.get_pop_coll()
        return render_template('user_pages/no_recs.html', pop_games=pop_games, pop_coll=pop_coll)
    if not User.get(uid) or not current_user.is_authenticated or current_user.uid != int(uid):
        return redirect(url_for("index.notFound"))

    pop_mech = Recommendation.get_pop_mech(uid)
    pop_name = pop_mech.mech_name
    pop_designer = Recommendation.get_pop_designer(uid)
    designer = pop_designer.name
    did = pop_designer.uid

    easy_recs = Recommendation.get_w_easy_mech(uid, pop_name)
    hard_recs = Recommendation.get_w_hard_mech(uid, pop_name)
    design_recs = Recommendation.get_w_designer(uid, did)
    sim_coll = Recommendation.get_sim_coll(pop_name)
 
    return render_template('user_pages/recommended.html', user=User.get(uid), easy_recs=easy_recs, hard_recs=hard_recs,
     pop_name=pop_name, designer=designer, design_recs=design_recs, sim_coll=sim_coll)

class Search(FlaskForm):
    search = StringField('Search', validators=[DataRequired()])

class Create(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Create')

@bp.route('/users/<uid>/collections', methods=['GET', 'POST'])
def collections(uid):
    if not User.get(uid):
        return redirect(url_for("index.notFound"))

    collections = Collection.get_user_collections(uid)
    search_form = Search()
    prev_search_string = ""
    
    if "search" in request.args:
        collections = filter(lambda x : request.args.get("search").lower() in x.title.lower(), collections)
        prev_search_string = request.args.get("search")

    create_form = Create() if current_user.is_authenticated and current_user.uid == int(uid) else None

    if create_form and create_form.validate_on_submit():
        collection = Collection.create(create_form.title.data, create_form.description.data, current_user.uid)
        if collection:
            return redirect(url_for('users.collections', uid=uid))

    return render_template('user_pages/collections.html', user=User.get(uid), collections=collections, form=search_form, prev_search_string = prev_search_string, create=create_form)

@bp.route('/users/<uid>/libraries', methods=['GET', 'POST'])
def libraries(uid):
    if not User.get(uid):
        return redirect(url_for("index.notFound"))
    
    libraries = Library.get_user_libraries(uid)
    form = Search()
    prev_search_string = ""

    if "search" in request.args:
        libraries = filter(lambda x : request.args.get("search").lower() in x.title.lower(), libraries)
        prev_search_string = request.args.get("search")

    create_form = Create() if current_user.is_authenticated and current_user.uid == int(uid) else None

    if create_form and create_form.validate_on_submit():
        library = Library.create(create_form.title.data, create_form.description.data, current_user.uid)
        if library:
            return redirect(url_for('users.libraries', uid=uid))

    return render_template('user_pages/libraries.html', user=User.get(uid), libraries=libraries, form=form, prev_search_string=prev_search_string, create=create_form)

@bp.route('/users/<uid>/borrowed')
def borrowed(uid):
    print("current",current_user)
    if not User.get(uid) or not current_user.is_authenticated or current_user.uid != int(uid):
        return redirect(url_for("index.notFound"))
    
    borrowed_copies = Copy.user_borrowed_copies(uid)
    owned_copies = Copy.user_owned_copies(uid)
    for copy in owned_copies:
        print(copy.cpid)
    form = Search()

    if "search" in request.args:
        borrowed_copies = filter(lambda x : request.args.get("search").lower() in x.game.name.lower(), borrowed_copies)

    return render_template('user_pages/borrowed.html', user=User.get(uid), borrowed_copies=borrowed_copies, owned_copies=owned_copies, form=form)

@bp.route('/users/<uid>/reviews', methods=['GET', 'POST'])
def reviews(uid):
    if not User.get(uid) or not current_user.is_authenticated or current_user.uid != int(uid):
        return redirect(url_for("index.notFound"))
    
    reviews = Review.get_all_user(int(uid))
    return render_template('user_pages/reviews.html', user=User.get(uid), review_history=reviews)
