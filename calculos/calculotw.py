import pyodbc
import configparser

def twtransporte():
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
        WHERE cnpj_transp = '89317697004472'
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
                peso
                freteum = 26.54 #Até 5kg
                fretedois = 28.34 #De 6 a 10KG
                fretetres = 29.98 #De 11 a 20KG
                fretequatro = 31.20 #De 21 a 30KG
                fretecinco = 33.72 #De 31 a 50KG
                freteseis = 37.67 #De 51 a 70KG
                fretesete = 48.97 #De 71 a 100KG
                pesoex = 0.49044
               
                    
                if peso > 100:
                    pesoextra = peso - 100
                    pesocobrado = pesoextra * pesoex
                        
                else:
                    pesoextra = 0
                    
                       
                #
                    if peso <5:
                        fretecobrado = round(freteum, 2)
                    elif  6 <= peso <11:
                        fretecobrado = round(fretedois, 2)
                    elif 11 <= peso <21:
                        fretecobrado = round(fretetres, 2)
                    elif 21 <= peso <31:
                        fretecobrado = round(fretequatro, 2)
                    elif 31 <= peso <51:
                        fretecobrado = round(fretecinco, 2)
                    elif 51 <= peso <71:
                        fretecobrado = round(freteseis, 2)
                    elif peso >100:
                        fretecobrado = round(fretesete + pesocobrado, 2)
                    else:
                        fretecobrado = 0
                        
              
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
                print('Frete calculado: ',fretecobrado)
                print('************************************')
                

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

# Chama a função
twtransporte()
