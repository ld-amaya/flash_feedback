from flask import Flask, request, render_template, jsonify, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User
from forms import RegistrationForm, LoginForm

app = Flask(__name__)

app.config['SECRET_KEY'] = 'iamlou'
app.config['DEBUG_TB_INTERCEPTS_REDIRECT'] = True

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///flash_feedback'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False

toolbar = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


@app.route("/")
def homepage():
    """Redirects user to registration page"""
    return redirect("/register")


@app.route("/users/<username>")
def user_profile(username):
    """Handles user redirection when user if logged in"""

    if "username" in session:
        return render_template("secret.html")
    return redirect("/login")


@app.route("/register", methods=['GET', 'POST'])
def registration():
    """Handles user registration"""

    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        user = User.register(username, password, email,
                             first_name, last_name, form)
        if user:
            session['username'] = user.username
            return redirect(f"/users/{user.username}")
        return render_template("registration.html", form=form)
    return render_template("registration.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def user_login():
    """Handles user login"""

    if "username" in session:
        return redirect(f"/users/{session['username']}")

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.login(username, password)

        if user:
            session['username'] = user.username
            return redirect(f"/users/{user.username}")
        flash(f"Incorrect credentials, please try again!")
        return redirect("/login")
    return render_template("login.html", form=form)


@app.route("/logout")
def user_logout():
    """Handles user logout"""
    session.pop("username")
    return redirect("/login")
