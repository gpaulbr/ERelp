# -*- coding: utf-8 -*-

#LEIA
#
#PARAMETROS DE ENTRADA:
#DIRETORIO TREINO - deve conter os textos separados em arquivos .txt
#DIRETORIO DE TRABALHO - será criado na execução
#QUANTIDADE DE FOLDS - numero de folds utilizadas no processo de cross validation
#DIRETORIO MALLET - diretorio que contem a biblioteca MALLET
#CATEGORIAS A UTILIZAR (2) - opcional, mas se for informado devem ser exatamente duas
#,(VÍRGULA) - obritagorio para extração dos parâmetros
#DICIONARIOS - dicionarios a serem utilizados como features
#
#USO:
#<interpretador_python_alternativo> ./NERcrf.py DIRETORIO_TREINO DIRETORIO_DE_TRABALHO QUANTIDADE_DE_FOLDS DIRETORIO_MALLET <CATEGORIA_A_UTILIZAR_1 CATEGORIA_A_UTILIZAR_2> , DICIONARIOS...
#<opcional>#

import math
import re
import os

import subprocess
import time

import Uteis

import os.path
import CRFnltk
from KNNUtil import classe

def processaTags(trainingTweets): #retorna lista no formato
    expressao2 = re.compile(r'\[(.*)\]', re.S)#expressao regular para encontra a forma canônica da palavra
    expressao3 = re.compile(r'<([^\s]*)>', re.S)#expressao regular para encontrar a marcação semântica da palavra
    
    
    #MONTAGEM DOS DICIONARIOS#########################################################################
    dicionariosFormat = list()#lista com os dicionarios formatados
    for dic in dicionarios:
        fileDic = open(dic,'r')
        dicFormat = fileDic.read()
        fileDic.close()
        
        dicSplited = dicFormat.split('\n')#divide o arquivo em linhas
        dicFormat = []
        for i in range(len(dicSplited)):#monta o dicionario usando o primeiro item de cada linha
            split = dicSplited[i].split(';')
            dicFormat.extend([itm.lower() for itm in split[:1]])
        dicionariosFormat.append(dicFormat)
    ##################################################################################################
    
    #INCIALIZAÇÕES DE VARIÁVEIS
    labelled = list()#retorno formatado do arquivo
    palavra = ''
    bil = ''
    classe = ''
    semanticNoun = ''
    relacoesTotal = 0    
    # variáveis de controle para extrair somente a relação
    extrai = False
    extrai2 = False
    
    p = re.compile(r'\$S-[0-9]*')#expressao para dividir textos de um arquivo

    frases = p.split(trainingTweets) # frases recebe a lista de sentenças do arquivo
    
    for frase in frases:#limpa frases extraidas erradas
        if frase == '':
            frases.remove('')
            
    frases = [frase.replace('</s>','') for frase in frases]#limpa marcação desnecessária
    
    
    for f in frases:
        p = list()
        vetBio = list()#vetor contendo os intens bil do texto
        tokens = f.split('\n')#tokens é um vetor das palavras
        for t in tokens:
                        
            classe = ''#POS da palavra
            sintatica = ''#marcação sintática do palavra
            semanticNoun = ''#HPROF ou HTIT
            
            classificacao = 'nulo'#classificação da EN
            
            gerarFeatures = False#se devem ser geradas features sobre a palavra atual
            bole = False#variavel para extrair sintatica e POS
            bole2 = False#variavel para extrair sintatica e POS
            
            if(t != ''):#verifica se a linha não está vazia
                splited = t.split()#splited é um vetor com as informações da palavra
                if(len(splited) > 2):#verifica se a linha contém informação de classificação
                    if splited[-2] in categUtilizadas:#verifica se a entidade em questão está entre as procuradas
                        extrai = not extrai
                        classificacao = splited[-2]#guarda a classificação da EN
                        
                gerarFeatures = extrai2 or extrai# só gera features entre as entidades incluindo-as
                    
                if(len(splited) < 2):#verificação de erros de marcação
                    print 'erro de formatação'
                    print splited
                    exit()
                if(len(splited) == 2):#token é uma pontuação
                    palavra = ''
                    for letra in t[1:]:#salva a pontuação como palavra
                        if letra != ' ':
                            palavra += letra
                        else:
                            break
                    classe = 'nulo'#não há POS
                    sintatica = 'nulo'#sem informação sintática
                    semantica = 'nulo'#sem informação semantica
                    semanticNoun = 'nulo'#sem informação semantica
                    bil = t.split()[1]
                else:#token é uma palavra
                    
                    if len(expressao3.findall(t)) == 0:#não há algumas informações na linha
                        semantica = 'nulo'#sem informação semantica
                        semanticNoun = 'nulo'#sem informação semantica
                        

                        
                        for tk in splited:#utiliza marcações do palavras para formar coletar as informações
                            if('[' in tk):
                                bole3 = True
                            if(']' in tk and bole3):
                                bole = True
                            if('[' not in tk and ']' not in tk and bole and not bole2):
                                classe = tk
                                bole2 = True
                            if('@' in tk and bole2):
                                sintatica = tk
                    else:#linha completa com todas as marcações do palavras
                        semantica = expressao3.findall(t)[0]
                        
                        if('<Hprof>' in t):#para semanticNoun só import hprof ou htit
                            semanticNoun = 'hprof'
                        elif('<Htit>' in t):
                            semanticNoun = 'htit'
                        else:
                            semanticNoun = 'nulo'  
                            
                        for tk in t.split():#utiliza marcações do palavras para formar coletar as informações                                
                            if('<' in tk):
                                bole3 = True                             
                            if('>' in tk and bole3):
                                bole = True
                            if('<' not in tk and '>' not in tk and bole and not bole2):
                                classe = tk
                                bole2 = True
                            if('@' in tk and bole2):
                                sintatica = tk
                        
                    #forma a palavra canônica da linha
                    if(not t.startswith('$')):#verifica se não é apenas uma pontuação
                        if(len(expressao2.findall(t)) == 0):#alguma falha de anotação
                            print t, 'sem forma canônica'
                            exit()
                        palavra = expressao2.findall(t)[0]
                        bil = t.split()[-1]
                    else:
                        palavra = splited[0]
                        if(palavra.startswith('$')):
                            palavra = palavra[1:]
                            for i in range(len(t))[len(palavra)+1:]:
                                if(t[i] != ' '):
                                    palavra += t[i]
                                else:
                                    break
                if(semanticNoun == ''):#falha de anotação
                    print t, 'não foi encontrado semanticNoun'
                    exit()
                
                items = list()
                items.extend([('palavra',palavra), ('classe',classe), ('semantica',semantica),
                              ('sintatica',sintatica),('semanticNoun',semanticNoun),
                              ('classificacao',classificacao),('gerarFeatures',gerarFeatures)])
                
                for i in range(len(dicionariosFormat)):
                    if(palavra.lower() in dicionariosFormat[i]):
                        items.append((('dicionario'+str(i)),'sim'))
                    else:
                        items.append((('dicionario'+str(i)),'nao'))
                        
                itemsDict = dict(items)
                
                p.append((itemsDict))#valores do vetor de entrada

                vetBio.append(bil)
                if(bil == 'B-REL'):
                    relacoesTotal += 1
                    
                extrai2 = extrai
        if(p != []):
            file = open(diretorioTrabalho+'/vetorEntrada.txt','a')
            file.write(str(p)+'\n')
            file.close()
            
            p2 = list()#vetor com as features das palavras
            for i in range(len(p)):
                if(p[i]['gerarFeatures']):
                    p2.append((extractFeatures(p,i),vetBio[i]))
            labelled.append(p2)

    return labelled, relacoesTotal


