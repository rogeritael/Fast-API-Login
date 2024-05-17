from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

from models import CONN, User, Tokens


from secrets import token_hex


app = FastAPI()

#utilizar a função connect() sempre que for utilizar o banco de dados
def connect():
    engine = create_engine(CONN, echo=True)
    Session = sessionmaker(bind=engine)
    return Session()

@app.post('/register')
def register(nome: str, user: str, senha: str):
    session = connect()
    user = session.query(User).filter_by(user=user,senha=senha).all() #verifica se existe um usuario com a senha já cadastrado

    if len(user) > 0:
        new_user = User(nome=nome,usuario=user, senha=senha)
        
        #adição no banco de dados
        session.add(new_user)
        session.commit()
        return {'status': 'usuario cadastrado com sucesso'}
    else:
        return {'status': 'Usuário já cadastrado'}
    

@app.post('/login')
def login(usuario: str, senha: str):
    session = connect()
    
    #recupera todos usuarios com login esenha
    user = session.query(User).filter_by(user=usuario,senha=senha).all() #session.query(nome_da_tabela) + query_de_consulta + .all()
    
    #se len for igual a 0 não existe um usuario cadastrado
    if len(user) == 0:
        return {'status': 'usuario não existe'}
    
    while True:
        token = token_hex() #token_hex(quantidade_de_bytes) 2 caracteres representam 1byte
        token_existe = session.query(Tokens).filter_by(token=token).all()

        if len(token_existe) == 0:
            pessoa_existe = session.query(Tokens).filter_by(user_id=user[0].id).all()
            if len(pessoa_existe) == 0:
                novo_token = Tokens(user_id=user[0].id,token=token)
                session.add(novo_token)
            elif len(pessoa_existe) > 0:
                pessoa_existe[0].token = token

            session.commit()
        return token