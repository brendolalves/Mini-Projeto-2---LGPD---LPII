import os, time, csv
from dotenv import load_dotenv
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Date, DateTime, insert, text
from datetime import datetime
from functools import wraps

load_dotenv()



DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")


def medir_tempo(func):
    """Decorator que mede o tempo de execução de uma função."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        inicio = time.perf_counter()  # tempo inicial (mais preciso que time.time)
        resultado = func(*args, **kwargs)
        fim = time.perf_counter()     # tempo final
        duracao = fim - inicio
        print(f"⏱ Função '{func.__name__}' executada em {duracao:.6f} segundos.")
        return resultado
    return wrapper

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL, echo=False)
metadata = MetaData()

usuarios = Table(
    'usuarios', metadata,
    Column('id', Integer, primary_key=True),
    Column('nome', String(50), nullable=False, index=True),
    Column('cpf', String(14), nullable=False),
    Column('email', String(100), nullable=False, unique=True),
    Column('telefone', String(20), nullable=False),
    Column('data_nascimento', Date, nullable=False),
    Column('created_on', DateTime(), default=datetime.now),
    Column('updated_on', DateTime(), default=datetime.now, onupdate=datetime.now)
)

metadata.create_all(engine)

@medir_tempo
def LGPD(row):
    row_list = list(row) #converte a tupla em lista para permitir modificações

    # mascarar o nome, mantendo a primeira letra e o sobrenome
    nome_completo = row_list[1].split()
    primeira_letra= nome_completo[0][0] if nome_completo else ""
    primeiro_nome = nome_completo[0] 
    sobrenome = " ".join(nome_completo[1:]) if len(nome_completo) > 1 else ""
    row_list[1] = primeira_letra + ("*" * (len(primeiro_nome) - 1)) + (" " + sobrenome if sobrenome else "")

    # mascarar o CPF, mantendo os 4 primeiros dígitos e substituindo os demais por asteriscos
    row_list[2] = row_list[2][:4] +"***.***-**"

    # mascrar o email, ocutando o prefixo, mantendo apenas a primeira letra e o domínio
    email = row_list[3]
    prefixo, dominio = email.split("@")
    row_list[3] = prefixo[0] + ("*" * (len(prefixo) - 1)) + "@" + dominio

    # ocultar os dígitos do telefone, mantendo apenas os 4 últimos dígitos
    row_list[4] = row_list[4][-4:]

    return tuple(row_list)


users = []
with engine.connect() as conn:
    result = conn.execute(text("SELECT * FROM usuarios LIMIT 5;"))
    for row in result:
        row = LGPD(row)
        users.append(row)

for user in users:
    print(user)
