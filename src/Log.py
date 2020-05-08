from datetime import datetime
class Log (object):

    def __init__(self, player):
        dateNow = datetime.now()
        date = "_"+str(dateNow.year)+"_"+str(dateNow.month)+"_"+str(dateNow.day)+"_"+str(dateNow.hour)+"_"+str(dateNow.minute)+"_"+str(dateNow.second)
        nameFile = "Log_for_"+player+date+".txt"
        try:
            self.file = open("log/"+nameFile, "w", encoding="utf8")
        except:
            self.file = open("../log/"+nameFile, "w", encoding="utf8")

    def writeLog(self, line):
        self.file.write(line+"\n")

    def jumpLine(self):
        self.file.write("\n")

    def writeTime(self, roundCounter, time):
        ''' 
        This method writes in log the time that an search take for an round
        @params:
                time -> number of seconds it spends in search
                depth -> maximum depth of the current search
                roung -> number of current round
        '''
        self.file.write("Para a jogada "+str(roundCounter)+" ==> "+str(time)+" segundos\n")
    
    def writeNodesAndPruning(self, roundCounter, totalNodes, totalPruned):
        self.file.write("Para a jogada "+str(roundCounter)+" ==> visitados "+str(totalNodes)+" nós, com "+str(totalPruned)+" podados\n")


    def writeChangesInBoard(self, roundCounter, moveToString):
        self.file.write("Para a jogada "+str(roundCounter)+" ==> "+moveToString+"\n")

    def saveAndCloseLog(self):
        self.file.close()