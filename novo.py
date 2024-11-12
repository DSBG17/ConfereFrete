from bs4 import BeautifulSoup
from pathlib import Path



with open('dirxml/TESTE/testeum.xml', 'r') as file:
    soupe = BeautifulSoup(file,'xml')
    
transportadora = soupe.find_all('emit')

for emit in transportadora:
    transp = emit.find('xNome')
    if transp:
        print(transp.text)
    else:
        print('Não encontrada')
    
    
    cnpj= emit.find('CNPJ')
    
    if cnpj:
        print(cnpj.text)
    else:
        print('Não encontrada')
    

