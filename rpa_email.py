# -*- coding: utf-8 -*-
# $Autor: Nicolás Lista $
# $Fecha de Creación: 20/08/2020 $
# Fecha de Modificación: 19/05/2021 $
import sys
import os
from os import listdir
from os.path import isfile, isdir
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from smtplib import SMTP

class Email:
    #parametros: mail emisor, contraseña, mail receptor, mensaje
    def __init__(self, sender="", password="", to="", cc="", subject="", message="", files_path=""):
        mime_message = MIMEMultipart()
        mime_message["Subject"] = subject
        mime_message["From"] = sender


        mime_message["To"] = to
        mime_message["Cc"] = cc

        mime_message.attach(MIMEText(message, 'html', _charset="utf-8"))
        if files_path:
            for file in listdir(files_path):
                if ".keep" not in file:
                    adjunto_MIME = MIMEBase('application', 'octet-stream')
                    adjunto_MIME.set_payload(open(files_path+str(file), 'rb').read())
                    encoders.encode_base64(adjunto_MIME)
                    adjunto_MIME.add_header('Content-Disposition', "attachment; filename= %s" % str(file))
                    mime_message.attach(adjunto_MIME)

        server = SMTP("smtp.gmail.com", 25)
        server.connect("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(sender, password)
        # server.sendmail(from, to, mime_message.as_string())
        server.send_message(mime_message)
        server.quit()
        print("Email enviado a: " + to)