def extractFeatures(tweet, indexWord):
    features = []#conjunto de features da palavra
    word = tweet[indexWord]['palavra']#propria palavra
    
    if not word == '':
       
        n_words = len(tweet)#numero de palavras da sentença
       
        limNucleos = []#conjunto que conterá os limites do núcleo da sentença
       
       
        provaveisApp = list()#provaveis inicios de apostos no formato ('<palavra de inicio>',<posição de inicio>)
        limitsApp = list()#limites do aposto
        nucleoApp = False#verifica se a palavra atual é o núcleo do aposto
        tipoFrase = 'nulo'#tipo de frase analisada dentre os definidos
        verbo = False#se a sentença possui um verbo
        substantivo = False#se a sentença possui um substantivo       
       
        tamanho = 0
        for i in range(len(tweet)):          
                
            if(len(tweet)-1 > i):#só entra se esta não for a última palavra da sentença
                if('—' == tweet[i]['palavra'] or ',' == tweet[i]['palavra'] or '(' == tweet[i]['palavra']):#para definir os limites do aposto
                    encontrouAposto = False#variavel de controle para limpar o provaveisApp
                    for (palavra,posicao) in provaveisApp:#pesquisa por um encerramento de aposto
                        if(palavra == tweet[i]['palavra'].replace('(',')')):
                            limitsApp.append((posicao+1,i-1))
                            encontrouAposto = True
                            break
                    if(encontrouAposto):#foi delimitado um aposto e deve ser removido dos provaveis
                        provaveisApp = list()
                    else:#foi encontrado um candidato a inicio de aposto
                        if((tweet[i+1]['classe'] == 'DET' and (tweet[i+2]['classe'] == 'N' or tweet[i+2]['classe'] == 'PERS'))
                           or (tweet[i+1]['classe'] == 'N' or tweet[i+1]['classe'] == 'PERS')):#verifica se a posição corresponde a um inicio de aposto de acordo com a regra do português
                            provaveisApp.append((tweet[i]['palavra'],i))
                        if((tweet[i+1]['classe'] == 'DET' and (tweet[i+2]['classe'] == 'N' or tweet[i+2]['classe'] == 'PERS') and i+2 == indexWord)
                           or ((tweet[i+1]['classe'] == 'N' or tweet[i+1]['classe'] == 'PERS') and i+1 == indexWord)):#verifica se a palavra atual é o núcleo
                            nucleoApp = True
                            
            #procura pelos limites do núcleo da sentença
            if(tweet[i]['sintatica'] == '@SUBJ>'):
                for j in range(len(tweet))[i:]:
                    if(tweet[j]['classe'] == 'V'):
                        limNucleos.append((i,j-1))
            if(tweet[i]['sintatica'] == '@<SUBJ'):
                temp = range(len(tweet))[:i]
                temp.reverse()
                for j in temp:
                    if(tweet[j]['classe'] == 'V'):
                        limNucleos.append((j+1,i))

            if(tweet[i]['gerarFeatures']):
                tamanho += 1

        features.append(('tamanho',tamanho))
        
        if nucleoApp:
            features.append(('nucleoAposto','sim'))
        else:
            features.append(('nucleoAposto','nao'))
       
        incluidaAposto = False#verifica se a palavra está dentro de um aposto procurando por todos os possíveis apostos da sentença
        for limite in limitsApp:
            if indexWord >= limite[0] and indexWord <= limite[1]:
                incluidaAposto = True
                break#encerra o laço ao encontrar o primeiro aposto que a palavra esteja inserida
        if(incluidaAposto):
            features.append(('estaAposto','sim'))
        else:
            features.append(('estaAposto','nao'))
            
        #feature extraídas diretamente do vetor de entrada
        features.append(('palavra',word.lower()))
        features.append(('POSTag',tweet[indexWord]['classe'].lower()))
        features.append(('phraseTag',tweet[indexWord]['sintatica']))
        features.append(('semanticNoun',tweet[indexWord]['semanticNoun']))
        features.append(('clas',tweet[indexWord]['classificacao']))

        #DICIONARIOS
        cont = 0
        for i in tweet[indexWord]:
            if('dicionario' in i):
                cont = cont+1
                features.append((i,tweet[indexWord][i]))

        #VERIFICAÇÃO BASEADA EM PADRÕES
        if(indexWord < len(tweet)-1):
            if(tweet[indexWord]['classe'] == 'V'):
                verbo = True
            if(verbo and tweet[indexWord+1]['classe'] == 'DET'):
                tipoFrase = 'verbArtigo'
            elif(verbo and tweet[indexWord+1]['classe'] == 'PRP'):
                tipoFrase = 'verbPrep'
            if(tweet[indexWord]['classe'] == 'N'):
                substantivo = True
            if(substantivo and tweet[indexWord+1]['classe'] == 'PRP'):
                tipoFrase = 'subsPrep'

        if(tipoFrase == 'verbArtigo'):
            features.append(('verbArtigo','sim'))
            features.append(('verbPrep','nao'))
            features.append(('subsPrep','nao'))
        elif(tipoFrase == 'verbPrep'):
            features.append(('verbArtigo','nao'))
            features.append(('verbPrep','sim'))
            features.append(('subsPrep','nao'))
        elif(tipoFrase == 'subsPrep'):
            features.append(('verbArtigo','nao'))
            features.append(('verbPrep','nao'))
            features.append(('subsPrep','sim'))
        else:
            features.append(('verbArtigo','nao'))
            features.append(('verbPrep','nao'))
            features.append(('subsPrep','nao'))           
                  
        #feature de verbo binária
        if(tweet[indexWord]['classe'] == 'V'):
            features.append(('verbo','sim'))
        else:
            features.append(('verbo','nao'))
            
        #FEATURE DE NÚCLEO DA SENTENÇA
        if((tweet[indexWord]['classe'] == 'N' or tweet[indexWord]['classe'] == 'PROP' or
                tweet[indexWord]['classe'] == 'PERS' or tweet[indexWord]['classe'] == 'NUM') and
                'SUBJ' in tweet[indexWord]['sintatica']):
            features.append(('nucleo','sim'))
        else:
            features.append(('nucleo','nao'))
            

        #FEATURES DE JANELA
        #se há palavra anterior a atual
        if indexWord > 0:
