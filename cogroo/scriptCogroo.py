# coding=utf-8
import os
import shutil
import en

os.mkdir("aux")
pontuacoes = ["!", "?", ","]
arquivos = os.listdir(os.path.expanduser("./entrada"))
for arquivo in arquivos:
        with open("./entrada/" + arquivo) as texto:
            for linha in texto:
                if not linha == '\n':
                    if not linha[-2:-1] in pontuacoes:
                        linha = linha.replace('\n', '. .\n')
                        linha = linha.replace('.. .', '.')
                        linha = linha.replace('. .', '.')
                file = open("./aux/" + arquivo, 'a')
                file.write(linha)
                file.close()
            print "arquivo " + arquivo + " foi preparado"
os.system("java -jar cogroo.jar ./aux ./saida")

shutil.rmtree("aux")

en.formata_textos()

print ("Executado com sucesso")
