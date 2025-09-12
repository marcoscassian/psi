from sqlalchemy.orm import Session
from modelo import Produto
from modelo import engine

with Session(bind=engine) as sessao:

    resultado = sessao.query(Produto).filter(Produto.nome.startswith('A')).all()
    print(resultado)