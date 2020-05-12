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
    return render_template("main.html", title="Welcome!")


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    return render_template("register.html", form=form)


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


if __name__ == '__main__':
    app.run()