#            if(tweet[indexWord-1]['classificacao'] != 'null'):#verifica se a palavra não é uma das EN de relação
#                features.append(('prevW',tweet[indexWord-1]['classificacao'].lower()))
#            else:
#                features.append(('prevW',tweet[indexWord-1]['palavra'].lower()))
            features.append(('prevClas',tweet[indexWord-1]['classificacao']))#para incluir a classificação como uma nova feature
            features.append(('prevW',tweet[indexWord-1]['palavra'].lower()))
            features.append(('prevT',tweet[indexWord-1]['classe'].lower()))
            features.append(('next0CT',tweet[indexWord-1]['classe']+' '+tweet[indexWord]['classe']))
            features.append(('prevPT',tweet[indexWord-1]['sintatica']))
            features.append(('prev0CPT',tweet[indexWord-1]['sintatica']+' '+tweet[indexWord]['sintatica']))
            features.append(('next0CW',tweet[indexWord-1]['palavra']+' '+tweet[indexWord]['palavra']))
            features.append(('prevSemanticNoun',tweet[indexWord-1]['semanticNoun']))
          
            if(tweet[indexWord-1]['classe'] == 'V'):
                features.append(('prevVerbo','sim'))
            else:
                features.append(('prevVerbo','nao'))

            incluidaAposto = False#verifica se a palavra está dentro de um aposto
            for limite in limitsApp:
                if indexWord-1 >= limite[0] and indexWord-1 <= limite[1]:
                    incluidaAposto = True
                    break
            if(incluidaAposto):
                features.append(('prevApost','sim'))
            else:
                features.append(('prevApost','nao'))

        else:#VALORES NULOS
            features.append(('prevW','null'))
            features.append(('prevT','null'))
            features.append(('next0CT','null'))
            features.append(('prevPT','null'))
            features.append(('prev0CPT','null'))
            features.append(('next0CW','null'))  
            features.append(('prevVerbo','null')) 
            features.append(('prevApost','null')) 
            features.append(('prevSemanticNoun','null'))
            features.append(('prevClas','null'))
                             
        #verifica se há palavra na posição p-2
        if indexWord > 1:
