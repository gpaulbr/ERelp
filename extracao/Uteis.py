# -*- coding: utf-8 -*-
'''
Created on Aug 14, 2012

@author: Lucas Pugens Fernandes
'''

import re
import nltk
from nltk.tokenize import word_tokenize

#RETORNA OS PARAGRAFOS DO TEXTO REMOVENDO AS <ALT>s
def paragrafos(arquivo):
    expr = re.compile(r'<P>(.*?)</P>', re.S)
    texto = arquivo.read()
    expression3 = re.compile(r'<ALT>(.*?)</ALT>', re.S)
    alts = expression3.findall(texto)    
    for i in alts:
        texto = texto.replace('<ALT>'+i+'</ALT>',selecaoAlt(i))
    return expr.findall(texto)


#SELECIONA QUAL DAS OPÇÕES <ALT> FOI ESCOLHIDA DE ACORDO COM AS REGRAS ESTABELECIDAS
def selecaoAlt(str):
    ex2 = re.compile(r'">(.*?)</EM>')
    ops = []
    podeQuebrar = True
    op = ''
    for l in range(len(str)):
        if(str[l] == '<'):
            if(str[l:l+3] == '<EM'):
                podeQuebrar = False
        if(str[l] == '>'):
            if(str[l-4:l] == '</EM'):
                podeQuebrar = True
        if(str[l] == '|' and podeQuebrar):
            ops.append(op)
            op = ''
            continue
        op += str[l]
    ops.append(op)
    op = ''
    votos = []
    maior = 0
    certa = ''
    for o in range(len(ops)):
        ems = ex2.findall(ops[o])
        if(len(ems) == 0):
            continue
        maiorEM = 0
        for em in ems:
            emTok = nltk.tokenize.word_tokenize(em)
            if(len(emTok) > maiorEM):
                maiorEM = len(emTok)
        votos.append((maiorEM,ems[0][0].isupper(),o))#(tamanho da entidade, começa ou nao com maiuscula, qual das opçoes ela pertence)
    maior = -1
    for i in range(len(votos)):
        if(votos[i][0] > maior):
            if(votos[i][1]):
                certa = ops[votos[i][2]]
                maior = votos[i][0]
    if(len(certa) < 3):
        maior = -1
        for i in range(len(votos)):
            if(votos[i][0] > maior):
                certa = ops[votos[i][2]]
                maior = votos[i][0]
    return certa

#PROCURA NO CONJUNTO DE textos A RELAÇAO rel REQUISITADA 
def relacoesDef(textos, rel):
    exprEm = re.compile(r'<EM[^>]*?>.*?</EM>', re.S)
    expr1 = re.compile(r'<EM[^>]*?ID="(.*?)".*?>.*?</EM>', re.S)
    expr2 = re.compile(r'<EM[^>]*?CATEG="(.*?)".*?>.*?</EM>', re.S)
    expr3 = re.compile(r'<EM[^>]*?TIPO="(.*?)".*?>.*?</EM>', re.S)
    expr4 = re.compile(r'<EM[^>]*?COREL="(.*?)".*?>.*?</EM>', re.S)
    expr5 = re.compile(r'<EM[^>]*?TIPOREL="(.*?)".*?>.*?</EM>', re.S)
    expr6 = re.compile(r'<EM.*?>(.*?)</EM>', re.S)
    expr8 = re.compile(r'<.*?>', re.S)
    result = []
    
    for arquivo in textos:
        texto = arquivo['texto']
        ems = exprEm.findall(texto)#entidades mencionadas encontradas no texto
        emsF = []#entidades mencionadas formatadas de acordo com a pesquisa
        for em in ems:
            #extração das informaçoes com expressoes regulares
            ID = expr1.findall(em)
            categ = expr2.findall(em)
            tipo = expr3.findall(em)
            corel = expr4.findall(em)
            tiporel = expr5.findall(em)
            conteudo = expr6.findall(em)

            #caso alguma expressao nao tenha tido retorno
            if(len(categ)==0): categ.append('')
            if(len(tipo)==0): tipo.append('')
            if(len(corel)==0): corel.append('')
            if(len(tiporel)==0): tiporel.append('')
            
            emsF.append(dict({'id':ID[0], 'categ':categ[0],'tipo':tipo[0],'corel':corel[0],'tiporel':tiporel[0],
                               'conteudo':expr8.sub('',conteudo[0]), 'completa':em}))
        
        #PROCURA PELA RELACAO REQUISITADA
        for emF in emsF:
            corels = emF['corel'].split()
            tiporels = emF['tiporel'].split()
            for i in range(len(tiporels)):
                if(rel == tiporels[i]):
                    tiporelSplit = tiporels[i].split('**')
                    if(len(tiporelSplit) > 1):
                        for emF2 in emsF:
                            if(tiporelSplit[2] == emF2['id']):
                                expr = r'' + emF['completa'].replace('*','\*').replace('|','\|') + '.*?' + emF2['completa'].replace('*','\*').replace('|','\|') + ''
                                expr7 = re.compile(expr, re.S)
                                intervalo = expr7.findall(texto)
                                if(len(intervalo) == 0):
                                    expr = r'' + emF2['completa'].replace('*','\*').replace('|','\|') + '.*?' + emF['completa'].replace('*','\*').replace('|','\|') + ''
                                    expr7 = re.compile(expr, re.S)
                                    intervalo = expr7.findall(texto)[0]
                                else:
                                    intervalo = intervalo[0]
                                intervalo = expr8.sub('',intervalo)
                                result.append(dict({'em1':emF['conteudo'],'id1':emF['id'],'categ1':tiporelSplit[0],'tipo':emF['tipo'],
                                                    'tiporel':tiporelSplit[1],'em2':emF2['conteudo'],'id2':emF2['id'],'categ2':tiporelSplit[-1],
                                                     'intervalo': intervalo}))
                    else:
                        for emF2 in emsF:
                            if(corels[i] == emF2['id'] and emF != emF2):
                                expr = r'' + emF['completa'].replace('*','\*').replace('|','\|') + '.*?' + emF2['completa'].replace('*','\*').replace('|','\|') + ''
                                expr7 = re.compile(expr, re.S)
                                intervalo = expr7.findall(texto)
                                if(len(intervalo) == 0):
                                    expr = r'' + emF2['completa'].replace('*','\*').replace('|','\|') + '.*?' + emF['completa'].replace('*','\*').replace('|','\|') + ''
                                    expr7 = re.compile(expr, re.S)
                                    intervalo = expr7.findall(texto)[0]
                                else:
                                    intervalo = intervalo[0]
                                intervalo = expr8.sub('',intervalo)
                                result.append(dict({'em1':emF['conteudo'],'id1':emF['id'],'categ1':emF['categ'],'tipo':emF['tipo'],
                                                    'tiporel':tiporels[i],'em2':emF2['conteudo'],'id2':emF2['id'],'categ2':emF2['categ'],
                                                         'intervalo': intervalo}))
    return result
        