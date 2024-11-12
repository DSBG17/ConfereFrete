import pyodbc
import configparser

def transluz():
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

    # String de conexão
    connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'
    
    try:
        # Cria a conexão
        print("Tentando conectar ao banco de dados...")
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()
        print("Conexão bem-sucedida.")
        
        # Primeira consulta
        querytrz = """
        SELECT id, transportadora, cnpj_transp, cidade_dest, estado_dest, regiao,totalnf,pesonf,valorfre
        FROM Cte
        WHERE cnpj_transp = '41596078000106'
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
                regiao = row[5] #regiao
                valor = row[6] #valornf
                peso = row[7] #peso
                frete = row[8] #frete                
                #Aqui começa os calculos de frete
                
                if regiao == 'REGIAO 1 - ITAPIRA':
                    fretemin = 22.01
                    pesoex = peso - 50.00
                    valorex = float ( pesoex * 0.30)
                    if pesoex <= 0:
                        pesoex = 0
                        valort = round(valor * 0.015,2)
                    else:
                        valort = round(valor * 0.015 + valorex,2)
                    if valort <= fretemin:
                        if pesoex <= 0:
                            pesoex = 0
                            valort = fretemin
                        else:
                            valort = fretemin + valorex
                        
                elif regiao == 'REGIAO 2 - BRAGANCA PAULISTA':
                    fretemin = 22.01
                    pesoex = peso - 50.00
                    valorex = float ( pesoex * 0.30)
                    if pesoex <= 0:
                        pesoex = 0
                        valort = round(valor * 0.015,2)
                    else:
                        valort = round(valor * 0.015 + valorex,2)
                    if valort <= fretemin:
                        if pesoex <= 0:
                            pesoex = 0
                            valort = fretemin
                        else:
                            valort = fretemin + valorex
                        
                elif regiao == 'REGIAO 3 - RIBEIRAO PRETO':
                    fretemin = 43.20
                    pesoex = peso - 50.00
                    valorex = float ( pesoex * 0.30)
                    fretemin = 43.20
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
                        
                elif regiao == 'REGIAO 4 - PIRACICABA':
                    fretemin = 22.01
                    pesoex = peso - 50.00
                    valorex = float ( pesoex * 0.30)
                    if pesoex <= 0:
                        pesoex = 0
                        valort = round(valor * 0.015,2)
                    else:
                        valort = round(valor * 0.015 + valorex,2)
                    if valort <= fretemin:
                        if pesoex <= 0:
                            pesoex = 0
                            valort = fretemin
                        else:
                            valort = fretemin + valorex
                        
                elif regiao == 'REGIAO 5 - CAMPINAS SP':
                    fretemin = 14.25
                    pesoex = peso - 50.00
                    valorex = float ( pesoex * 0.30)
                    if pesoex <= 0:
                        pesoex = 0
                        valort = round(valor * 0.013,2)
                    else:
                        valort = round(valor * 0.013 + valorex,2)
                    if valort <= fretemin:
                        if pesoex <= 0:
                            pesoex = 0
                            valort = fretemin
                        else:
                            valort = fretemin + valorex
                        
                elif regiao == 'REGIAO 6 - SOROCABA':
                    fretemin = 22.01
                    pesoex = peso - 50.00
                    valorex = float ( pesoex * 0.30)
                    if pesoex <= 0:
                        pesoex = 0
                        valort = round(valor * 0.015,2)
                    else:
                        valort = round(valor * 0.015 + valorex,2)
                    if valort <= fretemin:
                        if pesoex <= 0:
                            pesoex = 0
                            valort = fretemin
                        else:
                            valort = fretemin + valorex
                        
                elif regiao == 'REGIAO 7 - ITAPETININGA':
                    fretemin = 29.77
                    pesoex = peso - 50.00
                    valorex = float ( pesoex * 0.30)
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
                        
                elif regiao == 'REGIAO 8 - ABC / SAO PAULO / INTERIOR':
                    pesoex = peso - 50.00
                    valorex = float ( pesoex * 0.30)
                    fretemin = 38.50
                    if pesoex <= 0:
                        pesoex = 0
                        valort = round(valor * 0.015,2)
                    else:
                        valort = round(valor * 0.015  + valorex,2)
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
                print('Região: ',regiao)
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
                WHERE totalnf > 0 AND cnpj_transp = '41596078000106'

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
    transluz()
