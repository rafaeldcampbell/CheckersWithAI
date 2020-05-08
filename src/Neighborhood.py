from Position import *
from Board import *

class Neighbor (object):
    
    def __init__(self, row, column, canCapture = False, canBeCaptured = True):
        self.position = Position(row, column)
        self.canCapture = canCapture
        self.canBeCaptured = canBeCaptured

#endclassNeibor

class Neighbors (object):
    
    def __init__(self):
        '''
            dict <-  has           : if it is null or not              DEFAULT FALSE
                     isEmpty       : if it is "." or oponent           DEFAULT TRUE
                     position      : neighbor
                     canBeCaptured : if this neighbor can capture      DEFAULT TRUE
                     canCapture    : if it can capture this neighbot   DEFAULT FALSE
        '''
        self.lb = dict()
        self.lt = dict()
        self.rb = dict()
        self.rt = dict()
        self.canCaptureCount = 0
        self.canBeCapturedCount = 4

    def setLb(self, row, column):
        self.lb["isEmpty"] = False
        self.lb["position"] = Neighbor(row, column)

    def setLt(self, row, column):
        self.lt["isEmpty"] = False
        self.lt["position"] = Neighbor(row, column)

    def setRb(self, row, column):
        self.rb["isEmpty"] = False 
        self.rb["position"] = Neighbor(row, column)

    def setRt(self, row, column):
        self.rt["isEmpty"] = False
        self.rt["position"] = Neighbor(row, column)

    def toString(self):
        text = ""
        if(self.lb.get("has", False) and not self.lb.get("isEmpty", True)):
            text += "\n\t-> vizinho à esquerda-fundo"
            if(self.lb.get("canCapture", False)):
                text += ", pode ser capturado"
            if(self.lb.get("canBeCaptured", True)):
                text += ", ele pode nos capturar"
        if(self.lt.get("has", False) and not self.lt.get("isEmpty", True)):
            text += "\n\t-> vizinho à esquerda-topo"
            if(self.lt.get("canCapture", False)):
                text += ", pode ser capturado"
            if(self.lt.get("canBeCaptured", True)):
                text += ", ele pode nos capturar"
        if(self.rb.get("has", False) and not self.rb.get("isEmpty", True)):
            text += "\n\t-> vizinho à direita-fundo"
            if(self.rb.get("canCapture", False)):
                text += ", pode ser capturado"
            if(self.rb.get("canBeCaptured", True)):
                text += ", ele pode nos capturar"
        if(self.rt.get("has", False) and not self.rt.get("isEmpty", True)):
            text += "\n\t-> vizinho à direita-topo"
            if(self.rt.get("canCapture", False)):
                text += ", pode ser capturado"
            if(self.rt.get("canBeCaptured", True)):
                text += ", ele pode nos capturar"
        
        return text
#endclassNeibors

class Neighborhood (object):

    @staticmethod
    def verifyNeighborhood(boardClass = Board(), piecePosition = Position(0, 0)):
        neighbors = Neighbors()
        board = boardClass.getBoard()
        pieceType = boardClass.getPiece(piecePosition).lower()
        oponentType = "b" if pieceType == "w" else "w"

        #verifying if it has neighbors
        if ( piecePosition.row > 0 and piecePosition.column > 0): #can has someone left-bottom
            neighbors.lb["has"] = True
            if(board[piecePosition.row-1][piecePosition.column-1].lower() == oponentType):
                neighbors.setLb(piecePosition.row+1, piecePosition.column-1)
                
        if ( piecePosition.row > 0 and piecePosition.column < 7): #can has someone right-bottom
            neighbors.rb["has"] = True
            if(board[piecePosition.row-1][piecePosition.column+1].lower() == oponentType):
                neighbors.setRb( piecePosition.row-1, piecePosition.column+1 )
                
        if ( piecePosition.row < 7 and piecePosition.column > 0): #can has someone left-top
            neighbors.lt["has"] = True
            if(board[piecePosition.row+1][piecePosition.column-1].lower() == oponentType):
                neighbors.setLt( piecePosition.row+1, piecePosition.column-1 )
                
        if ( piecePosition.row < 7 and piecePosition.column < 7): #can has someone right-top
            neighbors.rt["has"] = True
            if(boardClass.getPiece(Position(piecePosition.row+1, piecePosition.column+1)).lower() == oponentType):
                neighbors.setRt( piecePosition.row+1, piecePosition.column+1 )

        #setting canBeCaptured for neighbors
        if((not neighbors.lt.get("isEmpty", True)) or (not neighbors.lt.get("has", False))):
            neighbors.canBeCapturedCount -= 1
            neighbors.rb["canBeCaptured"] = False

        if(not neighbors.rb.get("isEmpty", True)) or (not neighbors.rb.get("has", False)):
            neighbors.canBeCapturedCount -= 1
            neighbors.lt["canBeCaptured"] = False 

        if(not neighbors.lb.get("isEmpty", True)) or (not neighbors.lb.get("has", False)):
            neighbors.canBeCapturedCount -= 1
            neighbors.rt["canBeCaptured"] = False

        if((not neighbors.rt.get("isEmpty", True)) or (not neighbors.rt.get("has", False))):
            neighbors.canBeCapturedCount -= 1
            neighbors.lb["canBeCaptured"] = False
        

        #setting canCapture for neighbor
        if(neighbors.lt.get("has", False) and not neighbors.lt.get("isEmpty", False) and piecePosition.row < 6 and
         piecePosition.column > 1 and board[piecePosition.row+2][piecePosition.column-2] == "."):
            neighbors.lt["canCapture"] = True
            neighbors.canCaptureCount += 1

        if(neighbors.lb.get("has", False) and not neighbors.lb.get("isEmpty", False) and piecePosition.row > 1 and
         piecePosition.column > 1 and board[piecePosition.row-2][piecePosition.column-2] == "."):
            neighbors.lb["canCapture"] = True
            neighbors.canCaptureCount += 1

        if(neighbors.rt.get("has", False) and not neighbors.rt.get("isEmpty", False) and piecePosition.row < 6 and
         piecePosition.column < 6 and board[piecePosition.row+2][piecePosition.column+2] == "."):
            neighbors.rt["canCapture"] = True
            neighbors.canCaptureCount += 1

        if(neighbors.rb.get("has", False) and not neighbors.rb.get("isEmpty", False) and piecePosition.row > 1 and
         piecePosition.column < 6 and board[piecePosition.row-2][piecePosition.column+2] == "."):
            neighbors.rb["canCapture"] = True
            neighbors.canCaptureCount += 1

        return neighbors
