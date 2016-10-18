def escreve(newline):

    file = open("./sequencial/aa66435.cg", 'a')
    file.write(str(newline))
    file.close()


with open("./formatado/aa66435.cg") as texto:
    id_seq = 0
    for linha in texto:
        if linha.find('ID_S') != -1:
            newline = "ID_SEQ\t" + linha
            escreve(newline)
        else:
            if linha == '\n':
                pass
            else:
                newline = str(id_seq) + '\t' + linha
                id_seq += 1
                escreve(newline)
