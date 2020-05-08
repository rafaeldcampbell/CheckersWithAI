from Position import Position

class Moves (object):

    def __init__(self, initialPosition = Position(0,0), finalPosition = Position(0,0), capturedPieces = 0, gettingDouble = False):
        self.initialPosition = initialPosition
        self.finalPosition = finalPosition
        self.possibleMoves = []
        self.capturedPieces = capturedPieces
        self.gettingDouble = gettingDouble
        self.lost = False
        self.win = False

    def hasCaptured(self):
        if(self.capturedPieces > 0):
            return True
        return False
    
    def setLost(self):
        self.lost = True

    def setWin(self):
        self.win = True

    def toString(self):
        text = self.initialPosition.toString()+ " -> " + self.finalPosition.toString() + " | " #gettin first move
        text = text + " capturando "+str(self.capturedPieces)+" peça(s)"
        if(self.gettingDouble):
            text = text + " e virando dama"
        return text