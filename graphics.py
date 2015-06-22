import Tkinter
import sys
import math
import random
import string
import time
import types
from Tkinter import Frame, Tk, Text, E, W, S, N, BOTH, Canvas, Button, TOP, BOTTOM
import board


class Graphics(Frame):
    
    def __init__(self, parent, board):
        self.MARGIN = 20  # Pixels around the board
        self.SIDE = 50  # Width of every board cell.
        self.WIDTH = self.HEIGHT = self.MARGIN * 2 + self.SIDE * 9  # Width and height of the whole board
        self.board = board
        Frame.__init__(self, parent)
        self.parent = parent
        
        #Queue
        self.queue = []
        
        self.row, self.col = -1, -1
        self.parent.title("CSP Sudoku")
        self.pack(fill=BOTH, expand=1)
        
        self.canvas = Canvas(
            self, width=self.WIDTH, height=self.HEIGHT,
            highlightthickness=0
        )
        self.canvas.pack(fill=BOTH, side=TOP)
        
        
        self.canvas.bind("<Button-1>", self.cell_clicked)
        self.canvas.bind("<Key>", self.key_pressed)

        for i in xrange(10):
            self.canvas.create_line(
                self.MARGIN + i * self.SIDE, self.MARGIN,
                self.MARGIN + i * self.SIDE, self.HEIGHT - self.MARGIN,
                fill="blue" if i % 3 == 0 else "gray"
            )

            self.canvas.create_line(
                self.MARGIN, self.MARGIN + i * self.SIDE,
                self.WIDTH - self.MARGIN, self.MARGIN + i * self.SIDE,
                fill="blue" if i % 3 == 0 else "gray"
            )
        
        #Validation button
        validate_button = Button(
            self, text="Validate",
            command=self.queueValidate
        )
        validate_button.pack(fill=BOTH, side=BOTTOM)
         
        #Draws on the numbers     
        self.draw()
        
    def queueValidate(self):
        if self.board.isOver():
            print "You Win!"
            self.parent.destroy()
     
    #Highlights the selected box   
    def draw_cursor(self):
        self.canvas.delete("cursor")
        if self.row >= 0 and self.col >= 0:
            self.canvas.create_rectangle(
                self.MARGIN + self.col * self.SIDE + 1,
                self.MARGIN + self.row * self.SIDE + 1,
                self.MARGIN + (self.col + 1) * self.SIDE - 1,
                self.MARGIN + (self.row + 1) * self.SIDE - 1,
                outline="red", tags="cursor"
            )
            
    def cell_clicked(self, event,d_o_e=Tkinter.tkinter.dooneevent,
                 d_w=Tkinter.tkinter.DONT_WAIT):
        #d_o_e(d_w)
        x, y = event.x, event.y
        if (x > self.MARGIN and x < self.WIDTH - self.MARGIN and
            y > self.MARGIN and y < self.HEIGHT - self.MARGIN):
            self.canvas.focus_set()
            row, col = (y - self.MARGIN) / self.SIDE, (x - self.MARGIN) / self.SIDE
            if (row, col) == (self.row, self.col):
                self.row, self.col = -1, -1
            elif not (row, col) in self.board.original:
                self.row, self.col = row, col
        else:
            self.row, self.col = -1, -1

        self.draw_cursor()

    def key_pressed(self, event,d_o_e=Tkinter.tkinter.dooneevent,
                 d_w=Tkinter.tkinter.DONT_WAIT):
        if self.row >= 0 and self.col >= 0 and event.char in "1234567890" and not (self.row, self.col) in self.board.original:
            #self.board.put(self.row, self.col, int(event.char))
            self.queue.append((self.row, self.col, int(event.char)))
            code = self.board.put(self.row, self.col, int(event.char))
            self.draw()
            self.col, self.row = -1, -1
            #print self.queue
        
        d_o_e(d_w)

    
    def update(self, board):
        self.board = board
        self.draw()
    
    #This is like an "onDraw" method, when an update occurs we redraw stuff    
    def draw(self):
        self.canvas.delete("numbers")
        for i in xrange(9):
            for j in xrange(9):
                answer = self.board.get(i, j)
                fColor = "slate gray"
                if ((i, j) in self.board.original):
                    fColor = "black"
                if answer != 0:
                    self.canvas.create_text(
                        self.MARGIN + j * self.SIDE + self.SIDE / 2,
                        self.MARGIN + i * self.SIDE + self.SIDE / 2,
                        text=answer, tags="numbers",
                        fill= fColor
                    )
    
    