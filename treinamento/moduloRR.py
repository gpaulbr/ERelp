# coding=utf-8

import os
import CRFnltk
import pickle
from KNNUtil import classe


#avaliacao - funcao RR
#EFETUA O RECONHECIMENTO DE RELAÇÕES UTILIZANDO labelled COMO TREINO E test COMO TESTE, iteracao
#INFORMA EM QUAL FOLD SE ENCONTRA O PROCESSO DE CROSS VALIDATION
def RR(diretorioTrabalho, diretorioModelo, crossValidation, labelled, test, iteracao):
    #relações acertadas pelo sistema de acordo com a CD
    linha = 0
    relacoesAcertos = 0
    nrAcertos = 0
    nrparcial = 0
    nrtotal = 0
    orgorg = 0
    orglocal = 0
    orgpessoa = 0
    orgorgp = 0
    orglocalp = 0
    orgpessoap = 0
    nrEncontrados = 0
    nrEntrada = 0
    #relações descritas pelo sistema
    relacoesChutadas = 0
    
    #tabela de confusão da iteração
    result = [[0, 0], [0, 0]]

    #variável lab representa apenas valores válidos de labels, [[sent1],[sent2]...[sentN]]
    lab = []
    for label in labelled:
        if label == None:
            continue
        if label != []:
            for s in label[1]:
                if(s != []):
                    lab.append(s)

    #chamada do CRF para GERACAO DO MODELO no MALLET
    #treina ou abre o já treinado CRF
    #Obs.:Mudar na classe CRFnltk para não gravar sobre modelo gerado
    diretorioModeloAtual = diretorioModelo
    if crossValidation:
        diretorioModeloAtual = diretorioModelo+'_'+str(iteracao)
    if not os.path.exists(diretorioModeloAtual):
        print 'Modelo não encontrado, criando novo modelo', diretorioModeloAtual
        crf = CRFnltk.CRFTrain(lab, iteracao)
        pickle.dump(crf,open(diretorioModeloAtual,'w'))
    else:
        print 'Modelo encontrado:', diretorioModeloAtual, '. Utilizando modelo já existente'
        crf = pickle.load(open(diretorioModeloAtual,'r'))

    #variável para conter os resultados do CRF
    labels = []

    #arquivo para salvar em formato de Tabela
    dirExc = diretorioTrabalho+'/result_' + str(iteracao) + 'it.ods'
    tabeladescritores = open(diretorioTrabalho+'/tabela_descritores.ods','a')
    #limpa arquivof
    fileEx = open(dirExc,'w')
    fileEx.write('')
    fileEx.close()

    #contador de intens BILOU da iteração
    contBio = 0

    #itera sobre o conjunto de teste
    contador = 0
    descritorEntrada = open(diretorioTrabalho+'/Descritor_Entrada.txt','a')
    descritor = open(diretorioTrabalho+'/Descritor_Saida.txt','a')
    descritorCerto = open(diretorioTrabalho+'/DescritorCerto_Saida.txt','a')
    listadescritor = open(diretorioTrabalho+'/Lista_descritor.txt','a')
    listachaves = open(diretorioTrabalho+'/Lista_chaves.txt', 'a')
    for texto in test:
        if texto == None:
            continue
        if texto != []:
            #inicializa vetor da marcação correta do BIO
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
            #aplica o modelo crf nos textos de teste - tagged        
            labels = CRFnltk.CRF_prediction(crf, tagged)#toda a saida etiquetada pelo CRF
            
            #contador de labels
            contLabels = 0
            
            #limpa o arquivo com as marcações
            dir = diretorioTrabalho+'/marcados/iteracao ' + str(iteracao) + '/' + str(texto[0])
            file = open(dir,'w')
            file.write('')
            file.close()
	    #escreve o titulo dos textos no arquivo dos descritores
            if(linha == 0):
            	descritor.write(texto[0] + '\n')
            	descritorCerto.write(texto[0] + '\n')
	    elif(linha == 1):
            	descritor.write('\n' + texto[0] + '\n')
            	descritorCerto.write('\n' + texto[0] + '\n')
	    linha = 1
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
			verd = True
			parc = False
			num = 0
			num2 = 0
                        sinal = 0
			sinal2 = 0
                        sInicio = s[0]#primeira palavra da sentença
			sFim = s[-1]#ultima palavra da sentença
                        acerto = True#é acerto até que se prove o contrário
                        mostraErrados = False#variavel escrever as EN encontradas por engano pelo sistema na saida excell
                        
                        #itera sobre as palavras da sentença
                        for w in s:
                            #escreve no arquivo com as marcações
                            file = open(dir,'a')
                            file.write(str(w[0]['palavra']+" ") + '<' + str(w[0]['POSTag']) + ',' + labels[contLabels] + '> ')
                            file.close()
	
                            #incrementa a tabela de confusão
                            result[classe(truth[contLabels])][classe(labels[contLabels])] += 1
                ############# Numero total da entrada ########################
			    #faz a contagem da entrada e escreve no descritor de entrada primeira palavra+descritores+ultima palavra
			    if(truth[contLabels] == 'REL' and sinal2 == 0):
			    	nrEntrada += 1#contagem
                                descritorEntrada.write('[+'+sInicio[0]['palavraOriginal'] +"+, ")#primeira palavra
				sinal2 = 1
			    if(truth[contLabels] == 'REL' and sinal2 == 1):
			    	descritorEntrada.write(w[0]['palavra']+" ")#descritores
			    if(w[0]['palavra'] == sFim[0]['palavra'] and sinal2 == 1):
				descritorEntrada.write('; +' + sFim[0]['palavraOriginal'] +'+]' + sInicio[0]['clas'] +'-'+sFim[0]['clas'] +'\n')#ultima palavra
				sinal2 = 0
                ##############################################################
                ############# Numero de encontrados ##########################
			    #faz a contagem dos encontrados e escreve no descritor dos encontrados a primeira palavra + descritores + ultima palavra
			    if(labels[contLabels] == 'REL' and sinal == 0):
				 nrEncontrados += 1#contagem
				 descritor.write('[+'+sInicio[0]['palavraOriginal'] + "+, ")    #primeira palavra
				 sinal = 1
			    if(labels[contLabels] == 'REL' and sinal == 1):
				 descritor.write(' '+w[0]['palavra'])                           #descritores
			    if(w[0]['palavra'] == sFim[0]['palavra'] and sinal == 1):
				 descritor.write('; +'+sFim[0]['palavraOriginal'] +'+]\n')      #ultima palavra
				 sinal = 0
                ##############################################################
                            if(labels[contLabels] == 'REL'):#incrementa o número de relações encontradas pelo sistema
                                relacoesChutadas += 1
			    if(labels[contLabels] == 'REL' and truth[contLabels] == 'O'):#verifica se foi acerto parcial
				parc = True
			    if(labels[contLabels] == 'O' and truth[contLabels] == 'REL'):#verifica se foi acerto parcial
				parc = True
                ############ Numero de Acertos ################################
			    #faz a contagem dos acertos e escreve no descritor de acertos a primeira palavra+descritor+ultima palavra
			    if(labels[contLabels] == 'REL' and truth[contLabels] == 'REL' and num == 0):
				nrAcertos += 1 #contagem dos acertos
				tabeladescritores.write(sInicio[0]['palavra']+'('+sInicio[0]['clas']+')'+',')
                                listadescritor.write('[+'+sInicio[0]['palavraOriginal']+ '+,')
				listachaves.write('[+'+sInicio[0]['palavraOriginal']+'('+sInicio[0]['clas']+ ')+,')
			 	descritorCerto.write(sInicio[0]['palavraOriginal'] + '(' + sInicio[0]['clas'] + ')' + " ") #primeira palavra+(classificação)
				num = 1
				#faz a verificação da sentença, se é ORG-ORG ou ORG-LOCAL ou ORG-PESSOA
			    if(parc == True and num2 == 0 and num != 0):
				nrparcial += 1#contagem de acertos parciais
				num2 = 1
			    if(labels[contLabels] == 'REL' and truth[contLabels] == 'REL' and num == 1):
				descritorCerto.write(w[0]['palavra'] + " ")#descritores
				listadescritor.write(' '+w[0]['palavra']+" ")
				listachaves.write(' '+w[0]['palavra']+" ")
				tabeladescritores.write(w[0]['palavra']+' ')
			    if(w[0]['palavra'] == sFim[0]['palavra'] and num == 1):
				descritorCerto.write(sFim[0]['palavraOriginal'] + '(' + sFim[0]['clas'] + ')')              #ultima palavra+(classificação)
				listadescritor.write('; +'+sFim[0]['palavraOriginal']+'+]')
				listachaves.write('; +'+sFim[0]['palavraOriginal']+'('+sFim[0]['clas']+')+]')
				tabeladescritores.write(','+sFim[0]['palavra']+'('+sFim[0]['clas']+')'+'\n')
				num = 2
			    if(parc == True and num == 2):
				descritorCerto.write('PARCIAL'+'\n')    #escreve se a sentença é acerto parcial
				listachaves.write(sInicio[0]['clas'] + '-'+sFim[0]['clas']+ ' PARCIAL'+'\n')				
				listadescritor.write(sInicio[0]['clas'] + '-'+sFim[0]['clas']+ ' PARCIAL'+'\n')
				if(sInicio[0]['clas'] == 'ORG' and sFim[0]['clas'] == 'ORG'):
					orgorgp += 1
				if(sInicio[0]['clas'] == 'ORG' and sFim[0]['clas'] == 'LOCAL'):
					orglocalp += 1
				if(sInicio[0]['clas'] == 'LOCAL' and sFim[0]['clas'] == 'ORG'):
					orglocalp += 1
				if(sInicio[0]['clas'] == 'ORG' and sFim[0]['clas'] == 'PES'):
					orgpessoap += 1
				if(sInicio[0]['clas'] == 'PES' and sFim[0]['clas'] == 'ORG'):
					orgpessoap += 1
			    if(parc == False and num == 2):
				descritorCerto.write('TOTAL'+'\n')  #escreve se a sentença é acerto total
				listadescritor.write(sInicio[0]['clas'] +'-'+sFim[0]['clas'] +' TOTAL'+'\n')
				listachaves.write(sInicio[0]['clas'] +'-'+sFim[0]['clas'] +' TOTAL'+'\n')
				if(sInicio[0]['clas'] == 'ORG' and sFim[0]['clas'] == 'ORG'):
					orgorg += 1
				if(sInicio[0]['clas'] == 'ORG' and sFim[0]['clas'] == 'LOCAL'):
					orglocal += 1
				if(sInicio[0]['clas'] == 'LOCAL' and sFim[0]['clas'] == 'ORG'):
					orglocal += 1
				if(sInicio[0]['clas'] == 'ORG' and sFim[0]['clas'] == 'PES'):
					orgpessoa += 1
				if(sInicio[0]['clas'] == 'PES' and sFim[0]['clas'] == 'ORG'):
					orgpessoa += 1

                ################################################################                              
                            if(labels[contLabels] == 'REL' and truth[contLabels] == 'O'):   #uma entidade encontrada por engano
                                mostraErrados = True
                            if(mostraErrados):  #mostra toda a EN marcada por engano
                                #escreve no excell	
                                fileEx = open(dirExc,'a')
                                fileEx.write(str(w[0]['palavra']) + '<' + str(w[0]['POSTag']) + ','+ ',' + labels[contLabels] + '>;'+
                                             str(w[0]['palavra']) + '<' + str(w[0]['POSTag']) + ','+ ',' + truth[contLabels] + '>\n')
                                if labels[contLabels] != truth[contLabels]:
                                    acerto = False
                                fileEx.close()
                                
                            else:   #fim da EN marcada por engano
                                mostraErrados = False

                            #escreve no arquivo tabela o resultado do sistema e o correto
                            if(truth[contLabels] == 'REL' and labels[contLabels] == 'REL'): #parte de uma relação segundo a CD
                                acerto = True  #a principio é acerto
				relacoesAcertos += 1
                                #escreve a palavra na tabela
                                fileEx = open(dirExc,'a')
                                fileEx.write(str(w[0]['palavra']) + '<' + str(w[0]['POSTag']) + ','+ ',' + labels[contLabels] + '>;'+
                                             str(w[0]['palavra']) + '<' + str(w[0]['POSTag']) + ','+ ',' + truth[contLabels] + '>\n')
                                fileEx.write(';V')
				fileEx.write('\n')
				fileEx.close()                                                               

                            contLabels = contLabels + 1
                            
            else:
                print str(texto[0]), 'vazio'
                exit()
            contador += 1
            contBio += contLabels
        else:
            continue
    tabeladescritores.close()
    descritorEntrada.close()    
    descritor.close()   
    descritorCerto.close()
    listadescritor.close()
    listachaves.close()    
    return orgorgp, orglocalp, orgpessoap, orgorg, orglocal, orgpessoa, nrEntrada, nrEncontrados, nrparcial, nrtotal, nrAcertos, result, contBio,relacoesAcertos, relacoesChutadas
    #final da funcao RR - reconhecimento de relacoes