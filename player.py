import pexpect

# Classe que lida com o pexpect e o gnuchess. Uso so para iniciar um jogador e enviar e receber jogadas

class Player(object):

    def __init__(self, color, verbose=False):
        #constants
        self.verbose = verbose
        self.color = color

        #start gnuchess instance
        self.p = pexpect.spawn('gnuchess/games/gnuchess -x')

        output = self.p.expect(['Chess', pexpect.EOF])
        if output==0:
           if self.verbose: print "GNU Chess started"
        elif output==1:
           if self.verbose: print "error initializing GNU chess agent"
                   
        #change colors if neccessary
        if self.color=="white":
            self.p.sendline("black")
        
    # sends a move to chess engine, returns computer's subsequent move or -1
    def sendMove(self, cmd):
        
        keys = ['wins as black', 'wins as white', 'Illegal move', 'My move is', pexpect.EOF]
        
        self.p.sendline(cmd)
        output = self.p.expect(keys, timeout=240)
        
        if output==0 or output==1:
            if (self.color=="black" and output==0) or (self.color=="white" and output==1):
                if self.verbose: print "Computer wins"
                return -1
            else:
                if self.verbose: print "You win"
                return -1
        
        elif output==2:
            if self.verbose: print "Illegal move: %s" % cmd
            return -1
        
        elif output==3:
            move = self.stripMove(self.p.before)
            if self.verbose: print "Player move: %s" % cmd
            if self.verbose: print "Computer move: %s" % move
            return move
        
        elif output==4:
            if self.verbose: print "EOF reached"
            return -1

    # strips excess characters and returns only move string
    def stripMove(self, stringIn):
        tokens = stringIn.split('...')
        return tokens[len(tokens) - 1].strip()
