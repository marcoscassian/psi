import sqlite3

conexao = sqlite3.connect('banco.db')

arquivo = 'schema.sql'

with open(arquivo) as f:
    conexao.executescript(f.read())


conexao.close()