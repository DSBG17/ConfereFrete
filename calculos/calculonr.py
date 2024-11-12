import pyodbc
import configparser

def nrexpress():
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
        SELECT id, transportadora, cnpj_transp, cidade_dest, estado_dest, regiao, valorfre
        FROM Cte
        WHERE cnpj_transp = '32708094000144'
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
                cidade = row[3]  # cidade_dest
                estado = row[4]  # estado_dest
                regiao = row[5]  # regiao
                valor = row[6]  # valorfre
                
                # Consulta para buscar pesocubico na tabela chavecte
                query_chaves = """
                    SELECT pesocubico
                    FROM chavecte
                    WHERE id = ?
                """

                print(f'Executando consulta na tabela chavecte para id {id}...')
                cursor.execute(query_chaves, id)

                rows_peso = cursor.fetchall()

                if rows_peso:
                    pesocub = rows_peso[0][0]  # Acessa pesocubico
                    
                    
                    
                #Efetuar os calculos Primeira região
                
                if regiao == 'SP Metropolitana':
                    freteum = 40.00
                    fretedois = 48.00
                    fretetres = 72.00
                    pesoex = 0.75
                    pesocub
                    
                    if pesocub > 100:
                        pesoextra = pesocub - 100
                        pesocobrado = pesoextra * pesoex
                        
                    else:
                        pesoextra = 0
                    
                       
                #
                    if pesocub <30:
                        fretecobrado = round(freteum, 2)
                    elif  31 <= pesocub <71:
                        fretecobrado = round(fretedois, 2)
                    elif 71 <= pesocub <101:
                        fretecobrado = round(fretetres, 2)
                    elif pesocub >100:
                        fretecobrado = round(fretetres + pesocobrado, 2)
                    else:
                        fretecobrado = 0
                        
                        
                    # Segunda região
                    
                if regiao == 'SP Interior':
                    freteum = 58.00
                    fretedois = 58.00
                    fretetres = 95.00
                    pesoex = 1.10
                    pesocub
                    
                    if pesocub > 100:
                        pesoextra = pesocub - 100
                        pesocobrado = pesoextra * pesoex
                        
                    else:
                        pesoextra = 0
                    
                       
                #
                    if pesocub <30:
                        fretecobrado = round(freteum, 2)
                    elif  31 <= pesocub <71:
                        fretecobrado = round(fretedois, 2)
                    elif 71 <= pesocub <101:
                        fretecobrado = round(fretetres, 2)
                    elif pesocub >100:
                        fretecobrado = round(fretetres + pesocobrado, 2)
                    else:
                        fretecobrado = 0
                        
                # Terceira região
                    
                if regiao == 'CPS Regiao':
                    freteum = 42.00
                    fretedois = 50.00
                    fretetres = 75.00
                    pesoex = 0.75
                    pesocub
                    
                    if pesocub > 100:
                        pesoextra = pesocub - 100
                        pesocobrado = pesoextra * pesoex
                        
                    else:
                        pesoextra = 0
                    
                       
                #
                    if pesocub <30:
                        fretecobrado = round(freteum, 2)
                    elif  31 <= pesocub <71:
                        fretecobrado = round(fretedois, 2)
                    elif 71 <= pesocub <101:
                        fretecobrado = round(fretetres, 2)
                    elif pesocub >100:
                        fretecobrado = round(fretetres + pesocobrado, 2)
                    else:
                        fretecobrado = 0
                    

                  

                    # Exibe resultados
                    print('ID:', id)    
                    print('Transportadora:', transportadora)
                    print('CNPJ:', cnpj)
                    print('Cidade:', cidade)
                    print('Estado:', estado)
                    print('Região:', regiao)
                    print('Valor Frete:', valor)
                    print('Peso cúbico:', pesocub)
                    print('Frete calculado:', fretecobrado)
                    print('************************************')
                    
                    
                # Enviar para o banco
                update_query = """
                UPDATE Cte
                SET fretecalc = ?
                WHERE id = ?
                """
                cursor.execute(update_query, fretecobrado, id)
                
                update_query = """
                UPDATE Cte
                SET porcnf = ROUND ((valorfre / totalnf)*100,2)
                WHERE totalnf > 0 AND cnpj_transp = '32708094000144'

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
    nrexpress()
