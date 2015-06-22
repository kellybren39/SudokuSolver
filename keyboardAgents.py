import sudoku
import Tkinter
import sys
import math
import random
import string
import time
import types
from Tkinter import Frame, Tk, Text, E, W, S, N, BOTH, Canvas, Button, TOP, BOTTOM
import board
from graphics import Graphics

class KeyboardAgent(sudoku.Agent):
    
    def __init__(self, board):
        self.MARGIN = 20  # Pixels around the board
        self.SIDE = 50  # Width of every board cell.
        self.WIDTH = self.HEIGHT = self.MARGIN * 2 + self.SIDE * 9  # Width and height of the whole board
        self.board = board
        self.root = Tk()
        ui = Graphics(self.root, self.board)
        self.root.geometry("%dx%d" % (self.WIDTH, self.HEIGHT + 40))
        
    def run(self):
        self.root.mainloop()
        '''
        for i in xrange(9):
            for j in xrange(8):
                print i, j, self.board.get(i, j)
        '''