# -*- coding: utf-8 -*-

import math
import operator
import re
import os
import time
import CRFnltk
import KNNUtil
import sys
import moduloErros
import moduloChaves
import moduloRR
import moduloAux

#inicio da execucao
start_time = time.time()
argums1 = sys.argv[:sys.argv.index(',')]        #argumentos sem os dicionarios
dicionarios = sys.argv[sys.argv.index(',')+1:]  #dicionarios de argumentos

moduloAux.deletaModelos()                                 #Função que deleta os arquivos modelo_X na pasta modelos

if(len(argums1) < 8):
    moduloAux.erroParametro()

#VERIFICA SE OS DIRETORIOS PASSADOS POR PARÂMETROS EXISTEM
print 'confirmando diretorio de treino',argums1[1]
if os.path.exists(argums1[1]):
    print 'OK'
else:
    print 'não existe!'
    moduloAux.erroParametro()
print 'confirmando diretorio de teste',argums1[2]
if os.path.exists(argums1[2]):
    print 'OK'
else:
    print 'não existe!'
    moduloAux.erroParametro()

modeloExiste = False
diretorioModelo = re.findall('^.*/', sys.argv[3])[0]    #diretorioModelo recebe apenas o diretorio onde se encontra o mdelo especificado
print 'confirmando diretorio', diretorioModelo          #informando ou mostrando na tela ao usuario que esta verificando a existencia do diretorio.
if os.path.exists(diretorioModelo):                     #verificando a existencia do diretorio.
    print 'OK'
    if os.path.exists(sys.argv[3]):
        modeloExiste = True
        print 'modelo encontrado'
    else:
        modeloExiste = False
        print 'modelo não encontrado, um novo será criado'
else:
    print 'não existe!'
    moduloAux.erroParametro()

for dic in dicionarios:
    print 'confirmando diretorio de dicionario',dic
    if os.path.exists(dic):
        print 'OK'
    else:
        print 'não existe!'
        moduloAux.erroParametro()

#SALVA ALGUNS PARAMETROS
diretorioTreino = argums1[1]
diretorioTeste = argums1[2]
diretorioModelo = sys.argv[3]
now = time.localtime()
displaytime = time.strftime("%x %X",now)
diretorioTrabalho = argums1[4]+'_'+str(displaytime.replace('/','-'))    #cria o diretorio de trabalho com a data e hora
crossValidation = argums1[5] == 'true'
qtdFolds = int(argums1[6])
diretorioMallet = argums1[7]


print 'confirmando diretorio do MALLET',(diretorioMallet+'/bin/mallethon')
if os.path.exists(diretorioMallet+'/bin/mallethon'):
    print 'OK'
else:
    print 'não existe!'
    moduloAux.erroParametro()

categUtilizadas = list()
if(len(argums1) > 9):   #verifica se foram passadas as categorias a serem utilizadas
    categUtilizadas.append(argums1[8])
    categUtilizadas.append(argums1[9])
else:
    categUtilizadas.append('ORG')
    categUtilizadas.append('PES')
    categUtilizadas.append('LOCAL')

if(crossValidation):
    print 'utilizando CROSS-VALIDATION'
    if(qtdFolds < 2):
        print 'quantidade de folds muito pequena!'
        print 'mínimo: 2'
        exit()
    if(diretorioTreino != diretorioTeste):
        print 'diretorios de treino e teste diferentes não são permitidos no modo CROSS-VALIDATION!'
        exit()
else:
    print 'sem CROSS-VALIDATION'
    qtdFolds = 1

#CRIA DIRETORIOS DE TRABALHO
os.mkdir(diretorioTrabalho)
os.mkdir(diretorioTrabalho+"/marcados")
# if(crossValidation):
for i in range(qtdFolds):
    dir = diretorioTrabalho+'/marcados/iteracao '+str(i+1)
    print 'criando diretorio', dir
    os.mkdir(dir)
    print 'OK'

