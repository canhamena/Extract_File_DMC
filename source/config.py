from sqlalchemy import create_engine
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime, timedelta

server = r'NTBRCSDIT03\SPBDEV'  # Nome do servidor ou endereço IP
database = 'Comercio'  # Nome do banco de dados
driver = "ODBC Driver 17 for SQL Server"

# String de conexão com autenticação do Windows

# Informações do servidor Outlook
smtp_server = 'smtp.office365.com'
smtp_port = 587  # Porta TLS
email_usuario = 'admin@rcsangola.co.ao'  # Substitua com seu e-mail do Outlook
email_senha = 'AnGol@2022#!'  # Substitua com a senha do seu e-mail
## Mensagens...
data_hora = datetime.now()




# Adicionar o corpo do e-mail
body_fim = f"""
      Saudações prezados,

      Informamos que o carregamento dos dados da DCM Docuware foi concluido com sucesso . 

      Atenciosamente,
      Equipe de BI
        """
body_inicio = f"""
      Saudações prezados,

      Informamos que foi iniciado o carregamento dos dados da DCM Docuware. 

      Atenciosamente,
      Equipe de BI
        """
 

def envio_email_notificacao(mensagem):
     # Destinatário e conteúdo do e-mail
   destinatario = 'report@rcsangola.com'
   assunto = 'Carregamento de dados DIT - Docuware'
   msg = MIMEMultipart()
   msg['From'] = email_usuario
   msg['Subject'] = "Orquestração dos dados"
   corpo_email = MIMEText(mensagem, 'plain', 'utf-8')
   msg.attach(corpo_email)
   try:
       # Estabelecendo a conexão com o servidor SMTP do Outlook
       with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()  # Iniciar a criptografia TLS
        server.login(email_usuario, email_senha)  # Login no servidor
        server.sendmail(email_usuario, destinatario, msg.as_string())  # Enviar o e-mail
       mensagem = ""
   except Exception as e:
         print(f'Ocorreu um erro: {e}')

