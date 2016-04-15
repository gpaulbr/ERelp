# -*- coding: utf-8 -*-

'''
Created on Aug 14, 2012

@author: Lucas Pugens Fernandes
'''

#LEIA
#
#PARAMETROS DE ENTRADA:
#RELAÇAO PROCURADA
#DIRETORIO DOS TEXTOS
#
#USO:
#interpretador_python ./Main.py RELACAO_PROCURADA DIRETORIO_TEXTOS
#<opcional>#

import Uteis
import glob
import sys
import os.path
from os import mkdir

def erroParametro():
    print"""
PARAMETROS DE ENTRADA:
RELAÇAO PROCURADA
DIRETORIO DOS TEXTOS

USO:
interpretador_python ./Main.py RELACAO_PROCURADA DIRETORIO_TEXTOS
<opcional>
    """
    exit()

#PARAMETROS DE ENTRADA:
#RELAÇAO PROCURADA
#DIRETORIO DOS TEXTOS

relacao = sys.argv[1]
diretorioTextos = sys.argv[2]

print 'confirmando diretorio de dicionario',diretorioTextos
if os.path.exists(diretorioTextos):
    print 'OK'
else:
    print 'não existe!'
    erroParametro()

textosTmp = glob.glob(diretorioTextos+'/*.txt')
textos = []
diretoriosRelacoes = []
for t in textosTmp:
    textos.append({'titulo':t,'texto':open(t).read()})
    diretoriosRelacoes.append('../textos/relacoes/'+t[10:])

if(len(textos) == 0):
    exit()
        
relacoes = Uteis.relacoesDef(textos, relacao)

saida = open('./relacoes_'+relacao+'.ods', 'w')
saida.write( 'ENTIDADE1;ID1;CATEGORIA1;TIPO;RELAÇÃO;ENTIDADE2;ID2;CATEGORIA2;INTERVALO\n')

for rel in relacoes:

    saida.write( '"'+rel['em1'].replace('"','\'')+'"' +
                 ';' + '"'+rel['id1'].replace('"','\'')+'"' +
                  ';' + '"'+rel['categ1'].replace('"','\'')+'"' +
                   ';' + '"'+rel['tipo'].replace('"','\'')+'"' +
                    ';' + '"'+rel['tiporel'].replace('"','\'')+'"' +
                     ';' + '"'+rel['em2'].replace('"','\'')+'"' +
                      ';' + '"'+rel['id2'].replace('"','\'')+'"' +
                       ';' + '"'+rel['categ2'].replace('"','\'')+'"' +
                        ';' + '"'+rel['intervalo'].replace('"','\'')+'"' + '\n')
        
                        
saida.close()