# coding=utf-8

import re

def processaTags(diretorioTrabalho, categUtilizadas, trainingTweets, dicionariosFormat):    #retorna lista no formato
    expressao2 = re.compile(r'\[(.*)\]', re.S)          #expressao regular para encontra a forma canônica da palavra
    expressao3 = re.compile(r'<([^\s]*)>', re.S)        #expressao regular para encontrar a marcação semântica da palavra
                                                        #need re
    #INCIALIZAÇÕES DE VARIÁVEIS                         #categUtilizadas
    labelled = list()  #retorno formatado do arquivo
    palavra = ''
    bil = ''
    classe = ''
    semanticNoun = ''
    relacoesTotal = 0
    # variáveis de controle para extrair somente a relação
    extrai = False
    extrai2 = False

    p = re.compile(r'\$S-[0-9]*')       #expressao para dividir textos de um arquivo

    frases = p.split(trainingTweets)    #frases recebe a lista de sentenças do arquivo
                                        #divide o arquivo por sentenças
    for frase in frases:                #limpa frases extraidas erradas
        if frase == '':
            frases.remove('')

    frases = [frase.replace('</s>','') for frase in frases] #limpa marcação desnecessária

    #execucao por sentenca
    for f in frases:
        p = list()
        vetBio = list()         #vetor contendo os itens bil do texto
        #quebra da sentenca por palavra - eh executado para cada palavra
        tokens = f.split('\n')  #tokens é um vetor das palavras

        #inicio da execucao por palavra
        for t in tokens:

            classe = ''         #POS da palavra
            sintatica = ''      #marcação sintática do palavra
            semanticNoun = ''   #HPROF ou HTIT

            classificacao = 'nulo'  #classificação da EN

            gerarFeatures = False   #se devem ser geradas features sobre a palavra atual
            bole = False            #variavel para extrair sintatica e POS
            bole2 = False           #variavel para extrair sintatica e POS
	    numdicionario = 0
	    estanodicionario = False
	    salvadic = 0

            if(t != ''):                                #verifica se a linha não está vazia
                splited = t.split()                     #splited é um vetor com as informações da palavra
                if(len(splited) > 2):                   #verifica se a linha contém informação de classificação - se eh uma EN
                    if splited[-2] in categUtilizadas:  #verifica se a entidade em questão está entre as procuradas
                        extrai = not extrai             #seta a EN como um delimitador de inicio ou final
                        classificacao = splited[-2]     #guarda a classificação da EN

                gerarFeatures = extrai2 or extrai       #só gera features entre as entidades incluindo-as
                #caso nao queira que gere feature para as ENs trocar or por and

               # if(len(splited) < 2):#verificação de erros de marcação
               #     print 'erro de formatação'
                 #   print splited
                  #  exit()
                if(len(splited) == 2):                  #token é uma pontuação
                    palavra = ''
                    for letra in t[1:]:                 #salva a pontuação como palavra
                        if letra != ' ':
                            palavra += letra
                        else:
                            break
                    classe = palavra                    #não há POS ANTES ESTAVA 'NULO' PARA POS PONTUACAO
                    sintatica = 'nulo'                  #sem informação sintática
                    semantica = 'nulo'                  #sem informação semantica
                    semanticNoun = 'nulo'               #sem informação semantica
                    bil = t.split()[1]
                else:   #token é uma palavra

                    if len(expressao3.findall(t)) == 0: #não há algumas informações na linha de inf. semantica
                        semantica = 'nulo'              #sem informação semantica
                        semanticNoun = 'nulo'           #sem informação semantica



                        for tk in splited:              #utiliza marcações do CG do Palavras para formar coletar as informações
                            if('[' in tk):
                                bole3 = True
                            if(']' in tk and bole3):
                                bole = True
                            if('[' not in tk and ']' not in tk and bole and not bole2):
                                classe = tk
                                bole2 = True
                            if('@' in tk and bole2):
                                sintatica = tk
                    else:   #linha completa com todas as marcações do palavras
                        semantica = expressao3.findall(t)[0]

                        if('<Hprof>' in t):     #para semanticNoun só import hprof ou htit
                            semanticNoun = 'hprof'
                        elif('<Htit>' in t):
                            semanticNoun = 'htit'
                        else:
                            semanticNoun = 'nulo'

                        for tk in t.split():    #utiliza marcações do palavras para coletar as informações de POS e sintatica
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
                    if(not t.startswith('$')):                  #verifica se não é apenas uma pontuação
                        if(len(expressao2.findall(t)) == 0):    #alguma falha de anotação
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
                if(semanticNoun == ''):    #falha de anotação
                    print t, 'não foi encontrado semanticNoun'
                    exit()

                #GERACAO DO VETOR DE ENTRADA de cada palavra
                items = list()
                items.extend([('palavra',palavra), ('classe',classe), ('semantica',semantica),
                              ('sintatica',sintatica),('semanticNoun',semanticNoun),
                              ('classificacao',classificacao),('gerarFeatures',gerarFeatures)])

                #indicacao do dicionario(s) no vetor de entrada
		for j in dicionariosFormat:
			for k in j:
				k = k.replace('Í','í')
				k = k.replace('Ì','ì')
				k = k.replace('Á','á')
				k = k.replace('À','à')
				k = k.replace('Ã','ã')
				k = k.replace('Â','â')
				k = k.replace('É','é')
				k = k.replace('Ê','ê')
				k = k.replace('É','é')
				k = k.replace('Ó','ó')
				k = k.replace('Õ','õ')
				k = k.replace('Ô','ô')
				k = k.replace('Ú','ú')
				if(palavra==k):
					#listadic.write(str(palavra)+'=='+str(k)+'\n')
					estanodicionario = True
					salvadic = numdicionario
			numdicionario += 1
		if(estanodicionario == True):
			items.append((('dicionario'+str(salvadic)),'sim'))
		elif(estanodicionario == False):
			items.append((('dicionario'+str(salvadic)),'nao'))
                #for i in range(len(dicionariosFormat)):
                    #if(palavra.lower() in dicionariosFormat[i]):
                        #items.append((('dicionario'+str(i)),'sim'))
                    #else:
                        #items.append((('dicionario'+str(i)),'nao'))

                itemsDict = dict(items)

                #vetor de entrada da sentenca []
                p.append((itemsDict))   #valores do vetor de entrada

                #vetor com o BIO de toda a sentenca
                vetBio.append(bil)
                if(bil == 'REL'):       #agora só verifica se é REL
                    relacoesTotal += 1

                extrai2 = extrai        #seta o inicio ou final da descricao
                #final do laco da execucao por palavra

        #geracao dos arquivos com os vetores de entrada, para cada sentenca eh escrita uma linha no arquivo
        if(p != []):
            file = open(diretorioTrabalho+'/vetorEntrada.txt','a')
            file.write(str(p)+'\n')
            file.close()

            file = open(diretorioTrabalho+'/vetorEntradaBio.txt','a')
            file.write(str(vetBio)+'\n')
            file.close()

            #GERACAO DAS FEATURES - CHAMADA DA FUNCAO extractFeatures
            p2 = list()    #vetor com as features das palavras
            #verficacao se as features devem ser geradas ou nao para a palavra
            for i in range(len(p)):
                if(p[i]['gerarFeatures']):#soh gera features qdo setado true o parametro gerarFeatures
                	p2.append((extractFeatures(diretorioTrabalho, p, i), vetBio[i]))
            labelled.append(p2)
            # print 'P1---------------------------------'
            # for i in p:
            #     print i
            # print 'P2---------------------------------'
            # for i in p2:
            #     print i
            # print 'labelled---------------------------'
            # print labelled

    return labelled, relacoesTotal

