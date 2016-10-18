# coding=utf-8

def string_replaces(a_string):
    a_string = a_string.replace("+", "")
    a_string = a_string.replace("="," ")
    a_string = a_string.replace(";", ",")
    a_string = a_string.replace("[", "(")
    a_string = a_string.replace("]", ")")
    return a_string
	
def replaces(word):
    word = word.replace("+", "")
    word = word.replace("=", " ")
    word = word.replace("(ORG)", "")
    word = word.replace("(PES)", "")
    word = word.replace("(LOC)", "")
    word = word.replace("ã", "Ã")
    word = word.replace("é", "É")
    word = word.replace("ê", "Ê")
    word = word.replace('í','Í')
    word = word.replace('ì','Ì')
    word = word.replace('á','Á')
    word = word.replace('à','À')
    word = word.replace('ú','Ú')
    word = word.replace('â','Â')
    word = word.replace('ó','Ó')
    word = word.replace('ô','Ô')
    word = word.replace('õ','Õ')
    word = word.replace('ç','Ç')
    return word