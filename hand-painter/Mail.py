from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib, ssl
global CONFIG
import os
from dotenv import dotenv_values

class Mail:
    def __init__(self):
        self.port = 465
        self.smtp_server_domain_name = "smtp.gmail.com"

        config = {
            **dotenv_values(".env"),
            **os.environ,  
        }

        self.sender_mail = config["EMAIL"]
        self.password = config["PASSWORD"]

    def send(self, to, images):
        try:
            ssl_context = ssl.create_default_context()
            service = smtplib.SMTP_SSL(self.smtp_server_domain_name, self.port, context=ssl_context)
            service.login(self.sender_mail, self.password)

            msg = MIMEMultipart()
            msg['Subject'] = 'NIAEFEUP - Semana Profissão Engenheiro'
            msg['From'] = self.sender_mail
            msg['To'] = to

            text = MIMEText("""
            Olá!

            Obrigado por teres passado na nossa banca e teres ficado a conhecer aquilo que fazemos no Núcleo e na faculdade!

            Segue-nos nas nossas redes sociais para que estejas a par de tudo aquilo que fazemos! @niaefeup

            Enviamos em anexo os teus desenhos!
            """)
            msg.attach(text)

            for image in images:
                with open(image, 'rb') as f:
                    img_data = f.read()
                    image = MIMEImage(img_data, name=image)
                    msg.attach(image)

            service.sendmail(self.sender_mail, to, msg.as_string())

            service.quit()
        except Exception as e:
            print("Error sending email: ", e)