#funcao de extracao das features
def extractFeatures(diretorioTrabalho, tweet, indexWord):
    features = [] #conjunto de features da palavra
    word = tweet[indexWord]['palavra']#propria palavra

    POSLongRangeSemEN  = ""  # valor para a feature de longo alcance sem as ENs
    POSLongRangeComEN  = ""  # valor para a feature de longo alcance com as ENs

    if not word == '':

        n_words = len(tweet)#numero de palavras da sentença

        limNucleos = []#conjunto que conterá os limites do núcleo da sentença

        provaveisApp = list()  # provaveis inicios de apostos no formato ('<palavra de inicio>',<posição de inicio>)
        limitsApp = list()  # limites do aposto
        nucleoApp = False  # verifica se a palavra atual é o núcleo do aposto
        tipoFrase = 'nulo'  # tipo de frase analisada dentre os definidos
        verbo = False  # se a sentença possui um verbo
        substantivo = False  # se a sentença possui um substantivo
        adverbio = 'nulo'  # padrao de adverbio
        objDireto = False  # verifica se eh objeto direto

        tamanho = 0  # tamanho do segmento

        #variavel para extrair features de longo alcance
        entreENs = False

        for i in range(len(tweet)):  # laço percorre toda a sentença

            #formação das features de longo alcance
            if(tweet[i]['gerarFeatures']):  # setado para todas as palavras com gerarFeatures= true
                POSLongRangeComEN += tweet[i]['classe'] + " "

                if(i < len(tweet)-1):  # se a palavra não é a ultima
                    if(not tweet[i+1]['gerarFeatures']):  # olha para a proxima palavra, se gerarFeatures=false, a atual eh arg2
                        entreENs = False  # arg2 nao sera incluido
                if(entreENs):
                    POSLongRangeSemEN += tweet[i]['classe'] + " "
                if(i > 0):  # se a palavra não é a primeira
                    if(not tweet[i-1]['gerarFeatures']):  # olha para a palavra anterior
                        entreENs = True

            #verifica se ocorre aposto e delimitacao do aposto
            if(len(tweet)-1 > i):  # só entra se esta não for a última palavra da sentença
                if('—' == tweet[i]['palavra'] or ',' == tweet[i]['palavra'] or '(' == tweet[i]['palavra']):  # para definir os limites do aposto
                    encontrouAposto = False  # variavel de controle para limpar o provaveisApp
                    for (palavra, posicao) in provaveisApp:  # pesquisa por um encerramento de aposto
                        if(palavra == tweet[i]['palavra'].replace('(', ')')):
                            limitsApp.append((posicao+1, i-1))
                            encontrouAposto = True
                            break
                    if(encontrouAposto):  # foi delimitado um aposto e deve ser removido dos provaveis
                        provaveisApp = list()
                    else:  # foi encontrado um candidato a inicio de aposto
                        if((tweet[i+1]['classe'] == 'DET' and (tweet[i+2]['classe'] == 'N' or tweet[i+2]['classe'] == 'PERS'))
                           or (tweet[i+1]['classe'] == 'N' or tweet[i+1]['classe'] == 'PERS')):  # verifica se a posição corresponde a um inicio de aposto de acordo com a regra do português
                            provaveisApp.append((tweet[i]['palavra'], i))
                        if((tweet[i+1]['classe'] == 'DET' and (tweet[i+2]['classe'] == 'N' or tweet[i+2]['classe'] == 'PERS') and i+2 == indexWord)
                           or ((tweet[i+1]['classe'] == 'N' or tweet[i+1]['classe'] == 'PERS') and i+1 == indexWord)):  # verifica se a palavra atual é o núcleo
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

            if(tweet[i]['gerarFeatures']):#verifica se o parametro gerar feature eh True
                tamanho += 1
		#feature do tamanho do segmento - EN1 + descritor de relacao + EN2
        features.append(('tamanho',tamanho))

        #aplicacao da feature de longo alcance
        features.append(('POSlongoAlcanceComEN',POSLongRangeComEN))#incluindo as ENS na sequencia
        features.append(('POSlongoAlcanceSemEN',POSLongRangeSemEN))#sem as ENS na sequencia

        #feature se a palavra atual eh nucleo do aposto
        if nucleoApp:
            features.append(('nucleoAposto','sim'))
        else:
            features.append(('nucleoAposto','nao'))

       #feature da palavra atual estar ou nao contida num aposto
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
        #features aplicadas a palavra atual
        features.append(('palavra',word.lower()))
        features.append(('POSTag',tweet[indexWord]['classe'].lower()))
        features.append(('phraseTag',tweet[indexWord]['sintatica']))
        features.append(('semanticNoun',tweet[indexWord]['semanticNoun']))
        features.append(('clas',tweet[indexWord]['classificacao']))
        features.append(('palavraOriginal',word)) #classe NER

        #DICIONARIOS
        cont = 0
        for i in tweet[indexWord]:
            if('dicionario' in i):#verifica se tem um dicionario em uso
                cont = cont+1
                features.append((i,tweet[indexWord][i]))#atribui sim/nao caso a palavra esteja (ou nao) contida no dicionario corresponde


        #VERIFICAÇÃO FEATURES BASEADAS EM PADRÕES
        if(indexWord < len(tweet)-1):
            if(tweet[indexWord]['classe'] == 'V'):
                verbo = True
            if(verbo and tweet[indexWord+1]['classe'] == 'DET'):
                tipoFrase = 'verbArtigo'
            elif(verbo and tweet[indexWord+1]['classe'] == 'PRP'):
                tipoFrase = 'verbPrep'
                if(indexWord < len(tweet)-2):
            		if(tweet[indexWord+2]['classe'] == 'DET'):
            			tipoFrase = 'verbPrepDet'
            if(tweet[indexWord]['classe'] == 'N'):
                substantivo = True
            if(substantivo and tweet[indexWord+1]['classe'] == 'PRP'):
                tipoFrase = 'subsPrep'

		#feature VERBO + ARTIGO
        if(tipoFrase == 'verbArtigo'):
            features.append(('verbArtigo','sim'))
            features.append(('verbPrep','nao'))
            features.append(('verbPrepDet','nao'))
            features.append(('subsPrep','nao'))
        #feature VERBO + PREP
        elif(tipoFrase == 'verbPrep'):
            features.append(('verbArtigo','nao'))
            features.append(('verbPrep','sim'))
            features.append(('verbPrepDet','nao'))
            features.append(('subsPrep','nao'))
             #feature VERBO + PREP + DET
        elif(tipoFrase == 'verbPrepDet'):
            features.append(('verbArtigo','nao'))
            features.append(('verbPrep','nao'))
            features.append(('verbPrepDet','sim'))
            features.append(('subsPrep','nao'))
        #feature SUBSTANTIVO + PREP
        elif(tipoFrase == 'subsPrep'):
            features.append(('verbArtigo','nao'))
            features.append(('verbPrep','nao'))
            features.append(('verbPrepDet','nao'))
            features.append(('subsPrep','sim'))
        else:
            features.append(('verbArtigo','nao'))
            features.append(('verbPrep','nao'))
            features.append(('verbPrepDet','nao'))
            features.append(('subsPrep','nao'))

        #feature de verbo binária
        if(tweet[indexWord]['classe'] == 'V'):
            features.append(('verbo','sim'))
        else:
            features.append(('verbo','nao'))

        #verificacao da feature de ADVERBIO
        if(tweet[indexWord]['classe'] == 'ADV'): #verifica se a palavra eh um adverbio
        	adverbio = 'adv'
        	if(indexWord < len(tweet)-1):
        		if(tweet[indexWord+1]['classe'] == 'PRP'): #adverbio seguido de Prep
        			adverbio = 'advPrep'
        			if(indexWord < len(tweet)-2):
        				if(tweet[indexWord+2]['classe'] == 'DET'): #adverbio seguido de Prep+Det
        					adverbio = 'advPrepDet'

        #feature ADV
        if(adverbio == 'adv'):
            features.append(('adv','sim'))
            features.append(('advPrep','nao'))
            features.append(('advPrepDet','nao'))

        #feature ADV + PREP
        elif(adverbio == 'advPrep'):
            features.append(('adv','nao'))
            features.append(('advPrep','sim'))
            features.append(('advPrepDet','nao'))

         #feature ADV + PREP + DET
        elif(adverbio == 'advPrepDet'):
            features.append(('adv','nao'))
            features.append(('advPrep','nao'))
            features.append(('advPrepDet','sim'))
        else:
         	features.append(('adv','nao'))
         	features.append(('advPrep','nao'))
         	features.append(('advPrepDet','nao'))

         #verificacao da feature de OBJETO DIRETO
        if(indexWord < len(tweet)-1):
        	if(tweet[indexWord]['classe'] == 'V' and tweet[indexWord]['sintatica'] == '@<ACC'): #verifica se eh um verbo seguido de obj direto
        		objDireto = True
        	elif(indexWord < len(tweet)-2):
        		if(tweet[indexWord]['classe'] == 'V' and tweet[indexWord+1]['classe'] == 'DET' and tweet[indexWord+2]['sintatica'] == '@<ACC'): #verifica se eh um verbo seguido de Det + obj direto
        			objDireto = True

        #feature de OBJETO DIRETO
        if(objDireto == True):
            features.append(('objetoDireto','sim'))
        else:
            features.append(('objetoDireto','nao'))


        #FEATURE DE NÚCLEO DA SENTENÇA
        if((tweet[indexWord]['classe'] == 'N' or tweet[indexWord]['classe'] == 'PROP' or
                tweet[indexWord]['classe'] == 'PERS' or tweet[indexWord]['classe'] == 'NUM') and
                'SUBJ' in tweet[indexWord]['sintatica']):
            features.append(('nucleo','sim'))
        else:
            features.append(('nucleo','nao'))


        #FEATURES DE JANELA
        #se há palavra anterior a atual
        if indexWord > 0:#            if(tweet[indexWord-1]['classificacao'] != 'null'):#verifica se a palavra não é uma das EN de relação#                features.append(('prevW',tweet[indexWord-1]['classificacao'].lower()))#            else:#                features.append(('prevW',tweet[indexWord-1]['palavra'].lower()))
            features.append(('prevClas',tweet[indexWord-1]['classificacao']))#para incluir a classificação NER como uma nova feature #
            features.append(('prevW',tweet[indexWord-1]['palavra'].lower())) #
            features.append(('prevT',tweet[indexWord-1]['classe'].lower())) #POS #
            features.append(('next0CT',tweet[indexWord-1]['classe']+' '+tweet[indexWord]['classe']))#POS palavras consecutivas #
            features.append(('prevPT',tweet[indexWord-1]['sintatica'])) #
            features.append(('prev0CPT',tweet[indexWord-1]['sintatica']+' '+tweet[indexWord]['sintatica']))#sintatica palavras consecutivas #
            features.append(('next0CW',tweet[indexWord-1]['palavra']+' '+tweet[indexWord]['palavra']))#palavras consecutivas #
            features.append(('prevSemanticNoun',tweet[indexWord-1]['semanticNoun'])) #

            #feature baseada no verbo - se a palavra anterior eh um verbo
            if(tweet[indexWord-1]['classe'] == 'V'):
                features.append(('prevVerbo','sim'))
            else:
                features.append(('prevVerbo','nao'))

			#feature baseada no aposto -verifica se a palavra anterior estah num aposto
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
        if indexWord > 1:#            if(tweet[indexWord-2]['classificacao'] != 'null'):#verifica se a palavra não é uma das EN de relação#                features.append(('prev2W',tweet[indexWord-2]['classificacao'].lower()))#            else:#           	features.append(('prev2W',tweet[indexWord-2]['palavra'].lower()))
			#features aplicadas a palavra  p-2
            features.append(('prev2Clas',tweet[indexWord-2]['classificacao']))#para incluir a classificação NER como uma nova feature
            features.append(('prev2W',tweet[indexWord-2]['palavra'].lower())) #
            features.append(('prev2T',tweet[indexWord-2]['classe'].lower())) #
            features.append(('prev2PT',tweet[indexWord-2]['sintatica'])) #
            features.append(('prev1CT',tweet[indexWord-2]['classe']+' '+tweet[indexWord-1]['classe'])) #
            features.append(('prev1CPT',tweet[indexWord-2]['sintatica']+' '+tweet[indexWord-1]['sintatica'])) #
            features.append(('prev1CW',tweet[indexWord-2]['palavra']+' '+tweet[indexWord-1]['palavra'])) #
            features.append(('prev2SemanticNoun',tweet[indexWord-2]['semanticNoun'])) #

			#verifica se a palavra p-2 eh um verbo
            if(tweet[indexWord-2]['classe'] == 'V'):
                features.append(('prev2Verbo','sim'))
            else:
                features.append(('prev2Verbo','nao'))

            #verifica se a palavra p-2 está dentro de um aposto
            incluidaAposto = False
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

        #verifica se há palavra posterior a atual p+1
        if indexWord < n_words-1:#            if(tweet[indexWord+1]['classificacao'] != 'null'):#verifica se a palavra não é uma das EN de relação#                features.append(('nextW',tweet[indexWord+1]['classificacao'].lower()))#            else:#                features.append(('nextW',tweet[indexWord+1]['palavra'].lower()))
            features.append(('nextClas',tweet[indexWord+1]['classificacao']))#para incluir a classificação NER como uma nova feature
            features.append(('nextW',tweet[indexWord+1]['palavra'].lower()))
            features.append(('nextT',tweet[indexWord+1]['classe'].lower()))
            features.append(('next1CT',tweet[indexWord]['classe']+' '+tweet[indexWord+1]['classe'])) #
            features.append(('nextPT',tweet[indexWord+1]['sintatica']))
            features.append(('next1CPT',tweet[indexWord]['sintatica']+' '+tweet[indexWord+1]['sintatica']))
            features.append(('next1CW',tweet[indexWord]['palavra']+' '+tweet[indexWord+1]['palavra'])) #
            features.append(('nextSemanticNoun',tweet[indexWord+1]['semanticNoun']))

            #verifica se a palavra p+1 eh um verbo
            if(tweet[indexWord+1]['classe'] == 'V'):
                features.append(('nextVerbo','sim'))
            else:
                features.append(('nextVerbo','nao'))

            #verifica se a palavra p+1 está dentro de um aposto
            incluidaAposto = False
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
        if indexWord < n_words-2:#            if(tweet[indexWord+2]['classificacao'] != 'null'):#verifica se a palavra não é uma das EN de relação#                features.append(('next2W',tweet[indexWord+2]['classificacao'].lower()))#            else:#                features.append(('next2W',tweet[indexWord+2]['palavra'].lower()))
            features.append(('next2Clas',tweet[indexWord+2]['classificacao']))#para incluir a classificação NER como uma nova feature
            features.append(('next2W',tweet[indexWord+2]['palavra'].lower()))
            features.append(('next2T',tweet[indexWord+2]['classe'].lower()))
            features.append(('next2CT',tweet[indexWord+1]['classe']+' '+tweet[indexWord+2]['classe']))
            features.append(('next2PT',tweet[indexWord+2]['sintatica']))
            features.append(('next2CPT',tweet[indexWord+1]['sintatica']+' '+tweet[indexWord+2]['sintatica']))
            features.append(('next2CW',tweet[indexWord+1]['palavra']+' '+tweet[indexWord+2]['palavra']))
            features.append(('next2SemanticNoun',tweet[indexWord+2]['semanticNoun']))

            #verifica se a palavra p+2 eh um verbo
            if(tweet[indexWord+2]['classe'] == 'V'):
                features.append(('next2Verbo','sim'))
            else:
                features.append(('next2Verbo','nao'))

            #verifica se a palavra p+2 está dentro de um aposto
            incluidaAposto = False
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

    resul = dict(features) #criacao do vetor de feature para cada palavra

    file = open(diretorioTrabalho+'/vetorFeatures.txt','a')
    file.write(str(resul)+'\n')
    file.close()

    #fechamento do vetor de feature para cada palavra
    return resul

