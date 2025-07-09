import pandas as pd 
import requests
from datetime import datetime, timedelta
import itertools
import numpy as np


ano_em_vigor = datetime.now().year

meses = [
    "JANEIRO", "FEVEREIRO", "MARÇO", "ABRIL", "MAIO", "JUNHO",
    "JULHO", "AGOSTO", "SETEMBRO", "OUTUBRO", "NOVEMBRO", "DEZEMBRO"
]

def retorna_Transforma_linha_coluna(frame):
 try:
   colunas_sem_meses= [col for col in frame.columns if col.upper() not in meses]
   df_melted = frame.melt(id_vars=colunas_sem_meses, var_name='Mes',value_name='Valor Mensal')
   df_melted["Ano"] = ano_em_vigor
   return df_melted
 except requests.exceptions.RequestException as e:
     print(f" Error : {e}") 
     return pd.DataFrame()

  
def transfrom_data(frame):
   try:   
     frame = frame.fillna("")
     start_indices = frame[frame.apply(lambda row: row.astype(str).str.contains("Indicadores de Desempenho P04 - Ambiente", case=False, na=False).any(), axis=1)].index
     if start_indices.empty:
       frame.columns = frame.iloc[0]
       frame = frame[1:].reset_index(drop=True)
       return retorna_Transforma_linha_coluna(frame)
     
     return transform_much_table(start_indices,frame)
   
   except requests.exceptions.RequestException as e:
     print(f" Error : {e}") 
     return pd.DataFrame()
   



def transform_much_table(start_indices,frame):
 try:
   df_final =  pd.DataFrame()
   
   for i, idx in enumerate(start_indices):
        # Cabeçalho é a linha seguinte ao título
        start = start_indices[i]
        end = start_indices[i + 1] if i + 1 < len(start_indices) else len(frame)
        table = frame.iloc[start:end].reset_index(drop=True)
        Localidade = table.iloc[0][0]
        table.columns = table.iloc[1]
        table = table[2:].reset_index(drop=True)
        if "DEZEMBRO" in table.columns:
                 table = table.loc[:, : "DEZEMBRO"]
        table["Local"] = Localidade
        df_final = pd.concat([df_final, table], ignore_index=True)

   return retorna_Transforma_linha_coluna(df_final) 
   
       
 except requests.exceptions.RequestException as e:
     print(f" Error : {e}") 
     return pd.DataFrame()
 

def retorna_Transforma_Plano_Acao(frame):
 try:
     header_row = frame.apply(lambda row: row.astype(str).str.contains('PA N.º').any(), axis=1).idxmax()
     fim = frame.apply(lambda r: r.astype(str).str.contains('Tipo de Acção').any(), axis=1).idxmax()
     frame = frame[header_row:fim-1].reset_index(drop=True)
     frame.columns = frame.iloc[0]
     df = frame[1:].reset_index(drop=True)
     df = df.dropna(how='all')
     df = df.loc[:, df.columns.notna()]
     df["Ano"] = pd.to_datetime(df['Data']).dt.year 
     df = df[df["Ano"]==ano_em_vigor]
     return df
   
 except requests.exceptions.RequestException as e:
     print(f" Error : {e}") 
     return pd.DataFrame()
 

def  retorna_Transforma_Saida_RGT(frame):
 try:
     header_row = frame.apply(lambda row: row.astype(str).str.contains('N.º').any(), axis=1).idxmax()
     is_empty = frame.iloc[header_row+1:].isna().all(axis=1)
     fim = is_empty.idxmax()
     frame = frame[header_row:fim].reset_index(drop=True)
     frame.columns = frame.iloc[0]
     df = frame[1:].reset_index(drop=True)
     df = df.dropna(how='all')
     df = df.loc[:, df.columns.notna()]
     df["Ano"] = pd.to_datetime(df['Data RGT']).dt.year 
     
     return df
   
 except requests.exceptions.RequestException as e:
     print(f" Error : {e}") 
     return pd.DataFrame()
 

def  retorna_Transforma_Controlo_de_Alcoolemia(frame):
 try:
     header_row = frame.apply(lambda row: row.astype(str).str.contains('Data').any(), axis=1).idxmax()
     #fim = frame.apply(lambda row: row.astype(str).str.contains('v1').any(), axis=1).idxmax()
     frame = frame[header_row:].reset_index(drop=True)
     frame.columns = frame.iloc[0]
     df = frame[1:].reset_index(drop=True)
     df = df.dropna(how='all')
     df.rename(columns={df.columns[6]: 'Teste_alcool'}, inplace=True)
     df["Ano"] =  "2025"
     return df
 except requests.exceptions.RequestException as e:
     print(f" Error : {e}") 
     return pd.DataFrame()
 
def  retorna_Transforma_Controlo_Acidente_Trabalho(frame):
 try:
     header_row = frame.apply(lambda row: row.astype(str).str.contains('AT n.º').any(), axis=1).idxmax()
     #fim = frame.apply(lambda row: row.astype(str).str.contains('v1').any(), axis=1).idxmax()
     frame = frame[header_row:].reset_index(drop=True)
     frame.columns = frame.iloc[0]
     df = frame[1:].reset_index(drop=True)
     df = df.dropna(how='all')
     df = df.loc[:, df.columns.notna()]
     df["Ano"] = "2025"
     df = df[df['Data do AT'].notnull() & (df['Data do AT'] != '')]
     df = df[df["AT n.º"].notna()]
     return df
 except requests.exceptions.RequestException as e:
     print(f" Error : {e}") 
     return pd.DataFrame()
 
