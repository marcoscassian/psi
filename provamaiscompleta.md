Claro! Vou criar uma prova prática mais complexa, envolvendo **todos os conceitos que você listou** (Flask, rotas, métodos HTTP, request, make\_response, cookies, session, secret\_key, url\_for, templates com extends/include/flash, Flask-Login com LoginManager, login\_required, login\_user, logout\_user, @login\_manager.user\_loader, etc).

Vou estruturar a prova com vários requisitos, incluindo autenticação, sessão, uso de cookies, templates organizados, controle de acesso e mensagens flash.

---

# Prova Prática Completa — Aplicação Web “Portal Escolar Seguro”

---

## Contextualização

Você foi contratado para desenvolver o “Portal Escolar Seguro”, uma aplicação web onde usuários podem:

* Se cadastrar e fazer login;
* Editar seu perfil (nome e curso);
* Visualizar seu perfil;
* Acessar páginas protegidas apenas para usuários autenticados;
* Usar cookies e sessões para manter estado e personalizar a experiência;
* Receber mensagens flash de feedback nas operações.

---

## Requisitos

### 1. Configuração inicial

* Usar Flask e Flask-Login;
* Configurar `SECRET_KEY` para a sessão;
* Criar modelo `User` em um arquivo separado para gerenciamento de usuários (em memória ou sessão);
* Usar `werkzeug.security` para hash de senhas.

### 2. Autenticação

* Rota `/register` para cadastro de usuário (nome, email, senha, curso);
* Rota `/login` para login;
* Rota `/logout` para logout;
* Usar `login_user`, `logout_user`, `login_required`, `LoginManager`, `@login_manager.user_loader`.

### 3. Perfil do usuário

* Rota `/profile` protegida (login requerido);
* Mostrar dados do usuário;
* Formulário para editar nome e curso;
* Salvar alterações no “banco” em memória/sessão.

### 4. Cookies e sessão

* Usar cookie para armazenar preferências (exemplo: tema claro/escuro);
* Usar session para armazenar dados temporários do usuário;
* Exibir mensagem personalizada com base em cookie e sessão.

### 5. Templates

* Usar base.html com blocos (`extends`, `block`, `include`);
* Templates separados para registro, login, perfil, dashboard;
* Usar `flash` para mensagens de sucesso/erro (ex.: “Usuário cadastrado com sucesso”, “Senha incorreta”, etc).

---

## Estrutura mínima de arquivos para entregar:

```
portal_escolar_seguro/
├── app.py
├── models.py
├── templates/
│   ├── base.html
│   ├── components/
│   │   └── messages.html
│   ├── auth/
│   │   ├── login.html
│   │   └── register.html
│   ├── profile.html
│   └── dashboard.html
└── static/
    └── style.css
```

---

## Prova: Desenvolva a aplicação que atende a todos os requisitos acima.

---

# Resolução Comentada (exemplo completo)

Vou mandar abaixo a resolução com todos os arquivos comentados.

---

### 1. `models.py` — Modelo User

```python
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask import session

class User(UserMixin):
    def __init__(self, email, nome, curso, password):
        self.email = email
        self.nome = nome
        self.curso = curso
        self.password_hash = generate_password_hash(password)  # Armazena hash da senha

    def check_password(self, password):
        # Verifica se a senha fornecida corresponde ao hash armazenado
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        # Método obrigatório para Flask-Login: retorna identificador único do usuário
        return self.email

    def save(self):
        # Salva ou atualiza o usuário na "base de dados" armazenada na sessão
        usuarios = session.get('usuarios', {})
        usuarios[self.email] = {
            'nome': self.nome,
            'curso': self.curso,
            'password_hash': self.password_hash
        }
        session['usuarios'] = usuarios

    @staticmethod
    def get(email):
        # Recupera usuário pelo email da sessão
        usuarios = session.get('usuarios', {})
        dados = usuarios.get(email)
        if not dados:
            return None
        user = User(email, dados['nome'], dados['curso'], '')
        user.password_hash = dados['password_hash']
        return user
```

