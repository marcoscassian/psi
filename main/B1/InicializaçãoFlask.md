# 🚀 Iniciando um Projeto Flask

Este guia mostra como configurar um projeto Flask do zero, utilizando ambiente virtual e modo debug.

---

## 📁 1. Acesse a pasta do projeto

```bash
cd caminho/da/sua/pasta
```

---

## 🐍 2. Crie um ambiente virtual

```bash
python -m venv env
```

---

## ✅ 3. Ative o ambiente virtual

- **Windows**:
  ```bash
  env\Scripts\activate
  ```

- **Linux/Mac**:
  ```bash
  source env/bin/activate
  ```

---

## 📦 4. Instale o Flask

```bash
pip install flask
```

---

## 📝 5. Crie o arquivo `app.py`

```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return 'Olá, Flask!'

if __name__ == '__main__':
    app.run()
```

---

## ▶️ 6. Execute o servidor Flask (modo debug)

```bash
flask run --debug
```

---

## ⚠️ Caso necessário, defina a variável `FLASK_APP`

- **Windows (CMD):**
  ```cmd
  set FLASK_APP=app.py
  ```

- **Linux/Mac:**
  ```bash
  export FLASK_APP=app.py
  ```

---

## ✅ Pronto!

Acesse o projeto no navegador:  
[http://127.0.0.1:5000/](http://127.0.0.1:5000/)

---

> Feito para estudos da disciplina **Programação de Sistemas para Internet (PSI)**.
