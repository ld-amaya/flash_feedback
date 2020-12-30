from flask_wtf import FlaskForm
from wtforms import StringField, TextField, PasswordField, TextAreaField
from wtforms.validators import InputRequired, Length, Email
from models import db, User


class RegistrationForm(FlaskForm):
    """Defines form to be used for registration"""
    username = StringField(
        "Username",
        validators=[InputRequired(), Length(min=1, max=20)])

    password = PasswordField(
        "Password",
        validators=[InputRequired(), Length(min=6, max=55)])
    email = StringField(
        "Email",
        validators=[InputRequired(), Email(), Length(max=50)])
    first_name = StringField(
        "First Name",
        validators=[InputRequired(), Length(min=1, max=30)])
    last_name = StringField(
        "Last Name",
        validators=[InputRequired(), Length(min=1, max=30)])


class LoginForm(FlaskForm):
    """Defines form to be used for login"""
    username = StringField(
        "Username",
        validators=[InputRequired(), Length(min=1, max=20)])

    password = PasswordField(
        "Password",
        validators=[InputRequired(), Length(min=6, max=55)])


class FeedbackForm(FlaskForm):
    """Defines feedback form"""
    title = StringField(
        "Title",
        validators=[InputRequired(), Length(min=1, max=100)])

    content = TextAreaField(
        "Content",
        validators=[InputRequired()])
