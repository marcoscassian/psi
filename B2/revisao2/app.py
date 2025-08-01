from flask import Flask, request, url_for, redirect
from flask import render_template

import sqlite3


def obter_conexao():
    conn = sqlite3.connect('jogo.db')
    conn.row_factory = sqlite3.Row
    return conn

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/personagens')
def personagens():
    conn = obter_conexao()
    SQL = "SELECT * FROM jogo"
    lista = conn.execute(SQL).fetchall()
    conn.close()
    return render_template("personagens.html", lista=lista)
  
@app.route('/novo', methods=['GET', 'POST'])
def novo():
    if request.method == "POST":
        nomepersonagem = request.form['nomepersonagem']
        jogoorigem = request.form['jogoorigem']
        habilidade = request.form['habilidade']

        conn = obter_conexao()

        SQL = "INSERT INTO jogo(nomepersonagem, jogoorigem, habilidade) VALUES (?, ?, ?)"
        conn.execute(SQL, (nomepersonagem, jogoorigem, habilidade))
        conn.commit()
        conn.close()


        return redirect(url_for('personagens'))

    return redirect(url_for('novo.html'))
