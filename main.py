from flask import Flask, render_template, session, make_response, redirect, request, abort
from data import db_session, __all_models, users_api
from forms.user import RegisterForm, LoginForm, JobsForm
from data.users import User
from data.employment import Employment as Jobs
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_session.global_init("db/blogs.db")
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route("/")
def server():
    a = {}
    db_session.global_init("db/blogs.db")
    db_sess = db_session.create_session()
    works = db_sess.query(Jobs).all()
    for i in db_sess.query(User).all():
        a[i.id] = i.name
        a[str(i.id)] = i.name
    for item in works:
        item.user = a[item.team_leader]
        db_sess.add(item)
        db_sess.commit()
    return render_template("work.html", works=works)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_session.global_init("db/blogs.db")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        db_session.global_init("db/blogs.db")
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/addjob', methods=['GET', 'POST'])
@login_required
def addjob():
    form = JobsForm()
    if form.validate_on_submit():
        db_session.global_init("db/blogs.db")
        db_sess = db_session.create_session()
        jobs = Jobs(
            team_leader=db_sess.query(User).filter(User.name == current_user.name).first().id,
            email=form.email.data,
            job=form.job.data,
            experience=form.experience.data,
            work_size=form.work_size.data,
            start_time=form.start_time.data,
            end_time=form.end_time.data,
        )
        db_sess.add(jobs)
        db_sess.commit()
        return redirect('/')
    return render_template('jobs.html', title='Добавить работу', form=form)


@app.route('/addjob/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_job(id):
    form = JobsForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        try:
            if id == 1:
                jobs = db_sess.query(Jobs).filter(Jobs.id == id).first()
            else:
                if db_sess.query(User).filter(User.id ==
                                              db_sess.query(Jobs).filter(Jobs.id == id)
                                              .first().team_leader).first().name == current_user.name:
                    jobs = db_sess.query(Jobs).filter(Jobs.id == id).first()
                else:
                    jobs = False
            if jobs:
                form.job.data = jobs.job
                form.work_size.data = jobs.work_size
                form.experience.data = jobs.experience
                form.email.data = jobs.email
                form.start_time.data = jobs.start_time
                form.end_time.data = jobs.end_time
            else:
                abort(404)
        except:
            return redirect('/')

    if form.validate_on_submit():
        db_sess = db_session.create_session()
        jobs = db_sess.query(Jobs).filter(Jobs.id == id).first()
        if jobs:
            jobs.job = form.job.data
            jobs.work_size = form.work_size.data
            jobs.experience = form.experience.data
            jobs.email = form.email.data
            jobs.start_time = form.start_time.data
            jobs.end_time = form.end_time.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('jobs.html',
                           title='Редактирование работы',
                           form=form
                           )


@app.route('/job_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def job_delete(id):
    db_sess = db_session.create_session()
    try:
        if id == 1:
            jobs = db_sess.query(Jobs).filter(Jobs.id == id).first()
        else:
            if db_sess.query(User).filter(User.id ==
                                          db_sess.query(Jobs).filter(Jobs.id == id).
                                          first().team_leader).first().name == current_user.name:
                jobs = db_sess.query(Jobs).filter(Jobs.id == id).first()
            else:
                jobs = False
        if jobs:
            db_sess.delete(jobs)
            db_sess.commit()
        else:
            abort(404)
        return redirect('/')
    except:
        abort(404)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


if __name__ == '__main__':
    db_session.global_init("db/blogs.db")
    app.register_blueprint(users_api.blueprint)
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

