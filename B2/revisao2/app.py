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
    return render_template("personagens.html")
  
@app.route('/novo', methods=['GET', 'POST'])
def novo():
    if request.method == "POST":
        conn = obter_conexao()
        
    return render_template("novo.html")
