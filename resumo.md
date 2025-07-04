# ✅ Guia Teórico Profundo – Flask + Flask-Login

## 1. Criar Ambiente

### ✔ Conceito
O ambiente virtual isola o projeto para que dependências não entrem em conflito com outros projetos Python do sistema.

### ✔ Quando usar?
**Sempre** que iniciar um novo projeto Python.

### ✔ Comandos
```bash
python -m venv venv
source venv/bin/activate      # Linux/macOS
venv\Scripts\activate.bat     # Windows


⸻

2. Instalar pacotes

📦 Pacotes principais:

Pacote	Função
Flask	Framework web principal.
Flask-Login	Gerenciar autenticação e sessões de login.

pip install flask flask-login

Para salvar dependências:

pip freeze > requirements.txt


⸻

3. Rotas e Métodos HTTP

🚏 Rotas

@app.route('/')
def index():
    return "Página principal"

📥 Métodos HTTP:

Método	Uso comum
GET	Buscar dados / mostrar form
POST	Enviar dados (formulário)
PUT	Atualizar dados (API)
DELETE	Apagar dados (API)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        ...
    return render_template('login.html')


⸻

4. request

request.form['campo']  # POST
request.args['q']      # GET (?q=valor)
request.method         # GET ou POST


⸻

5. make_response

from flask import make_response

@app.route('/set-cookie')
def set_cookie():
    resp = make_response("Cookie criado!")
    resp.set_cookie('tema', 'escuro')
    return resp


⸻

6. Cookies, Session e Secret Key

app.secret_key = 'senha-super-secreta'
session['usuario'] = 'admin'

	•	Cookies: armazenados no navegador.
	•	Session: armazenado no servidor (usa secret_key).
	•	Flask-Login usa session para guardar ID do usuário.

⸻

7. url_for

url_for('login')                  # /login
url_for('perfil', id=3)           # /perfil/3
return redirect(url_for('home')) # redirecionamento

No HTML (Jinja2):

<a href="{{ url_for('logout') }}">Sair</a>


⸻

8. Templates (extends, include, flash)

🔧 extends

{% extends 'base.html' %}
{% block conteudo %}
  <h1>Bem-vindo!</h1>
{% endblock %}

🔧 include

{% include 'navbar.html' %}

🔔 flash

flash('Senha incorreta!')

{% with msgs = get_flashed_messages() %}
  {% for msg in msgs %}
    <div class="alert">{{ msg }}</div>
  {% endfor %}
{% endwith %}


⸻

9. Flask-Login

🔹 LoginManager

from flask_login import LoginManager

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

🔹 @login_manager.user_loader

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

🔹 login_user(usuario)

from flask_login import login_user
login_user(usuario)

🔹 logout_user()

from flask_login import logout_user
logout_user()

🔹 @login_required

@app.route('/painel')
@login_required
def painel():
    return "Área protegida"


⸻

Classe User com UserMixin

from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, nome, senha):
        self.id = id
        self.nome = nome
        self.senha = senha


⸻

📊 Conexões entre tudo:

Elemento	Ligação com outros
request.form	Captura dados do formulário (POST)
flash()	Feedback entre rotas (login inválido, logout, etc)
session	Usada para manter dados de sessão do usuário
make_response	Define resposta personalizada (cookies, headers)
@login_required	Protege rotas que exigem login
url_for()	Gera URLs dinâmicas e seguras
