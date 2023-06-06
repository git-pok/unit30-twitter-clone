import os

from flask import Flask, render_template, request, flash, redirect, session, g
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
import requests
from forms import UserAddForm, LoginForm, MessageForm, UserEditForm
from models import db, connect_db, User, Message, Follows, Likes
from app_methods import update_user, add_to_like, delete_like, xml_check_for_header_img

CURR_USER_KEY = "curr_user"

app = Flask(__name__)

# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql:///warbler'))
# test db
# app.config['SQLALCHEMY_DATABASE_URI'] = (
#     os.environ.get('DATABASE_URL', 'postgresql:///warbler-test'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")
toolbar = DebugToolbarExtension(app)

connect_db(app)

# import pdb
# pdb.set_trace()
# raise

##############################################################################
# User signup/login/logout


@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""
    # this view runs before every request
    # line 39 creates a g object with info for the logged in user 
    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


def do_login(user):
    """Log in user."""
    # creates a session variable to track user
    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


@app.route('/signup', methods=["GET", "POST"])
def signup():
    """Handle user signup. 

    Create new user and add to DB. Redirect to home page.

    If form not valid, present form.

    If the there already is a user with that username: flash message
    and re-present form.
    """
    form = UserAddForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
                image_url=form.image_url.data or User.image_url.default.arg,
            )
            db.session.commit()
            # Added line 81
            session[CURR_USER_KEY] = user.id

        except IntegrityError:
            flash("Username already taken", 'danger')
            return render_template('users/signup.html', form=form)

        do_login(user)

        return redirect("/")

    else:
        return render_template('users/signup.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login."""
    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)

        if user:
            do_login(user)
            # Added line 114
            flash(f"Hello, {user.username}!", "success")
            return redirect("/")

        flash("Invalid credentials.", 'danger')

    return render_template('users/login.html', form=form)


@app.route('/logout')
def logout():
    """Handle logout of user."""
    # wrote all logic
    session.clear()
    flash(f"Successfully logged out!", "success")
    return redirect('/')


##############################################################################
# General user routes:

@app.route('/users')
def list_users():
    """Page with listing of users.

    Can take a 'q' param in querystring to search by that username.
    """
    # Added line 141, 142 and 151-153.
    try:
        if session.get(CURR_USER_KEY) == g.user.id:
            search = request.args.get('q')

            if not search:
                users = User.query.all()
            else:
                users = User.query.filter(User.username.ilike(f"%{search}%")).all()

            return render_template('users/index.html', users=users)
    except AttributeError:
        flash("Access unauthorized.", "danger")
        return redirect('/')


@app.route('/users/<int:user_id>')
def users_show(user_id):
    """Show user profile."""
    # Added line 160-161, 165, 167, and 179-181.
    try:
        if session.get(CURR_USER_KEY) == g.user.id:
            user = User.query.get_or_404(user_id)

            # line 153 is for xml images not appearing in headers
            status_code = xml_check_for_header_img(user)
    
            likes = db.session.query(Likes).join().all()
            # snagging messages in order from the database;
            # user.messages won't be in order by default
            messages = (Message
                        .query
                        .filter(Message.user_id == user_id)
                        .order_by(Message.timestamp.desc())
                        .limit(100)
                        .all())
            return render_template('users/show.html', user=user, messages=messages,
            status_code=status_code
            )
    except AttributeError:
        flash("Access unauthorized.", "danger")
        return redirect('/')


@app.route('/users/<int:user_id>/following')
def show_following(user_id):
    """Show list of people this user is following."""
    # Added line 188-189, 197, and 202-204.
    try:
        if session.get(CURR_USER_KEY) == g.user.id:
            if not g.user:
                flash("Access unauthorized.", "danger")
                return redirect("/")

            user = User.query.get_or_404(user_id)

            # line 180 is for xml images not appearing in headers
            status_code = xml_check_for_header_img(user)

            return render_template('users/following.html', user=user,
            status_code=status_code
            )
    except AttributeError:
        flash("Access unauthorized.", "danger")
        return redirect('/')


