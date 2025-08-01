import sqlite3
import os
print("Diretório atual:", os.getcwd())

arquivo = 'schema.sql'
conexao = sqlite3.connect('jogo.db')

with open(arquivo) as f:
    conexao.executescript(f.read())

conexao.close()
