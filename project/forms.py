from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length
from flask_wtf import FlaskForm
from . import db


class EditProfileForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
    old_password = StringField('old password', validators=[DataRequired()])
    new_password = StringField('new password', validators=[DataRequired()])
    submit = SubmitField('Submit')


