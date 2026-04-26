import os, time, csv, logging
from collections import defaultdict
from dotenv import load_dotenv
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Date, DateTime, insert, text
from datetime import datetime
from functools import wraps

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format= '%(asctime)s - %(message)s',
    handlers=[
        logging.FileHandler("excucao.log"),
        logging.StreamHandler()
    ]
)

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL, echo=False)
metadata = MetaData()


def medir_tempo(func):
    """Decorator que mede o tempo de execução de uma função."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        inicio = time.perf_counter()  # tempo inicial (mais preciso que time.time)
        resultado = func(*args, **kwargs)
        fim = time.perf_counter()     # tempo final
        duracao = fim - inicio
        print(f"Função '{func.__name__}' executada em {duracao:.6f} segundos.")
        return resultado
    return wrapper


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


@medir_tempo
# CSV anuais com os dados anonimizados
def csv_anual_oculto():

    registros_por_ano = defaultdict(list) #dicionário para armazenar os registros agrupados por ano de nascimento
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM usuarios;")) #seleciona todos os registros da tabela usuarios
        

        #percorre os registros, anonimiza os dados e agrupa por ano de nascimento
        for row in result:
            row_anonimizado = LGPD(row)
            campo_data = row[5]
            try: #tenta extrair o ano diretamente do campo_data, caso seja um objeto datetime
                ano = campo_data.year
            except AttributeError: #caso o campo_data seja uma string, converte para datetime e extrai o ano
                ano = datetime.strptime(campo_data, "%Y-%m-%d").year
            registros_por_ano[ano].append(row_anonimizado)
    
    #gera um arquivo CSV para cada ano de nascimento, contendo os registros anonimizados correspondentes
    for ano, dados in registros_por_ano.items():
        nome_arquivo = f'{ano}.csv'
        try: #tenta criar o arquivo CSV e escrever os dados anonimizados
            with open(nome_arquivo, mode = 'w', newline='', encoding='utf-8') as f:
                escritor = csv.writer(f)
                escritor.writerow(['id', 'nome', 'cpf', 'email', 'telefone', 'data_nascimento', 'created_on', 'updated_on'])
                escritor.writerows(dados)
            print(f"Sucesso: Arquivo '{nome_arquivo}' criado com {len(dados)} registros.")
        except Exception as e: 
            print(f"Erro ao criar arquivo '{nome_arquivo}': {e}")


# CSV geral com os dados limpos (nome e CPF)
@medir_tempo
def csv_geral():
    nome_arquivo = 'todos.csv'

    try: #tenta criar o arquivo CSV e escrever os dados nome e CPF
        with engine.connect() as conn:
            query = text("SELECT nome, cpf FROM usuarios;") #consulta SQL para selecionar apenas os campos nome e CPF da tabela usuarios
            result = conn.execute(query)
            
            with open(nome_arquivo, mode='w', newline="", encoding='utf-8') as f:
                escritor = csv.writer(f)
                escritor.writerow(['nome', 'cpf'])
                for row in result:
                    escritor.writerow([row.nome, row.cpf])
            
            print(f"Sucesso: Arquivo '{nome_arquivo}' criado com os dados nome e CPF.")

    except Exception as e:
        print(f"Erro ao criar arquivo '{nome_arquivo}': {e}")


users = []
with engine.connect() as conn:
    result = conn.execute(text("SELECT * FROM usuarios LIMIT 5;"))
    for row in result:
        row = LGPD(row)
        users.append(row)

for user in users:
    print(user)

if __name__ == "__main__":
    logging.info("Início da execução do script.")
    csv_anual_oculto()
    csv_geral()
    logging.info("Fim da execução do script.")