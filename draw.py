import Image

# Funcoes para desenhar o tabuleiro

# Desenha uma peca em um quadrado
def watermark(im, mark, offset=(50,50)):
        if(mark != ''):
            layer = Image.new('RGBA', im.size, (0,0,0,0))
            layer.paste(mark, offset)
            return Image.composite(layer, im, layer)
        return im

# Carrega o sprite de uma peca
def get_mark(square):
    piece = square[0]
    pos = square[1]
    color = square[2]

    mark = ''
    resources = 'Resources/images/'

    if(piece == 'R'):
        if(color == '1'):
            mark = Image.open(resources + 'kb.png')
        elif(color=='2'):
            mark = Image.open(resources + 'kw.png')
    elif(piece == 'D'):
        if(color == '2'):
            mark = Image.open(resources + 'qw.png')
        elif(color=='1'):
            mark = Image.open(resources + 'qb.png')
    elif(piece == 'T'):
        if(color == '2'):
            mark = Image.open(resources + 'rw.png')
        elif(color == '1'):
            mark = Image.open(resources + 'rb.png')
    elif(piece == 'C'):
        if(color == '2'):
            mark = Image.open(resources + 'nw.png')
        elif(color == '1'):
            mark = Image.open(resources + 'nb.png')
    elif(piece == 'B'):
        if(color == '2'):
            mark = Image.open(resources + 'bw.png')
        elif(color == '1'):
            mark = Image.open(resources + 'bb.png')
    elif(piece == 'p'):
        if(color == '2'):
            mark = Image.open(resources + 'pw.png')
        elif(color == '1'):
            mark = Image.open(resources + 'pb.png')
    else:
        mark = ''
            
    return mark

# Desenha o tabuleiro em um estado qualquer
def draw_chessboard(pixel_width, tabuleiro, file="Resources/images/state.png"):
    
    image = Image.open("Resources/images/tabuleiro.png")

    for i in range(64):
        square = tabuleiro[i]
        mark = get_mark(square)

        offset = ((i%8)*63, (i/8)*62)
        image = watermark(image, mark, offset)
    
    if (file != "Resources/images/state.png"):
        image.save(file)
            
    image.save("Resources/images/state.png")
