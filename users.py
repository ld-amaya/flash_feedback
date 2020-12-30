from models import db, connect_db, User


class Verification():
    def __init__(self, username, email):
        self.username = username
        self.email = email

    def existing_user(self):
        """Check if user is existing"""

        user = User.query.filter_by(username=self.username).first()
        if user:
            return user
        return False

    def existing_email(self):
        """Check if email is existing"""

        user = User.query.filter_by(email=self.email).first()
        if user:
            return user
        return False
