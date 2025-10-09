from database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Float, ForeignKey, Table

# --------------------------
# Relacionamento 1:N
# Um Autor pode ter vários Livros
# --------------------------

class Autor(Base):
    __tablename__ = "autores"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(100))
    nacionalidade: Mapped[str] = mapped_column(String(50))

    livros = relationship('Livro', back_populates='autor')


class Livro(Base):
    __tablename__ = "livros"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    titulo: Mapped[str] = mapped_column(String(100))
    genero: Mapped[str] = mapped_column(String(50))
    ano: Mapped[int] = mapped_column(Integer)

    autor_id: Mapped[int] = mapped_column(ForeignKey('autores.id'))
    autor = relationship('Autor', back_populates='livros')
