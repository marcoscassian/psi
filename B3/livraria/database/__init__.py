from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session

engine = create_engine('sqlite:///biblioteca.db', echo=True)
#engine = create_engine('mysql://root:@localhost/bancao')
session = Session(bind=engine)

class Base(DeclarativeBase):
    pass
