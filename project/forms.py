from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length
from flask_wtf import FlaskForm
from . import db


class EditProfileForm(FlaskForm):
    name = TextAreaField('name', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])
    submit = SubmitField('Submit')