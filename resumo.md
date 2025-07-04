✅ Guia Teórico Profundo – Flask + Flask-Login

⸻

1. Criar Ambiente

✔ Conceito

O ambiente virtual isola o projeto para que dependências não entrem em conflito com outros projetos Python do sistema.

✔ Quando usar?

Sempre que iniciar um novo projeto Python.

✔ Comandos explicados

python -m venv venv  # Cria o ambiente
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate  # Windows

Você deve ativar o ambiente antes de instalar bibliotecas ou rodar o servidor Flask.

⸻

2. Instalar pacotes

📦 Pacotes principais:

Pacote	Função
Flask	Framework web principal.
Flask-Login	Gerenciar autenticação e sessões de login.

pip install flask flask-login

📄 Requisitos (opcional):

Crie um requirements.txt para facilitar instalação em outro ambiente:

pip freeze > requirements.txt
# Depois, use: pip install -r requirements.txt


⸻

3. Rotas e Métodos HTTP

🚏 Rotas

Cada rota está ligada a uma view function que retorna uma resposta (normalmente HTML ou JSON).

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
        # processa o login
        ...
    return render_template('login.html')


⸻

4. request

📌 O que é?

Objeto do Flask que traz informações da requisição feita pelo navegador.

🧪 Formas comuns de uso:

request.form['campo']  # Dados enviados via POST
request.args['q']      # Dados enviados via GET (?q=valor)
request.method         # Tipo da requisição (GET ou POST)

📦 Observação:

Sempre valide os dados para evitar erros e falhas de segurança (ex: SQL Injection).

⸻

5. make_response

🔧 O que faz?

Permite customizar a resposta que será enviada ao navegador:
	•	Adicionar cookies
	•	Alterar cabeçalhos
	•	Definir status HTTP

from flask import make_response

@app.route('/set-cookie')
def set_cookie():
    resp = make_response("Cookie criado!")
    resp.set_cookie('tema', 'escuro')
    return resp


⸻

6. Cookies, Session e Secret Key

🍪 Cookies:

Armazenados no navegador do usuário. Úteis para coisas leves (tema, idioma, etc).

🗂️ Session:

Usado pelo servidor para manter informações seguras, como o ID do usuário logado. Depende de secret_key.

app.secret_key = 'senha-super-secreta'
session['usuario'] = 'admin'

🧠 Relação com Flask-Login:

Flask-Login usa session por trás dos panos para armazenar o ID do usuário logado.

⸻

7. url_for

🔗 Gera URLs dinamicamente:

url_for('login')  # /login
url_for('perfil', id=3)  # /perfil/3

Evita erro por digitação de rotas e facilita mudanças futuras no nome da URL.

✅ Exemplos:

return redirect(url_for('dashboard'))

No HTML:

<a href="{{ url_for('logout') }}">Sair</a>


⸻

8. Templates (extends, include, flash)

🔧 extends

Define que um template herda de outro (ex: layout padrão).

<!-- dashboard.html -->
{% extends 'base.html' %}
{% block conteudo %}
  <h1>Bem-vindo!</h1>
{% endblock %}

🔧 include

Inclui trechos reutilizáveis (navbar, rodapé):

{% include 'navbar.html' %}

🔔 flash

Permite enviar mensagens entre requisições:

flash('Senha incorreta!')
return redirect(url_for('login'))

No HTML:

{% with msgs = get_flashed_messages() %}
  {% for msg in msgs %}
    <div class="alert">{{ msg }}</div>
  {% endfor %}
{% endwith %}


⸻

9. Flask-Login

🔐 Visão Geral

Gerencia autenticação sem precisar escrever todo o sistema de login manualmente.

⸻

🔹 LoginManager

Instancia o gerenciador de sessão:

from flask_login import LoginManager

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


⸻

🔹 @login_manager.user_loader

Define como o usuário será buscado com base no user_id salvo na session:

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))  # ou busca no dicionário/fake DB


⸻

🔹 login_user(usuario)

Faz login de um usuário e armazena seu ID na sessão:

from flask_login import login_user

login_user(usuario)


⸻

🔹 logout_user()

Remove o ID do usuário da sessão:

from flask_login import logout_user

logout_user()


⸻

🔹 @login_required

Impede acesso a rotas se o usuário não estiver logado:

@app.route('/painel')
@login_required
def painel():
    return "Área protegida"

Você deve redirecionar para a rota definida em:

login_manager.login_view = 'login'


⸻

🔹 Classe User + UserMixin

A classe de usuário deve implementar os métodos esperados:

from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, nome, senha):
        self.id = id
        self.nome = nome
        self.senha = senha

O UserMixin já fornece:
	•	is_authenticated
	•	is_active
	•	get_id()

⸻

📊 Conexões entre tudo:

Elemento	Ligação com outros
request.form	Usado em rotas com POST para capturar login.
flash()	Mostra feedback ao usuário após redirecionamento.
session	Usada por Flask-Login para guardar user_id.
make_response + set_cookie	Personaliza resposta e define cookies do navegador.
@login_required	Protege páginas com conteúdo privado.
url_for()	Gera rotas dinâmicas usadas em redirect() e templates.
