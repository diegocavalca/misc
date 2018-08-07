import requests, json, os, sys, platform, re
from bs4 import BeautifulSoup

def cps(tipoUnidade, tipoProcesso, params):
	
	oportunidades = []

	urlCPS = 'https://www.urhsistemas.cps.sp.gov.br'

	tipoUnidade = tipoUnidade.upper()
	tipoProcesso = tipoProcesso.upper()

	if tipoUnidade == 'FATEC':
		if tipoProcesso == 'CONCURSO':
			#url = urlCPS + '/dgsdad/SelecaoPublica/FATEC/ConcursoDocente/Inscricoesabertas.aspx'
			oportunidades.append( 
							cps_fatec_concurso(
								urlCPS, 
								'/dgsdad/SelecaoPublica/FATEC/ConcursoDocente/Abertos.aspx',
								tipoProcesso,
								params)
						) 
		else:
			oportunidades.append( 
							cps_fatec_processo(
								urlCPS, 
								'/dgsdad/SelecaoPublica/FATEC/ProcessoSeletivo/Abertos.aspx',
								tipoProcesso,
								params)
						) 
	elif tipoUnidade == 'ETEC':
		if tipoProcesso == 'CONCURSO':
			oportunidades.append( 
							cps_etec_concurso(
								urlCPS, 
								'/dgsdad/SelecaoPublica/ETEC/ConcursoDocente/Abertos.aspx',
								tipoProcesso,
								params)
						) 
		else:
			oportunidades.append( 
							cps_etec_processo(
								urlCPS, 
								'/dgsdad/SelecaoPublica/ETEC/ProcessoSeletivo/Abertos.aspx',
								tipoProcesso,
								params)
						) 
	else:
		print('Erro 999: Parâmetro de concurso desconhecido.')
		return false

	if len(oportunidades)>0:
		return oportunidades[0]
	else:
		return oportunidades

def cps_fatec_concurso(urlCPS, urlOportunidades, tipoProcesso, params):
	oportunidades = []

	print('Extraindo '+tipoProcesso+'S abertos nas FATECS...', end='')

	# Parser content webscrapping
	site = requests.get(urlCPS + urlOportunidades, verify=False)
	if site:
		
		# Extrair lista de concursos (tabela)
		content = BeautifulSoup(site.content, 'html.parser') 

		tabelaOpts = content.find("table")

		if tabelaOpts:
			lista = tabelaOpts.find_all('tr')

			if lista:
				# Remover cabecalho
				del lista[0]

				# Montando lista de concursos
				for oportunidade in lista:
					
					# Dados da oportunidade
					itens = oportunidade.find_all('td')
					
					# Verificar distancias (casa > unidade)
					cidade = itens[3].get_text()
					disciplina = itens[6].get_text()
					# Depois validar disciplinas...
					distancia = distance(cidade, params)
					
					if distancia < params['maxDist']:
				
						link = itens[0].find('a')
						link = urlCPS + endOportunidades.replace('Abertos.aspx', link['href'])

						prazo = 'VERIFICAR'
						
						oportunidades.append({
											'Tipo'         : tipoProcesso,                                
											'Instituicao'  : itens[2].get_text().replace('\n',''),
											'Oportunidade' : ('Professor - ' + disciplina),
											'Cidade'       : cidade,
											'Distancia'    : float(distancia),
											'Prazo'		   : prazo,
											'Edital'       : link#'<a href="'+link+'">LINK</a>'
										 })
	print(' Ok!')
	return oportunidades

