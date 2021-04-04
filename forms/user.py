from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, BooleanField
from wtforms.fields.html5 import EmailField, IntegerField, DateField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    name = StringField('Имя пользователя', validators=[DataRequired()])
    about = TextAreaField("Немного о себе")
    submit = SubmitField('Войти')


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class JobsForm(FlaskForm):
    job = TextAreaField('Описание работы', validators=[DataRequired()])
    work_size = IntegerField("Время работы", validators=[DataRequired()])
    age = IntegerField("Возраст", validators=[DataRequired()])
    email = EmailField('Почта', validators=[DataRequired()])
    collaborators = TextAreaField("Id участников", validators=[DataRequired()])
    start_date = DateField("Дата начала")
    end_date = DateField("Дата окончания")
    is_finished = BooleanField("Эта работа окончена?")
    submit = SubmitField('Разместить')
