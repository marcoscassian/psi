from database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Float, ForeignKey, Table

# --------------------------
# Relacionamento N:N
# Um Estudante pode fazer vários Cursos
# --------------------------

estudante_curso = Table(
    'estudantes_cursos',
    Base.metadata,
    mapped_column('estudante_id', ForeignKey('estudantes.id'), primary_key=True),
    mapped_column('curso_id', ForeignKey('cursos.id'), primary_key=True)
)

class Estudante(Base):
    __tablename__ = "estudantes"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(30))

    cursos = relationship('Curso', secondary=estudante_curso, back_populates='estudantes')


class Curso(Base):
    __tablename__ = "cursos"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(30))

    estudantes = relationship('Estudante', secondary=estudante_curso, back_populates='cursos')


# --------------------------
# Exemplo de User/Produto (1:N)
# --------------------------

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(30))
    email: Mapped[str] = mapped_column(String(100), unique=True)

    produtos = relationship('Product', backref='user')


class Product(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(30))
    valor: Mapped[float] = mapped_column(Float)

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))