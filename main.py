from flask import Flask, render_template, redirect
from flask_ngrok import run_with_ngrok
from flask_login import LoginManager, login_required, login_user, current_user, logout_user
from flask_wtf import FlaskForm
from wtforms import PasswordField, BooleanField, SubmitField, StringField, IntegerField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired
from data import db_session
from data.user import User


app = Flask(__name__)
app.config['SECRET_KEY'] = 'asd130298sF130298sFew19998donohwthvyacheslav'
run_with_ngrok(app)
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


@app.route('/moder_tools')
def moderator_page():
    if not current_user.is_authenticated and not current_user.moderator:
        return redirect('/')
    return render_template('moder_tools.html', title='Модерация')


@app.route('/moder_tools/add_item', methods=['GET', 'POST'])
def moderator_page_item():
    if not current_user.is_authenticated and not current_user.moderator:
        return redirect('/')
    form = AddItemForm()
    return render_template('moder_item.html', title='Модерация', form=form)


@app.route('/moder_tools/add_method', methods=['GET', 'POST'])
def moderator_page_method():
    if not current_user.is_authenticated and not current_user.moderator:
        return redirect('/')
    form = AddMethodForm()
    return render_template('moder_method.html', title='Модерация', form=form)


@app.route('/redact_arsenal', methods=['GET', 'POST'])
def load_redactor():
    if not current_user.is_authenticated:
        return redirect('/')
    return render_template('redact_arsenal.html', title='Редактор')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


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


@app.route("/")
def index():
    owned = None
    if current_user.is_authenticated:
        session = db_session.create_session()
        owned = [int(i) for i in
                 session.query(User).filter(User.id == current_user.id).first().owned.split()]
    return render_template("main.html", title="Welcome!", owned=owned)


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password2.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        session = db_session.create_session()
        if session.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User()
        user.rank = form.rank.data
        user.name = form.name.data
        user.email = form.email.data
        user.nick = form.nick.data
        user.set_password(form.password.data)
        user.owned = ''
        session.add(user)
        session.commit()
        return redirect('/login')
    return render_template("register.html", form=form, title='Регистрация')


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class RegisterForm(FlaskForm):
    nick = StringField('Имя профиля', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password2 = PasswordField('Пароль', validators=[DataRequired()])
    name = StringField('Как вас называть?', validators=[DataRequired()])
    rank = IntegerField('Ваш ранг мастерства на данный момент', validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')


class AddItemForm(FlaskForm):
    wtype = StringField('Тип элемента', validators=[DataRequired()])
    name = StringField('Название элемента', validators=[DataRequired()])
    obtaining = StringField('Способ получения(id)', validators=[DataRequired()])
    submit = SubmitField('Зарегистрировать элемент арсенала')


class AddMethodForm(FlaskForm):
    mtype = StringField('Тип элемента', validators=[DataRequired()])
    name = StringField('Название элемента', validators=[DataRequired()])
    submit = SubmitField('Зарегистрировать способ получения')


if __name__ == '__main__':
    db_session.global_init("db/profiles.sqlite")
    app.run()
