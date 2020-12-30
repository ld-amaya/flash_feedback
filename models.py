from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy.exc import IntegrityError

db = SQLAlchemy()
bcrypt = Bcrypt()


class User(db.Model):
    """Creates the user model"""

    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    username = db.Column(db.String(20),
                         nullable=False,
                         unique=True)

    password = db.Column(db.Text,
                         nullable=False)
    email = db.Column(db.String(50),
                      nullable=False,
                      unique=True)
    first_name = db.Column(db.String(30),
                           nullable=False)
    last_name = db.Column(db.String(30),
                          nullable=False)

    feedback = db.relationship("Feedback", backref="user",
                               cascade="all, delete-orphan")

    @classmethod
    def register(cls, username, password, email, first_name, last_name, form):
        """Register user with hashed password and return class user"""

        hashed = bcrypt.generate_password_hash(password)

        # turn byte string to normal (unicode utf8) string
        hashed_utf8 = hashed.decode("utf8")

        user = cls(
            username=username,
            password=hashed_utf8,
            email=email,
            first_name=first_name,
            last_name=last_name
        )
        db.session.add(user)
        db.session.commit()
        return user

    @classmethod
    def login(cls, username, password):
        """Handles User Login"""

        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            return user
        return False


class Feedback(db.Model):
    """Create feedback model"""

    __tablename__ = "feedbacks"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    title = db.Column(db.String(100),
                      nullable=False)
    content = db.Column(db.Text,
                        nullable=False)
    username = db.Column(db.String(20),
                         db.ForeignKey('users.username'),
                         nullable=False)


def connect_db(app):
    """Connect to the database"""
    db.app = app
    db.init_app(app)
