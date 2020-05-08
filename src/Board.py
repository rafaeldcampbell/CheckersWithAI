from Position import Position
from Moves import Moves
from copy import deepcopy

'''
"w" for white pieces and "W" for double white pieces
"b" for black pieces and "B" for double black pieces
"a" for black or white pieces
'''
class Board (object):

    def __init__(self):
        self.initializeBoard()
        self.blackCaptured = 0
        self.whiteCaptured = 0
        self.blackDoubles = 0
        self.whiteDoubles = 0
        self.gameover = False

    def getBoard(self):
        return self.board

    def doublePiece(self, position = Position(0,0)):
        self.board[position.row][position.column] = self.board[position.row][position.column].upper()


    def getPiece(self, position = Position(0,0)):
        return self.board[position.row][position.column]


    def initializeBoard(self):
        self.board = []
        for i in range(8):
            row = []
            for j in range(8):
                if(i > 4 and (i+j)%2 != 0): # 
                    row.append("w")
                elif(i < 3 and (i+j)%2 != 0): # 
                    row.append("b")
                else:
                    if((i+j)%2 == 0): row.append("-")
                    else: row.append(".") # "." for empty spaces
            self.board.append(row)
        return True


    def printBoard(self):
        print("\n\n")
        for i in range(7, -1, -1):
            print(i, end="    ")
            for j in range(8):
                print(self.board[i][j], end="  ")
            print()
        print()
        print("     ", end="")
        for num in range(8):
            print(num, end="  ")
        print("\n\n")
        return True


    def movePiece(self, initialState = Position(0, 0), finalState = Position(1, 1), becomeDouble = False):
        aux = self.board[finalState.row][finalState.column]
        if(becomeDouble):
            self.board[finalState.row][finalState.column] = self.board[initialState.row][initialState.column].upper()
            if(self.board[initialState.row][initialState.column].lower() == "b"):
                self.blackDoubles += 1
            else:
                self.whiteDoubles += 1
        else:
            self.board[finalState.row][finalState.column] = self.board[initialState.row][initialState.column]
        self.board[initialState.row][initialState.column] = aux


    def capturePiece(self, position = Position(0, 0)):
        '''
        This method will capture one piece passed by the position and
        increase the respective pieceCaptured counter.
        When this method is called, it's important that the position
        passed is, assuredly, one black or white piece. 
        '''

        if(self.board[position.row][position.column].lower() == "b"):
            self.blackCaptured += 1
            if(self.blackCaptured == 12):
                self.gameover = True
        else:
            self.whiteCaptured += 1
            if(self.whiteCaptured == 12): 
                self.gameover = True
        
        self.board[position.row][position.column] = "."

    def capturePieceForDouble(self, p1 = Position(0, 0), p2 = Position(0, 0), type = "b"):
        oponentType = "w" if type == "b" else "b"
        column = p2.column - p1.column
        row = p2.row - p1.row
        mcolumn = column if column > 0 else -column
        mrow = row if row > 0 else -row
        if(mcolumn > mrow):
            for i in range(mrow):
                if(self.board[p1.row+(int(row/mrow)*i)][p1.column+(int(column/mcolumn)*i)].lower() == oponentType):
                    self.capturePiece(Position(p1.row+(int(row/mrow)*i), p1.column+(int(column/mcolumn)*i)))
        else:
            for i in range(mcolumn):
                if(self.board[p1.row+(int(row/mrow)*i)][p1.column+(int(column/mcolumn)*i)].lower() == oponentType):
                    self.capturePiece(Position(p1.row+(int(row/mrow)*i), p1.column+(int(column/mcolumn)*i)))

    def executeMove(self, move):
        '''
        From here, it's important that move is assuredly a valid move
        '''
        self.movePiece(move.initialPosition, move.finalPosition, move.gettingDouble)
        if(move.capturedPieces > 0):
            type = self.board[move.finalPosition.row][move.finalPosition.column]
            if(type.isupper()):
                self.capturePieceForDouble(move.initialPosition, move.finalPosition, type.lower())
            else:
                self.capturePiece(Position(int((move.initialPosition.row + move.finalPosition.row)/2), int((move.initialPosition.column + move.finalPosition.column)/2)))
                

    def getAllPieces(self, type = "a"):
        '''
        this method will return a list of all pieces
        '''
        pieces = []
        for i in range(8):
            for j in range(8):
                if (type == "a"):
                    if(self.getPiece(Position(i, j)).lower() in ["w", "b"]):
                        pieces.append(Position(i, j))
                elif(self.getPiece(Position(i, j)).lower() == type.lower()):
                        pieces.append(Position(i, j))
        return pieces

    def copyBoard(self):
    	return deepcopy(self)

    def isGameOver(self, mg): #returns ifGameIsOver/winner
        if(self.gameover):
            return True
        if(len(mg.possibleActions(self))== 0): 
            self.gameover = True
            return True
        if(len(mg.possibleOponentActions(self)) == 0):
            self.gameover = True
            return True
        return False


    def winner(self, mg): #returns ifGameIsOver/winner
        if(self.gameover):
            if(self.blackCaptured == 12): return "w"
            if(self.whiteCaptured == 12): return "b"
        if(len(mg.possibleActions(self))== 0): 
            self.gameover = True
            return mg.oponentType
        if(len(mg.possibleOponentActions(self)) == 0):
            self.gameover = True
            return mg.type
        return "."
