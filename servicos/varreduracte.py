import xmltodict
import os
from pathlib import Path
import pyodbc
import configparser

# Função para varrer o diretório de arquivos XML e carregá-los
def varreduracte():
    # Define o diretório onde os arquivos XML estão localizados
    diretorio = Path('dirxml/CTE')

    conteudos_xml = []
    # Lê todos os arquivos XML na pasta
    for root_dir, _, files in os.walk(diretorio):
        for arquivo in files:
            if arquivo.endswith(".xml"):
                caminho_completo = os.path.join(root_dir, arquivo)
                with open(caminho_completo, 'r', encoding='utf-8') as file:
                    xml_content = file.read()
                    conteudos_xml.append(xmltodict.parse(xml_content))

    # Extrai as informações necessárias de cada conteúdo XML
    resultados = [extrair_chaves_especificas(xml) for xml in conteudos_xml]
    return resultados

# Função para extrair tags específicas do dicionário
def extrair_chaves_especificas(dicionario):
    dados_extracao = {}
    
    try:
        # Acessa os dados sob a tag 'emit'
        Numerocte = dicionario['cteProc']['CTe']['infCte']['ide']['nCT']
        Emissao = dicionario['cteProc']['CTe']['infCte']['ide']['dhEmi']
        IE = dicionario['cteProc']['CTe']['infCte']['emit'].get('IE')
        CNPJ = dicionario['cteProc']['CTe']['infCte']['emit'].get('CNPJ')
        xNome = dicionario['cteProc']['CTe']['infCte']['emit'].get('xNome')
        inf_nfe = dicionario['cteProc']['CTe']['infCte']['infCTeNorm']['infDoc'].get('infNFe')
        Cidadedest = dicionario['cteProc']['CTe']['infCte'].get('receb', {}).get('enderReceb', {}).get('xMun')
        Estadodest = dicionario['cteProc']['CTe']['infCte'].get('receb', {}).get('enderReceb', {}).get('UF')
        Codibge = dicionario['cteProc']['CTe']['infCte'].get('receb', {}).get('enderReceb', {}).get('cMun')
        Valor = dicionario['cteProc']['CTe']['infCte']['infCTeNorm']['infCarga'].get('vCarga')
        
        # Verifica se 'Comp' é uma lista e extrai o 'vComp'
        ValorFrete = None
        comp_list = dicionario['cteProc']['CTe']['infCte']['vPrest'].get('Comp')
        if isinstance(comp_list, list):
            for comp in comp_list:
                if 'vComp' in comp:
                    ValorFrete = comp['vComp']  # Pega o valor do primeiro 'vComp'
                    break
        else:
            ValorFrete = comp_list.get('vComp') if comp_list else None
        
        # Lista para armazenar as chaves (caso haja mais de uma)
        chaves = []
        
        # Verifica se infNFe é uma lista (múltiplas notas) ou um único item
        if isinstance(inf_nfe, list):
            for nfe in inf_nfe:
                chaves.append(nfe['chave'])  # Adiciona cada chave à lista
        elif inf_nfe:
            chaves.append(inf_nfe['chave'])  # Adiciona a única chave
            
        # Teste para peso cubico
        pesocb = dicionario['cteProc']['CTe']['infCte']['infCTeNorm']['infCarga']['infQ']

        # Verifica se 'pesocb' é uma lista
        if isinstance(pesocb, list):
            # Pega o valor de 'qCarga' do último item da lista
            pesocubr = pesocb[-1].get('qCarga')
        else:
            # Caso seja um único item, pega o valor de 'qCarga'
            pesocubr = pesocb.get('qCarga')

        # Armazena os valores no dicionário de retorno
        dados_extracao['IE'] = IE
        dados_extracao['CNPJ'] = CNPJ
        dados_extracao['Transportadora'] = xNome
        dados_extracao['Cidadedest'] = Cidadedest
        dados_extracao['Estadodest'] = Estadodest
        dados_extracao['Cod_ibge'] = Codibge
        dados_extracao['Frete'] = ValorFrete
        dados_extracao['Valor total'] = Valor
        dados_extracao['Chave'] = chaves  # Aqui armazenamos a lista de chaves
        dados_extracao['Emissao'] = Emissao
        dados_extracao['Numerocte'] = Numerocte
        dados_extracao['Peso cubico'] = pesocubr

    except KeyError as e:
        print(f"Chave {e} não encontrada no dicionário.")
    
    return dados_extracao

