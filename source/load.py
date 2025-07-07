from sqlalchemy import create_engine,text,inspect
from source.config import envio_email_notificacao,body_fim,body_inicio
import pandas.api.types as ptypes
from sqlalchemy.exc import SQLAlchemyError
from source.extract import *
from source.apis import *
from source.transform import *
##from source.extract import extract_primavera
server = r'NTBRCSDIT03\SPBDEV'  # Nome do servidor ou endereço IP
database = 'Comercio'  # Nome do banco de dados
driver = "ODBC Driver 17 for SQL Server"

# String de conexão com autenticação do Windows

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
def carrgaemnto_to_sqlserver(dados):
    with engine.connect() as conn:
        # Iniciar transação
        transacao = conn.begin()
        insp = inspect(engine)
        tabela = "Plano_de_Accao"
        AdicionarColunas(dados,tabela)
     
        try:
            if dados.empty == True:
                    print(f"error : {e}")
                    envio_email_notificacao("erro: Api fora de serviço...")
                    return 
            # Carregar os dados da API para a tabela temporária
            Delete_intervalo = text(f"""
                 delete from {tabela} where  Ano = {ano_em_vigor} 
            """)
            result  = conn.execute(Delete_intervalo)
            if result.rowcount > 0:
               print("Carregando dados na tabela temporária...")
               dados.to_sql("Plano_de_Accao", con=engine, if_exists="append", index=False)
               insert_query_historico = text("""
                   INSERT INTO DAF_historico_carregamentos ([origem dos dados])
                  VALUES (:origem_dos_dados)
                 """)
                  # Executando o comando de inserção com os parâmetros
            conn.execute(insert_query_historico, { 'origem_dos_dados': "Inserido com sucesso IndicadoresDesempenho"})
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
          return_data()
          dados =  frame = extract_file_excel()
          frame = retorna_Transforma_Plano_Acao(dados)
          dado=carrgaemnto_to_sqlserver(frame)
          #file_backup()
          #delete_folder()
     except Exception as e:
            #envio_email_notificacao(e)
            print(f"Erro durante a transação: {e}")
            raise
     
        
                




      
     




