from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required

from . import app, db
from .models import User, Course, Student, UserMixin
from .forms import UserLoginForm, UserRegisterForm, Course, CourseForm, CourseUpdateForm, StudentForm, StudentUpdateForm


def index():
    students = Student.query.all()
    return render_template('index.html', students=students)


def student_view():
    students = Student.query.all()
    return render_template('student_view.html', students=students)


def course_view():
    courses = Course.query.all()
    return render_template('course_view.html', courses=courses)


@login_required
def course_add():
    form = CourseForm(meta={'csrf': False})
    if request.method == 'POST':
        if form.validate_on_submit():
            new_courses = Course(
                language=form.language.data,
                date_start=form.date_start.data,
                date_end=form.date_end.data
            )
            db.session.add(new_courses)
            db.session.commit()
            flash('Курс успешно добавлен', 'Успешно!')
            return redirect(url_for('index'))
        else:
            print(form.errors)
            text_list = []
            for field, errors in form.errors.items():
                text_list.append(f'{field} : {", ".join(errors)}')
            flash(f'При добавлении курса произошла ошибка{". ".join(text_list)}', 'Ошибка!')
    return render_template('course_add.html', form=form)


@login_required
def admin_course_update(course_id):
    courses = Course.query.get(course_id)
    form = CourseUpdateForm(meta={'csrf': False}, obj=courses)
    if request.method == 'POST':
        if form.validate_on_submit():
            form.populate_obj(courses)
            db.session.add(courses)
            db.session.commit()
            flash('Курс успешно обновлен', 'Успешно!')
            return redirect(url_for('index'))
        else:
            print(form.errors)
            text_list = []
            for field, errors in form.errors.items():
                text_list.append(f'{field} : {", ".join(errors)}')
            flash(f'При обновлении Курса произошла ошибка{". ".join(text_list)}', 'Ошибка!')
    return render_template('course_add.html', form=form)


@login_required
def admin_course_delete(courses_id):
    courses = Course.query.get(courses_id)
    if request.method == 'POST':
        db.session.delete(courses)
        db.session.commit()
        flash('Курс успешно удален', 'Успешно!')
        return redirect(url_for('index'))
    return render_template('course_delete.html', courses=courses)


@login_required
def student_add():
    form = StudentForm(meta={'csrf': False})
    if request.method == 'POST':
        if form.validate_on_submit():
            new_students = Student(
                name=form.name.data,
                course_id=form.course_id.data
            )
            db.session.add(new_students)
            db.session.commit()
            flash('Студент успешно добавлен', 'Успешно!')
            return redirect(url_for('index'))
        else:
            print(form.errors)
            text_list = []
            for field, errors in form.errors.items():
                text_list.append(f'{field} : {", ".join(errors)}')
            flash(f'При добавлении студента произошла ошибка{". ".join(text_list)}', 'Ошибка!')
    return render_template('student_add.html', form=form)


@login_required
def admin_student_update(student_id):
    students = Student.query.get(student_id)
    form = StudentUpdateForm(meta={'csrf': False}, obj=students)
    if request.method == 'POST':
        if form.validate_on_submit():
            form.populate_obj(students)
            db.session.add(students)
            db.session.commit()
            flash('Студент успешно обновлен', 'Успешно!')
            return redirect(url_for('index'))
        else:
            print(form.errors)
            text_list = []
            for field, errors in form.errors.items():
                text_list.append(f'{field} : {", ".join(errors)}')
            flash(f'При обновлении Студента произошла ошибка{". ".join(text_list)}', 'Ошибка!')
    return render_template('student_add.html', form=form)


@login_required
def admin_student_delete(student_id):
    students = Student.query.get(student_id)
    if request.method == 'POST':
        db.session.delete(students)
        db.session.commit()
        flash('Студент успешно удален', 'Успешно!')
        return redirect(url_for('index'))
    return render_template('student_delete.html', students=students)


def user_register():
    form = UserRegisterForm()
    title = 'Регистрация'
    if request.method == 'POST':
        if form.validate_on_submit():
            new_user = User()
            form.populate_obj(new_user)
            db.session.add(new_user)
            db.session.commit()
            flash(f'Пользователь {new_user.username} успешно зарегистрирован!', 'success!')
            return redirect(url_for('user_login'))
        else:
            text_list = []
            for field, errors in form.errors.items():
                text_list.append(f'{field} : {", ".join(errors)}')
            flash(f'При регистрации произошла ошибка{". ".join(text_list)}', 'Ошибка!')

    return render_template('accounts/form.html', form=form, title=title)


def user_login():
    form = UserLoginForm()
    title = 'Авторизация'
    if request.method == 'POST':
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            user = User.query.filter_by(username=username).first()
            if user and user.check_password(password):
                login_user(user)
                flash('Вы успешно вошли в систему, Успех!')
                return redirect(url_for('index'))
            else:
                flash('Неверные логин и пароль', 'Ошибка!')
    return render_template('accounts/form.html', form=form, title=title)


def user_logout():
    logout_user()
    return redirect(url_for('user_login'))
