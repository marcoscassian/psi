import sqlite3

conexao = sqlite3.connect('banco.db')

sql = "INSERT INTO livros(titulo, usuario_id) VALUES('EU', 2)"

conexao.execute("PRAGMA foreign_keys = ON")
conexao.execute(sql)
conexao.commit()

conexao.close()