---

### 2. `app.py`

```python
from flask import Flask, render_template, request, redirect, url_for, flash, session, make_response
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'chave-secreta-muito-segura'

# Configuração do LoginManager
login_manager = LoginManager()
login_manager.login_view = 'login'  # Redireciona usuário para login se rota protegida for acessada sem autenticação
login_manager.init_app(app)

# Função para carregar usuário da sessão com base no ID (email)
@login_manager.user_loader
def load_user(email):
    return User.get(email)

@app.before_request
def criar_usuarios_sessao():
    # Garante que o dicionário de usuários exista na sessão para armazenar dados
    if 'usuarios' not in session:
        session['usuarios'] = {}

# Rota inicial - Dashboard, protegida
@app.route('/')
@login_required
def dashboard():
    # Exibe página inicial para usuário logado
    tema = request.cookies.get('tema', 'claro')  # Usa cookie para tema
    return render_template('dashboard.html', tema=tema)

# Rota para registro de usuário
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        nome = request.form['nome']
        curso = request.form['curso']
        senha = request.form['senha']

        # Verifica se já existe usuário com esse email
        if User.get(email):
            flash('Usuário já cadastrado', 'error')
            return redirect(url_for('register'))

        # Cria usuário e salva na sessão
        user = User(email, nome, curso, senha)
        user.save()

        # Loga o usuário após registro
        login_user(user)
        flash('Cadastro realizado com sucesso!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('auth/register.html')

# Rota para login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        user = User.get(email)
        if user and user.check_password(senha):
            login_user(user)
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Email ou senha incorretos', 'error')
            return redirect(url_for('login'))

    return render_template('auth/login.html')

# Rota para logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você saiu da sessão', 'success')
    return redirect(url_for('login'))

# Rota para visualizar e editar perfil
@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        # Atualiza nome e curso do usuário atual
        nome = request.form['nome']
        curso = request.form['curso']

        # Atualiza dados no "banco"
        usuarios = session.get('usuarios')
        usuarios[current_user.email]['nome'] = nome
        usuarios[current_user.email]['curso'] = curso
        session['usuarios'] = usuarios

        flash('Perfil atualizado com sucesso!', 'success')
        return redirect(url_for('profile'))

    # GET - renderiza perfil atual
    return render_template('profile.html', user=current_user)

# Rota para alterar tema (cookie)
@app.route('/set_tema/<tema>')
@login_required
def set_tema(tema):
    # Define cookie para preferência de tema, válido por 30 dias
    if tema not in ['claro', 'escuro']:
        flash('Tema inválido', 'error')
        return redirect(url_for('dashboard'))

    resposta = make_response(redirect(url_for('dashboard')))
    resposta.set_cookie('tema', tema, max_age=60*60*24*30)
    flash(f'Tema alterado para {tema}', 'success')
    return resposta

if __name__ == '__main__':
    app.run(debug=True)
```

---

### 3. Templates (resumo e exemplos principais)

---

#### `templates/base.html`

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8" />
    <title>{% block title %}Portal Escolar Seguro{% endblock %}</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}" />
</head>
<body class="{{ 'dark' if request.cookies.get('tema') == 'escuro' else 'light' }}">
    <header>
        <h1>Portal Escolar Seguro</h1>
        {% if current_user.is_authenticated %}
            <nav>
                <a href="{{ url_for('dashboard') }}">Dashboard</a> |
                <a href="{{ url_for('profile') }}">Perfil</a> |
                <a href="{{ url_for('logout') }}">Sair</a>
            </nav>
        {% else %}
            <nav>
                <a href="{{ url_for('login') }}">Login</a> |
                <a href="{{ url_for('register') }}">Registrar</a>
            </nav>
        {% endif %}
    </header>

    <!-- Inclui mensagens flash -->
    {% include 'components/messages.html' %}

    <main>
        {% block content %}{% endblock %}
    </main>

    <footer>
        <p>© 2025 Portal Escolar Seguro</p>
    </footer>