#            if(tweet[indexWord-2]['classificacao'] != 'null'):#verifica se a palavra não é uma das EN de relação
#                features.append(('prev2W',tweet[indexWord-2]['classificacao'].lower()))
#            else:
#                features.append(('prev2W',tweet[indexWord-2]['palavra'].lower()))
            features.append(('prev2Clas',tweet[indexWord-2]['classificacao']))#para incluir a classificação como uma nova feature
            features.append(('prev2W',tweet[indexWord-2]['palavra'].lower()))
            features.append(('prev2T',tweet[indexWord-2]['classe'].lower()))
            features.append(('prev2PT',tweet[indexWord-2]['sintatica']))
            features.append(('prev1CT',tweet[indexWord-2]['classe']+' '+tweet[indexWord-1]['classe']))
            features.append(('prev1CPT',tweet[indexWord-2]['sintatica']+' '+tweet[indexWord-1]['sintatica']))
            features.append(('prev1CW',tweet[indexWord-2]['palavra']+' '+tweet[indexWord-1]['palavra']))
            features.append(('prev2SemanticNoun',tweet[indexWord-2]['semanticNoun']))

            if(tweet[indexWord-2]['classe'] == 'V'):
                features.append(('prev2Verbo','sim'))
            else:
                features.append(('prev2Verbo','nao'))              
             
            incluidaAposto = False#verifica se a palavra está dentro de um aposto
            for limite in limitsApp:
                if indexWord-2 >= limite[0] and indexWord-2 <= limite[1]:
                    incluidaAposto = True
                    break

            if(incluidaAposto):
                features.append(('prev2Apost','sim'))
            else:
                features.append(('prev2Apost','nao'))
                              
        else:          
            features.append(('prev2W','null'))
            features.append(('prev2T','null'))
            features.append(('prev2PT','null'))
            features.append(('prev1CT','null'))
            features.append(('prev1CPT','null'))
            features.append(('prev1CW','null'))   
            features.append(('prev2Verbo','null'))   
            features.append(('prev2Apost','null'))  
            features.append(('prev2SemanticNoun','null'))
            features.append(('prev2Clas','null'))

        #verifica se há palavra posterior a atual
        if indexWord < n_words-1:
#            if(tweet[indexWord+1]['classificacao'] != 'null'):#verifica se a palavra não é uma das EN de relação
#                features.append(('nextW',tweet[indexWord+1]['classificacao'].lower()))
#            else:
#                features.append(('nextW',tweet[indexWord+1]['palavra'].lower()))
            features.append(('nextClas',tweet[indexWord+1]['classificacao']))#para incluir a classificação como uma nova feature
            features.append(('nextW',tweet[indexWord+1]['palavra'].lower()))
            features.append(('nextT',tweet[indexWord+1]['classe'].lower()))
            features.append(('next1CT',tweet[indexWord]['classe']+' '+tweet[indexWord+1]['classe']))
            features.append(('nextPT',tweet[indexWord+1]['sintatica']))
            features.append(('next1CPT',tweet[indexWord]['sintatica']+' '+tweet[indexWord+1]['sintatica']))
            features.append(('next1CW',tweet[indexWord]['palavra']+' '+tweet[indexWord+1]['palavra']))
            features.append(('nextSemanticNoun',tweet[indexWord+1]['semanticNoun'])) 
                             
            if(tweet[indexWord+1]['classe'] == 'V'):
                features.append(('nextVerbo','sim'))
            else:
                features.append(('nextVerbo','nao'))      
              
            incluidaAposto = False#verifica se a palavra está dentro de um aposto
            for limite in limitsApp:
                if indexWord+1 >= limite[0] and indexWord+1 <= limite[1]:
                    incluidaAposto = True
                    break

            if(incluidaAposto):
                features.append(('nextApost','sim'))
            else:
                features.append(('nextApost','nao'))
         
        else:
            features.append(('nextW','null'))
            features.append(('nextT','null'))
            features.append(('next1CT','null'))
            features.append(('nextPT','null'))
            features.append(('next1CPT','null'))
            features.append(('next1CW','null'))
            features.append(('nextVerbo','null'))
            features.append(('nextApost','null'))
            features.append(('nextSemanticNoun','null'))
            features.append(('nextClas','null'))

        #verifica se há palavra na posição p+2
        if indexWord < n_words-2:
