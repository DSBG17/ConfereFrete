"""Um arquivo para criar uma conexão ao banco, para pode utilizar em todos os arquivos como class,
ficando um codigo mais limpo"""
import configparser
import pyodbc


def conexaobanco():
    config = configparser.ConfigParser()
    config.read('../config.ini')
    
    server = config['database']['server']
    database = config['database']['database']
    username = config['database']['username']
    password = config['database']['password']



    
    conn_string = (
        #f"DRIVER = {{ODBC Driver 18 for SQL Server}};"
        f"SERVER = {server};"
        f"DATABASE = {database};"
        f"UID = {username};"
        f"PWD = {password};"
    )



    try:
        conn = pyodbc.connect(conn_string)
        print('Conexão bem-sucedida')

        print(f"Server: {server}")
        print(f"Database: {database}")
        print(f"Username: {username}")
        print(f"Password: {password}")

    except pyodbc.Error as e:
        print('Erro ao conectar', e)


conexaobanco()