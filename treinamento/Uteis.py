# -*- coding: utf-8 -*-
'''
Created on Aug 14, 2012

@author: 11112456
'''

import re
import nltk
from nltk.tokenize import word_tokenize

#RETORNAR O TÍTULO DO TEXTO JUNTO
def paragrafos(arquivo):
    expr = re.compile(r'<P>(.*?)</P>', re.S)
    texto = arquivo.read()
    expression3 = re.compile(r'<ALT>(.*?)</ALT>', re.S)
    alts = expression3.findall(texto)
    
    for i in alts:
        texto = texto.replace('<ALT>'+i+'</ALT>',selecaoAlt(i))
    return expr.findall(texto)

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
        print 't4'
        texto = arquivo['texto']
        ems = exprEm.findall(texto)
        emsF = []
        for em in ems:
            ID = expr1.findall(em)
            categ = expr2.findall(em)
            tipo = expr3.findall(em)
            corel = expr4.findall(em)
            tiporel = expr5.findall(em)
            conteudo = expr6.findall(em)
                       
            if(len(categ)==0): categ.append('')
            if(len(tipo)==0): tipo.append('')
            if(len(corel)==0): corel.append('')
            if(len(tiporel)==0): tiporel.append('')
            
            emsF.append(dict({'id':ID[0], 'categ':categ[0],'tipo':tipo[0],'corel':corel[0],'tiporel':tiporel[0],
                               'conteudo':expr8.sub('',conteudo[0]), 'completa':em}))
        

        for emF in emsF:
            corels = emF['corel'].split()
            tiporels = emF['tiporel'].split()
            for i in range(len(tiporels)):
                if(rel in tiporels[i]):
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
                
        

def relacoes(paragrafos, tipo1, tipo2):
    expr2 = re.compile(r'<.*?>|\r\n\s*|^\s+?|\s+$', re.S)
    expr = re.compile(r'<EM[^>]*?CATEG="[^"]*?' + tipo1 +'.*?".*?>(.*?)</EM>(.*?)<EM[^>]*?CATEG="[^"]*?' + tipo2 +'.*?".*?>(.*?)</EM>', re.S)
    cont = 0
    res = []
    for p in paragrafos:
        resTmp = expr.findall(p)
        if(len(resTmp) > 0):
            res.append((resTmp[0][0],expr2.sub(' ',resTmp[0][1]),resTmp[0][2]))
            
            print res[len(res)-1]
#            print res[len(res)-1]
#                print resTmp
#                cont += len(resTmp)
#                print cont
    print res
    return res
                
        