@app.route('/users/<int:user_id>/followers')
def users_followers(user_id):
    """Show list of followers of this user."""
    # Added line 211-212, 220, and 225-227.
    try:
        if session.get(CURR_USER_KEY) == g.user.id:
            if not g.user:
                flash("Access unauthorized.", "danger")
                return redirect("/")

            user = User.query.get_or_404(user_id)

            # line 198 is for xml images not appearing in headers
            status_code = xml_check_for_header_img(user)

            return render_template('users/followers.html', user=user,
            status_code=status_code
            )
    except AttributeError:
        flash("Access unauthorized.", "danger")
        return redirect('/')


@app.route('/users/follow/<int:follow_id>', methods=['GET', 'POST'])
def add_follow(follow_id):
    """Add a follow for the currently-logged-in user."""
    # Added line 234-235, and 245-247.
    try:
        if session.get(CURR_USER_KEY) == g.user.id:
            if not g.user:
                flash("Access unauthorized.", "danger")
                return redirect("/")

            followed_user = User.query.get_or_404(follow_id)
            g.user.following.append(followed_user)
            db.session.commit()

            return redirect(f"/users/{g.user.id}/following")
    except AttributeError:
        flash("Access unauthorized.", "danger")
        return redirect('/')


@app.route('/users/stop-following/<int:follow_id>', methods=['GET', 'POST'])
def stop_following(follow_id):
    """Have currently-logged-in-user stop following this user."""
    # Added line 254-255, and 265-267.
    try:
        if session.get(CURR_USER_KEY) == g.user.id:
            if not g.user:
                flash("Access unauthorized.", "danger")
                return redirect("/")

            followed_user = User.query.get(follow_id)
            g.user.following.remove(followed_user)
            db.session.commit()

            return redirect(f"/users/{g.user.id}/following")
    except AttributeError:
        flash("Access unauthorized.", "danger")
        return redirect('/')


@app.route('/users/profile', methods=["GET", "POST"])
def profile():
    """Update profile for current user."""
    # Added all logic here
    try:
        if session.get(CURR_USER_KEY) == g.user.id:
            form = UserEditForm()
            session_id = session.get('curr_user', False)
            user = User.query.filter_by(id = session_id).first()

            if not session_id:
                return redirect(f"/users/{user.id}")

            if form.validate_on_submit():
                edit_form_auth = User.authenticate(g.user.username,
                form.password.data
                )

                if edit_form_auth:
                    form_data = form.data
                    form_data.pop("password")
                    form_data.pop("csrf_token")
                    update_user(form_data, user)
                    flash(f"Successfully edited user!", "success")
                    return redirect(f"/users/{user.id}")
                else:
                    flash("Access unauthorized.", "danger")
                    return render_template('/users/edit.html', form=form)

    
            return render_template('/users/edit.html', form=form)
    except AttributeError:
        flash("Access unauthorized.", "danger")
        return redirect('/')


@app.route('/users/delete', methods=["GET", "POST"])
def delete_user():
    """Delete user."""
    # Added line 312-313, and 324-326.
    try:
        if session.get(CURR_USER_KEY) == g.user.id:
            if not g.user:
                flash("Access unauthorized.", "danger")
                return redirect("/")

            do_logout()

            db.session.delete(g.user)
            db.session.commit()

            return redirect("/signup")
    except AttributeError:
        flash("Access unauthorized.", "danger")
        return redirect('/')


##############################################################################
# Messages routes:

@app.route('/messages/new', methods=["GET", "POST"])
def messages_add():
    """Add a message:

    Show form if GET. If valid, update message and redirect to user page.
    """
    # Added line 339-340, and 355-357.
    try:
        if session.get(CURR_USER_KEY) == g.user.id:
            if not g.user:
                flash("Access unauthorized.", "danger")
                return redirect("/")

            form = MessageForm()

            if form.validate_on_submit():
                msg = Message(text=form.text.data)
                g.user.messages.append(msg)
                db.session.commit()

                return redirect(f"/users/{g.user.id}")

            return render_template('messages/new.html', form=form)
    except AttributeError:
        flash("Access unauthorized.", "danger")
        return redirect('/')


