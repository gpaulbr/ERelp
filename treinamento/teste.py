import moduloAux

categorias = list()

categorias.append('ORG')
categorias.append('PES')
dicionarios = list()
dicionarios.append('./Dicionarios/Profissao_Titulo.txt')
entrada, relacoes = moduloAux.textosTreinamento('./teste', categorias, dicionarios, './entrada/')

# file = open('./saida/saida.txt', 'a')
# file.write(str(entrada))
# file.close()

print entrada
print ('--------------------------------------------------')
print relacoes
