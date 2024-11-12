import xmltodict
import os
from pathlib import Path
import shutil
import pyodbc
import configparser


def varreduranf():
    # Define o diretório onde os arquivos XML estão localizados
    diretorio = Path('dirxml/NFE')
    diretorio_invalidos = Path('dirxml/erros_nf')

    # Cria a pasta 'erros_nf' caso ela não exista
    diretorio_invalidos.mkdir(parents=True, exist_ok=True)

    conteudos_xml = []
    #arquivos_validos = []

    # Lê todos os arquivos XML na pasta
    for root_dir, _, files in os.walk(diretorio):
        for arquivo in files:
            if arquivo.endswith(".xml"):
                caminho_completo = os.path.join(root_dir, arquivo)
                with open(caminho_completo, 'r', encoding='utf-8') as file:
                    xml_content = file.read()
                    try:
                        conteudo = xmltodict.parse(xml_content)
                        conteudos_xml.append((caminho_completo, conteudo))
                    except Exception as e:
                        print(f"Erro ao ler o arquivo XML {arquivo}: {e}")
                        continue  
    return conteudos_xml


# Função para extrair tags específicas do dicionário
def extrair_chaves_especificas(dicionario):
    dados_extracao = {}

    try:
        # Tenta extrair as tags do dicionário XML
        NumeroNF = dicionario['nfeProc']['NFe']['infNFe']['ide']['nNF']
        transp = dicionario['nfeProc']['NFe']['infNFe']['transp']
        emissao = dicionario['nfeProc']['NFe']['infNFe']['ide']['dhEmi']

        if transp and 'transporta' in transp and transp['transporta']:
            Transportadora = transp['transporta']['xNome']
            CNPJ = transp['transporta']['CNPJ']
        else:
            Transportadora = 'None'
            CNPJ = 'None'

        Cidadedest = dicionario['nfeProc']['NFe']['infNFe']['dest']['enderDest']['xMun']
        Estadodest = dicionario['nfeProc']['NFe']['infNFe']['dest']['enderDest']['UF']
        Codigoibge = dicionario['nfeProc']['NFe']['infNFe']['dest']['enderDest']['cMun']

        PesoB = 0
        vol = dicionario['nfeProc']['NFe']['infNFe']['transp']['vol']
        if isinstance(vol, list):
            PesoB = sum(float(volume['pesoB']) for volume in vol)
        else:
            PesoB = float(vol['pesoB'])

        ValorNF = 0
        detPag = dicionario['nfeProc']['NFe']['infNFe']['pag']['detPag']
        if isinstance(detPag, list):
            for pag in detPag:
                ValorNF += float(pag['vPag'])
        else:
            ValorNF = float(detPag['vPag'])

        Chave = dicionario['nfeProc']['protNFe']['infProt']['chNFe']

        # Prepara os dados extraídos
        dados_extracao['Numero da NFe'] = NumeroNF
        dados_extracao['Transportadora'] = Transportadora
        dados_extracao['CNPJ'] = CNPJ
        dados_extracao['Cidade de destino'] = Cidadedest
        dados_extracao['Estado de destino'] = Estadodest
        dados_extracao['Codigo IBGE'] = Codigoibge
        dados_extracao['Peso Bruto'] = PesoB
        dados_extracao['Valor da NFe'] = ValorNF
        dados_extracao['Chave da NFe'] = Chave
        dados_extracao['Emissão'] = emissao
        

    except KeyError as e:
        print(f"Chave {e} não encontrada no dicionário.")
        dados_extracao = 0  # Retorna 0 se faltar alguma tag

    return dados_extracao


