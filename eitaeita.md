Aqui está a interpretação detalhada da sua avaliação prática de Flask, com os conceitos explicados e um esboço de resolução em Markdown para você se orientar e programar com clareza.

⸻

📝 Avaliação Prática – Flask

Disciplina: Desenvolvimento Web
Professor: Romerito Campos de Andrade
Aluno: Nomer Co

⸻

❓ Questões Teóricas

Questão 1 (10 pontos) – Sessões

Pergunta: Qual a função da sessão em Flask?

✅ Resposta correta: B)
“Guardar dados que identificam o usuário entre requisições.”

Explicação: O protocolo HTTP é stateless, ou seja, não guarda o estado entre requisições. A sessão permite que o Flask memorize dados importantes do usuário (como seu ID ou login) enquanto ele navega no site, armazenando-os no lado do servidor e identificando-os com um cookie de sessão.

⸻

Questão 2 (10 pontos) – Flask-Login e load_user

Pergunta: Para que serve a função load_user no Flask-Login?

✅ Resposta correta: C)
“Carregar o objeto de usuário a partir do identificador salvo na sessão.”

Explicação: O Flask-Login salva o ID do usuário logado na sessão. A função load_user recebe esse ID e retorna o objeto de usuário correspondente. É obrigatória para que o Flask-Login funcione corretamente, pois ele precisa recuperar os dados completos do usuário logado.

⸻

🧑‍💻 Questão Prática – Sistema de Cadastro e Login em Flask

Você deve desenvolver um site com:
	•	Cadastro de usuário (matrícula, email, senha)
	•	Login usando matrícula
	•	Área restrita (acessível só após login)
	•	Logout
	•	Senha criptografada
	•	Dados persistidos em memória (por dicionário, por exemplo)
	•	Mensagens de feedback

⸻

📁 Estrutura Esperada do Projeto

/meuapp/
│
├── app.py
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── cadastro.html
│   ├── area_restrita.html
│
├── static/
│   └── (opcional: CSS, imagens)


⸻

🧠 Conceitos Envolvidos

🔐 Sessões

Flask usa a variável session para armazenar dados temporários entre requisições. Exige app.secret_key.

session['user_id'] = usuario.id

🔑 Flask-Login

Biblioteca para autenticação:
	•	LoginManager()
	•	@login_required
	•	login_user(usuario)
	•	logout_user()
	•	current_user

🔄 Criptografia de Senha

Use werkzeug.security:

from werkzeug.security import generate_password_hash, check_password_hash


⸻

✅ Resolução em Markdown (com código comentado)

# Resolução da Questão Prática – Flask Login

## Requisitos Atendidos:
✅ Estrutura com templates e herança  
✅ Cadastro com validações e criptografia  
✅ Login com sessão e proteção de rota  
✅ Logout funcionando  
✅ Links e mensagens de feedback  

---

## Código: app.py (resumo comentado)

```python
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'minha_chave_secreta'

login_manager = LoginManager(app)
login_manager.login_view = 'login'

# "Banco de dados" em memória
usuarios = {}

# Modelo de usuário
class Usuario(UserMixin):
    def __init__(self, matricula, email, senha_hash):
        self.id = matricula
        self.email = email
        self.senha_hash = senha_hash

    def verificar_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)

@login_manager.user_loader
def load_user(matricula):
    return usuarios.get(matricula)

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        matricula = request.form['matricula']
        email = request.form['email']
        senha = request.form['senha']
        
        if not matricula or not email or not senha:
            flash("Todos os campos são obrigatórios.")
            return redirect(url_for('cadastro'))

        if matricula in usuarios:
            flash("Usuário com essa matrícula já existe.")
            return redirect(url_for('cadastro'))

        for u in usuarios.values():
            if u.email == email:
                flash("Email já cadastrado.")
                return redirect(url_for('cadastro'))

        senha_hash = generate_password_hash(senha)
        usuarios[matricula] = Usuario(matricula, email, senha_hash)

        flash("Usuário cadastrado com sucesso!")
        return redirect(url_for('login'))

    return render_template('cadastro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        matricula = request.form['matricula']
        senha = request.form['senha']
        
        usuario = usuarios.get(matricula)

        if usuario and usuario.verificar_senha(senha):
            login_user(usuario)
            flash("Login realizado com sucesso!")
            return redirect(url_for('restrita'))

        flash("Login inválido.")
    return render_template('login.html')

@app.route('/restrita')
@login_required
def restrita():
    return render_template('area_restrita.html', usuario=current_user)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logout realizado com sucesso.")
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)


⸻

🖼️ Templates

base.html

<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}Sistema Flask{% endblock %}</title>
</head>
<body>
    <nav>
        <a href="{{ url_for('login') }}">Login</a>
        <a href="{{ url_for('cadastro') }}">Cadastro</a>
        {% if current_user.is_authenticated %}
        <a href="{{ url_for('restrita') }}">Área Restrita</a>
        <a href="{{ url_for('logout') }}">Logout</a>
        {% endif %}
    </nav>
    {% with messages = get_flashed_messages() %}
      {% for msg in messages %}
        <p>{{ msg }}</p>
      {% endfor %}
    {% endwith %}
    {% block content %}{% endblock %}
</body>
</html>

cadastro.html

{% extends "base.html" %}
{% block content %}
<h2>Cadastro</h2>
<form method="post">
    Matrícula: <input type="text" name="matricula"><br>
    Email: <input type="email" name="email"><br>
    Senha: <input type="password" name="senha"><br>
    <input type="submit" value="Cadastrar">
</form>
{% endblock %}

login.html

{% extends "base.html" %}
{% block content %}
<h2>Login</h2>
<form method="post">
    Matrícula: <input type="text" name="matricula"><br>
    Senha: <input type="password" name="senha"><br>
    <input type="submit" value="Entrar">
</form>
{% endblock %}

area_restrita.html

{% extends "base.html" %}
{% block content %}
<h2>Bem-vindo!</h2>
<p>Você está logado como: {{ usuario.email }}</p>
{% endblock %}


⸻

Se quiser, posso gerar uma versão em .zip da aplicação ou criar mais funcionalidades, como esqueci minha senha, níveis de acesso ou banco SQLite.

Deseja isso?