# Lidar com Webdriver - Paginacao de resultados
def cps_fatec_processo(urlCPS, endOportunidades, tipoProcesso, params):
	oportunidades = []

	print('Extraindo '+tipoProcesso+'S abertos nas FATECS...', end='')

	# Parser content webscrapping
	site = requests.get(urlCPS + endOportunidades, verify=False)
	if site:
		
		# Extrair lista de concursos (tabela)
		content = BeautifulSoup(site.content, 'html.parser') 

		tabelaOpts = content.find(id="ContentPlaceHolderPrincipal_conteudoSelecao_GridView2")
		#print(tabelaOpts)

		if tabelaOpts:
			lista = tabelaOpts.find_all('tr')

			if lista:
				# Remover cabecalho / rodape
				del lista[0]
				#del lista[-2:]

				# Montando lista de concursos
				for oportunidade in lista:
					
					# Dados da oportunidade
					itens = oportunidade.find_all('td')
					
					# Verificar se é /rodape
					if len(itens) > 3:
						# Verificar distancias (casa > unidade)
						cidade = itens[3].get_text()
						disciplina = itens[6].get_text()
						# Depois validar disciplinas...
						distancia = distance(cidade, params)
						
						if distancia < params['maxDist']:
					
							link = itens[0].find('a')
							link = urlCPS + endOportunidades.replace('Abertos.aspx', link['href'])
							
							oportunidades.append({
												'Tipo'         : tipoProcesso,                                
												'Instituicao'  : itens[2].get_text().replace('\n',''),
												'Oportunidade' : ( disciplina ),
												'Cidade'       : cidade,
												'Distancia'    : float(distancia),
												'Prazo'		   : itens[8].get_text(),
												'Edital'       : link#'<a href="'+link+'">LINK</a>'
											 })
	print(' Ok!')
	return oportunidades

def cps_etec_concurso(urlCPS, endOportunidades, tipoProcesso, params):
	oportunidades = []

	print('Extraindo '+tipoProcesso+'S abertos nas ETECS...', end='')

	# Parser content webscrapping
	site = requests.get(urlCPS + endOportunidades, verify=False)
	if site:
		
		# Extrair lista de concursos (tabela)
		content = BeautifulSoup(site.content, 'html.parser') 

		tabelaOpts = content.find(id="ContentPlaceHolderPrincipal_conteudoSelecao_GridView2")

		if tabelaOpts:
			lista = tabelaOpts.find_all('tr')

			if lista:
				# Remover cabecalho
				del lista[0]

				# Montando lista de concursos
				for oportunidade in lista:
					
					# Dados da oportunidade
					itens = oportunidade.find_all('td')
					
					# Verificar se é /rodape
					if len(itens) > 3:
						# Verificar distancias (casa > unidade)
						cidade = itens[3].get_text()
						disciplina = itens[6].get_text()
						# Depois validar disciplinas...
						distancia = distance(cidade, params)
						
						if distancia < params['maxDist']:
					
							link = itens[0].find('a')
							link = urlCPS + endOportunidades.replace('Abertos.aspx', link['href'])

							prazo = 'VERIFICAR'
							
							oportunidades.append({
												'Tipo'         : tipoProcesso,                                
												'Instituicao'  : 'ETEC',#itens[2].get_text().replace('\n',''),
												'Oportunidade' : ( disciplina ),
												'Cidade'       : cidade,
												'Distancia'    : float(distancia),
												'Prazo'		   : prazo,
												'Edital'       : link#'<a href="'+link+'">LINK</a>'
											 })
	print(' Ok!')
	return oportunidades

def cps_etec_processo(urlCPS, endOportunidades, tipoProcesso, params):
	oportunidades = []

	print('Extraindo '+tipoProcesso+'S abertos nas ETECS...', end='')

	# Parser content webscrapping
	site = requests.get(urlCPS + endOportunidades, verify=False)
	if site:
		
		# Extrair lista de concursos (tabela)
		content = BeautifulSoup(site.content, 'html.parser') 

		tabelaOpts = content.find("table")

		if tabelaOpts:
			lista = tabelaOpts.find_all('tr')

			if lista:
				# Remover cabecalho
				del lista[0]

				# Montando lista de concursos
				for oportunidade in lista:
					
					# Dados da oportunidade
					itens = oportunidade.find_all('td')
					
					# Verificar distancias (casa > unidade)
					cidade = itens[3].get_text()
					distancia = distance(cidade, params)
					
					if distancia < params['maxDist']:
				
						link = itens[0].find('a')
						link = urlCPS + endOportunidades.replace('Abertos.aspx', link['href'])
						
						oportunidades.append({
											'Tipo'         : tipoProcesso,                                
											'Instituicao'  : 'ETEC',#itens[2].get_text().replace('\n',''),
											'Oportunidade' : ( itens[5].get_text()+' disciplinas' ),
											'Cidade'       : cidade,
											'Distancia'    : float(distancia),
											'Prazo'		   : itens[7].get_text(),
											'Edital'       : link#'<a href="'+link+'">LINK</a>'
										 })
	print(' Ok!')
	return oportunidades

