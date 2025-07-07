import pandas as pd 
import requests
from datetime import datetime, timedelta
import itertools


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
 

 



  


  





    