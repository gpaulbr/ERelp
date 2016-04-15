# coding=utf-8

import operator
import os
import difflib
from moduloTroca import string_replaces
from moduloTroca import replaces

def listaorganizada(diretorioTrabalho, resultado, resultado1):
    wordcount = {}                                                          #dicionário onde ficam armazenadas as Entidades Nomeadas
    string = 'portugal] <civ> <*> prop m s @p<   ['                         #string para dar replace
    with open(diretorioTrabalho+'/Lista_descritor.txt','r+') as entrada:    #Usando como entrada Lista_descritor.txt cria uma saida formatada
        with open(diretorioTrabalho+'/saida.txt', 'w') as saida:
            for line in entrada:
                line = line.replace(string, "")
                line1 = line[line.find("[") + 1:line.find(",")]
                line2 = line[line.find(";") + 1:line.find("]")]
                line1 = line1.replace(" ", "")
                line2 = line2.replace(" ", "")
                saida.write(line1 + '\n')
                saida.write(line2 +'\n')
    with open(diretorioTrabalho+'/saida.txt','r') as file: #utilizando a saida formata efetua uma contagem e armazena no dicionário
        for word in file.read().split():
            word1 = word.lower()
            if word1 not in wordcount:
                wordcount[word1] = 1
            else:
                wordcount[word1] += 1
    sorted_x = sorted(wordcount.items(), key=operator.itemgetter(1), reverse=True) #ordena o dicionário por ordem de valor (ocorrencia)
    with open(diretorioTrabalho+'/lista_ocorrencia.txt','w') as saida2:
        for key, value in sorted_x:
            if key != 'de' and key != 'o' and key != 'da' and key != 'do' and key != 'em' and key != 'a': #Cria a Lista_Ocorrencia
                key = key.replace('=', " ")
                key = key.replace('+', '')
                saida2.write(key + ' foi encontrado: ')
                saida2.write(str(value) + ' vezes\n\n')
    with open(diretorioTrabalho+'/saida3.txt','w') as saida3:
        for key, value in sorted_x:
            if key != 'de' and key != 'o' and key != 'da' and key != 'do' and key != 'em' and key != 'a':
                saida3.write(key+'\n')
    with open(diretorioTrabalho+'/Saida_ordenada.txt', 'w') as saida4: #Procura pelas sentenças na Lista_descritor.txt e escreve as sentenças 
        with open(diretorioTrabalho+'/saida3.txt','r') as words_file:  #que contém a Entidade Nomeada
            with open(diretorioTrabalho+'/Lista_descritor.txt','r+') as strings_file:
                all_strings = list(map(str.strip, strings_file))
                i=0
                for word in words_file:
                    word = word.replace("\n", "")
                    word2 = replaces(word)
                    word2= word2.upper()
                    saida4.write(word2+':\n')
                    for a_string in all_strings:
                        if word.lower() in a_string.lower():
                            a_string = a_string.replace(string, "")
                            a_string = a_string.replace(string, "")
                            a_string = string_replaces(a_string)
                        saida4.write(a_string + '\n')
                    saida4.write("\n")
                saida4.write('\nresultados parciais:'+str(resultado)+'\n\nresultados totais:'+str(resultado1))
    os.remove(diretorioTrabalho+'/saida.txt')
    os.remove(diretorioTrabalho+'/saida3.txt')
    os.remove(diretorioTrabalho+'/Lista_descritor.txt')

def erro_aproximado(diretorioTrabalho):
    with open(diretorioTrabalho+'/DescritorCerto_Saida.txt','r+') as file:
        with open(diretorioTrabalho+'/Saida.txt','w') as saida:
            for line in file:
                line1 = line.replace("(ORG)", "")
                line1 = line1.replace("(LOCAL)", "")
                line1 = line1.replace("(PES)", "")
                line1 = line1.replace(" -- TOTAL", "")
                line1 = line1.replace(" -- PARCIAL", "")
                saida.write(line1)
    with open(diretorioTrabalho+'/Saida.txt', "r+") as saida:
        with open(diretorioTrabalho+"/saida2.txt", 'w') as saida2:
             with open(diretorioTrabalho+"/Descritor_Saida.txt", 'r') as descritor:
                 descritor1 = list(map(str.strip, descritor))
                 saida1 = list(map(str.strip, saida))
                 diff = difflib.unified_diff(saida1, descritor1, fromfile='/saida.txt', lineterm='', n=0)
                 lines = list(diff)
                 added = [line[1:] for line in lines if line[0] == '+']
                 removed = [line[1:] for line in lines if line[0] == '-']
                 for line in added:
                    if line not in removed:
                       saida2.write(line+'\n\n')
    i=1
    string ="] <top> <newlex> <*> prop m s @p<   [África"
    with open(diretorioTrabalho+"/saida2.txt", 'r+') as saida2:
        with open(diretorioTrabalho+"/Lista_ErroParcial.txt", "w") as Lista_Erro:
            Lista_Erro.write('Relaçoes extraidas incorretas:')
            for line in saida2:
                line = line.replace('(++ )', "")
                line = line.replace(string, "")
                if line != "\n" and "Encontrados" not in line:
                   i+=1
            if "Encontrados" not in line:           
                Lista_Erro.write(line)
    os.remove(diretorioTrabalho+'/Saida.txt')
    os.remove(diretorioTrabalho+'/saida2.txt')
    erroOcorrencia(diretorioTrabalho)

