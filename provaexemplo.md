Segue o arquivo `.md` completo com a prova prática e a resolução detalhada comentada, no estilo que pediu:

---

```markdown
# Avaliação – Programação de Sistemas para Internet – Turma 1M

## Prova Prática: Aplicação "Meu Perfil Escolar"

### Contextualização

Você foi contratado para desenvolver uma aplicação web chamada **Meu Perfil Escolar**. Nessa aplicação, o usuário poderá se cadastrar informando seu nome e curso, visualizar um resumo desses dados e ter uma experiência personalizada através do uso de cookies.

A aplicação deve permitir ainda acesso direto ao perfil via parâmetros na URL (query string).

---

### Requisitos da Aplicação

1. **Página Inicial (`/`)**  
   - Deve exibir um link para a rota `/cadastro`.

2. **Página de Cadastro (`/cadastro`)**  
   - Exibir um formulário HTML com dois campos:
     - Nome (input texto)
     - Curso (input texto)  
   - O formulário deve usar o método POST e enviar os dados para a mesma rota (`/cadastro`).  
   - Após o envio do formulário:
     - Armazenar o nome em um cookie com duração de 2 minutos.  
     - Redirecionar o usuário para a rota `/perfil` passando o nome e curso como parâmetros de consulta (query string).

3. **Página de Perfil (`/perfil`)**  
   - Exibir o nome e curso obtidos da query string.  
   - Exibir uma mensagem de boas-vindas personalizada com o nome obtido do cookie.  
   - Caso o cookie não esteja presente, exibir "Visitante" no lugar do nome.

---

### Estrutura de Arquivos que Deve Ser Entregue

```

/meu\_perfil\_escolar
├── app.py
├── templates/
│   ├── index.html
│   ├── cadastro.html
│   └── perfil.html
└── static/
└── style.css  (opcional)

````

---

# Resolução Detalhada Comentada

---

## 1. Arquivo `app.py`

```python
from flask import Flask, request, render_template, redirect, url_for, make_response

app = Flask(__name__)

# Rota para a página inicial '/'
@app.route('/')
def index():
    # Retorna template index.html com link para /cadastro
    return render_template('index.html')

# Rota para cadastro, aceita GET para mostrar o formulário e POST para receber os dados
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        # Coleta os dados enviados pelo formulário (nome e curso)
        nome = request.form.get('nome')
        curso = request.form.get('curso')

        # Prepara redirecionamento para /perfil com query string nome e curso
        redirecionar = redirect(url_for('perfil', nome=nome, curso=curso))

        # Cria resposta para poder adicionar o cookie
        resposta = make_response(redirecionar)

        # Define cookie 'nome' com o valor do nome enviado e tempo de vida de 120 segundos (2 minutos)
        resposta.set_cookie('nome', nome, max_age=120)

        # Retorna a resposta com redirecionamento e cookie definido
        return resposta

    # Se o método for GET, renderiza o formulário para cadastro
    return render_template('cadastro.html')

# Rota para a página de perfil que recebe nome e curso pela query string
@app.route('/perfil')
def perfil():
    # Pega os dados da query string (parâmetros enviados na URL)
    nome_query = request.args.get('nome')
    curso = request.args.get('curso')

    # Busca o cookie 'nome' para personalizar a mensagem de boas-vindas
    nome_cookie = request.cookies.get('nome', 'Visitante')  # Caso não tenha cookie, usa 'Visitante'

    # Renderiza o template perfil.html passando os dados necessários
    return render_template('perfil.html', nome_query=nome_query, curso=curso, nome_cookie=nome_cookie)

if __name__ == '__main__':
    app.run(debug=True)
````

### Comentários:

* **`request.method`**: Usado para diferenciar GET (mostrar formulário) e POST (processar dados).
* **`request.form`**: Captura os dados enviados via formulário HTML.
* **`redirect` + `url_for`**: Envia o usuário para outra rota, construindo a URL dinamicamente, incluindo parâmetros na query string.
* **`make_response`**: Permite modificar a resposta HTTP, como adicionar cookies.
* **`set_cookie`**: Define um cookie que o navegador irá armazenar, com tempo de vida limitado (2 minutos aqui).
* **`request.cookies.get`**: Recupera o cookie enviado pelo navegador na requisição.

---

## 2. Templates HTML (em `/templates/`)

---

### `index.html`

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8" />
    <title>Meu Perfil Escolar - Início</title>
</head>
<body>
    <h1>Bem-vindo ao Meu Perfil Escolar</h1>
    <!-- Link para a página de cadastro -->
    <a href="{{ url_for('cadastro') }}">Ir para Cadastro</a>
</body>
</html>
```

