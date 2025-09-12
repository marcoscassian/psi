from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

SQLITE = 'sqlite:///biblioteca.db'
engine = create_engine(SQLITE)

with Session(bind=engine) as sessao:
    SQL = text ("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL
                )
                """)
    sessao.execute(SQL)

    sessao.rollback()

    sessao.commit()