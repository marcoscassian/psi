from database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Float, ForeignKey, Table, Column
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from typing import List

user_livro = Table(
    'users_livros',
    Base.metadata,
    Column('user_id', ForeignKey('users.id'), primary_key=True),
    Column('livro_id', ForeignKey('livros.id'), primary_key=True)
)

class User(Base, UserMixin):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(200), nullable=False)
    
    livros:Mapped[List['Livro']] = relationship(secondary=user_livro, back_populates='users')

class Livro(Base):
    __tablename__ = 'livros'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    titulo: Mapped[str] = mapped_column(String(120), nullable=False)
    ano: Mapped[int] = mapped_column(Integer, nullable=True)
    autor_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)

    users:Mapped[List['User']] = relationship(secondary=user_livro, back_populates='livros')