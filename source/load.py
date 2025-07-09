from sqlalchemy import create_engine,text,inspect
from source.config import envio_email_notificacao,body_fim,body_inicio
import pandas.api.types as ptypes
from sqlalchemy.exc import SQLAlchemyError
from source.extract import *
from source.apis import *
from source.transform import *
from source.regras import *
##from source.extract import extract_primavera
server = r'NTBRCSDIT03\SPBDEV'  # Nome do servidor ou endereço IP
database = 'Comercio'  # Nome do banco de dados
driver = "ODBC Driver 17 for SQL Server"

# String de conexão com autenticação do Windows
ano_em_vigor = datetime.now().year
conn_str = (
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER={server};"
    f"DATABASE={database};"
    "Trusted_Connection=yes;"
)

engine = create_engine(f"mssql+pyodbc://@{server}/{database}?driver={driver}&trusted_connection=yes")

def AdicionarColunas(dados,tabela):
       
         try:
             ##Inspeciona a estrutura de um banco de dados
             insp = inspect(engine)
             colunas_existentes_bd = [col['name'] for col in insp.get_columns(tabela)]
             novas_colunas = [col for col in dados.columns if col not in colunas_existentes_bd]
             for coluna in novas_colunas:
                   add_column_query = text(f"""ALTER TABLE {tabela} ADD [{coluna}] VARCHAR(255) """) 
                   try:
                       with engine.connect() as conn:
                           transacao = conn.begin()
                           conn.execute(add_column_query)
                           transacao.commit()
                           print("Campo adicionado com sucesso")

                   except SQLAlchemyError as e:
                         #envio_email_notificacao(f"Erro ao adicionar coluna {coluna}: {e}")
                         return; 
         except Exception as e:
                # Reverter transação em caso de erro
                envio_email_notificacao(f"Erro durante a criação de novo campo: {e}")
                return
                
          
  ## Fazer o carregamento       
def carrgaemnto_to_sqlserver(dados,tabela,variavel):
    with engine.connect() as conn:
        # Iniciar transação
        transacao = conn.begin()
        insp = inspect(engine)
        AdicionarColunas(dados,tabela) 
        try:
            if dados.empty == True:
                    print(f"error : ")
                    envio_email_notificacao("erro: Api fora de serviço...")
                    return 
            # Carregar os dados da API para a tabela temporária
            Delete_intervalo = text(f"""
                 delete from {tabela} where  Year([{variavel}]) = {ano_em_vigor} 
            """)
            result  = conn.execute(Delete_intervalo)
            if result.rowcount > 0:
               print("Carregando dados na tabela temporária...")
               dados.to_sql(tabela, con=engine, if_exists="append", index=False)
               insert_query_historico = text("""
                   INSERT INTO DAF_historico_carregamentos ([origem dos dados])
                   VALUES (:origem_dos_dados)
                 """)
                  # Executando o comando de inserção com os parâmetros
               conn.execute(insert_query_historico, { 'origem_dos_dados': f"Inserido com sucesso {tabela}"})
                 # Confirmar transação
            transacao.commit()
            print("Transação concluída com sucesso!")
        except Exception as e:
            # Reverter transação em caso de erro
            transacao.rollback()
            #envio_email_notificacao(e)
            print(f"Erro durante a transação: {e}")
            raise
        
  
def load_data():
     
     try:
          index=0
          for tabela in tabelas.items():
                frame = return_data(folha[index],ficheiro[index],titulo[index])
                if(tabelas[index] =="Plano_de_Accao"):
                       dados = retorna_Transforma_Plano_Acao(frame)
                elif(tabelas[index] =="Saidas_da_RGT"):
                     dados = retorna_Transforma_Saida_RGT(frame)
                elif(tabelas[index] =="Controlo_de_Alcoolemia"):
                     dados = retorna_Transforma_Controlo_de_Alcoolemia(frame)
                elif(tabelas[index] =="Controlo_de_Acidentes_de_Trabalho"):
                     dados = retorna_Transforma_Controlo_Acidente_Trabalho(frame)
                elif(tabelas[index] =="Controlo_de_Incidentes_de_Trabalho"):
                     dados = retorna_Transforma_Controlo_Incidente_Trabalho(frame)
                elif(tabelas[index] =="Cronograma_Minutos_Seguranca"):
                     dados = retorna_Transforma_Cronograma_Minutos_seguranca(frame)
                elif(tabelas[index] =="Controlo_Accoes_de_HSE"):
                     dados = retorna_Transforma_Controlo_Accoees_HSE(frame)
                elif(tabelas[index] =="Controlo_de_Impressoras_Doadas") and not frame.empty:
                     dados = retorna_Transforma_Impressora_Doadas(frame)
                elif(tabelas[index] =="Plano_de_Prevencao_de_Doencas_Promocao_da_Saude") and not frame.empty:
                     dados = retorna_Transforma_Plano_Prevenção_Doenças_Promoção_Saude(frame)
                     carrgaemnto_to_sqlserver(dados,tabelas[index],campo[index])
                     
                     
                file_backup(ficheiro[index])
                delete_folder()
                index+=1
          print("Executado com sucesso")
     except Exception as e:
            #envio_email_notificacao(e)
            print(f"Erro durante a transação: {e}")
            raise
     
        
                




      
     




