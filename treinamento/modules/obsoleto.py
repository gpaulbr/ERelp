########## Essas duas funções não são mais usadas ##############
def iniEnt(bilou, pos): #verifica se o item bilou[pos] representa o início de uma relação

    if(bilou[pos] == 'REL' and bilou[pos-1] == 'O'):
        return True
    else:
        return False

def endEnt(bilou, pos): #verifica se o item bilou[pos] representa o fim de uma relação

    if(bilou[pos] == 'O'):
        return False
    else:
        if(bilou[pos] == 'REL' and bilou[pos+1] == 'O'):
		return True
	else:
		return False
