#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 29 10:30:20 2017

@author: diegocavalca
"""
def main():
    import sys
    import pandas as pd
    from datetime import datetime
    
    # Params
    params = {'origin'     : 'Pirajui,SP',
              'maxDist'    : float(sys.argv[1]),
              'API_KEY'    : sys.argv[2],
              'toaddr'	   : sys.argv[3],
              'fromaddr'   : sys.argv[4],
              'server'	   : sys.argv[5],
              'port'	   : int(sys.argv[6]),
              'password'   : sys.argv[7]}

    oportunidades = []
    
    # Centro Paula Souza
    from funcoes import cps
    oportunidades.extend( cps('FATEC', 'CONCURSO', params) )
    oportunidades.extend( cps('FATEC', 'PROCESSO', params) )
    oportunidades.extend( cps('ETEC', 'CONCURSO', params) )
    oportunidades.extend( cps('ETEC', 'PROCESSO', params) )

    # Senac
    from funcoes import senac
    oportunidades.extend( senac(params) )

    # IFSP: https://www.ifsp.edu.br/processos-seletivos?layout=edit&id=390

    # Fapesp
    from funcoes import fapesp
    oportunidades.extend( fapesp(params) )

    #print(oportunidades)

    # Organizando resultados
    df = pd.DataFrame(oportunidades)#, columns=['Tipo', 'Instituicao', 'Oportunidade', 'Cidade', 'Distancia', 'Prazo', 'Edital'])
    df = df.sort_values('Distancia')

    # Enviando email
    from funcoes import sendmail
    print('Enviando dados coletados por email...')

    toaddr = params['toaddr']
    fromaddr = params['fromaddr']
    server = params['server']
    port = params['port']
    password = params['password']

    today = datetime.now().strftime("%d/%m/%Y")
    subject = "Concursos CPS - "+today

    body = 'Ol&aacute; Diego, <br><br> Segue abaixo a rela&ccedil;&atilde;o de oportunidades encontradas, com base na origem '+params['origin']+' (raio de '+str(params['maxDist'])+'km):<br><br>'
    with pd.option_context('display.max_colwidth', -1):
      body += df.to_html()
    body += '<br><br>Boa sorte! ;)'

    #print( df )
    sendmail(fromaddr, toaddr, subject, body, [], server, port, password)

if __name__ == '__main__':
    main()