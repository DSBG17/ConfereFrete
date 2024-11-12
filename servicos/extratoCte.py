import configparser
import pyodbc
import sys
import pandas as pd
import numpy as np

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
server = config['database']['server']
database = config['database']['database']
username = config['database']['username']
password = config['database']['password']

# String de conexão
connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'

# Função para extrair dados da tabela Cte
def extratogeral(cnpj):
    try:
        # Estabelecer conexão com o banco de dados
        conn = pyodbc.connect(connection_string)
        query = f"""SELECT transportadora,cnpj_transp,valorfre,valortotal,totalnf,pesonf,fretecalc,emissao,numerocte,porcnf 
        FROM Cte WHERE totalnf <> 0 AND cnpj_transp = '{cnpj}' """
        extrato = pd.read_sql(query, conn)
    #Criar duas colunas a mais no extrato ("Eu tenho que parar de inventar essas parada")
        extrato['% Conforme combinado'] = np.where (extrato['porcnf']<2.5,'Conforme','Verificar')
        return extrato
    except pyodbc.Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
    finally:
        if 'conn' in locals() and conn:
            conn.close()

def relatorio():
    # Definir CNPJs
    cnpjhpl = '12945197000110'
    dfhpl = extratogeral(cnpjhpl)

    cnpjhr = '28493959000125'
    dfhr = extratogeral(cnpjhr)

    cnpjnr = '32708094000144'
    dfnr = extratogeral(cnpjnr)

    cnpjrb = '19931010000179'
    dfrb = extratogeral(cnpjrb)

    cnpjtrz = '41596078000106'
    dftrz = extratogeral(cnpjtrz)

    # Salvar os dados no Excel
    with pd.ExcelWriter(r'Extrato/RelatorioEX1.xlsx', engine='xlsxwriter') as writer:
        # HelpLog
        dfhpl.to_excel(writer, sheet_name=f'Help Log', index=False)

        # HRExpress
        dfhr.to_excel(writer, sheet_name=f'HR', index=False)

        # NRExpress
        dfnr.to_excel(writer, sheet_name=f'NR', index=False)

        # Ribeiro
        dfrb.to_excel(writer, sheet_name=f'Ribeiro', index=False)

        # TRZ
        dftrz.to_excel(writer, sheet_name=f'TRZ', index=False)

        print('Dados extraídos com sucesso.')
        
        

        

# Chamando a função main apenas quando o script for executado diretamente
if __name__ == "__main__":
    relatorio()
