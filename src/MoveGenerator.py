'''
This class will be responsable for generating all moves for one player in one defined state


                                                           _____________________________________
                                                          |                                     |
                                                          |      HIERARCHY OF HEURISTIC         |
Heuristic:                                                |_____________________________________|
                                                          |                                     |
                                                          |   Double + capture + canCapture   1 |
                                                          |         Double + capture          2 |
                                                          |     capture > 3 + canCapture      3 |
                                                          |         Double + canCapture       4 |
                                                          |     capture < 3 + canCapture      5 |  
    heuristicToMove(i)    <-- tax                         |            capture > 3            6 |
            willCapture   <-- + number of captures*3      |               double              7 |
            becomeDouble  <-- + 9                         |            capture < 3            8 |
                                                          |_____________________________________|
    tax <-- [2+(canCapture - canBeCaptured)] (since is guaranteed it variate from -2 to 3
                                                              this tax will go from 0 to 5)
'''
from Board import Board
from RuleEngine import RuleEngine
from Neighborhood import Neighborhood
from copy import deepcopy

class MoveGenerator (object):
    def __init__(self, type = "b"):
        self.type = type
        self.oponentType = "w" if self.type == "b" else "b"
        self.MAX_ITE = 6
        self.hasEverCaptured = False

    def playablePieces(self, board = Board()):
        self.hasEverCaptured = False
        actions = []
        moveablePieces = []
        playable = []
        pieces = board.getAllPieces(self.type)
        for piece in pieces:
            ans = RuleEngine.possibleStates(board, piece)
            if(len(ans[0]) > 0):
                actions.append([piece, ans[1]])
                moveablePieces.append(piece)
            if(ans[1]):
                self.hasEverCaptured = True
        if(self.hasEverCaptured): #if you can capture any piece, you must capture some piece
            for piece in actions:
                if(piece[1]):
                    playable.append(piece[0])
            return playable
        else:
            return moveablePieces

    def possibleActions(self, board = Board()):
        '''
        this method returns all actions the current player can take, as (initialPosition) -> (finalPosition)
        '''
        gameover = board.gameover
        goodActions = []
        if(not gameover):
            actions = []
            self.hasEverCaptured = False
            for piece in board.getAllPieces(self.type):
                moves,ans = RuleEngine.possibleStates(board, piece)
                actions = actions+moves
                if(ans):
                    self.hasEverCaptured = True
            if(self.hasEverCaptured): #if you can capture any piece, you must capture some piece
                for i in range (len(actions)):
                    if(actions[i].hasCaptured()): 
                        goodActions.append(actions[i])
            else:
                goodActions = actions[:]
        
        return goodActions
    

    def possibleOponentActions(self, board = Board()):
        '''
        this method returns all actions the oponent player can take, as (initialPosition) -> (finalPosition)
        '''
        gameover = board.gameover
        goodActions = []
        if(not gameover):
            actions = []
            self.hasEverCaptured = False
            for piece in board.getAllPieces(self.oponentType):
                moves,ans = RuleEngine.possibleStates(board, piece)
                actions = actions+moves
                if(ans):
                    self.hasEverCaptured = True
            if(self.hasEverCaptured): #if you can capture any piece, you must capture some piece
                for i in range (len(actions)):
                    if(actions[i].hasCaptured()): 
                        goodActions.append(actions[i])

            else:
                goodActions = actions[:]
            
        return goodActions


    def heuristic(self, board, move):
        becomeDouble = 0
        if(move.gettingDouble):
            becomeDouble = 9
        willCapture = move.capturedPieces*3
        board.executeMove(move)
        neighbors = Neighborhood.verifyNeighborhood(board, move.finalPosition)
        return (2+(neighbors.canCaptureCount - neighbors.canBeCapturedCount)) + willCapture + becomeDouble

    def utility(self, oldBoard, newBoard):
        blackdoubles = newBoard.blackDoubles - oldBoard.blackDoubles
        whitedoubles = newBoard.whiteDoubles - oldBoard.whiteDoubles

        capturedBlacks = newBoard.blackCaptured - oldBoard.blackCaptured
        capturedWhites = newBoard.whiteCaptured - oldBoard.whiteCaptured
        
        if (self.type.lower() == "b"):
            if newBoard.whiteCaptured == 12: return 999999
            return ((blackdoubles - whitedoubles)*3) + (capturedWhites - capturedBlacks)
        else:
            if newBoard.blackCaptured == 12: return 999999
            return ((whitedoubles - blackdoubles)*3) + (capturedBlacks - capturedWhites)