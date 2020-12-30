from flask import Flask, request, render_template, jsonify, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Feedback
from forms import RegistrationForm, LoginForm, FeedbackForm
from users import Verification

app = Flask(__name__)

app.config['SECRET_KEY'] = 'iamlou'
app.config['DEBUG_TB_INTERCEPTS_REDIRECT'] = True

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///flash_feedback'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False

toolbar = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

####### User Get Reqeusts ######################################


@app.route("/")
def homepage():
    """Redirects user to registration page"""
    return redirect("/register")


####### User Page ######################################


@app.route("/users/<username>")
def user_profile(username):
    """Handles display of user details and feedbacks when user if logged in"""
    user = User.query.filter_by(
        username=username).first()
    if "username" in session and session['username'] == username:
        return render_template("show.html", user=user)
    return redirect("/login")


####### User Registration ######################################


@app.route("/register", methods=['GET', 'POST'])
def registration():
    """Handles user registration"""

    if 'username' in session:
        return redirect(f"/users/{session['username']}")

    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        # Check if username exists
        user_verification = Verification(username, email)

        if user_verification.existing_user():
            form.username.errors.append("Username exists, try again or login!")
            return render_template("registration.html", form=form)
        if user_verification.existing_email():
            form.email.errors.append("Email exists, try again!")
            return render_template("registration.html", form=form)

        # Register User to database
        user = User.register(username, password, email,
                             first_name, last_name, form)
        session['username'] = user.username
        return redirect(f"/users/{user.username}")
    return render_template("registration.html", form=form)


####### User Login ######################################


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


####### Add Feedback ######################################

@app.route("/users/<username>/feedback/add", methods=["GET", "POST"])
def user_feedback(username):
    """Handles adding of feedback by the user"""

    if "username" not in session:
        return redirect("/login")

    form = FeedbackForm()
    if form.validate_on_submit():
        feedback = Feedback(
            title=form.title.data,
            content=form.content.data,
            username=username
        )
        db.session.add(feedback)
        db.session.commit()
        flash(f"Successfully added feedback", "success")
        return redirect(f"/users/{username}")
    return render_template("/feedback/feedback.html", form=form, username=username)

####### Feedback Update ######################################


@app.route("/feedback/<int:id>/update", methods=["GET", "POST"])
def feedback_update(id):
    """Handles feedback updates by the user"""

    # Check if user is in session
    if "username" not in session:
        return redirect("/login")

    feedback = Feedback.query.get_or_404(id)

    if feedback.user.username == session['username']:
        form = FeedbackForm(obj=feedback)
        if form.validate_on_submit():
            feedback.title = form.title.data
            feedback.content = form.content.data
            db.session.add(feedback)
            db.session.commit()
            flash(f"Successfully updated feedback", "success")
            return redirect(f"/users/{session['username']}")
        return render_template("/feedback/edit.html", form=form, feedback=feedback)

    return redirect("/login")

###### Feedback Delete ######################################


@app.route("/feedback/<int:id>/delete", methods=["POST"])
def delete_feedback(id):
    """Handles feedback delete by user"""

    if "username" not in session:
        return redirect("/login")

    feedback = Feedback.query.get_or_404(id)
    if feedback.user.username == session['username']:
        db.session.delete(feedback)
        db.session.commit()
        flash(f"Successfully deleted feedback", "delete")
    return redirect(f"/users/{session['username']}")


####### User logout ######################################

@app.route("/logout", methods=["POST"])
def user_logout():
    """Handles user logout"""
    session.pop("username")
    return redirect("/login")
