from unidecode import unidecode


def confere(entrada, letras):
    letra = unidecode(entrada)
    if (len(letra) != 1) or (letra in letras) or (not letra.isalpha()):
        return False
    return True

def letraNome(letra, name, nameVerifica, tam):
    nameTemp = ""
    #acert = False
    for i in range(0, tam):
        if name[i] == letra:
            nameTemp += name[i]
            #acert = True
        else:
            nameTemp += nameVerifica[i]

    return nameTemp


def verificaVit(name, nameVerifica):
    if name == nameVerifica:
        return True
    return False


def mostraNome(nameVerifica, tam):
    nameTemp = ""
    for i in range(0, tam):
        if nameVerifica[i].isalpha():
            nameTemp += nameVerifica[i]
        elif nameVerifica[i] == " ":
            nameTemp += nameVerifica[i]*2
        else:
            nameTemp += "_."
    return nameTemp


def verificaEspaco(name, tam):
    nameTemp = ""
    for i in range(0, tam):
        if name[i] == " ":
            nameTemp += name[i]
        else:
            nameTemp += "_"
    return nameTemp
