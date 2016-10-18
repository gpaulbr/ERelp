#coding=utf-8
import os


def formata_textos():
    arquivos = os.listdir(os.path.expanduser("./saida"))
    for arquivo in arquivos:
        if(not arquivo.endswith('~') and arquivo.endswith('.txt')):
            with open("./saida/" + arquivo) as texto:
                for linha in texto:
                    if linha == '\n':
                        newline = linha
                    elif linha.find('ID_S') != -1:
                        newline = linha[:-1] + '\tNE\tREL\n'
                    elif linha.find('\t') != -1:
                        newline = linha[:-1] + '\t-\t-\n'
                    file = open("./formatado/" + arquivo[:arquivo.find('.txt')] + '.cg', 'a')
                    file.write(str(newline))
                    file.close()
        print "arquivo " + arquivo + " foi processado"

formata_textos()
