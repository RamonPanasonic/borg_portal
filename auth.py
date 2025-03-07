from flask import Blueprint, render_template, redirect, url_for, request, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from models.users import Users

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    if current_user.is_authenticated:
        if  current_user.role == 3:
            return redirect(url_for('supervisors.index'))
        return redirect(url_for('main.dashboard'))
    return render_template('/login/login.html')

@auth.route('/loginp', methods=['POST'])
def login_post():
    from db import db  # ⬅️ Importar dentro de la función para evitar el ciclo

    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    remember = True if data.get('remember') else False
    user = Users.query.filter_by(username=username).first()

    if not user or not check_password_hash(user.password, password):
        return make_response('Usuario o contraseña incorrectos.', 301)

    login_user(user, remember=remember)
    return make_response('Inicio exitoso.', 201)

@auth.route('/signup', methods=['POST'])
def signup_post():
    from db import db  # ⬅️ Importación dentro de la función

    username = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    user = Users.query.filter_by(username=username).first()

    if user:
        return redirect(url_for('auth.signup'))

    new_user = Users(username=username, name=name, password=generate_password_hash(password, method='sha256'))
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('auth.login'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))