import configparser
import pyodbc
import sys
import pandas as pd

config = configparser.ConfigParser()

    # Verifica se o arquivo config.ini foi carregado corretamente
if not config.read('config.ini'):
        print("Arquivo config.ini não encontrado ou não pôde ser lido.")
        sys.exit()

    # Verifica se a seção 'database' está presente
if 'database' not in config:
        print("Seção 'database' não encontrada em config.ini.")
        sys.exit()



server = config['database']['server']
database = config['database']['database']
username = config['database']['username']
password = config['database']['password']

connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'

try:
    conn = pyodbc.connect(connection_string)
    
    def extratoTRZ():
        conn = pyodbc.connect(connection_string)
        print("Conexão com o banco de dados bem-sucedida!")

        
        
       
        query = "SELECT*FROM Cte WHERE cnpj_transp = '41596078000106'"
        TRZ = pd.read_sql(query, conn)
        
        TRZ.to_excel(r'TRZ/Relatorio atual TRZ.xlsx', index=False)
        

        print(TRZ)
        
        extratoTRZ()   
        
    def extratoHELP():
        conn = pyodbc.connect(connection_string)
        print("Conexão com o banco de dados bem-sucedida!")

        
        
       
        query = "SELECT*FROM Cte WHERE cnpj_transp = '12945197000110'"
        MOTOLOG = pd.read_sql(query, conn)
        
        MOTOLOG.to_excel(r'TRZ/Relatorio atual ML.xlsx', index=False)
        

        print(MOTOLOG)
        
        extratoHELP()
        
    def extratoHELP():
        conn = pyodbc.connect(connection_string)
        print("Conexão com o banco de dados bem-sucedida!")

        
        
       
        query = "SELECT*FROM Cte WHERE cnpj_transp = '32708094000144'"
        NRE = pd.read_sql(query, conn)
        
        NRE.to_excel(r'TRZ/Relatorio atual NRE.xlsx', index=False)
        

        print(NRE)
        
        extratoHELP()
        
        
        
except pyodbc.Error as e:
    print(f"Erro ao conectar ao banco: {e}")
    
finally:
    if 'conn' in locals() and conn:
        conn.close()
        print('Conexão encerrada')