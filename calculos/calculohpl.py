import pyodbc
import configparser


def motohelp():
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

    try:
        # Cria a conexão
        print("Tentando conectar ao banco de dados...")
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()
        print("Conexão bem-sucedida.")
        
        # Primeira consulta
        querytrz = """
        SELECT id, transportadora, cnpj_transp, cidade_dest, estado_dest,totalnf,pesonf,valorfre
        FROM Cte
        WHERE cnpj_transp = '12945197000110'
        """
        
        print('Executando consulta...')
        cursor.execute(querytrz)
        
        rows = cursor.fetchall()
        
        if rows:
            for row in rows:
                # Acessa os valores por índice ou nome das colunas
                id = row[0]  # id
                transportadora = row[1]  # transportadora
                cnpj = row[2]  # cnpj_transp
                cidade = row[3] # cidade_dest
                estado = row[4] # estado_dest
                valor = row[5] #valornf
                peso = row[6] #peso
                frete = row[7] #frete                
                #Aqui começa os calculos de frete
                

                fretemin = 25.00
                pesoex = peso - 100.00
                valorex = float ( pesoex * 0.80)
                if pesoex <= 0:
                        pesoex = 0
                        valort = round(valor * 0.010,2)
                else:
                        valort = round(valor * 0.010 + valorex,2)
                if valort <= fretemin:
                        if pesoex <= 0:
                            pesoex = 0
                            valort = fretemin
                        else:
                            valort = fretemin + valorex
                        
                
                #Limite
                print('ID: ',id)    
                print('Transportadora: ',transportadora)
                print('CNPJ: ',cnpj)
                print('Cidade: ',cidade)
                print('Estado: ',estado)
                print('Valor total das NF''s'': ',valor)
                print('Peso total das NF''s'': ',peso)
                print('Frete Cte: ',frete)
                print('Frete calculado: ',valort)
                print('************************************')
                
                # Enviar para o banco
                update_query = """
                UPDATE Cte
                SET fretecalc = ?
                WHERE id = ?
                """
                cursor.execute(update_query, valort, id)
                
                update_query = """
                UPDATE Cte
                SET porcnf = ROUND ((valorfre / totalnf)*100,2)
                WHERE totalnf > 0 AND cnpj_transp = '12945197000110'

                """
                cursor.execute(update_query)

            # Confirma as alterações no banco
            conn.commit()
            print("Atualizações salvas com sucesso.")

        else:
            print("Nenhum resultado encontrado.")
            
    except Exception as e:
        print(f"Erro na conexão ou execução da consulta: {e}")
    
    finally:
        # Garante que a conexão será fechada
        if 'conn' in locals():
            conn.close()
            print("Conexão fechada.")

if __name__ == "__main__":

    motohelp()