@app.route('/messages/<int:message_id>', methods=["GET"])
def messages_show(message_id):
    """Show a message."""
    # Added line 364-365, and 368-370.
    try:
        if session.get(CURR_USER_KEY) == g.user.id:
            msg = Message.query.get(message_id)
            return render_template('messages/show.html', message=msg)
    except AttributeError:
        flash("Access unauthorized.", "danger")
        return redirect('/')


@app.route('/messages/<int:message_id>/delete', methods=["GET", "POST"])
def messages_destroy(message_id):
    """Delete a message."""
    # Added line 377-378, and 388-390.
    try:
        if session.get(CURR_USER_KEY) == g.user.id:
            if not g.user:
                flash("Access unauthorized.", "danger")
                return redirect("/")

            msg = Message.query.get(message_id)
            db.session.delete(msg)
            db.session.commit()

            return redirect(f"/users/{g.user.id}")
    except AttributeError:
        flash("Access unauthorized.", "danger")
        return redirect('/')

##############################################################################
# Like routes

@app.route('/users/add_like/<int:message_id>', methods=['GET', 'POST'])
def add_like(message_id):
    """Add a like for a message."""
    # Created all logic.
    # try:
    if session.get(CURR_USER_KEY) == g.user.id:
        if not g.user:
            flash("Access unauthorized.", "danger")
            return redirect("/")

        liked_message = Message.query.get_or_404(message_id)
        message_user_id = liked_message.user_id
        curr_user_id = session['curr_user']

        like = Likes.query.filter(
        Likes.user_id == curr_user_id, Likes.message_id == message_id
        ).first()

        like_exists = True if like else False
        add_to_like(curr_user_id, message_id, like_exists, message_user_id)
        return redirect(f"/users/{message_user_id}")
    # except AttributeError:
    #     flash("Access unauthorized.", "danger")
    #     return redirect('/')


@app.route('/users/<int:user_id>/likes', methods=['GET'])
def likes_page(user_id):
    """Show likes for a user."""
    # Created all logic.
    try:
        if session.get(CURR_USER_KEY) == g.user.id:
            user = User.query.get_or_404(user_id)
            liked_messages = user.likes
            # line 369 is for xml images not appearing in headers
            status_code = xml_check_for_header_img(user)

            return render_template('users/likes.html', user=user,
            liked_messages=liked_messages, status_code=status_code
            )
    except AttributeError:
        flash("Access unauthorized.", "danger")
        return redirect('/')


##############################################################################
# Homepage and error pages


@app.route('/')
def homepage():
    """Show homepage:

    - anon users: no messages
    - logged in: 100 most recent messages of followed_users
    """
    # Added line 462
    # g is a flask object that has data of the logged in user.
    # g.user returns a User object of the current user
    if g.user:
        # Line 391 is for xml images not appearing in headers.
        status_code = xml_check_for_header_img(g.user)

        messages = (Message
                    .query
                    .order_by(Message.timestamp.desc())
                    .limit(100)
                    .all())

        return render_template('home.html', messages=messages,
        status_code=status_code
        )

    else:
        return render_template('home-anon.html')


##############################################################################
# Turn off all caching in Flask
#   (useful for dev; in production, this kind of stuff is typically
#   handled elsewhere)
#
# https://stackoverflow.com/questions/34066804/disabling-caching-in-flask

@app.after_request
def add_header(req):
    """Add non-caching headers on every request."""

    req.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    req.headers["Pragma"] = "no-cache"
    req.headers["Expires"] = "0"
    req.headers['Cache-Control'] = 'public, max-age=0'
    return req
