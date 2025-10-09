from flask import Flask, render_template, request, redirect, url_for
from database import engine, Base, session
from models import Autor, Livro

# Cria as tabelas no banco (se não existirem)
Base.metadata.create_all(bind=engine)

app = Flask(__name__)

# --------------------------
# Página Inicial
# --------------------------
@app.route('/')
def index():
    return render_template('index.html')


# --------------------------
# Rotas de Autores
# --------------------------
@app.route('/autores')
def listar_autores():
    autores = session.query(Autor).all()
    return render_template('autores.html', autores=autores)

@app.route('/autores/novo', methods=['GET', 'POST'])
def novo_autor():
    if request.method == 'POST':
        nome = request.form['nome']
        nacionalidade = request.form['nacionalidade']
        autor = Autor(nome=nome, nacionalidade=nacionalidade)
        session.add(autor)
        session.commit()
        return redirect(url_for('listar_autores'))
    return render_template('novo_autor.html')


# --------------------------
# Rotas de Livros
# --------------------------
@app.route('/livros')
def listar_livros():
    livros = session.query(Livro).all()
    return render_template('livros.html', livros=livros)

@app.route('/livros/novo', methods=['GET', 'POST'])
def novo_livro():
    autores = session.query(Autor).all()
    if request.method == 'POST':
        titulo = request.form['titulo']
        genero = request.form['genero']
        ano = int(request.form['ano'])
        autor_id = int(request.form['autor_id'])
        livro = Livro(titulo=titulo, genero=genero, ano=ano, autor_id=autor_id)
        session.add(livro)
        session.commit()
        return redirect(url_for('listar_livros'))
    return render_template('novo_livro.html', autores=autores)


if __name__ == '__main__':
    app.run(debug=True)
