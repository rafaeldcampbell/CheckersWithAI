
'''
This class represent a position or a move.
'''

class Position (object):

    def __init__(self, row, column):
        self.row = row
        self.column = column
        self.isDouble = False

    def toString(self):
        text = "("+str(self.row)+", "+str(self.column)+")"
        return text

    def becomeDouble(self):
        self.isDouble = True