#            if(tweet[indexWord+2]['classificacao'] != 'null'):#verifica se a palavra não é uma das EN de relação
#                features.append(('next2W',tweet[indexWord+2]['classificacao'].lower()))
#            else:
#                features.append(('next2W',tweet[indexWord+2]['palavra'].lower()))
            features.append(('next2Clas',tweet[indexWord+2]['classificacao']))#para incluir a classificação como uma nova feature
            features.append(('next2W',tweet[indexWord+2]['palavra'].lower()))
            features.append(('next2T',tweet[indexWord+2]['classe'].lower()))
            features.append(('next2CT',tweet[indexWord+1]['classe']+' '+tweet[indexWord+2]['classe']))
            features.append(('next2PT',tweet[indexWord+2]['sintatica']))
            features.append(('next2CPT',tweet[indexWord+1]['sintatica']+' '+tweet[indexWord+2]['sintatica']))
            features.append(('next2CW',tweet[indexWord+1]['palavra']+' '+tweet[indexWord+2]['palavra']))
            features.append(('next2SemanticNoun',tweet[indexWord+2]['semanticNoun']))
                    
            if(tweet[indexWord+2]['classe'] == 'V'):
                features.append(('next2Verbo','sim'))
            else:
                features.append(('next2Verbo','nao'))      
              
            incluidaAposto = False#verifica se a palavra está dentro de um aposto
            for limite in limitsApp:
                if indexWord+2 >= limite[0] and indexWord+2 <= limite[1]:
                    incluidaAposto = True
                    break

            if(incluidaAposto):
                features.append(('next2Apost','sim'))
            else:
                features.append(('next2Apost','nao'))

        else:
            features.append(('next2W','null'))
            features.append(('next2T','null'))
            features.append(('next2CT','null'))
            features.append(('next2PT','null'))
            features.append(('next2CPT','null'))
            features.append(('next2CW','null'))    
            features.append(('next2Verbo','null'))   
            features.append(('next2Apost','null'))    
            features.append(('next2SemanticNoun','null'))
            features.append(('next2Clas','null'))

    resul = dict(features)
    
    file = open(diretorioTrabalho+'/vetorFeatures.txt','a')
    file.write(str(resul)+'\n')
    file.close()
    
    return resul


def iniEnt(bilou, pos):#verifica se o item bilou[pos] representa o início de uma relação

    if(bilou[pos] != 'B-REL'):
        return False
    else:
        return True

def endEnt(bilou, pos):#verifica se o item bilou[pos] representa o fim de uma relação

    if(bilou[pos] == 'O'):
        return False
    else:
        if(bilou[pos] == 'I-REL'):
            if(pos == 0):
                return False
            if(pos < len(bilou)-1):
                if(bilou[pos+1] == 'I-REL'):
                    return False
            aux2 = pos-1
            while(bilou[aux2] != 'B-REL'):
                if(bilou[aux2] != 'I-REL'):
                    return False
                aux2 -= 1
                if(aux2 < 0):
                    return False
        elif(bilou[pos] == 'B-REL'):
            if(pos < len(bilou)-1):
                if(bilou[pos+1] == 'I-REL'):
                    return False;
    return True



