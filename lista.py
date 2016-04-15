# -*- coding: UTF-8 -*-
import os

arquivos = os.listdir('textos/relacoes/ORG_LOC/')
# define a função a ser usada na comparação
def comparar(x,y):
  if x.lower() > y.lower():
    return 1
  elif x.lower() == y.lower():
    return 0
  else:
    return -1
# ordena a lista
arquivos.sort(comparar)

# exibe a lista ordenada
print arquivos
