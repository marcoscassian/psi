from sqlalchemy import create_engine, text, String
from sqlalchemy.orm import Session, DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column

from faker import Faker

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

faker = Faker('pt_BR')

#pip install faker
with Session(bind=engine) as sessao:
    for x in range(10):
        prod_nome = faker.name()
        produto = Produto(nome=prod_nome)
        sessao.add(produto)
    
    sessao.commit()
