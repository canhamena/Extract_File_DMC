import PyPDF2
##import camelot
from pdf2image import convert_from_path
import pandas as pd 
import pytesseract
from sqlalchemy import create_engine,text,inspect
import pandas.api.types as ptypes
from sqlalchemy.exc import SQLAlchemyError





def extract_text_from_pdf(pdf_path, text_pages):
    reader = PyPDF2.PdfReader(pdf_path)
    text_data = []

    for page_number in range(text_pages):
        page = reader.pages[page_number]
        text = page.extract_text()
        # Adiciona o número da página e o texto como uma linha
        text_data.append({'Page': page_number + 1, 'Content': text})
    
    # Converte os dados para um DataFrame
    df = pd.DataFrame(text_data)
    return df

"""def extract_tables_from_pdf(pdf_path, table_pages):
   
    table_data = {}
    
    for page_number in table_pages:
        # Camelot lê a tabela da página específica
        tables = camelot.read_pdf(pdf_path, pages=str(page_number + 1))
        table_data[page_number] = [table.df for table in tables]
    
    return table_data

def extract_tables_from_images(pdf_path, table_pages):

    table_data = {}
    images = convert_from_path(pdf_path)
    
    for page_number in table_pages:
        img = images[page_number]
        text = pytesseract.image_to_string(img, lang="por")  # OCR
        table_data[page_number] = text  # Você pode usar mais regras para estruturar os dados
    
    return table_data

# Configurações
pdf_path = "seu_arquivo.pdf"
text_pages = range(0, 5)  # Exemplo: páginas 0 a 4 (só texto)
table_pages = range(5, 10)  # Exemplo: páginas 5 a 9 (só tabelas)

# Extração de texto
text_data = extract_text_from_pdf(pdf_path, text_pages)

# Extração de tabelas (escolha Camelot ou OCR dependendo do PDF)
try:
    table_data = extract_tables_from_pdf(pdf_path, table_pages)
except Exception:
    print("Falha ao usar Camelot. Tentando com OCR...")
    table_data = extract_tables_from_images(pdf_path, table_pages)

# Exibe os resultados
print("Texto Extraído:")
for page, text in text_data.items():
    print(f"Página {page}:\n{text}\n")

print("Tabelas Extraídas:")
for page, tables in table_data.items():
    print(f"Página {page}:")
    for table in tables:
        print(table)"""