# Função para enviar os dados para o banco de dados
def enviar_para_banco(resultadosnf):
    config = configparser.ConfigParser()

    # Verifica se o arquivo config.ini foi carregado corretamente
    if not config.read('config.ini'):
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

        for resultado in resultadosnf:
            # Verifica se o Número da NF já existe no banco de dados
            cursor.execute("SELECT COUNT(*) FROM Nfe WHERE numeronf = ?", resultado['Numero da NFe'])
            row = cursor.fetchone()

            if row[0] > 0:
                print(f"Nota Fiscal {resultado['Numero da NFe']} já existe no banco. Pulando inserção.")
                continue  # Pula para o próximo registro se a NF já existir

            # Verificando se já existe uma chave na tabela chavecte
            cursor.execute("SELECT id, COUNT(*) FROM chavecte WHERE chave_nf = ? GROUP BY id", resultado['Chave da NFe'])
            row_chavecte = cursor.fetchone()

            if row_chavecte and row_chavecte[1] > 0:
                id_chavecte = row_chavecte[0]
                # Atualizando os dados na tabela chavecte
                cursor.execute("""
                    UPDATE chavecte 
                    SET valornf = ?, peso = ?
                    WHERE chave_nf = ?
                """, (resultado['Valor da NFe'], resultado['Peso Bruto'], resultado['Chave da NFe']))

                # Inserir os dados na tabela Nfe com o mesmo id
                cursor.execute(""" 
                    INSERT INTO Nfe (
                        id, transportadora_nf, cnpj_transp_nf, cod_ibge, cidade_dest_nf, estado_dest_nf,
                        chaveda_nf, numeronf, emissao
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, id_chavecte,
                resultado['Transportadora'],
                resultado['CNPJ'],
                resultado['Codigo IBGE'],
                resultado['Cidade de destino'],
                resultado['Estado de destino'],
                resultado['Chave da NFe'],
                resultado['Numero da NFe'],
                resultado['Emissão'])
                
               

            else:
                # Inserindo os dados na tabela chavecte e gerando um novo id
                cursor.execute(""" 
                    INSERT INTO chavecte (chave_nf, valornf, peso) OUTPUT INSERTED.id VALUES (?, ?, ?)
                """, (resultado['Chave da NFe'], resultado['Valor da NFe'], resultado['Peso Bruto']))
                id_gerado = cursor.fetchone()[0]

                # Inserindo os dados na tabela Nfe com o id gerado
                cursor.execute(""" 
                    INSERT INTO Nfe (
                        id, transportadora_nf, cnpj_transp_nf, cod_ibge, cidade_dest_nf, estado_dest_nf,
                        chaveda_nf, numeronf, emissao
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, id_gerado,
                resultado['Transportadora'],
                resultado['CNPJ'],
                resultado['Codigo IBGE'],
                resultado['Cidade de destino'],
                resultado['Estado de destino'],
                resultado['Chave da NFe'],
                resultado['Numero da NFe'],
                resultado['Emissão'])

        # Salvar as alterações no banco
        conn.commit()

        

        

    except Exception as e:
        print(f"Erro ao enviar para o banco de dados: {e}")
        
        


    finally:
        if 'conn' in locals():
            conn.close()

    

# Código que será executado apenas quando o arquivo for executado diretamente
if __name__ == "__main__":
    # Extrai dados de todos os conteúdos XML e separa os inválidos
    conteudos_xml = varreduranf()
    resultadosnf = []
    diretorio_invalidos = Path('dirxml/erros_nf')

    for caminho_arquivo, conteudo in conteudos_xml:
        resultado = extrair_chaves_especificas(conteudo)

        if resultado:  # Se o resultado não for None
            # Adiciona à lista de arquivos válidos
            resultadosnf.append(resultado)
        else:
            # Se resultado for None, move o arquivo para a pasta 'erros_nf'
            arquivo_destino = diretorio_invalidos / Path(caminho_arquivo).name
            shutil.move(caminho_arquivo, arquivo_destino)
            print(f"Arquivo {caminho_arquivo} movido para {arquivo_destino} por falta de tags.")

    # Exibe os dados extraídos dos arquivos válidos
    print("Dados extraídos dos arquivos válidos: ")
    for resultado in resultadosnf:
        print(resultado)

    # Envia os resultados válidos para o banco de dados
    
    
    
    enviar_para_banco(resultadosnf)


