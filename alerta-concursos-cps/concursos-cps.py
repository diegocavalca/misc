#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 29 10:30:20 2017

@author: diegocavalca
"""
def main():
    import requests, json, os, sys, platform
    import pandas as pd
    from bs4 import BeautifulSoup
    from datetime import datetime
    
    # Params
    params = {'maxDist'    : float(sys.argv[1]),
              'API_KEY'    : sys.argv[2]}
    
    ''' CONCURSOS FATEC '''
    
    # Extrair concursos FATEC (abertos)
    print('Extraindo concursos abertos da FATEC...')
    concursoFATEC = requests.get("http://cpssitevm.cloudapp.net/dgsdad/SelecaoPublica/FATEC/ConcursoDocente/Inscricoesabertas.aspx")
    
    # Parser content webscrapping
    soup = BeautifulSoup(concursoFATEC.content, 'html.parser')
    
    # Extrair lista de concursos (tabela)
    lista = soup.find_all('tr')
    
    # Remover cabecalho
    del lista[0]
    
    # Montando lista de concursos
    concursos = []
    for concurso in lista:
        
        # Dados do concurso
        itens = concurso.find_all('td')
        
        # Verificar distancias (casa > unidade)
        cidade = itens[3].find('font').get_text()
        
        GAPI_URL = 'https://maps.googleapis.com/maps/api/distancematrix/json?origins=Pirajui,SP&destinations='+cidade+',SP&key='+params['API_KEY']
        GAPI_RESULT = requests.get(GAPI_URL)
        GAPI_RESULT = json.loads(GAPI_RESULT.content)
    
        if GAPI_RESULT['status'] == 'OK':
            distancia = GAPI_RESULT['rows'][0]['elements'][0]['distance']['value']/1000
        
            if distancia < params['maxDist']:
        
                link = itens[0].find('a')
                link = 'http://cpssitevm.cloudapp.net/'+link['href']
                
                concursos.append({  'TipoUnidade' : 'FATEC',
                                    'Tipo'        : 'CONCURSO',                                
                                    'CodUnidade'  : itens[1].find('font').get_text(), 
                                    'Unidade'     : itens[2].find('font').get_text(),
                                    'Cidade'      : cidade,
                                    'Distancia'   : distancia,
                                    'FimInscricao': itens[5].find('font').get_text(),
                                    'Edital'      : link 
                                 })
    
    ###############################################################################
    
    ''' CONCURSOS ETEC '''
    
    # Extrair concursos ETEC (abertos)
    print('Extraindo concursos abertos da ETEC...')
    concursoETEC = requests.get("http://cpssitevm.cloudapp.net/dgsdad/SelecaoPublica/ETEC/ConcursoDocente/Inscricoesabertas.aspx")
    
    # Parser content webscrapping
    soup = BeautifulSoup(concursoETEC.content, 'html.parser')
    
    # Extrair lista de concursos (tabela)
    lista = soup.find_all('tr')
    
    # Remover cabecalho
    del lista[0]
    
    # Montando lista de concursos
    #concursosETEC = []
    for concurso in lista:
        
        # Dados do concurso
        itens = concurso.find_all('td')
        
        # Verificar distancias (casa > unidade)
        cidade = itens[3].find('font').get_text()
        
        GAPI_URL = 'https://maps.googleapis.com/maps/api/distancematrix/json?origins=Pirajui,SP&destinations='+cidade+',SP&key='+params['API_KEY']
        GAPI_RESULT = requests.get(GAPI_URL)
        GAPI_RESULT = json.loads(GAPI_RESULT.content)
    
        if GAPI_RESULT['status'] == 'OK':
            distancia = GAPI_RESULT['rows'][0]['elements'][0]['distance']['value']/1000
        
            if distancia < params['maxDist']:
        
                link = itens[0].find('a')
                link = 'http://cpssitevm.cloudapp.net/'+link['href']
                
                concursos.append({  'TipoUnidade' : 'ETEC',
                                    'Tipo'        : 'CONCURSO', 
                                    'CodUnidade': itens[1].find('font').get_text(), 
                                    'Unidade'   : itens[2].find('font').get_text(),
                                    'Cidade'    : cidade,
                                    'Distancia'   : distancia,
                                    'FimInscricao': itens[5].find('font').get_text(),
                                    'Edital'    : link  })
    
    ###############################################################################
    
    ''' PROCESSOS-SELETIVO FATEC '''
    
    # Extrair processos seletivos FATEC (abertos)
    print('Extraindo processos seletivos abertos da FATEC...')
    concursoFATEC = requests.get("http://cpssitevm.cloudapp.net/dgsdad/SelecaoPublica/FATEC/ProcessoSeletivo/Inscricoesabertas.aspx")
    
    # Parser content webscrapping
    soup = BeautifulSoup(concursoFATEC.content, 'html.parser')
    
    # Extrair lista de concursos (tabela)
    lista = soup.find_all('tr')
    
    # Remover cabecalho
    del lista[0]
    
    # Montando lista de processos
    for concurso in lista:
        
        # Dados do processos
        itens = concurso.find_all('td')
        
        # Verificar distancias (casa > unidade)
        cidade = itens[3].find('font').get_text()
        
        GAPI_URL = 'https://maps.googleapis.com/maps/api/distancematrix/json?origins=Pirajui,SP&destinations='+cidade+',SP&key='+params['API_KEY']
        GAPI_RESULT = requests.get(GAPI_URL)
        GAPI_RESULT = json.loads(GAPI_RESULT.content)
    
        if GAPI_RESULT['status'] == 'OK':
            distancia = GAPI_RESULT['rows'][0]['elements'][0]['distance']['value']/1000
        
            if distancia < params['maxDist']:
        
                link = itens[0].find('a')
                link = 'http://cpssitevm.cloudapp.net/'+link['href']
                
                concursos.append({  'TipoUnidade' : 'FATEC',
                                    'Tipo'        : 'PROCESSO-SELETIVO',                                
                                    'CodUnidade'  : itens[1].find('font').get_text(), 
                                    'Unidade'     : itens[2].find('font').get_text(),
                                    'Cidade'      : cidade,
                                    'Distancia'   : distancia,
                                    'FimInscricao': itens[5].find('font').get_text(),
                                    'Edital'      : link 
                                 })
        
    # Salvando concursos em arquivo CSV
    print('Salvando dados obtidos...')
    abspath = os.path.abspath(__file__)
    os.chdir(os.path.dirname(abspath)+'/historico-concursos')
    now = datetime.now()
    arquivo = str(now.year)+'-'+(str(now.month) if now.month >= 10 else '0'+str(now.month))+'-'+str(now.day)+'_dist-'+str(params['maxDist'])+'.xls'
    if os.path.isfile(arquivo):
        os.remove(arquivo)
    df = pd.DataFrame(concursos, columns=['TipoUnidade', 'Tipo', 'CodUnidade', 'Unidade', 'Cidade', 'Distancia', 'FimInscricao', 'Edital'])
    df.to_excel(arquivo)
    
    print('Concursos analisados e salvo com sucesso no arquivo '+arquivo+'!')

    if platform.system() == 'Windows':
        os.system("start " + arquivo)
    else:
        os.system("open " + arquivo)

if __name__ == '__main__':
    main()