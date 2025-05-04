from flask_wtf import FlaskForm
from wtforms.fields.simple import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, EqualTo


class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[InputRequired(), Length(min=3, max=20)])
    password = PasswordField('Пароль', validators=[InputRequired(), Length(min=6, max=30)])
    submit = SubmitField('Войти')

class RegisterForm(FlaskForm):
    username = StringField('Придумайте логин', validators=[
        InputRequired(), Length(min=3, max=30)
    ])
    password = PasswordField('Пароль', validators=[
        InputRequired(), Length(min=6)
    ])
    confirm_password = PasswordField('Повторите пароль', validators=[
        InputRequired(), EqualTo('password', message='Пароли должны совпадать')
    ])
    submit = SubmitField('Зарегистрироваться')