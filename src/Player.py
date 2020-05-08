from itertools import starmap

from Position import Position
from Moves import Moves
from RuleEngine import RuleEngine
from MoveGenerator import MoveGenerator
from Board import Board

class Player (object):
    def __init__(self, type):
        self.type = type
        self.lastMoveHasCaptured = False
        self.mg = MoveGenerator(type)
        self.lastMove = Moves()
        self.counter = 0
        self.prunedCounter = 0

    def getMove(self, board = Board()):
        moves = []
        playables = self.mg.playablePieces(board)
        if(len(playables) == 0):
            move = Moves()
            move.setLost()
            return move
        if(self.type == board.winner(self.mg)):
            move = Moves()
            move.setWin()
            return move
        if(self.lastMoveHasCaptured):
            move = []
            ans = RuleEngine.possibleStates(board, self.lastMove.finalPosition)
            for move in ans[0]:
                if move.hasCaptured():
                    moves.append(move)
            if(len(moves) == 0):
                print("Você não tem mais jogadas disponíveis!")
                self.lastMoveHasCaptured = False
                return Moves(Position(-1, -1))
        if(self.lastMoveHasCaptured):
            print("Saindo de "+self.lastMove.finalPosition.toString())
            startPos = self.lastMove.finalPosition
        else:
            print("Qual peça você quer mover? <linha> <coluna>")
            rightInput = False
            while(not rightInput):
                start = input().split()
                while(len(start) != 2):
                    print("Entrada inválida!")
                    start = input().split()
                try:
                    startPos = Position(int(start[0]), int(start[1]))
                    if(board.getPiece(startPos).lower() != self.type):
                        print("Você deve escolher uma peça sua para mover!")
                    else:
                        for pos in playables:
                            if(startPos.column == pos.column and startPos.row == pos.row):
                                rightInput = True
                                break
                        if(not rightInput):
                            print("Essa peça não pode ser movida!")
                except:
                    print("Entrada inválida!")
        #by this part, you already has an valid startPosition
        print("Para onde você quer ir? <linha> <coluna>")
        rightInput = False
        while(not rightInput):
            target = input().split()
            while(len(target) != 2):
                print("Dê uma entrada válida: ")
                target = input().split()
            try:
                targetPos = Position(int(target[0]), int(target[1]))
                if(len(moves) == 0):
                    ans = RuleEngine.possibleStates(board, startPos)
                    moves = ans[0]
                if(len(moves) == 0): #if you dont have any move to do
                    move = Moves()
                    move.setLost()
                    return move
                for m in moves:
                    if(m.finalPosition.column == targetPos.column and m.finalPosition.row == targetPos.row):
                        move = m
                        rightInput = True
                if(not rightInput):
                    print("Jogada inválida!")
            except:
                print("Entrada inválida!")
        print(move.toString())
        self.lastMoveHasCaptured = move.hasCaptured()
        self.lastMove = move
        return move
