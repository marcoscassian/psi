from sqlalchemy import create_engine, text, String
from sqlalchemy.orm import Session, DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column

#engine = create_engine('sqlite:///mercado.db')
engine = create_engine('mysql://root:@localhost/mercado')
sessao = Session(bind=engine)

class Base(DeclarativeBase):
    pass

class Produto(Base):
    __tablename__ = 'produtos'
    id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nome:Mapped[str] = mapped_column(String(30))

    #representação em String do objeto
    def __repr__(self):
        return f"Produto: {self.nome}"

#criar o banco de dados com base nas informações dos modelos
Base.metadata.create_all(bind=engine)

sessao.begin()
#realizar algumas operações
sessao.close()