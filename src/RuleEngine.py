from Position import *
from Board import Board
from Moves import Moves
from Position import Position
from copy import deepcopy

'''
This class is responsable for evaluating if some move on the board is valid or not.
 Also it will produce all the moves possibles for each state of a piece.
'''

class RuleEngine (object):

    @staticmethod
    def possibleStates(boardClass = Board(), initialState = Position(0, 0)):
        ''' 
        This method will return all possible states for a piece on a list of Positions.
        Params: 
                board -> the current state of the board
                initialState -> position of actual state of the piece
        '''
        possibleMoves = []
        type = boardClass.getPiece(initialState)
        board = boardClass.getBoard()
        hasEverCapture = False

        if(type == "."):    
            return possibleMoves, False
        if(type.isupper()): #its a double piece and it can move multiply spaces descrease and increaseingly
            #considering top-left
            j = (7-initialState.row) if (7-initialState.row) < initialState.column else initialState.column
            i = 1
            captureAnyPiece = False
            while(i <= j):
                #in case it found one piece from same colour
                if ( board[initialState.row+i][initialState.column-i].lower() == type.lower()):
                    break
                #in case it found an empty space
                elif ( board[initialState.row+i][initialState.column-i] == "." and not captureAnyPiece):
                    possibleMoves.append(Moves(initialState, Position(initialState.row+i, initialState.column-i), 0, False))
                
                #the only rest case, it found an piece to capture and tests if it can jump over
                elif (i < j and (board[initialState.row+i][initialState.column-i].lower() != type.lower() or captureAnyPiece)):
                    if (board[initialState.row+i+1][initialState.column-i-1] == "."):
                        possibleMoves.append(Moves(initialState, Position(initialState.row+i+1, initialState.column-i-1), 1, False))
                        hasEverCapture = True
                        captureAnyPiece = True
                    else:
                        break
                elif (captureAnyPiece and board[initialState.row+i][initialState.column-i] != "."):
                    break
                i += 1

            #considering top-right
            j = (7-initialState.row) if (7-initialState.row) < 7-initialState.column else (7 - initialState.column)
            i = 1
            captureAnyPiece = False
            while(i <= j):
                #in case it found one piece from same colour
                if ( board[initialState.row+i][initialState.column+i].lower() == type.lower()):
                    break
                #in case it found an empty space
                elif ( board[initialState.row+i][initialState.column+i] == "." and not captureAnyPiece):
                    possibleMoves.append(Moves(initialState, Position(initialState.row+i, initialState.column+i), 0, False))
                
                #the only rest case, it found an piece to capture and tests if it can jump over
                elif (i < j and (board[initialState.row+i][initialState.column+i].lower() != type.lower() or captureAnyPiece)):
                    if (board[initialState.row+i+1][initialState.column+i+1] == "."):
                        possibleMoves.append(Moves(initialState, Position(initialState.row+i+1, initialState.column+i+1), 1, False))
                        hasEverCapture = True
                        captureAnyPiece = True
                    else:
                        break
                elif (captureAnyPiece and board[initialState.row+i][initialState.column+i] != "."):
                    break
                i += 1

            #considering bottom-left
            j = (initialState.row) if (initialState.row) < initialState.column else (initialState.column)
            i = 1
            captureAnyPiece = False
            while(i <= j):
                #in case it found one piece from same colour
                if ( board[initialState.row-i][initialState.column-i].lower() == type.lower()):
                    break
                #in case it found an empty space
                elif ( board[initialState.row-i][initialState.column-i] == "." and not captureAnyPiece):
                    possibleMoves.append(Moves(initialState, Position(initialState.row-i, initialState.column-i), 0, False))
                
                #the only rest case, it found an piece to capture and tests if it can jump over
                elif (i < j and (board[initialState.row-i][initialState.column-i].lower() != type.lower() or captureAnyPiece)):
                    if(board[initialState.row-i-1][initialState.column-i-1] == "."):
                        possibleMoves.append(Moves(initialState, Position(initialState.row-i-1, initialState.column-i-1), 1, False))
                        hasEverCapture = True
                        captureAnyPiece = True
                    else:
                        break
                elif (captureAnyPiece and board[initialState.row-i][initialState.column-i] != "."):
                    break
                i += 1

            #considering bottom-right
            j = (initialState.row) if (initialState.row) < 7-initialState.column else (7 - initialState.column)
            i = 1
            captureAnyPiece = False
            while(i <= j):
                #in case it found one piece from same colour
                if ( board[initialState.row-i][initialState.column+i].lower() == type.lower()):
                    break
                #in case it found an empty space
                elif ( board[initialState.row-i][initialState.column+i] == "." and not captureAnyPiece):
                    possibleMoves.append(Moves(initialState, Position(initialState.row-i, initialState.column+i), 0, False))
                
                #the only rest case, it found an piece to capture and tests if it can jump over
                elif (i < j and (board[initialState.row-i][initialState.column+i].lower() != type.lower() or captureAnyPiece)):
                    if(board[initialState.row-i-1][initialState.column+i+1] == "."):
                        possibleMoves.append(Moves(initialState, Position(initialState.row-i-1, initialState.column+i+1), 1, False))
                        hasEverCapture = True
                        captureAnyPiece = True
                    else:
                        break
                elif (captureAnyPiece and board[initialState.row-i][initialState.column+i] != "."):
                    break
                i += 1


        else: #it is a single piece

            if(type.lower() == "b"): #shoud be evaluate mostly increasingly
                
                if(initialState.row < 6): #it still can capture other piece
                    #considering a capture
                    if(initialState.column < 6 and board[initialState.row+1][initialState.column+1].lower() == "w" and board[initialState.row+2][initialState.column+2] == "."):
                        if(initialState.row + 2 == 7): #it will also become double
                            possibleMoves.append(Moves(initialState, Position(initialState.row+2, initialState.column+2), 1, True))
                        else:
                            possibleMoves.append(Moves(initialState, Position(initialState.row+2, initialState.column+2), 1, False))
                        hasEverCapture = True

                    if(initialState.column > 1 and board[initialState.row+1][initialState.column-1].lower() == "w" and board[initialState.row+2][initialState.column-2] == "."):
                        if(initialState.row + 2 == 7): #it will also become double
                            possibleMoves.append(Moves(initialState, Position(initialState.row+2, initialState.column-2), 1, True))
                        else:
                            possibleMoves.append(Moves(initialState, Position(initialState.row+2, initialState.column-2), 1, False))
                        hasEverCapture = True

                    #considering only a simple diagonal move (without capture)    
                    if(initialState.column < 7 and board[initialState.row+1][initialState.column+1] == "."):
                        possibleMoves.append(Moves(initialState, Position(initialState.row+1, initialState.column+1), 0, False))
                    if(initialState.column > 0 and board[initialState.row+1][initialState.column-1] == "."):
                        possibleMoves.append(Moves(initialState, Position(initialState.row+1, initialState.column-1), 0, False))

                else: #now it can only become double
                    if(initialState.column < 7 and board[initialState.row+1][initialState.column+1] == "."):
                        possibleMoves.append(Moves(initialState, Position(initialState.row+1, initialState.column+1), 0, True))
                    if(initialState.column > 0 and board[initialState.row+1][initialState.column-1] == "."):
                        possibleMoves.append(Moves(initialState, Position(initialState.row+1, initialState.column-1), 0, True))
                
                if(initialState.row > 1): #considering it can capture backward
                    if(initialState.column < 6 and board[initialState.row-1][initialState.column+1].lower() == "w" 
                                                        and board[initialState.row-2][initialState.column+2] == "."):
                        possibleMoves.append(Moves(initialState, Position(initialState.row-2, initialState.column+2), 1, False))
                        hasEverCapture = True
                    if(initialState.column > 1 and board[initialState.row-1][initialState.column-1].lower() == "w" 
                                                        and board[initialState.row-2][initialState.column-2] == "."):
                        possibleMoves.append(Moves(initialState, Position(initialState.row-2, initialState.column-2), 1, False))
                        hasEverCapture = True
            
            else: #shoud be evaluate mostly decreasingly
                if(initialState.row > 1): #it still can capture other piece
                    if(initialState.column < 6 and board[initialState.row-1][initialState.column+1].lower() == "b" and board[initialState.row-2][initialState.column+2] == "."):
                        if(initialState.row-2 == 0): #it will also become double
                            possibleMoves.append(Moves(initialState, Position(initialState.row-2, initialState.column+2), 1, True))
                        else:
                            possibleMoves.append(Moves(initialState, Position(initialState.row-2, initialState.column+2), 1, False))
                        hasEverCapture = True

                    if(initialState.column > 1 and board[initialState.row-1][initialState.column-1].lower() == "b" and board[initialState.row-2][initialState.column-2] == "."):
                        if(initialState.row-2 == 0): #it will also become double
                            possibleMoves.append(Moves(initialState, Position(initialState.row-2, initialState.column-2), 1, True))
                        else:
                            possibleMoves.append(Moves(initialState, Position(initialState.row-2, initialState.column-2), 1, False))
                        hasEverCapture = True

                    #considering only a simple diagonal move (without capture)    
                    if(initialState.column < 7 and board[initialState.row-1][initialState.column+1] == "."):
                        possibleMoves.append(Moves(initialState, Position(initialState.row-1, initialState.column+1), 0, False))
                    if(initialState.column > 0 and board[initialState.row-1][initialState.column-1] == "."):
                        possibleMoves.append(Moves(initialState, Position(initialState.row-1, initialState.column-1), 0, False))
                
                else: #now it can only become double
                    if(initialState.column < 7 and board[initialState.row+1][initialState.column+1] == "."):
                        possibleMoves.append(Moves(initialState, Position(initialState.row-1, initialState.column+1), 0, True))
                    if(initialState.column > 0 and board[initialState.row+1][initialState.column-1] == "."):
                        possibleMoves.append(Moves(initialState, Position(initialState.row-1, initialState.column-1), 0, True))
        
                if(initialState.row < 6): #considering it can capture backward
                    if(initialState.column < 6 and board[initialState.row+1][initialState.column+1].lower() == "b"  and board[initialState.row+2][initialState.column+2] == "."):
                        possibleMoves.append(Moves(initialState, Position(initialState.row+2, initialState.column+2), 1, False))
                        hasEverCapture = True
                    if(initialState.column > 1 and board[initialState.row+1][initialState.column-1].lower() == "b"  and board[initialState.row+2][initialState.column-2] == "."):
                        possibleMoves.append(Moves(initialState, Position(initialState.row+2, initialState.column-2), 1, False))
                        hasEverCapture = True

        if(hasEverCapture): #if you can capture any piece, you must capture some piece
            for possibleMove in possibleMoves:
                if(not possibleMove.hasCaptured()):
                    possibleMoves.remove(possibleMove)

        return possibleMoves, hasEverCapture