# Função para enviar dados ao banco de dados
def enviar_para_banco(resultados):
    config = configparser.ConfigParser()

    # Verifica se o arquivo config.ini foi carregado corretamente
    if not config.read('../config.ini'):
        print("Arquivo config.ini não encontrado ou não pôde ser lido.")
        return

    # Verifica se a seção 'database' está presente
    if 'database' not in config:
        print("Seção 'database' não encontrada em config.ini.")
        return

    # Conexão com o banco de dados SQL Server
    server = config['database']['server']
    database = config['database']['database']
    username = config['database']['username']
    password = config['database']['password']

    connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'

    try:
        conn = pyodbc.connect(connection_string)
        print("Conexão com o banco de dados bem-sucedida!")

        cursor = conn.cursor()

        for resultado in resultados:
            numerocte = resultado.get('Numerocte')
            
            # Verifica se o numerocte já existe no banco
            cursor.execute("SELECT COUNT(1) FROM Cte WHERE numerocte = ?", numerocte)
            existe = cursor.fetchone()[0]

            if existe:
                print(f"CTe com numerocte {numerocte} já existe no banco. Ignorando inserção.")
                continue

            # Verifica se todos os dados necessários estão presentes
            if not all(key in resultado for key in ['Transportadora', 'CNPJ', 'IE', 'Cod_ibge', 'Cidadedest', 'Estadodest', 'Frete', 'Valor total']):
                print(f"Dados faltando para inserir: {resultado}")
                continue

            print(f"Preparando para inserir: {resultado}")  # Print para depuração
            try:
                cursor.execute(""" 
                    INSERT INTO Cte (
                        transportadora, cnpj_transp, ie_transp, codibge, cidade_dest, estado_dest, valorfre, valortotal, emissao, numerocte
                    ) OUTPUT INSERTED.id
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, 
                resultado['Transportadora'],
                resultado['CNPJ'],
                resultado['IE'],
                resultado['Cod_ibge'],
                resultado['Cidadedest'],
                resultado['Estadodest'],
                resultado['Frete'],
                resultado['Valor total'],
                resultado['Emissao'],
                resultado['Numerocte']
                )

                # Obtendo o ID gerado pelo INSERT
                cte_id = cursor.fetchone()

                if cte_id is None:
                    print(f"Erro: Não foi possível inserir o registro no Cte para o arquivo. cte_id é NULL.")
                    continue

                cte_id = cte_id[0]

                # Inserindo as chaves na tabela ChavesCte usando o cte_id
                for chave in resultado['Chave']:
                    peso = resultado ['Peso cubico']
                    cursor.execute(""" INSERT INTO chavecte (id, chave_nf, pesocubico) VALUES (?, ?, ?) """, (cte_id, chave, peso))

            except pyodbc.Error as e:
                print(f"Erro ao inserir dados: {e}")
        
        
        #Regiao TransLuz
                
        update_query = ("""
            UPDATE Cte
            SET regiao = todasregiao.regiao
            FROM Cte
            INNER JOIN todasregiao ON Cte.codibge = todasregiao.cod_ibge
            WHERE Cte.cnpj_transp = '41596078000106';
            """)
                
        cursor.execute(update_query)
        
        #Regiao NR
                
        update_query = ("""
            UPDATE Cte
            SET regiao = regiaonr.regiao
            FROM Cte
            INNER JOIN regiaonr ON Cte.codibge = regiaonr.codIbge
            WHERE Cte.cnpj_transp = '32708094000144';
            """)
                
        cursor.execute(update_query)
        
        
        


        # Commit das mudanças
        conn.commit()
        print("Dados inseridos com sucesso!")

    except pyodbc.Error as e:
        print("Erro ao conectar ou inserir no banco de dados:")
        print(e)

    finally:
        # Feche o cursor e a conexão
        cursor.close()
        conn.close()
        print("Conexão fechada.")

if __name__ == "__main__":
    # Extrai as chaves desejadas de cada arquivo XML
    resultados = varreduracte()

    # Adiciona os resultados ao banco de dados
    enviar_para_banco(resultados)
