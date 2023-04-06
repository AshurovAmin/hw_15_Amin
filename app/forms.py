from flask_wtf import FlaskForm
import wtforms as wf
from . import app

from .models import Course, User, UserMixin



def validate_date_out(form, field):
    date_start = form.date_start.data
    date_end = field.data
    if date_end < date_start:
        raise wf.ValidationError("Дата окончания курса не может быть раньше даты начала курса")


class CourseForm(FlaskForm):
    language = wf.StringField(label='Язык программирования', validators=[
        wf.validators.DataRequired(),
    ])
    date_start = wf.DateField(label='Дата старта курса', validators=[
        validate_date_out
    ])
    date_end = wf.DateField(label='Дата окончания курса', validators=[
        validate_date_out
    ])


class CourseUpdateForm(FlaskForm):
    language = wf.StringField(label='Язык программирования', validators=[
        wf.validators.DataRequired(),
    ])
    date_start = wf.DateField(label='Дата старта курса')
    date_end = wf.DateField(label='Дата окончания курса')


def course_choices():
    course_choices = []
    with app.app_context():
        courses = Course.query.all()
        for course in courses:
            course_choices.append((course.id, course.language))
    return course_choices


class StudentForm(FlaskForm):
    name = wf.StringField(label='ФИО Студента')
    course_id = wf.SelectField(label="Курс", choices=course_choices)


class StudentUpdateForm(FlaskForm):
    name = wf.StringField(label='ФИО Студента')
    course_id = wf.SelectField(label="Курс", choices=course_choices)


class UserLoginForm(FlaskForm):
    username = wf.StringField(label='Логин', validators=[
        wf.validators.DataRequired(),
        wf.validators.Length(min=3, max=20)
    ])
    password = wf.PasswordField(label='Пароль', validators=[
        wf.validators.DataRequired(),
    ])

    def validate_password(self, field):
        if len(field.data) < 8:
            raise wf.ValidationError('Длина пароля должна быть минимум 8 символов')


class UserRegisterForm(UserLoginForm):
    password_2 = wf.PasswordField(label='Пароль', validators=[
        wf.validators.DataRequired(),
    ])

    def validate(self, *args, **kwargs):
        if not super().validate(*args, **kwargs):
            return False
        if self.password.data != self.password_2.data:
            self.password_2.errors.append('Пароли должны совпадать')
            return False
        return True

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).count() > 0:
            raise wf.ValidationError('Пользователь с таким username уже существует')