</body>
</html>
```

---

#### `templates/components/messages.html`

```html
{% with messages = get_flashed_messages(with_categories=true) %}
  {% if messages %}
    <ul class="messages">
      {% for category, message in messages %}
        <li class="{{ category }}">{{ message }}</li>
      {% endfor %}
    </ul>
  {% endif %}
{% endwith %}
```

---

#### `templates/auth/login.html`

```html
{% extends "base.html" %}

{% block title %}Login{% endblock %}

{% block content %}
<h2>Login</h2>
<form method="POST" action="{{ url_for('login') }}">
    <input type="email" name="email" placeholder="Email" required />
    <input type="password" name="senha" placeholder="Senha" required />
    <button type="submit">Entrar</button>
</form>
{% endblock %}
```

---

#### `templates/auth/register.html`

```html
{% extends "base.html" %}

{% block title %}Registrar{% endblock %}

{% block content %}
<h2>Registrar</h2>
<form method="POST" action="{{ url_for('register') }}">
    <input type="text" name="nome" placeholder="Nome" required />
    <input type="email" name="email" placeholder="Email" required />
    <input type="text" name="curso" placeholder="Curso" required />
    <input type="password" name="senha" placeholder="Senha" required />
    <button type="submit">Cadastrar</button>
</form>
{% endblock %}
```

---

#### `templates/dashboard.html`

```html
{% extends "base.html" %}

{% block title %}Dashboard{% endblock %}

{% block content %}
<h2>Bem-vindo, {{ current_user.nome }}!</h2>
<p>Seu curso: {{ current_user.curso }}</p>
<p>Tema atual: {{ 'Escuro' if request.cookies.get('tema') == 'escuro' else 'Claro' }}</p>

<p>Alterar tema:</p>
<ul>
    <li><a href="{{ url_for('set_tema', tema='claro') }}">Claro</a></li>
    <li><a href="{{ url_for('set_tema', tema='escuro') }}">Escuro</a></li>
</ul>
{% endblock %}
```

---

#### `templates/profile.html`

```html
{% extends "base.html" %}

{% block title %}Perfil{% endblock %}

{% block content %}
<h2>Editar Perfil</h2>
<form method="POST" action="{{ url_for('profile') }}">
    <label>Nome:</label><br/>
    <input type="text" name="nome" value="{{ user.nome }}" required /><br/><br/>

    <label>Curso:</label><br/>
    <input type="text" name="curso" value="{{ user.curso }}" required /><br/><br/>

    <button type="submit">Salvar</button>
</form>
{% endblock %}
```

---

### 4. `static/style.css` (exemplo simples)

```css
body.light {
    background-color: #fff;
    color: #000;
}

body.dark {
    background-color: #222;
    color: #eee;
}

header, footer {
    background-color: #004a99;
    color: white;
    padding: 10px;
    text-align: center;
}

nav a {
    color: #fff;
    margin: 0 10px;
    text-decoration: none;
}

nav a:hover {
    text-decoration: underline;
}

.messages li {
    list-style: none;
    padding: 8px;
    margin: 5px 0;
}

.messages li.success {
    background-color: #d4edda;
    color: #155724;
    border-left: 6px solid #155724;
}

.messages li.error {
    background-color: #f8d7da;
    color: #721c24;
    border-left: 6px solid #721c24;
}
```

---

# Explicação Final

* **Autenticação:** feita com Flask-Login, controlando acesso com `login_required` e gerenciando sessão.
* **Hash de senha:** para segurança, senhas nunca são armazenadas em texto puro.
* **Cookies:** usados para salvar a preferência de tema, acessado em templates e alterado via rota.
* **Session:** mantém lista de usuários em memória (simulando um banco de dados simples).
* **Templates:** organizados com base, blocos, includes, mensagens flash.
* **Redirecionamentos e mensagens:** feedback ao usuário para sucesso e erros.
* **Rotas protegidas:** apenas usuários logados acessam dashboard e perfil.

---

Se quiser, posso gerar o arquivo `.zip` com essa estrutura para você testar direto, ou criar um passo a passo de instalação e execução.

Quer?
