# coding=utf-8

import os
import moduloExtrai

#soma duas tabelas de tamanho igual
def soma(A, B):
    if len(A) != len(B):
        raise ValueError
    for i in range(len(A)):
        for j in range(len(A[i])):
            A[i][j] += B[i][j]
    return A

# define a função a ser usada na comparação
def comparar(x,y):
  if x.lower() > y.lower():
    return 1
  elif x.lower() == y.lower():
    return 0
  else:
    return -1

#carrega todos os textos dourados em uma lista no formato
#[('nomeDoTexto.txt',[[({features...},bil),({features...},bil),({features...},bil)],[({features...},bil),({features...},bil),({features...},bil)]])]
def textosTreinamento(diretorioTrabalho, categUtilizadas, dicionarios, pasta):    
    #lista com o nome de todos os arquivos do diretorio
    dicionariosFormat = formataDic(dicionarios)
    arquivos = os.listdir(os.path.expanduser(pasta))
    arquivos.sort(comparar)
    entradas = []
    relacoesTotal = 0
    
    for a in arquivos:
        aux = open(pasta + a).read()
        if(not a.endswith('~')):#evita arquivos temporários
            textos,relacoesTotalAux = moduloExtrai.processaTags(diretorioTrabalho, categUtilizadas, aux, dicionariosFormat)
            relacoesTotal += relacoesTotalAux
            entradas.append((a,textos))
    return entradas, relacoesTotal

def deletaModelos():
    print "deletando modelos"
    if os.listdir("modelos/") == []:
        print "diretorio ja estava vazio"
    else:
        os.system('rm modelos/*')
        if os.listdir("modelos/") == []:
            print "OK"
        else: 
            print "modelos nao foram deletados"

def formataDic(dicionarios):
    dicionariosFormat = list()  #lista com os dicionarios formatados
    for dic in dicionarios:
        fileDic = open(dic,'r')
        dicFormat = fileDic.read()
        fileDic.close()
        
        dicSplited = dicFormat.split('\n')  #divide o arquivo em linhas
        dicFormat = []
        for i in range(len(dicSplited)):    #monta o dicionario usando o primeiro item de cada linha
            split = dicSplited[i].split(';')
            dicFormat.extend([itm.lower() for itm in split[:1]])
        dicionariosFormat.append(dicFormat)
    return dicionariosFormat

def erroParametro():
    print"""
PARAMETROS DE ENTRADA:
DIRETORIO TREINO - deve conter os textos separados em arquivos .txt
DIRETORIO DE TESTE - diretorio contendo os textos a serem testados
DIRETORIO DO MODELO - diretorio apontando para o modelo utilizado, caso o arquivo não exista será criado um novo, caso exista será utilizado o que já está salvo
DIRETORIO DE TRABALHO - será criado na execução
CROSS VALIDATION - se deseja utilizar a técnica de cross validation (true ou false)
QUANTIDADE DE FOLDS - numero de folds utilizadas no processo de cross validation
DIRETORIO MALLET - diretorio que contem a biblioteca MALLET
CATEGORIAS A UTILIZAR (2) - opcional, mas se for informado devem ser exatamente duas
,(VÍRGULA) - obritagorio para extração dos parâmetros
DICIONARIOS - dicionarios a serem utilizados como features

USO:
interpretador_python ./RRcrf.py DIRETORIO_TREINO DIRETORIO_TESTE DIRETORIO_DE_TRABALHO DIRETORIO_MODELO CROSS_VALIDATION QUANTIDADE_DE_FOLDS DIRETORIO_MALLET <CATEGORIA_A_UTILIZAR_1 CATEGORIA_A_UTILIZAR_2> , DICIONARIOS...
<OPCIONAL>
    """
    exit()