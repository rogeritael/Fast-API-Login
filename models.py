from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

USER = 'root'
PASSWORD = ''
HOST = 'localhost'
DATABASE = 'pyauthentication'
PORT = '3306'

CONN = f'mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}'

# se conecta no banco, echo true printa informações no console(interessante setar como false ao colocar em produção)
engine = create_engine(CONN, echo=True)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    nome = Column(String(50)) #maximo 50 caracteres
    usuario = Column(String(20))
    senha = Column(String(10))

class Tokens(Base):
    __tablename__ = 'tokens'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    token = Column(String(100))
    data = Column(DateTime, default=datetime.datetime.now())

Base.metadata.create_all(engine)