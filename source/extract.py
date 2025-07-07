import pandas as pd 
import requests
from sqlalchemy import create_engine
import os
import zipfile
from datetime import datetime, timedelta
import shutil
from source.role import *

urls = []

import requests
ano_em_vigor = datetime.now().year

pasta_destino = r"C:\Teste\excel_dmc"  
pasta_backup=r"C:\Teste\excel_dmc\Backup"
os.makedirs(pasta_destino, exist_ok=True)
nome_arquivo = os.path.join(pasta_destino, "documento_baixado.xlsx")

HEADERS = {"API-KEY" : 'vbHNzgBPW9L9ud7MNY+oMMYgfhi7nWxisSKAGM2u0pI'}


##{'API-KEY' : 'vbHNzgBPW9L9ud7MNY+oMMYgfhi7nWxisSKAGM2u0pI'}



def extract_api(api_url):
 try:  
    limit = 10000

    pagina = 1
    dados = pd.DataFrame()
    while True:
        response = requests.get(api_url,params={'count': limit , 'page': pagina})
        if(response.status_code != 200):
             break
        data = response.json()
        if not data :
            break
        conver_data = pd.DataFrame(data)
        conver_data = conver_data.fillna("")
        dados = pd.concat([dados,conver_data], ignore_index=True)
        pagina += 1

    return dados
 except Exception as e:
     print(f"error : {e}")
     return pd.DataFrame()
 


def dawnload_pdf(api_url,dados):
 try:
     
     if len(dados) >1:
         dados = dados.iloc[:1]
     docuntoId = dados["Document ID"].replace(" ", "")
     response = requests.get(api_url,params={'cabinetId': dados['cabinetId'] , 'documentId': docuntoId},stream=True)
     if response.status_code == 200:
        with open(nome_arquivo, "wb") as file:
         for chunk in response.iter_content(chunk_size=1024):
            file.write(chunk)
    
        print(f"Download concluído: {nome_arquivo}")
     else:
        print(f"Erro ao baixar o arquivo. Código: ")
 except Exception as e:
     print(f"error : {e}")
     return pd.DataFrame()
    

def extrair_Zip(pasta_destino,caminho_zip):
 try:
    if zipfile.is_zipfile(caminho_zip):
        with zipfile.ZipFile(caminho_zip, "r") as zip_ref:
            zip_ref.extractall(pasta_destino)  # Extrai para a mesma pasta
            print(f"Arquivos extraídos para: {caminho_zip}")
    else:
        print("O arquivo baixado não é um ZIP válido.")
 except Exception as e:
     print(f"error : {e}")
     return pd.DataFrame()




 
def extract_file_excel():
    try:
       
       caminho = r"C:\Teste\excel_dmc\documento_baixado.xlsx"
       nome_folha_atual =  "2022"
       # Verificar se a folha existe
       with pd.ExcelFile(caminho) as excel:
         if nome_folha_atual == " ":
            df = pd.read_excel(excel,header=None, dtype=str)
            print(f" Dados da folha: {nome_folha_atual}")
            return df  # Exibir as primeiras linhas
         elif nome_folha_atual in excel.sheet_names:
            df = pd.read_excel(excel,header=None, dtype=str, sheet_name=nome_folha_atual)
            print(f" Dados da folha: {nome_folha_atual}")
            return df  # Exibir as primeiras linhas
         else:
             print(f"A folha '{nome_folha_atual}' não foi encontrada.")
    
    except Exception as e:
         print(f"error : {e}")
         return pd.DataFrame()
    
def return_data():
 try:
  
   os.makedirs(pasta_destino, exist_ok=True)
   nome_arquivo = os.path.join(pasta_destino, "documento_baixado.xlsx")
   dados = extract_api(r"http://api.rcsangola.co.ao/api/qhsa")
   if dados.empty : return "Dados Não encontrado"
   #Plano de Acção,Saídas da RGT,Controlo de Alcoolemia
   dado = convert_type_data(dados,"Controlo de Acidentes de Trabalho","Em vigor")
   dawnload_pdf(r"http://api.rcsangola.co.ao/api/download-document",dado)
   # dados = extract_file_excel(pasta_destino)
   return dados
 except requests.exceptions.RequestException as e:
     print(f" Error : {e}") 
     return pd.DataFrame()
 

def file_backup():
    try:
      if os.path.exists(nome_arquivo) and nome_arquivo.lower().endswith(".zip"):
          os.makedirs(pasta_backup, exist_ok=True)  # Cria a pasta backup se não existir
          shutil.copy(nome_arquivo, os.path.join(pasta_backup, os.path.basename(nome_arquivo)))
          print("Arquivo ZIP copiado com sucesso!")
      else:
           print("O arquivo não existe ou não é um ZIP.")
    except requests.exceptions.RequestException as e:
     print(f" Error : {e}") 
     return pd.DataFrame()
 

def delete_folder():
    try:
        for arquivo in os.listdir(pasta_destino):
          caminho_arquivo = os.path.join(pasta_destino, arquivo)
          if caminho_arquivo != pasta_backup:
             if os.path.isfile(caminho_arquivo) or caminho_arquivo.endswith(".zip"):
                 os.remove(caminho_arquivo)
             elif os.path.isdir(caminho_arquivo):  # Remove subpastas também
                  shutil.rmtree(caminho_arquivo)

        print("Todos os arquivos, incluindo ZIPs, e subpastas foram removidos!")
    except requests.exceptions.RequestException as e:
     print(f" Error : {e}") 
     return pd.DataFrame()




































