def senac(params):
	oportunidades = []
	
	print('Extraindo oportunidades SENAC...', end='')
	listaConcursos = requests.get('http://www.sp.senac.br/recru/portal/_display.jsp', verify=False)

	# Parser content webscrapping
	soup = BeautifulSoup(listaConcursos.content, 'html.parser')
	
	# Extrair lista de oportunidades
	lista = soup.select('div.box.bgGray')
	
	# Montando lista de concursos
	if lista:
		for oportunidade in lista:
			
			cidade = oportunidade.find_all("div", class_="v1")[1].get_text(strip=True).replace('Local','')
			distancia = distance(cidade, params)
			
			if distancia < params['maxDist'] + 200:
		
				# Remover oportunidades não aderentes
				titulo = oportunidade.find(id='titVaga').get_text(strip=True)
				if 'docente' in titulo.lower(): #not any(re.findall(r'PD|Mestrado|Iniciação Científica|Doutorado Direto', titulo, re.IGNORECASE)):

					link = 'http://www.sp.senac.br/recru/portal/_display.jsp'#urlCPS + endOportunidades.replace('Abertos.aspx', link['href'])
					prazo = oportunidade.find_all("div", class_="v2")[0].get_text(strip=True).replace('Período de Inscrição','').split(' - ')[1]
					
					oportunidades.append({
										'Tipo'         : 'CONTRATO',                                
										'Instituicao'  : cidade,
										'Oportunidade' : titulo,
										'Cidade'       : cidade.replace('Senac ',''),
										'Distancia'    : float(distancia),
										'Prazo'		   : prazo,
										'Edital'       : link#'<a href="'+link+'">LINK</a>'
									 })

	print(' Ok!')
	return oportunidades

def fapesp(params):
	oportunidades = []
	
	print('Extraindo oportunidades FAPESP...', end='')
	listaConcursos = requests.get('http://www.fapesp.br/oportunidades/', verify=False)

	# Parser content webscrapping
	soup = BeautifulSoup(listaConcursos.content, 'html.parser')
	
	# Extrair lista de oportunidades
	lista = soup.select('li.box_col.aberta.pt')
	
	# Montando lista de concursos
	if lista:
		for oportunidade in lista:
			
			# Detalhes da oportunidade
			dados = oportunidade.find_all('strong')

			# Remover PD/Mestrado
			titulo = dados[0].text
			if not any(re.findall(r'PD|Mestrado|Iniciação Científica|Doutorado Direto', titulo, re.IGNORECASE)):

				# Verificar distancias (casa > unidade)
				cidade = dados[2].next_sibling
				distancia = distance(cidade, params)
				if distancia < params['maxDist']+200:

					link = 'http://www.fapesp.br'+oportunidade.find('a').get('href') 

					oportunidades.append({
										'Tipo'        : 'FAPESP',                                
										'Instituicao' : dados[1].next_sibling,#itens[2].find('font').get_text(),
										'Oportunidade': titulo,
										'Cidade'      : cidade,
										'Distancia'   : distancia,
										'Prazo'		  : dados[3].next_sibling,
										'Edital'      : link#'<a href="'+link+'">LINK</a>'
									 })
	print(' Ok!')
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