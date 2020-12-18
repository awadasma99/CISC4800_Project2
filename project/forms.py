from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length
from wtforms.widgets import html_params, HTMLString
from flask_wtf import FlaskForm
from . import db


class EditProfileForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
    old_password = StringField('old password', validators=[DataRequired()])
    new_password = StringField('new password', validators=[DataRequired()])
    submit = SubmitField('Submit')

class ButtonWidget(object):
    """
    Renders a multi-line text area.
    `rows` and `cols` ought to be passed as keyword args when rendering.
    """
    input_type = 'submit'

    html_params = staticmethod(html_params)

    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', field.id)
        kwargs.setdefault('type', self.input_type)
        if 'value' not in kwargs:
            kwargs['value'] = field._value()

        return HTMLString('<button {params}>{label}</button>'.format(
            params=self.html_params(name=field.name, **kwargs),
            label=field.label.text)
        )

class ButtonField(StringField):
    widget = ButtonWidget()

class SaveRecipe(FlaskForm):
    save = ButtonField('Save Recipe')