#EFETUA O RECONECIMENTO DE RELAÇÕES UTILIZANDO labelled COMO TREINO E test COMO TESTE, iteracao
#INFORMA EM QUAL FOLD SE ENCONTRA O PROCESSO DE CROSS VALIDATION
def RR(labelled, test, iteracao):
    #relações acertadas pelo sistema de acordo com a CD
    relacoesAcertos = 0
    #relações descritas pelo sistema
    relacoesChutadas = 0
    
    #tabela de confusão da iteração
    result = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

    #variável lab representa apenas valores válidos de labels, [[sent1],[sent2]...[sentN]]
    lab = []
    for label in labelled:
        if label == None:
            continue
        if label != []:
            for s in label[1]:
                if(s != []):
                    lab.append(s)
    
    #treina ou abre o já treinado CRF
    #Obs.:Mudar na classe CRFnltk para não gravar sobre modelo gerado
    crf = CRFnltk.CRFTrain(lab, iteracao)
    

    #variável para conter os resultados do CRF
    labels = []

    #arquivo para salvar em formato de Tabela
    dirExc = diretorioTrabalho+'/result_' + str(iteracao) + 'it.ods'

    #limpa arquivo
    fileEx = open(dirExc,'w')
    fileEx.write('')
    fileEx.close()

    #contador de intens BILOU da iteração
    contBio = 0

    #itera sobre o conjunto de teste
    contador = 0
    for texto in test:
        if texto == None:
            continue
        if texto != []:
            #inicializa vetor da marcação correta do BILOU
            truth = []
            #inicializa vetor com as informações de cada palavra
            tagged = []
            #itera sobre as sentenças do texto
            for s in texto[1]:
                if(s != []):
                    for w in s:
                        tagged.append(w[0])
                        truth.append(w[1])

            #usa o CRF para determinar o valor BILOU da palavra
            labels = CRFnltk.CRF_prediction(crf, tagged)
            
            #contador de labels
            contLabels = 0
            
            #adiciona o inicio do texto à saída no formato HAREM
            saida = open(diretorioTrabalho+'/saidaHarem.xml', 'a')
            saida.write('<DOC DOCID="' + str(texto[0])[:-4] + '">\n')
            saida.close()
            
            #limpa o arquivo com as marcações
            dir = diretorioTrabalho+'/marcados/iteracao ' + str(iteracao) + '/' + str(texto[0])
            file = open(dir,'w')
            file.write('')
            file.close()
            
            #escreve o titulo do texto no arquivo excell
            fileEx = open(dirExc,'a')
            fileEx.write(str(texto[0]) +'\n\n\n')
            fileEx.close()
            
            print 'gravando em', dir, '...'
                        
            if texto != []:
                #itera sobre sentenças do texto
                for s in texto[1]:
                    if(s != []):
                        
                        file = open(dir,'a')
                        file.write('\n\t')
                        file.close()
                        
                        acerto = True#é acerto até que se prove o contrário
                        mostraErrados = False#variavel escrever as EN encontradas por engano pelo sistema na saida excell
                        
                        #itera sobre as palavras da sentença
                        for w in s:

                            #escreve no arquivo com as marcações
                            file = open(dir,'a')
                            file.write(str(w[0]['palavra']) + '<' + str(w[0]['POSTag']) + ',' + labels[contLabels] + '> ')
                            file.close()

                            #verifica se a palavra é início de uma entidade
                            if(iniEnt(labels, contLabels)):
                                #se for inicio de EN, escreve a tag de inicio de EN da CD
                                saida = open(diretorioTrabalho+'/saidaHarem.xml', 'a')
                                saida.write('<EM ID="' + str(texto[0])[:-4] + '"> ')
                                saida.close()

                            #escreve a palavra na saída do formato harem
                            saida = open(diretorioTrabalho+'/saidaHarem.xml', 'a')
                            saida.write(str(w[0]['palavra']) + ' ')
                            saida.close()

                            #incrementa a tabela de confusão
                            result[classe(truth[contLabels])][classe(labels[contLabels])] += 1

                            #verifica se a palavra é fim de uma entidade
                            if(endEnt(labels,contLabels)):
                                #se for fim de EN, escreve a tage de inicio de EN da CD
                                saida = open(diretorioTrabalho+'/saidaHarem.xml', 'a')
                                saida.write('</EM>')
                                saida.close()

                            if(labels[contLabels] == 'B-REL'):#incrementa o número de relações encontradas pelo sistema
                                relacoesChutadas += 1
                                
                            if(labels[contLabels] == 'B-REL' and truth[contLabels] == 'O'):#uma entidade encontrada por engano
                                mostraErrados = True
                            if(mostraErrados and labels[contLabels] != 'O'):#mostra toda a EN marcada por engano
                                #escreve no excell
                                fileEx = open(dirExc,'a')
                                fileEx.write(str(w[0]['palavra']) + '<' + str(w[0]['POSTag']) + ','+ ',' + labels[contLabels] + '>;'+
                                             str(w[0]['palavra']) + '<' + str(w[0]['POSTag']) + ','+ ',' + truth[contLabels] + '>\n')
                                if labels[contLabels] != truth[contLabels] or truth[contLabels]=='O':
                                    acerto = False
                                fileEx.close()
                                
                            else:#fim da EN marcada por engano
                                mostraErrados = False

                            #escreve no arquivo tabela o resultado do sistema e o correto
                            if(truth[contLabels] == 'B-REL' or truth[contLabels] == 'I-REL'):#parte de uma relação segundo a CD
                                if(truth[contLabels] == 'B-REL'):
                                    acerto = True#a princio é acerto
                                #escreve a palavra na tabela
                                fileEx = open(dirExc,'a')
                                fileEx.write(str(w[0]['palavra']) + '<' + str(w[0]['POSTag']) + ','+ ',' + labels[contLabels] + '>;'+
                                             str(w[0]['palavra']) + '<' + str(w[0]['POSTag']) + ','+ ',' + truth[contLabels] + '>\n')
                                fileEx.close()
                                
                                if labels[contLabels] != truth[contLabels] or truth[contLabels]=='O':#erro na marcação
                                    acerto = False
                                
                                if acerto:#verificar se realmente foi acerto
                                    if len(truth)-1 == contLabels:
                                        relacoesAcertos += 1
                                        fileEx = open(dirExc,'a')
                                        fileEx.write(';V')
                                        fileEx.close()
                                        acerto = False
                                    elif truth[contLabels+1] != 'I-REL' and labels[contLabels+1]!='I-REL':
                                        relacoesAcertos += 1
                                        fileEx = open(dirExc,'a')
                                        fileEx.write(';V')
                                        fileEx.close()
                                        acerto = False 
                                                                  
                                #verifica o fim da relação
                                if(endEnt(truth, contLabels)):
                                    #escreve o fim da relação marcada como uma linha em branco no excell
                                    fileEx = open(dirExc,'a')
                                    fileEx.write('\n')
                                    fileEx.close()

                            contLabels = contLabels + 1
                        
                        saida = open(diretorioTrabalho+'/saidaHarem.xml', 'a')
                        saida.write('\n')
                        saida.close()
            else:
                print str(texto[0]), 'vazio'
                exit()
            saida = open(diretorioTrabalho+'/saidaHarem.xml', 'a')
            saida.write('</DOC>\n')
            saida.close()
            contador += 1
            contBio += contLabels
        else:
            continue
        
        
    return result, contBio,relacoesAcertos, relacoesChutadas
     
