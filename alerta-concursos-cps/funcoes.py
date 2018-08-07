import requests, json, os, sys, platform, re
from bs4 import BeautifulSoup

def cps(tipoUnidade, tipoProcesso, params):
	
	urlCPS = 'https://www.urhsistemas.cps.sp.gov.br'

	tipoUnidade = tipoUnidade.upper()
	tipoProcesso = tipoProcesso.upper()

	if tipoUnidade == 'FATEC':
		if tipoProcesso == 'CONCURSO':
			url = urlCPS + '/dgsdad/SelecaoPublica/FATEC/ConcursoDocente/Inscricoesabertas.aspx'
		else:
			url = urlCPS + '/dgsdad/SelecaoPublica/FATEC/ProcessoSeletivo/Inscricoesabertas.aspx'
	elif tipoUnidade == 'ETEC':
		if tipoProcesso == 'CONCURSO':
			url = urlCPS + '/dgsdad/SelecaoPublica/ETEC/ConcursoDocente/Inscricoesabertas.aspx'
		else:
			url = urlCPS + '/dgsdad/SelecaoPublica/ETEC/ProcessoSeletivo/Inscricoesabertas.aspx'
	else:
		print('Erro 999: Parâmetro de concurso desconhecido.')
		return false

	# Extrair concursos (abertos)
	concursos = []

	print('Extraindo '+tipoProcesso+'S/'+tipoUnidade+' abertos no CPS...')
	listaConcursos = requests.get(url, verify=False)

	# Parser content webscrapping
	soup = BeautifulSoup(listaConcursos.content, 'html.parser')
	
	# Extrair lista de concursos (tabela)
	lista = soup.find_all('tr')
	
	# Remover cabecalho
	del lista[0]
	
	# Montando lista de concursos
	for concurso in lista:
		
		# Dados do concurso
		itens = concurso.find_all('td')
		
		# Verificar distancias (casa > unidade)
		cidade = itens[3].find('font').get_text()
		distancia = distance(cidade, params)
		
		if distancia < params['maxDist']:
	
			link = itens[0].find('a')
			link = urlCPS+link['href']
			
			concursos.append({
								'Tipo'        : tipoProcesso,                                
								'Instituicao' : itens[2].find('font').get_text(),
								'Oportunidade': 'Professor',
								'Cidade'      : cidade,
								'Distancia'   : distancia,
								'Prazo'		  : itens[5].find('font').get_text(),
								'Edital'      : link 
							 })
	return concursos

def fapesp(params):
	oportunidades = []
	
	print('Extraindo oportunidades FAPESP...')
	listaConcursos = requests.get('http://www.fapesp.br/oportunidades/', verify=False)

	# Parser content webscrapping
	soup = BeautifulSoup(listaConcursos.content, 'html.parser')
	
	# Extrair lista de oportunidades
	lista = soup.select('li.box_col.aberta.pt')
	
	# Montando lista de concursos
	for concurso in lista:
		
		# Detalhes da oportunidade
		dados = concurso.find_all('strong')

		# Remover PD/Mestrado
		titulo = dados[0].text
		if not any(re.findall(r'PD|Mestrado', titulo, re.IGNORECASE)):

			# Verificar distancias (casa > unidade)
			cidade = dados[2].next_sibling
			
			distancia = distance(cidade, params)

			if distancia < params['maxDist']:

					oportunidades.append({
										'Tipo'        : 'BOLSA',                                
										'Instituicao' : dados[1].next_sibling,#itens[2].find('font').get_text(),
										'Oportunidade': titulo,
										'Cidade'      : cidade,
										'Distancia'   : distancia,
										'Prazo'		  : dados[3].next_sibling,
										'Edital'      : 'http://www.fapesp.br'+concurso.find('a').get('href') 
									 })

	return oportunidades

def senac()
	oportunidades = []
	url = 'http://www.sp.senac.br/recru/portal/_display.jsp?_app=mural/consultaNewLayout.jsp'
	return oportunidades

def distance(destin, params):

	dist = 999
	GAPI_URL = 'https://maps.googleapis.com/maps/api/distancematrix/json?origins='+params['origin']+'&destinations='+destin+',SP&key='+params['API_KEY']
	GAPI_RESULT = requests.get(GAPI_URL)
	GAPI_RESULT = json.loads(GAPI_RESULT.content)

	if GAPI_RESULT['status'] == 'OK':
	    dist = GAPI_RESULT['rows'][0]['elements'][0]['distance']['value']/1000
	# dist = 100
	
	return dist

def sendmail(fromaddr, toaddr, subject, body, files,
				server, port, password):

	import smtplib
	from email.mime.multipart import MIMEMultipart
	from email.mime.text import MIMEText
	from email.mime.base import MIMEBase
	from email import encoders

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