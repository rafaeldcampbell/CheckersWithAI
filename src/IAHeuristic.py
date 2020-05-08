from MoveGenerator import MoveGenerator
from Board import Board
import sys
from copy import deepcopy
from Moves import Moves
from RuleEngine import RuleEngine
from Neighborhood import Neighborhood
from Position import Position
from random import randint

class IAHeuristic (object):

    def __init__(self, type, depthLimit = 6):
        self.DEPTH_LIMIT = depthLimit
        self.type = type
        self.mg = MoveGenerator(type)
        self.lastMove = Moves()
        self.lastMoveHasCaptured = False
        self.counter = 0
        self.prunedCounter = 0


    def Max(self, board = Board(), moves = [], depth = 0):
        v = - sys.maxsize - 1 #minint
        self.counter += 1

        cBoard = board.copyBoard() 
        for move in moves:
            cBoard.executeMove(move) #execute all last moves

        if(depth >= self.DEPTH_LIMIT or cBoard.gameover):
            return self.mg.heuristic(cBoard, moves[-1])

        if(moves[-1].hasCaptured()): #if it has captured a piece last move
            #still playing
                
            m = RuleEngine.possibleStates(cBoard, moves[-1].finalPosition)
            for move in m[0]:
                if(move.hasCaptured()):
                    moves.append(move)
                    auxV = self.Max(board, moves, depth+1)
                    if auxV > v:
                        v = auxV
                    moves.pop()
        else:
            #its the last move

            m = self.mg.possibleActions(cBoard)
            for possibleMove in m:
                auxV = self.Min(cBoard, [possibleMove], depth+1)
                if auxV > v:
                    v = auxV
        return v

    def Min(self, board = Board(), moves = [], depth = 0):
        v = sys.maxsize  #maxint
        self.counter += 1

        
        cBoard = board.copyBoard() 
        for move in moves:
            cBoard.executeMove(move) #execute all last moves

        if(depth >= self.DEPTH_LIMIT or cBoard.gameover):
            return self.mg.heuristic(cBoard, moves[-1])

        if((moves[-1]).hasCaptured()): #if it has captured a piece last move
            #still playing

            m = RuleEngine.possibleStates(cBoard, moves[-1].finalPosition)
            for move in m[0]:
                if(move.hasCaptured()):
                    moves.append(move)
                    auxV = self.Min(board, moves, depth+1)
                    if auxV < v:
                        v = auxV
                    moves.pop()
        else:
            #its the last move

            m = self.mg.possibleOponentActions(cBoard)
            for possibleMove in m:
                auxV = self.Max(cBoard, [possibleMove], depth+1)
                if auxV < v:
                    v = auxV
        return v


    def getMove(self, board = Board()):
        self.counter = 0
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