#NUMEROS INFORMATIVOS
relacoesTotal = 0
relacoesAcertos = 0
relacoesChutadas = 0
nrAcertos = 0
nrparcial = 0
nrtotal = 0
nrEncontrados = 0
nrEntrada = 0
OrgOrg = 0
OrgLocal = 0
OrgPessoa = 0
OrgOrgP = 0
OrgLocalP = 0
OrgPessoaP = 0

#carrega os textos dourados
entradas = []
if(crossValidation or not modeloExiste):
    entradas, relacoesTotal = moduloAux.textosTreinamento(diretorioTrabalho, categUtilizadas, dicionarios, diretorioTreino+'/')

teste = []
if(not crossValidation):
    teste, tmp = moduloAux.textosTreinamento(diretorioTrabalho, categUtilizadas, dicionarios, diretorioTeste+'/')

if(not crossValidation):
    relacoesTotal = tmp

#informa ao NLTK onde se encontra a biblioteca MALLET
CRFnltk.configMallet(diretorioMallet)

#variável para contar quantos itens BIO foram identificados na execução do programa
contBio = 0

#número de textos do diretorio
n1 = len(entradas)
n2 = len(teste)
if(crossValidation):
    print n1, 'textos utilizados no CROSS-VALIDATION'
elif(not crossValidation and modeloExiste):
    print n2, 'textos utilizados para teste'
else:
    print n1, 'textos utilizados para treino e', n2, 'utilizados para teste'
                                                        
#inicialização da matriz de confusão
resultado = [[0, 0], [0, 0]]

#inicialização do conjunto de teste
testset = []


