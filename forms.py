from flask_wtf import FlaskForm
from wtforms_alchemy import model_form_factory
from models import db, User

BaseModelForm = model_form_factory(FlaskForm)


class ModelForm(BaseModelForm):
    @classmethod
    def get_session(self):
        return db.get_session


class UserForm(ModelForm):
    class Meta:
        model = User