* Usa `url_for('cadastro')` para criar o link para a rota `/cadastro`.
* Simples página com um título e link.

---

### `cadastro.html`

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8" />
    <title>Cadastro</title>
</head>
<body>
    <h2>Cadastro de Usuário</h2>
    <!-- Formulário que envia dados para a mesma rota usando POST -->
    <form method="POST" action="{{ url_for('cadastro') }}">
        <label for="nome">Nome:</label>
        <input type="text" id="nome" name="nome" required /><br /><br />
        
        <label for="curso">Curso:</label>
        <input type="text" id="curso" name="curso" required /><br /><br />
        
        <button type="submit">Enviar</button>
    </form>
</body>
</html>
```

* Formulário com dois campos obrigatórios: nome e curso.
* Usa `url_for('cadastro')` para garantir que o formulário envie para a rota correta, independente do endereço base.

---

### `perfil.html`

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8" />
    <title>Perfil</title>
</head>
<body>
    <h2>Resumo do Perfil</h2>
    <p><strong>Nome (via query string):</strong> {{ nome_query }}</p>
    <p><strong>Curso:</strong> {{ curso }}</p>
    <p><strong>Mensagem personalizada:</strong> Bem-vindo(a), {{ nome_cookie }}!</p>
    <a href="{{ url_for('index') }}">Voltar para Início</a>
</body>
</html>
```

* Mostra as informações vindas da query string (`nome_query`, `curso`).
* Exibe a mensagem personalizada com o nome obtido do cookie (ou "Visitante" se cookie não existir).
* Link para voltar para a página inicial.

---

## 3. (Opcional) Arquivo `static/style.css`

Pode ser simples, para deixar visual mais agradável:

```css
body {
    font-family: Arial, sans-serif;
    background-color: #f4f4f4;
    margin: 40px;
    color: #333;
}

h1, h2 {
    color: #0055aa;
}

a {
    text-decoration: none;
    color: #0077cc;
}

a:hover {
    text-decoration: underline;
}
```

---

## Conceitos e Relações Aplicados nesta Prova

| Conceito             | Como está aplicado?                                                                                      |
| -------------------- | -------------------------------------------------------------------------------------------------------- |
| Rotas e métodos HTTP | Usamos GET para exibir páginas e POST para receber dados do formulário.                                  |
| `request`            | Para capturar dados enviados via formulário e cookies enviados pelo navegador.                           |
| `make_response`      | Para adicionar cookies na resposta HTTP.                                                                 |
| Cookies              | Armazenamos o nome do usuário com validade de 2 minutos para personalizar a experiência.                 |
| Redirecionamento     | Após receber dados do formulário, redirecionamos para outra rota passando parâmetros na query string.    |
| `url_for`            | Para construir URLs dinamicamente, deixando o código mais robusto e fácil de manter.                     |
| Templates Jinja2     | Separação da lógica (Python) da apresentação (HTML), utilizando variáveis e funções do Jinja2 (`{{ }}`). |

---

# Como rodar a aplicação

1. Certifique-se de ter o Python e Flask instalados (`pip install flask`).

2. Estruture os arquivos conforme o modelo da prova.

3. Execute o app:

```bash
python app.py
```

4. Acesse `http://127.0.0.1:5000/` no navegador e teste a aplicação.

---

Se quiser, posso ajudar a gerar o ZIP com os arquivos ou montar versões mais complexas que envolvam `session`, `flask-login` e outras coisas. Quer?

---

Se precisar, só falar!