#gera cinco intervalos distintos para teste e treino a cada iteração
if(crossValidation):
    moduloErros.descritorEntrada = open(diretorioTrabalho+'/Descritor_Entrada.txt','a')
    descritorCerto = open(diretorioTrabalho+'/DescritorCerto_Saida.txt','a')
    descritor = open(diretorioTrabalho+'/Descritor_Saida.txt','a')
    for i in range(qtdFolds):
        print (i+1), 'º Iteração'
        #limites do conjunto de teste
        limTest = ((i * n1 * 1/qtdFolds), (i + 1) * n1 * 1/qtdFolds)
        testset = entradas[limTest[0]:limTest[1]]


        #definindo os limites do conjunto de treino
        if(limTest[0] == 0):
            trainset = entradas[limTest[1]:]
        elif(limTest[1] >= n1):
            trainset = entradas[:limTest[0]]
        else:
            trainset = entradas[:limTest[0]] + entradas[limTest[1]:]

        print 'Teste', '[' , limTest[0] , ':' , limTest[1] , ']'

        print 'Treino',    
        if(limTest[0] == 0):
            print '[',limTest[1], ': ]'
        elif(limTest[1] >= n1):
            print '[ :',limTest[0], ']'
        else:
            print '[ :',limTest[0], '] [',limTest[1], ': ]'

        #retorna o resultado da iteração no formato de tabela de confusão e o contador de BIOs
        orgorgpaux, orglocalpaux, orgpessoapaux, orgorgaux, orglocalaux, orgpessoaaux, EntradaAux, EncontradosAux, parcialAux, totalAux, nrAcertosAux, resultadoAux, contBioAux, relacoesAcertosAux, relacoesChutadasAux = moduloRR.RR(diretorioTrabalho, diretorioModelo, crossValidation, trainset, testset, i+1)
	nrAcertos += nrAcertosAux
	nrparcial += parcialAux
	nrtotal += totalAux
	nrEncontrados += EncontradosAux
	nrEntrada += EntradaAux
	OrgOrg += orgorgaux
	OrgLocal += orglocalaux
	OrgPessoa += orgpessoaaux
	OrgOrgP += orgorgpaux
	OrgLocalP += orglocalpaux
	OrgPessoaP += orgpessoapaux
        contBio += contBioAux
        relacoesAcertos += relacoesAcertosAux
        relacoesChutadas += relacoesChutadasAux
        #soma a tabela de confusão da iteração com o geral
        resultado = moduloAux.soma(resultado, resultadoAux)
        #mostra resultado parcial
        print resultadoAux
	nrtotal = nrAcertos - nrparcial
    descritorCerto.write('\nacertos:'+str(nrAcertos)+'\n')
    descritorCerto.write('acertoparcial:'+str(nrparcial)+'\n')
    descritorCerto.write('acertototal:'+str(nrtotal)+'\n')
    descritorCerto.write('TOTAL = ORG-ORG:'+str(OrgOrg)+' '+'ORG-LOCAL:'+str(OrgLocal)+' '+'ORG-PESSOA:'+str(OrgPessoa)+'\n')
    descritorCerto.write('PARCIAL = ORG-ORG:'+str(OrgOrgP)+' '+'ORG-LOCAL:'+str(OrgLocalP)+' '+'ORG-PESSOA:'+str(OrgPessoaP))
    descritor.write('Encontrados:'+str(nrEncontrados))
    moduloErros.descritorEntrada.write('Entrada:'+str(nrEntrada))
    precisao = float(nrAcertos)/nrEncontrados
    recall = float(nrAcertos)/nrEntrada
    fmeasure1 = float(2*precisao*recall)
    fmeasure2 = float(precisao+recall)
    fmeasure = fmeasure1/fmeasure2
    resultado2 = ('\nacertos:'+str(nrAcertos)+'\nacerto parcial:'+str(nrparcial)+'\nacerto total:'+str(nrtotal)+'\nEntrada:'+str(nrEntrada)+'\nEncontrados:'+str(nrEncontrados)+'\nTOTAL = ORG-ORG:'+str(OrgOrg)+' '+'ORG-LOCAL:'+str(OrgLocal)+' '+'ORG-PESSOA:'+str(OrgPessoa)+'\n'+'PARCIAL = ORG-ORG:'+str(OrgOrgP)+' '+'ORG-LOCAL:'+str(OrgLocalP)+' ORG-PESSOA:'+str(OrgPessoaP)+'\nPrecisão(parcial):'+str(precisao)+'\nRecall(parcial):'+str(recall)+'\nFmeasure(parcial):'+str(fmeasure))
    precisao1 = float(nrtotal)/nrEncontrados
    recall1 = float(nrtotal)/nrEntrada
    fmeasure3 = float(2*precisao1*recall1)
    fmeasure4 = float(precisao1+recall1)
    fmeasure5 = fmeasure3/fmeasure4
    resultado3 = ('\nacertos:'+str(nrAcertos)+'\nacerto parcial:'+str(nrparcial)+'\nacerto total:'+str(nrtotal)+'\nEntrada:'+str(nrEntrada)+'\nEncontrados:'+str(nrEncontrados)+'\nTOTAL = ORG-ORG:'+str(OrgOrg)+' '+'ORG-LOCAL:'+str(OrgLocal)+' '+'ORG-PESSOA:'+str(OrgPessoa)+'\n'+'PARCIAL = ORG-ORG:'+str(OrgOrgP)+' '+'ORG-LOCAL:'+str(OrgLocalP)+' ORG-PESSOA:'+str(OrgPessoaP)+'\nPrecisão:'+str(precisao1)+'\nRecall:'+str(recall1)+'\nFmeasure:'+str(fmeasure5))
    moduloErros.descritorEntrada.close()
    descritor.close()
    descritorCerto.close()
else:
    resultado, contBio, relacoesAcertos, relacoesChutadas = moduloRR.RR(diretorioTrabalho, diretorioModelo, crossValidation, entradas, teste, 1)	



