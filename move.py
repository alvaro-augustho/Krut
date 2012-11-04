from detect import gerar_vetor
import aux

# Funcao para gerar o estado inicial do jogo
def init():
    
    resources = "Resources/init/"
    
    inicial = [line.rstrip('\n') for line in open(resources + "inicial.txt", "r")]
    posicoes = [line.rstrip('\n') for line in open(resources + "posicoes.txt", "r")]
    pecas = [line.rstrip('\n') for line in open(resources + "pecas.txt", "r")]

    t_inicial = []

    for i in range(64):
        peca = [pecas[i], posicoes[i], inicial[i]]
        t_inicial.append(peca)
        
    return t_inicial

# Funcao para identificar uma jogada. 
# Recebe um vetor representando o estado anterior do tabuleiro, com pecas identificadas, cores, posicoes etc
# E o vetor de 0s, 1s ou 2s
# Devolve uma string de 4 letras identificando a casa anterior de uma peca e a nova posicao dela
# So ta identificando movimentos simples e capturas de pecas
def identifica_jog(tab1, vetor):
    
    # Conta o numero de pecas nos dois vetores
    tab1_n = 0
    vetor_n = 0
    for i in range(64):
        if(tab1[i][2]!='0'):
            tab1_n = tab1_n+1
        if(vetor[i]!='0'):
            vetor_n = vetor_n+1

    # Ve as mudancas, com base nas cores de pecas em cada quadrado
    mudancas = []
    for i in range(64):
        anterior = tab1[i]
        novo = vetor[i]
        if anterior[2] != novo:
            mudancas.append([anterior, i, novo])
    
    # Monta a string da jogada, concatenando a posicao do quadrado q ficou vazio com o q nao esta vazio
    jogada=""
    if (tab1_n == vetor_n) : # Mesmo numero de pecas
 #       print "Movimento simples"
        if(mudancas[0][0][0] == ''):
            jogada=mudancas[1][0][1]+mudancas[0][0][1]            
        else:
            jogada=mudancas[0][0][1]+mudancas[1][0][1]
    
    elif (tab1_n > vetor_n): # Peca a menos
  #      print "Captura de peca"
        if(mudancas[1][2]=='0'):
            jogada=mudancas[1][0][1]+mudancas[0][0][1]
        else:
            jogada=mudancas[0][0][1]+mudancas[1][0][1]
    
    return jogada

# Funcao para gerar o novo estado do jogo com base numa jogada feita
def executa_jogada(jogada, tab):
    
    jogada = aux.trans(jogada)
    pos = aux.splitCount(jogada, 1)

    ints = []
    for i in range(4):
        ints.append(int(pos[i]))
    
    casa1 = tab[(ints[0]-1) + (8-ints[1])*8]
    casa2 = tab[(ints[2]-1) + (8-ints[3])*8]

    casa2[0] = casa1[0]
    casa2[2] = casa1[2]
    tab[(ints[2]-1) + (8-ints[3])*8] = casa2

    casa1[0] = ''
    casa1[2] = '0'
    tab[(ints[0]-1) + (8-ints[1])*8] = casa1