def erroOcorrencia(diretorioTrabalho):                                                                   #operator
    wordcount = {}                                                                      #diretorioTrabalho
    string = 'portugal] <civ> <*> prop m s @p<	 ['                                     #os
    with open(diretorioTrabalho+"/Lista_ErroParcial.txt",'r+') as entrada:
        with open(diretorioTrabalho+'/saida.txt', 'w') as saida:
            for line in entrada:
                line = line.replace(string, "")
                line1 = line[line.find("[") + 1:line.find(",")]
                line2 = line[line.find(";") + 1:line.find("]")]
                line1 = line1.replace(" ", "")
                line2 = line2.replace(" ", "")
                saida.write(line1 + '\n')
                saida.write(line2 + '\n')
    with open(diretorioTrabalho+'/saida.txt', 'r') as file:
        for word in file.read().split():
            word1 = word.lower()
	    if word1 not in wordcount:
                wordcount[word1] = 1
            else:
                wordcount[word1] += 1
    sorted_x = sorted(wordcount.items(), key=operator.itemgetter(1), reverse=True)
    with open(diretorioTrabalho+'/Ocorrencia_Erro.txt', 'w') as saida2:
        for key, value in sorted_x:
            if key != 'de' and key != 'o' and key != 'da' and key != 'do' and key != 'em' and key != 'a':
                key = key.replace('=', " ")
                key = key.replace('+', '')
                saida2.write(key + ' foi encontrado: ')
                saida2.write(str(value) + ' vezes\n\n')
    with open(diretorioTrabalho+'/saida3.txt', 'w') as saida3:
        for key, value in sorted_x:
            if key != 'de' and key != 'o' and key != 'da' and key != 'do' and key != 'em' and key != 'a' and key != 'e'\
            and key != 's':
                saida3.write(key + '\n')
    with open(diretorioTrabalho+'/Erro Aproximado Ocorrencia.txt','w') as saida4:
        with open(diretorioTrabalho+'/saida3.txt', 'r') as words_file:
            with open(diretorioTrabalho+"/Lista_ErroParcial.txt", 'r+') as strings_file:
                all_strings = list(map(str.strip, strings_file))
                for word in words_file:
                    word = word.replace("\n", "")
                    word2 = replaces(word)
                    word2 = word2.upper()
		    saida4.write(word2 + ':\n')
                for a_string in all_strings:
                    if word.lower() in a_string.lower():
                        a_string = a_string.replace(string, "")
                        a_string = string_replaces(a_string)
                saida4.write(a_string + '\n')
                saida4.write("\n")
    os.remove(diretorioTrabalho+'/saida.txt')
    os.remove(diretorioTrabalho+'/saida3.txt')
    os.remove(diretorioTrabalho+'/Lista_ErroParcial.txt')

def descritorentrada(diretorioTrabalho):
    wordcount = {}
    string = 'portugal] <civ> <*> prop m s @p<   ['
    with open(diretorioTrabalho+"/Descritor_Entrada.txt",'r+') as entrada:
        with open(diretorioTrabalho+'/saida.txt', 'w') as saida:
            for line in entrada:
                line = line.replace(string, "")
                line1 = line[line.find("[") + 1:line.find(",")]
                line2 = line[line.find(";") + 1:line.find("]")]
                line1 = line1.replace(" ", "")
                line2 = line2.replace(" ", "")
                saida.write(line1 + '\n')
                saida.write(line2 + '\n')
    with open(diretorioTrabalho+'/saida.txt', 'r') as file:
        for word in file.read().split():
            word1 = word.lower()
            if word1 not in wordcount:
                wordcount[word1] = 1
            else:
                wordcount[word1] += 1
    sorted_x = sorted(wordcount.items(), key=operator.itemgetter(1), reverse=True)
    with open(diretorioTrabalho+'/Ocorrencia_Entrada.txt', 'w') as saida2:
        for key, value in sorted_x:
            if key != 'de' and key != 'o' and key != 'da' and key != 'do' and key != 'em' and key != 'a':
                key = key.replace('=', ' ')
                key = key.replace('+', '')
                saida2.write(key + ' foi encontrado: ')
                saida2.write(str(value) + ' vezes\n\n')
    with open(diretorioTrabalho+'/saida3.txt', 'w') as saida3:
        for key, value in sorted_x:
            if key != 'de' and key != 'o' and key != 'da' and key != 'do' and key != 'em' and key != 'a' and key != 'e'\
            and key != 's':
                saida3.write(key + '\n')
    with open(diretorioTrabalho+'/Descritor_EntradaOcorrencia.txt','w') as saida4:
        with open(diretorioTrabalho+'/saida3.txt', 'r') as words_file:
            with open(diretorioTrabalho+'/Descritor_Entrada.txt', 'r+') as strings_file:
                all_strings = list(map(str.strip, strings_file))
                i = 0
                for word in words_file:
                    word = word.replace("\n", "")
                    word2 = replaces(word)
                    word2 = word2.upper()
                    saida4.write(word2 + ':\n')
                    for a_string in all_strings:
                        if word.lower() in a_string.lower():
                            a_string = a_string.replace(string, "")
                            a_string = string_replaces(a_string)
                    saida4.write(a_string + '\n')
                    saida4.write("\n")
    os.remove(diretorioTrabalho+'/saida.txt')
    os.remove(diretorioTrabalho+'/saida3.txt')

    