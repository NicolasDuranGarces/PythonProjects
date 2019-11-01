
from subprocess import call
from io import open
from os import remove
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.encoders import encode_base64
from tkinter import *
from tkinter import messagebox
import shutil
import smtplib
import getpass
import os


def enviarCorreo():
    user = "nicodg.papu@gmail.com"
    password = "1478963nicolas"

#Para las cabeceras del email
    remitente = "nicodg.papu@gmail.com"
    destinatario = "quegonohpkey@yopmail.com"
    asunto = "Ataques"
    mensaje = "<h1>Adjunto Direcciones IP las cuales intentaron acceder al sistema</h1>"
    call('sudo utmpdump /var/log/btmp| cut -d"[" -f8 | cut -d"]" -f1 > ips.txt', shell=True)
    archivo = 'ips.txt'

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

def obtenerLineas():
    call('sudo utmpdump /var/log/btmp| wc -l > numLineas.txt', shell=True)

def copiarArchivo():
    shutil.copy("numLineas.txt", "numLineasNuevas.txt")

def verificarArchivos():
    obtenerLineas()
    archivoLineasO = open("numLineas.txt","r")
    archivoLineasC = open("numLineasNuevas.txt", "r")
    numLineas = archivoLineasO.readlines()
    numLineasNuevas = archivoLineasC.readlines()
    remove("numLineasNuevas.txt")
    copiarArchivo()
    archivoLineasC.close()
    archivoLineasO.close()
    while True:
        if(numLineas[0]==numLineasNuevas[0]):
            print("Todo en orden")
            verificarArchivos()
        else:
            print("Ataque")
            messagebox.showwarning("Ataque Realizado")
            enviarCorreo()

verificarArchivos()
