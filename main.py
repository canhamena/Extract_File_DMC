from source.load import *
from source.config import envio_email_notificacao,body_fim,body_inicio
from source.teste_reader_pdf import *
from source.extract import *



def main():

 

 #search_file_excel(pasta_destino)
 #dados = load_data()
 #print(dados)
 return_data()
 frame = extract_file_excel()
 print(frame)
 """ frame = extract_file_excel()
 dados = retorna_Transforma_Controlo_de_Alcoolemia(frame)
 print(dados)"""

if __name__ == "__main__":
        main()
