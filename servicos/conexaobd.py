"""Um arquivo para criar uma conexão ao banco, para pode utilizar em todos os arquivos como class,
ficando um codigo mais limpo"""
import configparser
import pyodbc


class conection_:
    def __init__(self, config_file='../config.ini'):

        self.config = configparser.ConfigParser()
        self.config.read(config_file)

        self.server = self.config.get('database', 'server')
        self.database = self.config.get('database', 'database')
        self.username = self.config.get('database', 'username')
        self.password = self.config.get('database', 'password')
        self.driver = self.config.get('database', 'driver', fallback="{ODBC Driver 17 for SQL Server}")

        self.connection = None

    def conexao(self):
        try:
            self.connection = pyodbc.connect(
                f'DRIVER = {self.driver};'
                f'SERVER = {self.server};'
                f'DATABASE = {self.database};'
                f'UID = {self.username};'
                f'PWD = {self.password};'
                'timeout=30'
            )
            print('Conexão bem sucedida !')
        except pyodbc.Error as e:
            print(f'Erro ao conectar ao banco de dados: {e}')

    """def disconnect(self):
        if self.connection:
            self.connection.close()
            print('Conexão fechada.')
        else:
            print('Nenhuma conexão ativa para fechar.')

    def execute_query(self, query, params=None):

        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params or ())
            results = cursor.fetchall()
            return results
        except pyodbc.Error as e:
            print(f'Erro ao executar consulta: {e}')
            return None"""
