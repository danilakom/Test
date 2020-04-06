from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from flask import Flask, render_template, redirect, abort, request
from data import db_session
from data.users import User
from data.jobs import Jobs
from data.departments import Departament
from login import LoginForm
from add_job import Add_Job
from register import RegisterForm
from add_departament import Add_Departament
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return session.query(User).get(user_id)

@app.route('/')
def index():
    jobs = session.query(Jobs)
    t_l = {}
    for job in jobs:
        user = session.query(User).filter(User.id == job.team_leader).first()
        if user:
            t_l[job.id] = ' '.join([user.name, user.surname])
        else:
            t_l[job.id] = ''
    return render_template('index.html', jobs=jobs, t_l=t_l)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/add_job', methods=['GET', 'POST'])
@login_required
def add_job():
    form = Add_Job()
    if form.validate_on_submit():
        session = db_session.create_session()
        job = Jobs()
        a = [user.id for user in session.query(User)]
        if form.team_leader.data not in a:
            return render_template('add_job.html',
                               message="Такого пользователя не сущестсвует",
                               form=form)
        job.team_leader = form.team_leader.data
        job.job = form.job.data
        job.work_size = form.work_size.data
        job.collaborators = form.collaborators.data
        if form.start_date.data:
            job.start_date = datetime.strptime(form.start_date.data, '%d.%m.%Y').date()
        if form.end_date.data:
            job.end_date = datetime.strptime(form.end_date.data, '%d.%m.%Y').date()
        job.is_finished = form.is_finished.data
        session.add(job)
        session.commit()
        return redirect('/')
    return render_template('add_job.html', title='Добавление работы', form=form)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.r_password.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        if session.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            surname=form.surname.data,
            name=form.name.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data,
            email=form.email.data)
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route("/job_delete/<int:id>")
@login_required
def job_delete(id):
    session = db_session.create_session()
    job = session.query(Jobs).filter(Jobs.id == id, (Jobs.team_leader == current_user.id) | (current_user.id == 1)).first()
    if job:
        session.delete(job)
        session.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/edit_job/<int:id>', methods=["POST", "GET"])
@login_required
def edit_job(id):
    form = Add_Job()
    if request.method == 'GET':
        session = db_session.create_session()
        job = session.query(Jobs).filter(Jobs.id == id, (Jobs.team_leader == current_user.id) | (current_user.id == 1)).first()
        if job:
            form.team_leader.data = job.team_leader
            form.job.data = job.job
            form.work_size.data = job.work_size
            form.collaborators.data = job.collaborators
            form.start_date.data = job.start_date
            form.end_date.data = job.end_date
            form.is_finished.data = job.is_finished
        else:
            abort(404)
    if form.validate_on_submit():
        session = db_session.create_session()
        job = session.query(Jobs).filter(Jobs.id == id, (Jobs.team_leader == current_user.id) | (current_user.id == 1)).first()
        if job:
            job.team_leader = form.team_leader.data
            job.job = form.job.data
            job.work_size = form.work_size.data
            job.collaborators = form.collaborators.data
            if form.start_date.data:
                try:
                    job.start_date = datetime.strptime(form.start_date.data, '%d.%m.%Y  %H:%M:%S').date()
                except ValueError:
                    try:
                        job.start_date = datetime.strptime(form.start_date.data, '%Y-%m-%d  %H:%M:%S').date()
                    except ValueError:
                        return render_template('add_job.html', title='Редактирование новости', form=form, message="Неверная дата")
            if form.end_date.data:
                try:
                    job.end_date = datetime.strptime(form.end_date.data, '%d.%m.%Y %H:%M:%S')
                except ValueError:
                    try:
                        job.end_date = datetime.strptime(form.end_date.data, '%Y-%m-%d  %H:%M:%S')
                    except ValueError:
                        return render_template('add_job.html', title='Редактирование новости', form=form, message="Неверная дата")
            job.is_finished = form.is_finished.data
            session.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('add_job.html', title='Редактирование новости', form=form)


@app.route('/departaments')
def departaments():
    deps = session.query(Departament)
    chief = {}
    for dep in deps:
        user = session.query(User).filter(User.id == dep.chief).first()
        if user:
            chief[dep.id] = ' '.join([user.name, user.surname])
        else:
            chief[dep.id] = ''
    return render_template('departaments.html', departaments=deps, chief=chief)


@app.route('/add_departament', methods=['GET', 'POST'])
@login_required
def add_departament():
    form = Add_Departament()
    if form.validate_on_submit():
        session = db_session.create_session()
        dep = Departament()
        a = [user.id for user in session.query(User)]
        if form.chief.data not in a:
            return render_template('add_departament.html',
                               message="Такого пользователя не сущестсвует",
                               form=form)
        dep.chief = form.chief.data
        dep.title = form.title.data
        dep.members = form.members.data
        dep.email = form.email.data
        session.add(dep)
        session.commit()
        return redirect('/departaments')
    return render_template('add_departament.html', title='Добавление департамента', form=form)


@app.route("/departament_delete/<int:id>")
@login_required
def departament_delete(id):
    session = db_session.create_session()
    dep = session.query(Departament).filter(Departament.id == id, (Departament.chief == current_user.id) | (current_user.id == 1)).first()
    if dep:
        session.delete(dep)
        session.commit()
    else:
        abort(404)
    return redirect('/departaments')


@app.route('/edit_departament/<int:id>', methods=["POST", "GET"])
@login_required
def edit_departament(id):
    form = Add_Departament()
    if request.method == 'GET':
        session = db_session.create_session()
        dep = session.query(Departament).filter(Departament.id == id, (Departament.chief == current_user.id) | (current_user.id == 1)).first()
        if dep:
            form.title.data = dep.title
            form.chief.data = dep.chief
            form.members.data = dep.members
            form.email.data = dep.email
        else:
            abort(404)
    if form.validate_on_submit():
        session = db_session.create_session()
        dep = session.query(Departament).filter(Departament.id == id, (Departament.chief == current_user.id) | (current_user.id == 1)).first()
        if dep:
            dep.chief = form.chief.data
            dep.title = form.title.data
            dep.members = form.members.data
            dep.email = form.email.data
            session.commit()
            return redirect('/departaments')
        else:
            abort(404)
    return render_template('add_departament.html', title='Редактирование департамента', form=form)


if __name__ == "__main__":
    db_session.global_init("db/users.sqlite")
    session = db_session.create_session()
    app.run()