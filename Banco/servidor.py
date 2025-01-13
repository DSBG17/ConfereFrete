import pyodbc
import configparser


class Conexaobanco:
    
    config = configparser.ConfigParser()
    
        # Verifica se o arquivo config.ini foi carregado corretamente
    if not config.read('config.ini'):
        print("Arquivo config.ini não encontrado ou não pôde ser lido.")
        

    # Verifica se a seção 'database' está presente
    if 'database' not in config:
        print("Seção 'database' não encontrada em config.ini.")
        

    server = config['database']['server']
    database = config['database']['database']
    username = config['database']['username']
    password = config['database']['password']
    
    def __init__(self,servidor=server,usuario=username, password=password,database=database):
        self.servidor = servidor
        self.usuario = usuario
        self.password = password
        self.database = database
        self.cursor = None
        self.conexao = None
        self.drive = 'ODBC Driver 17 for SQL Server'
        
        def conecta(self):

            try:
                self.conexao = pyodbc.connect(
                    f"DRIVER = {self.drive};"
                    f"SERVER = {self.servidor};"
                    f"DATABASE = {self.database};"
                    f"USUARIO = {self.usuario};"
                    f"PASSWORD = {self.password}"        
                )
                self.cursor = self.conexao.cursor()
                
                print('Conexão estabelecida com sucesso')
                
            except pyodbc.Error as e:
                print('Erro ao conectar ao banco de dados:', e)

            