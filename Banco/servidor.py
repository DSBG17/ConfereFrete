import pyodbc



class Conexaobanco():
    

    def __init__(self):
        self.servidor = 'SERVIDORFRETE'
        self.usuario = 'Mestre1'
        self.password = 'S-45678'
        self.database = 'Frete'
        self.cursor = None
        self.conexao = None
        self.drive = 'ODBC Driver 17 for SQL Server'
        
    def conecta(self,driver:str,server:str,database:str,user:str,password:str):

        try:
            conn = pyodbc.connect(
                f"DRIVER = {driver};"
                f"SERVER = {server};"
                f"DATABASE = {database};"
                f"USUARIO = {user};"
                f"PASSWORD = {password}"        
            )
            
            cursor= conn.cursor()
            
            self.conexao = conn
            self.cursor = cursor
                
            print('Conexão estabelecida com sucesso')
                
        except pyodbc.Error as e:
                print('Erro ao conectar ao banco de dados:', e)

    def select(self,tabela:str):
        query = f"SELECT * FROM {tabela}"
        
        return self.cursor.execute(query) 

    def update(self,coluna: str,tabela: str,codigo:str):
        query = f"""UPDATE {tabela}
                    SET {coluna}
                    WHERE {codigo}"""
        return self.cursor.execute(query)
    
    def count(self,coluna:str,tabela:str,codigo:str):
        query = f"""SELECT COUNT(*)
                    FROM {tabela}
                    WHERE {coluna} = '{codigo}' """
                    
        self.cursor.execute(query,(codigo))
        return  self.cursor.fetchone()[0]
    
    def where(self,tabela:str,coluna:str, condicao:str):
        query = f"""SELECT FROM {tabela}
                    WHERE {coluna} = {condicao}"""
        self.cursor.execute(query)
        return self.cursor.fetchall()