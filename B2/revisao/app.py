from flask import Flask, request, url_for, redirect
from flask import render_template

import sqlite3


def obter_conexao():
    conn = sqlite3.connect('banco.db')
    conn.row_factory = sqlite3.Row
    return conn

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == "POST":
        nome = request.form['nome']

        conn = obter_conexao()

        SQL = "INSERT INTO users(nome) VALUES (?)"
        conn.execute(SQL, (nome,))
        conn.commit()
        conn.close()


        return redirect(url_for('index'))

    conn = obter_conexao()
    SQL = "SELECT * FROM users"
    lista = conn.execute(SQL).fetchall()
    conn.close()

    return render_template('index.html', lista=lista)