def retorna_Transforma_Controlo_Incidente_Trabalho(frame):
 try:
     header_row = frame.apply(lambda row: row.astype(str).str.contains('n.º').any(), axis=1).idxmax()
     frame = frame[header_row:].reset_index(drop=True)
     frame.columns = frame.iloc[0]
     df = frame[1:].reset_index(drop=True)
     df = df.dropna(how='all')
     df = df.loc[:, df.columns.notna()]
     df["Ano"] = "2025"
     df = df[df["n.º"].notna()]
     return df
 except requests.exceptions.RequestException as e:
     print(f" Error : {e}") 
     return pd.DataFrame()
 
def retorna_Transforma_Controlo_Acções_HSE(frame):
 try:
     header_row = frame.apply(lambda row: row.astype(str).str.contains('Nº').any(), axis=1).idxmax()
     frame = frame[header_row:].reset_index(drop=True)
     frame.columns = frame.iloc[0]
     df = frame[1:].reset_index(drop=True)
     df = df.dropna(how='all')
     df = df.loc[:, df.columns.notna()]
     df['Nº'] = df['Nº'].ffill()
     df['Nº REGISTO '] = df['Nº REGISTO '].ffill()
     df['RESP. Execução'] = df['RESP. Execução'].ffill()
     df['ACÇÕES A IMPLEMENTAR'] = (
     df.groupby('Nº')['ACÇÕES A IMPLEMENTAR']
      .ffill()
      .bfill()
      .infer_objects()
      )
     
     df['FORMATO'] = (
     df.groupby('Nº')['FORMATO']
      .ffill()
      .bfill()
      .infer_objects()
      )
     df['LOCAL'] = (
     df.groupby('Nº')['LOCAL']
      .ffill()
      .bfill()
      .infer_objects()
      )
     df['RESP. Observação'] = (
     df.groupby('Nº')['RESP. Observação']
      .ffill()
      .bfill()
      .infer_objects()
      )
     
     df["Ano"] = "2025"
     return df
 except requests.exceptions.RequestException as e:
     print(f" Error : {e}") 
     return pd.DataFrame()

def retorna_Transforma_Impressora_Doadas(frame):
 try:
     header_row = frame.apply(lambda row: row.astype(str).str.contains('Local').any(), axis=1).idxmax()
     frame = frame[header_row:].reset_index(drop=True)
     frame.columns = frame.iloc[0]
     df = frame[1:].reset_index(drop=True)
     df = df.dropna(how='all')
     #df = df.loc[:, df.columns.notna()]
     df.rename(columns={"Pessoa de contacto": 'Pessoa_Contacto_Nome'}, inplace=True)
     df.columns = [f'Pessoa_Contacto_{i+1}' if pd.isna(col) else col
    for i, col in enumerate(df.columns)]
     df.rename(columns={np.nan: 'Pessoa_Contacto_Contacto'}, inplace=True)
     df["Ano"] = pd.to_datetime(df['Data de doação']).dt.year 
     df['Local'] = df['Local'].ffill()
     df.rename(columns={"Pessoa_Contacto_12": 'Pessoa_Contacto_Contacto'}, inplace=True)
     df['Pessoa_Contacto_Contacto'] = df['Pessoa_Contacto_Contacto'].ffill()
     df['Pessoa_Contacto_Nome'] = df['Pessoa_Contacto_Nome'].ffill()
     df.rename(columns={"Instituição": 'Instituicao'}, inplace=True)
     df['Instituicao'] = df['Instituicao'].ffill()
     df.rename(columns={"Ticket de instalação": 'Ticket_Instalacao'}, inplace=True)
     df['Ticket_Instalacao'] = df['Ticket_Instalacao'].ffill()
     df['Data de doação'] = df['Data de doação'].ffill()
     df['Modelo'] = df['Modelo'].ffill()
     df['Número de Série'] = df['Número de Série'].ffill()
     df['Frequência de manutenção'] = df['Frequência de manutenção'].ffill()
     df.rename(columns={"Nº Técnicos/\nNº horas": 'N_Tecnico_N_Horas'}, inplace=True)
     df['N_Tecnico_N_Horas'] = df['N_Tecnico_N_Horas'].ffill()
     df['Status'] = df['Status'].ffill()
     df = df[df["Local"].notna()]
     return df
 except requests.exceptions.RequestException as e:
     print(f" Error : {e}") 
     return pd.DataFrame()
 

def retorna_Transforma_Plano_Prevenção_Doenças_Promoção_Saude(frame):
 try:
     header_row = frame.apply(lambda row: row.astype(str).str.contains('Nº').any(), axis=1).idxmax()
     frame = frame[header_row:].reset_index(drop=True)
     frame.columns = frame.iloc[0]
     df = frame[1:].reset_index(drop=True)
     df = df.dropna(how='all')
     df = df[df["Nº"].notna()]
     df = df.loc[:, df.columns.notna()]
     return df
 except requests.exceptions.RequestException as e:
     print(f" Error : {e}") 
     return pd.DataFrame()

def retorna_Transforma_Cronograma_Minutos_seguranca(frame):
 try:
     header_row = frame.apply(lambda row: row.astype(str).str.contains('Meses').any(), axis=1).idxmax()
     frame = frame[header_row:].reset_index(drop=True)
     frame.columns = frame.iloc[1]
     old_header = frame.iloc[0]
     new_names  = frame.iloc[1]
     old_header = old_header.tolist()
     old_header[1:-4] = new_names[1:-4]
     frame.columns = old_header
     df = frame[2:]
     df = df.loc[:, df.columns.notna()]
     return df
 except requests.exceptions.RequestException as e:
     print(f" Error : {e}") 
     return pd.DataFrame()
 
 
 

 



  


  





    