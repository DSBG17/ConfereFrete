import shutil
import os

def attdirnf():
    # Define os caminhos da origem e destino
    origem = r'F:/BI_COMPRAS/NFE_VENDAS/2024'
    destino = r'C:/Users/Davi Santos/Desktop/Conforme/dirxml/NFE'

    # Cria a pasta de destino, se ela não existir
    os.makedirs(destino, exist_ok=True)

    # Lista de pastas que não devem ser copiadas
    exclusoes = ['01', '02', '03','04','05','06','07','08','09']

    # Função para copiar com exclusão de itens
    for item in os.listdir(origem):
        # Verifica se o item está na lista de exclusão
        if item not in exclusoes:
            caminho_origem = os.path.join(origem, item)
            caminho_destino = os.path.join(destino, item)

            if os.path.isdir(caminho_origem):
                # Se for um diretório, copia recursivamente
                shutil.copytree(caminho_origem, caminho_destino, dirs_exist_ok=True)
            else:
                # Se for um arquivo, copia diretamente
                shutil.copy2(caminho_origem, caminho_destino)

if __name__ == "__main__":

# Chama a função
    attdirnf()
