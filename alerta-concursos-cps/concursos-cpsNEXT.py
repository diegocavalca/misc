#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 29 10:30:20 2017

@author: diegocavalca
"""
import requests, json, os, sys
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime

def extrairConcursos(tipoUnidade, tipoProcesso, cidadeOrigem, pMaxDist, pApiKey):
    
    tipoUnidade = tipoUnidade.upper()
    tipoProcesso = tipoProcesso.upper()

    if tipoUnidade == 'FATEC':
        if tipoProcesso == 'CONCURSO':
            url = 'http://cpssitevm.cloudapp.net/dgsdad/SelecaoPublica/FATEC/ConcursoDocente/Inscricoesabertas.aspx'
        else:
            url = 'http://cpssitevm.cloudapp.net/dgsdad/SelecaoPublica/FATEC/ProcessoSeletivo/Inscricoesabertas.aspx'
    elif tipoUnidade == 'ETEC':
        if tipoProcesso == 'CONCURSO':
            url = 'http://cpssitevm.cloudapp.net/dgsdad/SelecaoPublica/ETEC/ConcursoDocente/Inscricoesabertas.aspx'
        else:
            url = 'http://cpssitevm.cloudapp.net/dgsdad/SelecaoPublica/ETEC/ProcessoSeletivo/Inscricoesabertas.aspx'
    else:
        print('Erro 999: Parâmetro de concurso desconhecido.')
        return false

    # Extrair concursos abertos
    print('Extraindo '+tipoProcesso.lower()+' da '+tipoUnidade+'...')
    concursosUNIDADE = requests.get(url)
    
    # Parser content webscrapping
    soup = BeautifulSoup(concursosUNIDADE.content, 'html.parser')
    
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
        
        GAPI_URL = 'https://maps.googleapis.com/maps/api/distancematrix/json?origins='+cidadeOrigem+',SP&destinations='+cidade+',SP&key='+pApiKey
        GAPI_RESULT = requests.get(GAPI_URL)
        GAPI_RESULT = json.loads(GAPI_RESULT.content)
    
        if GAPI_RESULT['status'] == 'OK':
            distancia = GAPI_RESULT['rows'][0]['elements'][0]['distance']['value']/1000
        
            if distancia < pMaxDist:
        
                link = itens[0].find('a')
                link = 'http://cpssitevm.cloudapp.net/'+link['href']
                
                concursos.append({  'TipoUnidade' : tipoUnidade,
                                    'Tipo'        : tipoProcesso,                                
                                    'CodUnidade'  : itens[1].find('font').get_text(), 
                                    'Unidade'     : itens[2].find('font').get_text(),
                                    'Cidade'      : cidade,
                                    'FimInscricao': itens[5].find('font').get_text(),
                                    'Edital'      : link 
                                 })
    print(concursos)
    return concursos
    
def main():
    
    # Params
    cidadeOrigem = 'Pirajuí'
    dist = input('Qual a distância máxima de '+cidadeOrigem+' (Km)? ')
    params = {'maxDist'    : float(dist),
              'API_KEY'    : sys.argv[1]}
    
    # Concursos abertos...
    concursos = []
    # FATEC
    concursos.extend(extrairConcursos('FATEC', 'CONCURSO', cidadeOrigem, params['maxDist'], params['API_KEY']))
    concursos.extend(extrairConcursos('FATEC', 'PROCESSO-SELETIVO', cidadeOrigem, params['maxDist'], params['API_KEY']))

    # ETEC
    concursos.extend(extrairConcursos('ETEC', 'CONCURSO', cidadeOrigem, params['maxDist'], params['API_KEY']))
    concursos.extend(extrairConcursos('ETEC', 'PROCESSO-SELETIVO', cidadeOrigem, params['maxDist'], params['API_KEY']))    
        
    # Salvando concursos em arquivo CSV
    print('Salvando dados obtidos...')
    abspath = os.path.abspath(__file__)
    os.chdir(os.path.dirname(abspath)+'/alerta-concursos-cps')
    now = datetime.now()
    arquivo = str(now.year)+'-'+(str(now.month) if now.month >= 10 else '0'+str(now.month))+'-'+str(now.day)+'-dist_'+str(params['maxDist'])+'.xls'
    if os.path.isfile(arquivo):
        os.remove(arquivo)
    df = pd.DataFrame(concursos)#, columns=['TipoUnidade', 'Tipo', 'CodUnidade', 'Unidade', 'Cidade', 'FimInscricao', 'Edital'])
    df.to_excel(arquivo)
    
    print('Concursos analisados e salvos com sucesso no arquivo '+arquivo+'!...')

if __name__ == '__main__':
    main()