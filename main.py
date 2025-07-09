from source.load import *
from source.config import envio_email_notificacao,body_fim,body_inicio
from source.teste_reader_pdf import *
from source.extract import *



def main():
 dados = load_data()
 #search_file_excel(pasta_destino)
 print(dados)
 """frame = extract_file_excel()
 dados = retorna_Transforma_Cronograma_Minutos_seguranca(frame)
 print(dados)
dados = retorna_Transforma_Cronograma_Minutos_seguranca(frame)
 print(dados)
frame = extract_file_excel()
 dados = retorna_Transforma_Impressora_Doadas(frame)
 print(dados)
 frame = extract_file_excel()
 dados = retorna_Transforma_Controlo_Incidente_Trabalho(frame)
 print(dados)"""
 """dados = retorna_Transforma_Controlo_Acidente_Trabalho(frame)
 print(dados)"""
 """ frame = extract_file_excel()
 dados = retorna_Transforma_Controlo_de_Alcoolemia(frame)
 print(dados)"""

if __name__ == "__main__":
        main()
