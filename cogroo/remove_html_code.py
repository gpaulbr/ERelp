#coding=utf-8
import os


def remove_caracteres():
    arquivos = os.listdir(os.path.expanduser("./entrada"))
    for arquivo in arquivos:
        if(not arquivo.endswith('~') and arquivo.endswith('.txt')):
            if arquivo.startswith('HAREM'):
                with open("./entrada/" + arquivo) as texto:
                    texto = texto.read()
                    texto = texto.replace("&amp;", "&")
                    texto = texto.replace("&quot;", "\"")
                    texto = texto.replace("&apos;", "'")
                    texto = texto.replace("&gt;", "<;")
                    texto = texto.replace("%&gt;", ">")

                os.remove("./entrada/" + arquivo)
                file = open("./entrada/" + arquivo, 'w')
                file.write(texto)
                file.close()
                print "arquivo " + arquivo + " foi processado"

remove_caracteres()