#soma duas tabelas de tamanho igual
def soma(A, B):
    if len(A) != len(B):
        raise ValueError
    for i in range(len(A)):
        for j in range(len(A[i])):
            A[i][j] += B[i][j]
    return A


#carrega todos os textos dourados em uma lista no formato
#[('nomeDoTexto.txt',[[({features...},bil),({features...},bil),({features...},bil)],[({features...},bil),({features...},bil),({features...},bil)]])]
def textosTreinamento(pasta):    
    #lista com o nome de todos os arquivos do diretorio
    arquivos = os.listdir(os.path.expanduser(pasta))
    entradas = []
    relacoesTotal = 0
    
    for a in arquivos:
        aux = open(pasta + a).read()
        if(not a.endswith('~')):#evita arquivos temporários
            textos,relacoesTotalAux = processaTags(aux)
            relacoesTotal += relacoesTotalAux
            entradas.append((a,textos))
    return entradas, relacoesTotal

def erroParametro():
    print"""
PARAMETROS DE ENTRADA:
DIRETORIO TREINO - deve conter os textos separados em arquivos .txt
DIRETORIO DE TRABALHO - será criado na execução
QUANTIDADE DE FOLDS - numero de folds utilizadas no processo de cross validation
DIRETORIO MALLET - diretorio que contem a biblioteca MALLET
CATEGORIAS A UTILIZAR (2) - opcional, mas se for informado devem ser exatamente duas
,(VÍRGULA) - obritagorio para extração dos parâmetros
DICIONARIOS - dicionarios a serem utilizados como features

USO:
<opcional>
<interpretador_python_alternativo> ./NERcrf.py DIRETORIO_TREINO DIRETORIO_DE_TRABALHO QUANTIDADE_DE_FOLDS DIRETORIO_MALLET <CATEGORIA_A_UTILIZAR_1 CATEGORIA_A_UTILIZAR_2> , DICIONARIOS...
    """
    exit()

#PARAMETROS DE ENTRADA:
#DIRETORIO TREINO
#DIRETORIO DE TRABALHO
#QUANTIDADE DE FOLDS
#DIRETORIO DO MALLET
#CATEGORIAS A UTILIZAR (2)
#,(VÍRGULA)
#DICIONARIOS
import sys
import os.path
from os import mkdir

argums1 = sys.argv[:sys.argv.index(',')]#argumentos sem os dicionarios
dicionarios = sys.argv[sys.argv.index(',')+1:]#dicionarios de argumentos

if(len(argums1) < 5):
    erroParametro()

#VERIFICA SE OS DIRETORIOS PASSADOS POR PARÂMETROS EXISTEM
print 'confirmando diretorio de treino',argums1[1]
if os.path.exists(argums1[1]):
    print 'OK'
else:
    print 'não existe!'
    erroParametro()

for dic in dicionarios:
    print 'confirmando diretorio de dicionario',dic
    if os.path.exists(dic):
        print 'OK'
    else:
        print 'não existe!'
        erroParametro()

#SALVA ALGUNS PARAMETROS
diretorioTreino = argums1[1]
now = time.localtime()
displaytime = time.strftime("%x %X",now)
diretorioTrabalho = argums1[2]+'_'+str(displaytime.replace('/','-'))#cria o diretorio de trabalho com a data e hora
qtdFolds = int(argums1[3])
diretorioMallet = argums1[4]

print 'confirmando diretorio do MALLET',(diretorioMallet+'/bin/mallethon')
if os.path.exists(diretorioMallet+'/bin/mallethon'):
    print 'OK'
else:
    print 'não existe!'
    erroParametro()

categUtilizadas = list()
if(len(argums1) > 6):#verifica se foram passadas as categorias a serem utilizadas
    categUtilizadas.append(argums1[5])
    categUtilizadas.append(argums1[6])
else:
    categUtilizadas.append('ORG')
    categUtilizadas.append('PES')
    categUtilizadas.append('LOCAL')

#CRIA DIRETORIOS DE TRABALHO
mkdir(diretorioTrabalho)
mkdir(diretorioTrabalho+"/marcados")
for i in range(qtdFolds):
    dir = diretorioTrabalho+'/marcados/iteracao '+str(i+1)
    print 'criando diretorio', dir
    mkdir(dir)
    print 'OK'

