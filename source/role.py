import os
import zipfile
import pandas as pd 
import requests



def convert_type_data(frame,titulo,stuto):
   try:   
    frame["Modified on"] = pd.to_datetime(frame["Modified on"],errors="coerce")
    frame["Stored on"] = pd.to_datetime(frame["Stored on"],errors="coerce")
    frame.columns = [col.replace(" ", "") if " " not in col.strip() else col for col in frame.columns]
    dados = frame[(frame["Tipo de Documento"]=="Mapa") & (frame["Estatuto"]==stuto) & (frame["Titulo"] == titulo) ]
    return dados
   except requests.exceptions.RequestException as e:
     print(f" Error : {e}") 
     return pd.DataFrame()