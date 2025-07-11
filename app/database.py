from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from domain.models.base import Base

engine = create_engine('mysql+mysqlconnector://admin:12345@localhost/testdb', echo=True)
SessionLocal = sessionmaker(bind=engine)

def get_session():
    Base.metadata.create_all(engine)
    return SessionLocal()