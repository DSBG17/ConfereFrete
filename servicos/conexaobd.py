import pyodbc
import configparser
import sys


def conexao():
    config = configparser.ConfigParser()

    # Verifica se o arquivo config.ini foi carregado corretamente
    if not config.read('config.ini'):
        print("Arquivo config.ini não encontrado ou não pôde ser lido.")
        return

    # Verifica se a seção 'database' está presente
    if 'database' not in config:
        print("Seção 'database' não encontrada em config.ini.")
        return

    server = config['database']['server']
    database = config['database']['database']
    username = config['database']['username']
    password = config['database']['password']

    connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'

 # Cria a conexão
    print("Tentando conectar ao banco de dados...")
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()
    print("Conexão bem-sucedida.")