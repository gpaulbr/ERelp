# coding=utf-8
import operator
import os
from moduloTroca import string_replaces
from moduloTroca import replaces

def chaveOrg(diretorioTrabalho):
    wordcount = {}                                                      #dicionário onde ficam armazenadas as Entidades Nomeadas
    string = 'portugal] <civ> <*> prop m s @p<	 ['                     #string para dar replace
    with open(diretorioTrabalho+'/Lista_chaves.txt','r+') as entrada:   #Usando como entrada Lista_descritor.txt cria uma saida formatada
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
    with open(diretorioTrabalho+'/lista ocorrencia ORG.txt','w') as saida2:
        for key, value in sorted_x:
            if key != 'de' and key != 'o' and key != 'da' and key != 'do' and key != 'em' and key != 'a' and '(org)' in key.lower(): #Cria a Lista_Ocorrencia
                key = key.replace('=', " ")
		key = key.replace('+', '')
                saida2.write(key + ' foi encontrado: ')
                saida2.write(str(value) + ' vezes\n\n')
    with open(diretorioTrabalho+'/saida3.txt','w') as saida3:
        for key, value in sorted_x:
            if key != 'de' and key != 'o' and key != 'da' and key != 'do' and key != 'em' and key != 'a' and '(org)' in key.lower():
                saida3.write(key+'\n')
    with open(diretorioTrabalho+'/Saida Chave ORG.txt', 'w') as saida4: #Procura pelas sentenças na Lista_descritor.txt e escreve as sentenças 
        with open(diretorioTrabalho+'/saida3.txt','r') as words_file:   #que contém a Entidade Nomeada
            with open(diretorioTrabalho+'/Lista_chaves.txt','r+') as strings_file:
                all_strings = list(map(str.strip, strings_file))
		i=0
                for word in words_file:
                    word = word.replace("\n", "")
                    word2 = replaces(word)
		    word2= word2.upper()
		    if '(org)' in word.lower():
		        saida4.write(word2+':\n')
                        for a_string in all_strings:
                            if word.lower() in a_string.lower():
                                a_string = a_string.replace(string, "")
                                a_string = a_string.replace(string, "")
				a_string = a_string.replace("(ORG)", "")
				a_string = a_string.replace("(LOCAL)", "")
				a_string = a_string.replace("(PES)", "")
                                a_string = string_replaces(a_string)
                                saida4.write(a_string + '\n')
		    saida4.write("\n")
    os.remove(diretorioTrabalho+'/saida.txt')
    os.remove(diretorioTrabalho+'/saida3.txt')

def chaveLoc(diretorioTrabalho):
    wordcount = {}                                                       #dicionário onde ficam armazenadas as Entidades Nomeadas
    string = 'portugal] <civ> <*> prop m s @p<	 ['                      #string para dar replace
    with open(diretorioTrabalho+'/Lista_chaves.txt','r+') as entrada:    #Usando como entrada Lista_descritor.txt cria uma saida formatada
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
    with open(diretorioTrabalho+'/lista ocorrencia LOCAL.txt','w') as saida2:
        for key, value in sorted_x:
            if key != 'de' and key != 'o' and key != 'da' and key != 'do' and key != 'em' and key != 'a' and '(local)' in key.lower(): #Cria a Lista_Ocorrencia
                key = key.replace('=', " ")
		key = key.replace('+', '')
                saida2.write(key + ' foi encontrado: ')
                saida2.write(str(value) + ' vezes\n\n')
    with open(diretorioTrabalho+'/saida3.txt','w') as saida3:
        for key, value in sorted_x:
            if key != 'de' and key != 'o' and key != 'da' and key != 'do' and key != 'em' and key != 'a' and '(local)' in key.lower():
                saida3.write(key+'\n')
    with open(diretorioTrabalho+'/Saida Chave LOCAL.txt', 'w') as saida4:   #Procura pelas sentenças na Lista_descritor.txt e escreve as sentenças 
        with open(diretorioTrabalho+'/saida3.txt','r') as words_file:       #que contém a Entidade Nomeada
            with open(diretorioTrabalho+'/Lista_chaves.txt','r+') as strings_file:
                all_strings = list(map(str.strip, strings_file))
		i=0
                for word in words_file:
                    word = word.replace("\n", "")
                    word2 = replaces(word)
		    word2= word2.upper()
		    if '(local)' in word.lower():
		        saida4.write(word2+':\n')
                        for a_string in all_strings:
                            if word.lower() in a_string.lower():
                                a_string = a_string.replace(string, "")
                                a_string = a_string.replace(string, "")
				a_string = a_string.replace("(ORG)", "")
				a_string = a_string.replace("(LOCAL)", "")
				a_string = a_string.replace("(PES)", "")
                                a_string = string_replaces(a_string)
                                saida4.write(a_string + '\n')
		    saida4.write("\n")
    os.remove(diretorioTrabalho+'/saida.txt')
    os.remove(diretorioTrabalho+'/saida3.txt')

def chavePes(diretorioTrabalho):
    wordcount = {}                                                      #dicionário onde ficam armazenadas as Entidades Nomeadas
    string = 'portugal] <civ> <*> prop m s @p<	 ['                     #string para dar replace
    with open(diretorioTrabalho+'/Lista_chaves.txt','r+') as entrada:   #Usando como entrada Lista_descritor.txt cria uma saida formatada
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
    with open(diretorioTrabalho+'/lista ocorrencia PES.txt','w') as saida2:
        for key, value in sorted_x:
            if key != 'de' and key != 'o' and key != 'da' and key != 'do' and key != 'em' and key != 'a' and '(pes)' in key.lower(): #Cria a Lista_Ocorrencia
                key = key.replace('=', " ")
		key = key.replace('+', '')
                saida2.write(key + ' foi encontrado: ')
                saida2.write(str(value) + ' vezes\n\n')
    with open(diretorioTrabalho+'/saida3.txt','w') as saida3:
        for key, value in sorted_x:
            if key != 'de' and key != 'o' and key != 'da' and key != 'do' and key != 'em' and key != 'a' and '(pes)' in key.lower():
                saida3.write(key+'\n')
    with open(diretorioTrabalho+'/Saida Chave PES.txt', 'w') as saida4: #Procura pelas sentenças na Lista_descritor.txt e escreve as sentenças 
        with open(diretorioTrabalho+'/saida3.txt','r') as words_file:   #que contém a Entidade Nomeada
            with open(diretorioTrabalho+'/Lista_chaves.txt','r+') as strings_file:
                all_strings = list(map(str.strip, strings_file))
		i=0
                for word in words_file:
                    word = word.replace("\n", "")
                    word2 = replaces(word)
		    word2= word2.upper()
		    if '(pes)' in word.lower():
		        saida4.write(word2+':\n')
                        for a_string in all_strings:
                            if word.lower() in a_string.lower():
                                a_string = a_string.replace(string, "")
                                a_string = a_string.replace(string, "")
				a_string = a_string.replace("(ORG)", "")
				a_string = a_string.replace("(LOCAL)", "")
				a_string = a_string.replace("(PES)", "")
                                a_string = string_replaces(a_string)
                                saida4.write(a_string + '\n')
		    saida4.write("\n")
    os.remove(diretorioTrabalho+'/saida.txt')
    os.remove(diretorioTrabalho+'/saida3.txt')
    os.remove(diretorioTrabalho+'/Lista_chaves.txt')