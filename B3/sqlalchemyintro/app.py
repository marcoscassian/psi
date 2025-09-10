from sqlalchemy import create_engine, text

SQLITE = 'sqlite:///database.db'
engine = create_engine(SQLITE)

with engine.connect() as conexao:
    SQL = text ("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome VARCHAR NOT NULL)""")
    conexao.execute(SQL)
    conexao.commit()
    #conexao.close()

#pip install mysqlclient
MYSQL = "mysql://root:@localhost/flask"
engine = create_engine(MYSQL)

conexao = engine.connect() #msm coisa da linha 6, so que precisa ser fechado
SQL = text ("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTO_INCREMENT,
            nome VARCHAR(50) NOT NULL)""")
conexao.execute(SQL)
conexao.commit()

SQL = "INSERT INTO users (nome) VALUES (:nome)"
nome = 'zebeleu'
conexao.execute(text(SQL), {'nome': nome})
conexao.commit()

conexao.close()
