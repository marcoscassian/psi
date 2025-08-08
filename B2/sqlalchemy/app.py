from flask import Flask, render_template
from flask import request, session, redirect, url_for
from flask import flash
from db import db
from models import Usuario

from flask_login import LoginManager, UserMixin, logout_user
from flask_login import login_required, login_user, current_user

from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

import sqlite3

login_manager = LoginManager()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db' #define a url do banco de dados sqlite
db.init_app(app) #Inicializa o db

with app.app_context():
    db.create_all()
login_manager.__init__(app)

app.secret_key = 'chave_secreta'

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        nome = request.form['name']
        senha = request.form['password']

        usuario = Usuario.query.filter_by(nome=nome).first()

        if usuario and usuario.senha == senha:
            login_user(usuario)
            return redirect(url_for('dash'))
        else:
            flash('Dados incorretos', category='error')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        nome = request.form['name']
        senha= request.form['password']

        novo_usuario = Usuario(nome=nome, senha=senha)
        db.session.add(novo_usuario)
        db.session.commit()
        return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dash():
    return render_template('dash.html')

@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))