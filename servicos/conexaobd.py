import pyodbc
import configparser
import sys


def conexao():
    # Carregar o arquivo config.ini
    config = configparser.ConfigParser()

    # Verifica se o arquivo config.ini foi carregado corretamente
    if not config.read('config.ini'):
        print("Arquivo config.ini não encontrado ou não pôde ser lido.")
        sys.exit()

    # Verifica se a seção 'database' está presente
    if 'database' not in config:
        print("Seção 'database' não encontrada em config.ini.")
        sys.exit()

    # Pegar as informações do arquivo config.ini
    try:
        server = config['database']['server']
        database = config['database']['database']
        username = config['database']['username']
        password = config['database']['password']
    except KeyError as e:
        print(f"Chave {e} não encontrada em config.ini.")
        sys.exit()

    # String de conexão
    connection_string = (
        f'DRIVER={{ODBC Driver 17 for SQL Server}};'
        f'SERVER={server};DATABASE={database};UID={username};PWD={password}'
    )

    try:
        # Usar o bloco with para gerenciar a conexão
        with pyodbc.connect(connection_string) as conn:
            print('Conexão efetuada')
    except pyodbc.Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
    

# Exemplo de uso
if __name__ == "__main__":
    conexao()
