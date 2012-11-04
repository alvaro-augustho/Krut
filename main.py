import move
import subprocess
import aux
import player
from detect import gerar_vetor
import time
import draw

# Principal

game_state  = move.init() # monta o estado inicial do jogo
draw.draw_chessboard(500, game_state) #desenha o estado inicial
viewer = subprocess.Popen(['/usr/bin/eog', 'Resources/images/state.png']) # e exibe

# Esse loop abre imagem a imagem da pasta de screenshots e analisa a jogada entre uma imagem e a proxima. 
# Na quinta imagem uma rainha branca era identificada como preta e tudo dava pau

"""
vetor = gerar_vetor("images/chess-1.png")
jogada = move.identifica_jog(game_state, vetor)
print "-1",jogada
move.executa_jogada(jogada, new)

for i in range(5):
    
    path = "images/chess" + str(i) + ".png"
    vetor = gerar_vetor(path)

    if(i == 4):
        print vetor
    
    jogada = move.identifica_jog(game_state, vetor)
    print str(i),jogada
    move.executa_jogada(jogada, game_state)

"""



# Nao sei se tinha algum jeito mais pythonico de fazer esse loop
i = 0
while True:
    if(i == 0): # jogada inicial
        p1 = player.Player("black", True) # cria os jogadores, iniciando 2 gnuchess, e coloca um contra o outro
        p2 = player.Player("black", True)
        jogada = p1.sendMove("go") # p1 comeca, e se torna o jogador branco
    elif ((i%2)==0):
        jogada = p1.sendMove(jogada)  # manda uma jogada para o adversario, e recebe a jogada dele como retorno
    else:
        jogada = p2.sendMove(jogada) # mesma coisa. Para colocar uma pessoa jogando eh so mudar uma dessas linhas
    
    move.executa_jogada(jogada, game_state) # muda o estado do tabuleiro com a nova jogada
    file = "images/chess" + str(i) + ".png"  # nome do novo screenshot que sera salvo
    draw.draw_chessboard(500, game_state, file)   # desenha o novo tabuleiro
    viewer = subprocess.Popen(['/usr/bin/eog', "Resources/images/state.png"]) # exibe o novo estado do jogo
    
    i = i+1
#    time.sleep(5)   # dorme por 5 segundos, para exibir o tabuleiro atual por este tempo