#NUMEROS INFORMATIVOS
relacoesTotal = 0
relacoesAcertos = 0
relacoesChutadas = 0

#carrega os textos dourados
entradas, relacoesTotal = textosTreinamento(diretorioTreino+'/')

#informa ao NLTK onde se encontra a biblioteca MALLET
CRFnltk.configMallet(diretorioMallet)

#limpa o arquivos de saida no formato do Segundo HAREM
saida = open(diretorioTrabalho+'/saidaHarem.xml', 'w')
saida.write('<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE colHAREM>\n<colHAREM versao="Segundo_dourada_com_relacoes_14Abril2010">\n')
saida.close()

#variável para contar quantos itens BIO foram identificados na execução do programa
contBio = 0

#número de textos do diretorio
n = len(entradas)         
print n
                                                        
#inicialização da matriz de confusão
resultado = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

#inicialização do conjunto de teste
testset = []


#gera cinco intervalos distintos para teste e treino a cada iteração
for i in range(qtdFolds):
    print (i+1), 'º Iteração'
    #limites do conjunto de teste
    limTest = ((i * n * 1/qtdFolds), (i + 1) * n * 1/qtdFolds)
    testset = entradas[limTest[0]:limTest[1]]


    #definindo os limites do conjunto de treino
    if(limTest[0] == 0):
        trainset = entradas[limTest[1]:]
    elif(limTest[1] >= n):
        trainset = entradas[:limTest[0]]
    else:
        trainset = entradas[:limTest[0]] + entradas[limTest[1]:]

    print 'Teste', '[' , limTest[0] , ':' , limTest[1] , ']'

    print 'Treino',    
    if(limTest[0] == 0):
        print '[',limTest[1], ': ]'
    elif(limTest[1] >= n):
        print '[ :',limTest[0], ']'
    else:
        print '[ :',limTest[0], '] [',limTest[1], ': ]'

    #retorna o resultado da iteração no formato de tabela de confusão e o contador de BIOs
    resultadoAux, contBioAux, relacoesAcertosAux, relacoesChutadasAux = RR(trainset, testset, i+1)
    contBio += contBioAux
    relacoesAcertos += relacoesAcertosAux
    relacoesChutadas += relacoesChutadasAux
    #soma a tabela de confusão da iteração com o geral
    resultado = soma(resultado, resultadoAux)
    #mostra resultado parcial
    print resultadoAux


#encerra o XML no formato do HAREM
saida = open(diretorioTrabalho+'/saidaHarem.xml', 'a')
saida.write('</colHAREM>\n')
saida.close()

now = time.localtime()
displaytime = time.strftime("%x %X",now)
cabecalho = str(contBio)+' marcações BIO\n'+'CROSS 5 FOLDS ' + str(displaytime) + '\n\tB-REL\tI-REL\tO\tRec\tPrec\tF-Measure'
print cabecalho


file = open(diretorioTrabalho+'/result.ods', 'a')
file.write('\n\n\n' + cabecalho + '\n')
file.close()

#itera sobre cada linha da tabela de confusão
for i in range(len(resultado)):
    prec = rec = 0
    #a recebe a soma de todos os itens da coluna da tabela
    a = (sum([resultado[j][i] for j in range(3)]))
    if a != 0:
        #calcula-se a precisão dividindo o que foi marcado certo
        #pelo que deveria ter sido marcado para o item
        prec = float(resultado[i][i]) / a

    #a recebe a soma de todos os itens da linha da tabela
    a = (sum([resultado[i][j] for j in range(3)]))
    if a != 0:
        #calcula-se a abrangência dividindo o que foi marcado certo
        #por tudo que foi marcado para o item
        rec = float(resultado[i][i]) / a

    #calcula a F-Measure
    if(prec+rec == 0):
        continue
    fMeasure = (2*prec*rec)/(prec+rec)

    #linha da tabela de confusão
    saida = str(classe(i))+ '\t'+ str(resultado[i][0])+ '\t'+ str(resultado[i][1])+ '\t'+ str(resultado[i][2])+ '\t'+ str(rec)+ '\t'+ str(prec) + '\t' + str(fMeasure)
        
    print saida
    
    file = open(diretorioTrabalho+'/result.ods', 'a')
    file.write(saida + '\n')
    file.close()
    
#MEDIDAS TOTAIS
prec = float(relacoesAcertos)/relacoesChutadas
rec = float(relacoesAcertos)/relacoesTotal
fmeasure = (2*prec*rec)/(prec+rec)

saida = '\n\n relacoes\n\ttotal:'+str(relacoesTotal)+'\n\tencontradas:'+str(relacoesChutadas)+'\n\tacertos:'+str(relacoesAcertos)+'\n\tprecisão:'+str(prec)+'\n\trecall:'+str(rec)+'\n\tfmeasure:'+str(fmeasure)
print saida    
file = open(diretorioTrabalho+'/result.ods', 'a')
file.write(saida + '\n')
file.close()
