# -*- coding: utf-8 -*-
import os

# define a função a ser usada na comparação
def comparar(x,y):
  if x.lower() > y.lower():
    return 1
  elif x.lower() == y.lower():
    return 0
  else:
    return -1
total = 0
lista = os.listdir("ORG_L/")
lista.sort(comparar)
tags = open("tags5.txt" , "w")
for arquivo in lista:
	normal = open("ORG_L/"+arquivo , "r")
	modificado = open("ORG_L_modificado/"+arquivo , "w")

	texto = normal.read()
	brel = texto.count("B-REL")
	irel = texto.count("I-REL")
	total = total + brel
	total = total + irel
	texto1 = texto.replace("B-REL", "REL")
	texto2 = texto1.replace("I-REL", "REL")
	tags.write("%s \n B-REL:%d I-REL:%d TOTAL: %d \n" %(arquivo,brel,irel,total))
	modificado.write(texto2)
	normal.close()
	modificado.close()
tags.write("Total de Relacoes: %d" %total)
tags.close()

