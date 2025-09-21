
# Instalando Dependências do Python via `requirements.txt`

## 1️⃣ Pré-requisitos
- Ter o **Python** instalado  
- Ter o **pip** instalado (geralmente já vem com o Python)  

Verifique com:
```bash
python --version
pip --version
````

---

## 2️⃣ Criar ou obter o `requirements.txt`

Se você já tem um projeto e quer gerar o arquivo com todas as dependências instaladas:

```bash
pip freeze > requirements.txt
```

Isso cria um arquivo `requirements.txt` com todas as libs e versões:

```
Flask==3.0.2
SQLAlchemy==2.0.30
requests==2.32.3
```

---

## 3️⃣ Instalar as dependências

Para instalar todas as libs listadas no `requirements.txt`:

```bash
pip install -r requirements.txt
```

* O Python vai instalar todas as bibliotecas necessárias.
* Se quiser atualizar pacotes, pode adicionar `--upgrade`:

```bash
pip install --upgrade -r requirements.txt
```

---

## 4️⃣ Dicas

* Sempre use **virtualenv** ou **venv** para não misturar pacotes do sistema:

```bash
python -m venv venv
source venv/bin/activate  # Linux / Mac
venv\Scripts\activate     # Windows
```

* Depois de ativar o ambiente, rode o `pip install -r requirements.txt`.

* Atualize o `requirements.txt` sempre que adicionar novas dependências:

```bash
pip freeze > requirements.txt
```
