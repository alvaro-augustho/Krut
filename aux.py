from string import maketrans

# Funcao que traduz uma letra em um numero. 
# Util para traduzir posicoes do tabuleiro para posicoes em um vetor ou matriz
def trans(jogada):

    intab = "abcdefgh"
    outtab = "12345678"
    trantab = maketrans(intab, outtab)

    return splitCount(jogada.translate(trantab), 1)

# Divide a string 's' em elementos de tamanho 'count'
def splitCount(s, count):

    return [''.join(x) for x in zip(*[list(s[z::count]) for z in range(count)])]

# Funcao para criar uma copia recursiva de uma lista.
# Usei muito no comeco, mas acho q nao uso mais em lugar nenhum agora
def unshared_copy(inList):

    if isinstance(inList, list):
        return list( map(unshared_copy, inList) )
    return inList
