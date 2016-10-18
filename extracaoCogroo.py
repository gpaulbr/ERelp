# coding=utf-8

import time
import os

def extracaoCogroo(diretorioTrabalho, categoriasUtilizadas, arquivo, vetDicionarios):
    vetorEntrada = list()
    vetorIO = list()
    # Dicionario com as palavras dos arquivos de dicionarios passados para o método
    dic = dict()
    numeroRelacoes = 0

    # Le os txts de dicionarios e formata eles no dic
    for dicionario in vetDicionarios:
        with open(dicionario) as dicForm:
            for linha in dicForm.readlines():
                dic[(linha[0:linha.find(';')])] = True

    with open(arquivo) as texto:
        features = list()
        gerarFeatureID = None
        gerarFeatureNE = str()

        next(texto)

        for linha in texto:

            dicPalavra = dict()

            lista = linha.split('\t')
            dicPalavra["ID_S"] = (lista[0])
            dicPalavra["ID"] = (lista[1])

            if dicPalavra["ID"] == 0:
                features = list()

            if lista[3] == '[]':

                dicPalavra["lemma"] = lista[2]

            else:

                dicPalavra["lemma"] = (lista[3][1:-1])

            dicPalavra["PoS"] = (lista[4])

            if lista[6] == 'O':

                dicPalavra["Head"] = True

            else:

                dicPalavra["Head"] = False

            dicPalavra["NP"] = (lista[7])
            dicPalavra["Structure"] = (lista[8])

            if lista[9] != '-':

                dicPalavra["NE"] = (lista[9])

            else:

                dicPalavra["NE"] = 'null'

            if lista[10][:-1] != '-':

                features = lista[10][1:-2].split('|')

            dicPalavra["gerarFeature"] = False

            # transforma a string em unicode para o uppercase funcionar nas
            # letras com acento
            lemma = dicPalavra["lemma"].decode('utf-8').upper()
            # Substitui os _ por espaços na string e verifica se ela está
            # no dicionário
            lemma = lemma.encode('utf-8').replace('_', ' ')
            try:
                dic[lemma]
                dicPalavra["dicionario"] = True

            except:
                dicPalavra["dicionario"] = False

            if dicPalavra["ID"] in features:

                vetorIO.append("I")
                numeroRelacoes += 1

            else:
                vetorIO.append("O")

            vetorEntrada.append(dicPalavra)

            if dicPalavra["NE"] in categoriasUtilizadas:

                if gerarFeatureID is None:

                    gerarFeatureID = int(dicPalavra["ID"])
                    gerarFeatureNE = dicPalavra["NE"]

                else:

                    if dicPalavra["NE"] != gerarFeatureNE:

                        diferenca = int(dicPalavra["ID"]) - gerarFeatureID

                        for index in range(vetorEntrada.index(dicPalavra)-diferenca, vetorEntrada.index(dicPalavra)+1):
                            vetorEntrada[index]["gerarFeature"] = True

    os.mkdir(diretorioTrabalho)
    file = open(diretorioTrabalho+'/vetorDeEntrada.txt', 'a')
    file.write(str(vetorEntrada)+'\n')
    file.close()
    file = open(diretorioTrabalho+'/vetorIO.txt', 'a')
    file.write(str(vetorIO)+'\n')
    file.close()

    for i in vetorEntrada:
        print i


displaytime = time.strftime("%x %X", time.localtime())
diretorioTrabalho = './saida_ORG_PES_Gabriel'+'_'+str(displaytime.replace('/', '-'))
categorias = ['PES', 'ORG']
dicionarios = ['../Dicionarios/Profissao_Titulo.txt', '../Dicionarios/Localizacao.txt']
extracaoCogroo(diretorioTrabalho, categorias, 'ric-42664.cg', dicionarios)


# def comparar(x, y):

#     if x.lower() > y.lower():
#         return 1
#     elif x.lower() == y.lower():
#         return 0
#     else:
#         return -1
