from flask import Flask, render_template, \
    request, make_response, redirect, url_for, session

from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user

app = Flask(__name__)
app.secret_key = 'marcos'  

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

users = {
    "admin": {"usuario": "admin", "senha": "123"}
}

class User(UserMixin):
    def __init__(self, id):
        self.id = id

@login_manager.user_loader
def load_user(user_id):
    if user_id in users:
        return User(user_id)
    return None

@app.route('/cadastro_usuario', methods=['GET', 'POST'])
def cadastro_usuario():
    if request.method == 'POST':
        usuario = request.form['usuario']
        senha = request.form['senha']

        if usuario in users:
            erro = 'Usuário já existe.'
            return render_template('cadastro_usuario.html', erro=erro)
        users[usuario] = {'usuario': usuario, 'senha': senha}
        login_user(User(usuario))
        return redirect(url_for('index'))

    return render_template('cadastro_usuario.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        senha = request.form['senha']
        user = users.get(usuario)
        if user and user['senha'] == senha:
            login_user(User(usuario))
            return redirect(url_for('index'))
        return render_template('login.html', erro='Usuário ou senha inválidos')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/cadastro', methods=['GET', 'POST'])
@login_required
def register():
    if request.method == 'GET':
        return render_template('cadastro.html')
    #<input type="text" name="nome" placeholder="Nome"> 
    nome = request.form['nome']
    genero = request.form['genero']

    filmes = session.get('preferencias', [])
    filmes.append(nome)
    session['preferencias'] = filmes

    # make_response(
    #     render_template('preferencias.html')
    # )
    response = make_response(
        redirect( url_for('preferencias') )
    )

    response.set_cookie('nome', nome,
        7*24*60*60
    )
    session['nome'] = nome
    return response


@app.route('/preferencias')
@login_required
def preferencias():
    return render_template('preferencias.html', filmes=session.get('preferencias', []))

@app.route('/preferencias/remover/<filme>')
@login_required
def remover_preferencia(filme):
    filmes = session.get('preferencias', [])
    if filme in filmes:
        filmes.remove(filme)
        session['preferencias'] = filmes
    return redirect(url_for('preferencias'))

if __name__ == '__main__':
    app.run(debug=True)