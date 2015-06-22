import board
import graphics
import Tkinter
import sys

#from keyboardAgents import KeyboardAgent
import keyboardAgents 
import cspAgents

class Sudoku():
    """
    This class drives the whole Sudoku game.
    """
    def __init__(self, agentNum, startVals):
        self.MARGIN = 20  # Pixels around the board
        self.SIDE = 50  # Width of every board cell.
        self.WIDTH = self.HEIGHT = self.MARGIN * 2 + self.SIDE * 9  # Width and height of the whole board
        self.gameOver = False
        self.board = board.Board(startVals)
        self.agent = self.getAgent(agentNum)
        self.run()
        
    def run(self):
        
        self.agent.run()
        for i in range(9):
            line = []
            for j in range(9):
                line.append(self.board.get(i, j))
            print line
        #something like return self.board
            
    def getAgent(self, agentNum):
        if(agentNum == 0):
            return keyboardAgents.KeyboardAgent(self.board)
        elif(agentNum == 1):
            return cspAgents.CSPAgent(self.board)

class Agent:
    """
    An agent must define a run method

    """
    def __init__(self):
        print "init"  
        
def getStartVals(sFile):
    startVals = []
    with open('%s.sudoku' % sFile, 'r') as pfile:
        i = 0
        for line in pfile:
            line = line.strip()
            if len(line) != 9:
                print "Each line in the sudoku puzzle must be 9 chars long."
                sys.exit(1)
            j = 0
            for c in line.strip():
                if c in "123456789":
                    startVals.append((i, j, int(c)))
                j += 1
            i += 1
    #print startVals
    return startVals

if __name__ == '__main__':
    import argparse, sys
    parser = argparse.ArgumentParser(description='CSP Sudoku solver')
    parser.add_argument('-a', '--agent', dest='agent', 
                       type=int, default=0,
                       help='Determines the solving agent to be used')
    parser.add_argument('-f', '--file', dest='file')
    
    args = parser.parse_args(sys.argv[1:])
    Sudoku(args.agent, getStartVals(args.file))
    