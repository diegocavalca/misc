import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def sendmail(fromaddr, toaddr, subject, body, files,
				server, port, password):
	 
	msg = MIMEMultipart()
	 
	# Header
	msg['From'] = fromaddr
	msg['To'] = toaddr
	msg['Subject'] = subject
	
	# Body/Content
	msg.attach(MIMEText(body, 'html'))

	for file in files:
		attachment = open(file, "rb")
		 
		part = MIMEBase('application', 'octet-stream')
		part.set_payload((attachment).read())
		encoders.encode_base64(part)
		_, filename = os.path.split(file)
		part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
		 
		msg.attach(part)
	 
	server = smtplib.SMTP(server, port)
	#server.starttls()
	server.login(fromaddr, password)
	text = msg.as_string()
	server.sendmail(fromaddr, toaddr, text)
	server.quit()

##### EXEMPLO
fromaddr = "robot@diegocavalca.com"
toaddr = "diegoluizcavalca@gmail.com"

import datetime
today = datetime.datetime.now().strftime("%d/%m/%Y")
subject = "Concursos CPS - "+today

path = "/Volumes/Toshiba/Github/misc/alerta-concursos-cps/concursos/"
filename = "2017-09-2_dist-200.0.xls"	
files = [path+filename]

import pandas as pd
df = pd.read_excel(path+filename)

body = ""
with pd.option_context('display.max_colwidth', -1):
	body += df.to_html()

server = "mail.diegocavalca.com"
port = 587
password = "1234mudar."

sendmail(fromaddr, toaddr, subject, body, files, server, port, password)