# if(crossValidation):
now = time.localtime()
displaytime = time.strftime("%x %X",now)
cabecalho = str(contBio)+' marcações IO\n'+'CROSS '+str(qtdFolds)+' FOLDS ' + str(displaytime) + '\n\tREL\tO\tRec\tPrec\tF-Measure'
os.system('clear')
print cabecalho

#inicia a escrita no arquivo de formato tabela
file = open(diretorioTrabalho+'/result.ods', 'a')
file.write('\n\n\n' + cabecalho + '\n')
file.close()

#itera sobre cada linha da tabela de confusão
for i in range(len(resultado)):
    prec = rec = 0
    #a recebe a soma de todos os itens da coluna da tabela
    a = (sum([resultado[j][i] for j in range(2)]))
    if a != 0:
        #calcula-se a precisão dividindo o que foi marcado certo
        #pelo que deveria ter sido marcado para o item
        prec = float(resultado[i][i]) / a

    #a recebe a soma de todos os itens da linha da tabela
    a = (sum([resultado[i][j] for j in range(2)]))
    if a != 0:
        #calcula-se a abrangência dividindo o que foi marcado certo
        #por tudo que foi marcado para o item
        rec = float(resultado[i][i]) / a

    #calcula a F-Measure
    if(prec+rec == 0):
        continue
    fMeasure = (2*prec*rec)/(prec+rec)

    #linha da tabela de confusão
    saida = str(KNNUtil.classe(i))+ '\t'+ str(resultado[i][0])+ '\t'+ str(resultado[i][1])+ '\t'+ str(rec)+ '\t'+ str(prec) + '\t' + str(fMeasure)
        
    print saida
    
    file = open(diretorioTrabalho+'/result.ods', 'a')
    file.write(saida + '\n')
    file.close()

#MEDIDAS TOTAIS
prec = float(relacoesAcertos)/relacoesChutadas
rec = float(relacoesAcertos)/relacoesTotal
fmeasure = (2*prec*rec)/(prec+rec)


saida = '\n\n Etiquetas IO:\n\ttotal:'+str(relacoesTotal)+'\n\tencontradas:'+str(relacoesChutadas)+'\n\tacertos:'+str(relacoesAcertos)+'\n\tprecisão:'+str(prec)+'\n\trecall:'+str(rec)+'\n\tfmeasure:'+str(fmeasure)
print saida
# if(crossValidation):
file = open(diretorioTrabalho+'/result.ods', 'a')
file.write(saida + '\n')
file.close()
moduloErros.listaorganizada(diretorioTrabalho, resultado2, resultado3)
moduloErros.descritorentrada(diretorioTrabalho)
moduloErros.erro_aproximado(diretorioTrabalho)
moduloChaves.chaveOrg(diretorioTrabalho)
moduloChaves.chaveLoc(diretorioTrabalho)
moduloChaves.chavePes(diretorioTrabalho)
segundos = time.time() - start_time
minutos = 0
horas = 0
if (segundos>60):
   minutos=int(segundos)/60
   segundos= segundos-(minutos*60)
if (minutos>60):
   horas=int(minutos)/60
   minutos = minutos-(horas*60)
print 	
print ('\nacertos:'+str(nrAcertos))
print ('acerto parcial:'+str(nrparcial))
print ('acerto total:'+str(nrtotal))
print ('TOTAL = ORG-ORG:'+str(OrgOrg)+' '+'ORG-LOCAL:'+str(OrgLocal)+' '+'ORG-PESSOA:'+str(OrgPessoa))
print ('PARCIAL = ORG-ORG:'+str(OrgOrgP)+' '+'ORG-LOCAL:'+str(OrgLocalP)+' '+'ORG-PESSOA:'+str(OrgPessoaP))
print '\n\nresultados parciais:'
print resultado2
print '\n\nresultados totais:'
print resultado3
print "\ntempo de execução:\n%02d:%02d:%02.2d" % (horas, minutos, segundos)
print '\nfim'