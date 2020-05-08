import sys
from copy import deepcopy
from MoveGenerator import MoveGenerator
from Board import Board
from Moves import Moves
from random import randint
from RuleEngine import RuleEngine
from Neighborhood import Neighborhood
from Position import Position

class IAPruning (object):
    
    def __init__(self, type):
        #sometimes, it try to preview a draw possibility, so it goes to the maximum depth recursion
        self.LIMIT_RECURSION_SECURITY = 200 #this constant is necessery to bypass this problem
        self.type = type
        self.mg = MoveGenerator(type)
        self.alpha = -sys.maxsize -1
        self.beta = sys.maxsize
        self.lastMove = Moves()
        self.lastMoveHasCaptured = False
        self.counter = 0
        self.prunedCounter = 0

    def Max(self, board = Board(), moves = [], depth = 0):
        v = - sys.maxsize - 1 #minint
        self.counter += 1
        if(moves[-1].hasCaptured()): #if it has captured a piece last move
            #still playing
            cBoard = board.copyBoard() 
            for move in moves:
                cBoard.executeMove(move) #execute all last moves
                
            m = RuleEngine.possibleStates(cBoard, moves[-1].finalPosition)
            for move in m[0]:
                if(move.hasCaptured()):
                    moves.append(move)
                    auxV = self.Max(board, moves, depth+1)
                    if auxV > v:
                        v = auxV
                    if auxV > self.alpha:
                        self.alpha = auxV
                    if auxV >= self.beta: #pruning
                        self.prunedCounter += 1
                        break
                    moves.pop()
        else:
            #its the last move

            cBoard = board.copyBoard() 
            for move in moves:
                cBoard.executeMove(move) #execute all last moves

            if (board.isGameOver(self.mg) or depth >= self.LIMIT_RECURSION_SECURITY): 
                return self.mg.utility(board, cBoard)

            m = self.mg.possibleActions(cBoard)
            for possibleMove in m:
                auxV = self.Min(cBoard, [possibleMove], depth+1)
                if auxV > v:
                    v = auxV
                if auxV > self.alpha:
                    self.alpha = auxV
                if auxV >= self.beta: #pruning
                    self.prunedCounter += 1
                    break
        return v

    def Min(self, board = Board(), moves = [], depth = 0):
        v = sys.maxsize  #maxint
        self.counter += 1
        if((moves[-1]).hasCaptured()): #if it has captured a piece last move
            #still playing
            cBoard = board.copyBoard() 
            for move in moves:
                cBoard.executeMove(move) #execute all last moves

            m = RuleEngine.possibleStates(cBoard, moves[-1].finalPosition)
            for move in m[0]:
                if(move.hasCaptured()):
                    moves.append(move)
                    auxV = self.Min(board, moves, depth+1)
                    if auxV < v:
                        v = auxV
                    if auxV < self.beta:
                        self.beta = auxV
                    if auxV <= self.alpha: #pruning
                        self.prunedCounter += 1
                        break
                    moves.pop()
        else:
            #its the last move
                        
            cBoard = board.copyBoard() 
            for move in moves:
                cBoard.executeMove(move) #execute all last moves

            if (board.isGameOver(self.mg) or depth >= self.LIMIT_RECURSION_SECURITY):
                return self.mg.utility(board, cBoard)

            m = self.mg.possibleOponentActions(cBoard)
            for possibleMove in m:
                auxV = self.Max(cBoard, [possibleMove], depth+1)
                if auxV < v:
                    v = auxV
                if auxV < self.beta:
                    self.beta = auxV
                if auxV <= self.alpha: #pruning
                    self.prunedCounter += 1
                    break
        return v


    def getMove(self, board = Board()):
        self.counter = 0
        self.prunedCounter = 0
        self.alpha = -sys.maxsize -1
        self.beta = sys.maxsize
        moves = []
        if(self.lastMoveHasCaptured):
            ans = RuleEngine.possibleStates(board, self.lastMove.finalPosition)
            for move in ans[0]:
                if move.hasCaptured():
                    moves.append(move)
            self.lastMoveHasCaptured = False
        else:
            moves = self.mg.possibleActions(board)
        bestMoveIndex = []
        maxV = -sys.maxsize -1
        for index in range(len(moves)):
            auxV = self.Min(board, [moves[index]])
            if auxV > maxV:
                maxV = auxV
                bestMoveIndex.clear()
                bestMoveIndex.append(index)
            elif auxV == maxV:
                bestMoveIndex.append(index)
        if(len(moves) > 0) :
            if(len(bestMoveIndex) == 0):
                print("==========================ERROR==============================")
                return False
            choose = randint(0, len(bestMoveIndex)-1)
            self.lastMove = moves[bestMoveIndex[choose]]
            if(self.lastMove.hasCaptured()):
                self.lastMoveHasCaptured = True
            return moves[bestMoveIndex[choose]]
        else:
            if(self.lastMove.hasCaptured()):
                return Moves(Position(-1, -1))
            winner = board.winner(self.mg)
            if(winner == self.type):
                move = Moves()
                move.setWin()
                return move
            elif(winner != "."):
                move = Moves()
                move.setLost()
                return move
            print("==========================ERROR==============================")
            return False