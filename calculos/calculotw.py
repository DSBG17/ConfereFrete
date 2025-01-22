from Banco.servidor import Conexaobanco

banco = Conexaobanco()

servidor = 'SERVIDORFRETE'
usuario = 'Mestre1'
password = 'S-45678'
database = 'Frete'
drive = 'ODBC Driver 17 for SQL Server'





print(banco.conecta(driver=drive,server=servidor,database=database,user=usuario,password=password))