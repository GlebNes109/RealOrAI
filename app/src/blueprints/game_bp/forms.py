from flask_wtf import FlaskForm
from wtforms.fields.simple import HiddenField


class AnswerForm(FlaskForm):
    csrf_token = HiddenField()
