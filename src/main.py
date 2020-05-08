from Board import Board
from RuleEngine import RuleEngine
from Position import Position
from Neighborhood import Neighborhood
from MoveGenerator import MoveGenerator
from IAPruning import IAPruning
from IAHeuristic import IAHeuristic
from Player import Player
import time
from Log import Log
import os
clear = lambda: os.system('cls') or None



print("Escolha o primeiro jogador (brancas):")
print("1. IA Minimax com Poda Alfa e Beta")
print("2. IA Minimax com profundidade limitada e avaliação heuristica")
print("3. Você")
choose = input()
while(choose not in ["1", "2", "3"]):
    print("Escolha entre 1, 2 e 3")
    choose = input()
if(choose == "1"):
    iaw = IAPruning("w")
    msgW = "Pruning"
elif(choose == "2"):
    iaw = IAHeuristic("w", 3)
    msgW = "Heuristic"
else:
    iaw = Player("w")
    msgW = "Player"

print("Escolha o segundo jogador (pretas):")
print("1. IA Minimax com Poda Alfa e Beta")
print("2. IA Minimax com profundidade limitada e avaliação heuristica")
print("3. Você")
choose = input()
while(choose not in ["1", "2", "3"]):
    print("Escolha entre 1, 2 e 3")
    choose = input()
if(choose == "1"):
    iab = IAPruning("b")
    msgB = "Pruning"
elif(choose == "2"):
    iab = IAHeuristic("b", 3)
    msgB = "Heuristic"
else:
    iab = Player("b")
    msgB = "Player"

logTotal = Log("whole_play_black_"+msgB+"_vs_white_"+msgW)
logTotal.writeLog("Blacks: "+msgB+"\nWhites: "+msgW+"\n\n")
endGame = False
gameCounter = 0
while(not endGame):
    gameCounter += 1
    turnB = False
    roundCounter = 0
    board = Board()
    logB = Log("black_"+msgB)
    logW = Log("white_"+msgW)
    wholeGameStartTimeStamp = time.time()
    while(roundCounter < 150):
        time.sleep(1)
        roundCounter += 1
        if(turnB):
            startTimeStamp = time.time()
            move = iab.getMove(board)
            finishTimeStamp = time.time()
            if(not move.lost):
                if(move.win):
                    wholeGameFinishTimeStamp = time.time()
                    print("=========== Pretas ganharam =============")
                    logB.writeLog("=========== VITÓRIA =============")
                    logW.writeLog("=========== DERROTA =============")
                    logTotal.writeLog("Para o jogo "+str(gameCounter)+" ==> pretas vencem em "+
                    str(wholeGameFinishTimeStamp - wholeGameStartTimeStamp - roundCounter)+" segundos\n\n")
                    break
                if(move.initialPosition.column == -1 and
                move.initialPosition.row == -1):
                    turnB = False
                else:
                    logB.writeTime(roundCounter, finishTimeStamp - startTimeStamp)
                    logB.writeNodesAndPruning(roundCounter, iab.counter, iab.prunedCounter)
                    logB.writeChangesInBoard(roundCounter, move.toString())
                    logB.jumpLine()
                    board.executeMove(move)   
                    clear()
                    print("Jogada", roundCounter, "B ==> ", move.toString())
                    board.printBoard()
                    print("\n\n")
                    if(not move.hasCaptured()):
                        turnB = False
            else:
                wholeGameFinishTimeStamp = time.time()
                print("=========== Brancas ganharam =============")
                logW.writeLog("=========== VITÓRIA =============")
                logB.writeLog("=========== DERROTA =============")
                logTotal.writeLog("Para o jogo "+str(gameCounter)+" ==> brancas vencem em "+
                    str(wholeGameFinishTimeStamp - wholeGameStartTimeStamp - roundCounter)+" segundos\n\n")
                break
        else:
            if(msgW == "Player" and roundCounter == 1):
                board.printBoard()
            startTimeStamp = time.time()
            move = iaw.getMove(board)
            finishTimeStamp = time.time()
            if(not move.lost):
                if(move.win):
                    wholeGameFinishTimeStamp = time.time()
                    print("=========== Brancas ganharam =============")
                    logW.writeLog("=========== VITÓRIA =============")
                    logB.writeLog("=========== DERROTA =============")
                    logTotal.writeLog("Para o jogo "+str(gameCounter)+" ==> brancas vencem em "+
                        str(wholeGameFinishTimeStamp - wholeGameStartTimeStamp - roundCounter)+" segundos\n\n")
                    break
                if(move.initialPosition.column == -1 and
                    move.initialPosition.row == -1):
                    turnB = True
                else:
                    logW.writeTime(roundCounter, finishTimeStamp-startTimeStamp)
                    logW.writeNodesAndPruning(roundCounter, iaw.counter, iaw.prunedCounter)
                    logW.writeChangesInBoard(roundCounter, move.toString())
                    logW.jumpLine()
                    board.executeMove(move)
                    clear()
                    print("Jogada", roundCounter, "W ==> ", move.toString())
                    board.printBoard()
                    print("\n\n")
                    if(not move.hasCaptured()): turnB = True
            else:
                wholeGameFinishTimeStamp = time.time()
                print("=========== Pretas ganharam =============")
                logB.writeLog("=========== VITÓRIA =============")
                logW.writeLog("=========== DERROTA =============")
                logTotal.writeLog("Para o jogo "+str(gameCounter)+" ==> pretas vencem em "+
                    str(wholeGameFinishTimeStamp - wholeGameStartTimeStamp - roundCounter)+" segundos\n\n")
                break

    if(roundCounter == 300):
        wholeGameFinishTimeStamp = time.time()
        print("=========== Pretas e brancas empataram =============")
        logTotal.writeLog("Para o jogo "+str(gameCounter)+" ==> brancas e pretas empataram em "+
            str(wholeGameFinishTimeStamp - wholeGameStartTimeStamp - roundCounter)+" segundos\n\n")
    
    print("Deseja continuar jogando? (s/n)")
    ans = input()
    while(ans not in ["s", "n"]):
        print("Entrada inválida!")
        ans = input()
    if(ans == "n"):
        endGame = True
    logW.saveAndCloseLog()
    logB.saveAndCloseLog()

logTotal.saveAndCloseLog()