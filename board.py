class Board():
    """
    A board represents the 9 by 9 grid that the game is played on. It keeps
    track of the values at each position, with 0 representing empty. It is
    essentially a dictionary initialized to 0, with a few helper functions
    to barf up errors if we try to access/place anything outside of Sudoku's
    rules, and some checks to see if we've won or something. It's conceptually 
    inspired by the Counter utility in programming assignment 3, but 
    implemented very differently.
    
    ...
    
    Return code cheat sheet (for return codes, not calculations by a function):
    0   -  Everything A-okay!
    -1  -  Requested location is not within the grid (i.e. less that (0,0) or
            greater than (8,8)
    -2  -  Value outside possible value range (i.e. trying to place something
            less than 1 or greater than 9)
    
    """
    def __init__(self, startVals):
        
        self.board = dict()
        self.MAX = 8
        self.MIN = 0
        self.V_MAX = 9
        self.V_MIN = 0
        self.fullSpots = 0
        self.SUBS = 3
        self.SUB_L = 3
        #The locations specified by the original puzzle
        self.original = []
        #A queue of actions executed by the player
        self.queue = []
        self.startVals = startVals
        self.setup(startVals)
        
    def get(self, x, y):
        if(x < self.MIN or y < self.MIN or x > self.MAX or y > self.MAX):
            print "X or Y out of range of board, X =", x, "and Y =", y
            return -1
        return self.board.get((x,y), 0)
    
    def put(self, x, y, val):
        if(x < self.MIN or y < self.MIN or x > self.MAX or y > self.MAX):
            print "X or Y out of range of board, X =", x, "and Y =", y
            return -1
        if(val < self.V_MIN or val > self.V_MAX):
            print "Value not allowed on board, value =", val
            return -2
        if self.get(x, y) == 0:
            if not val == 0:
                self.fullSpots += 1
        else:
            self.fullSpots -= 1
        self.board[(x,y)] = val
        return 0
    
    def isFull(self):
        fs = 0
        for i in range(9):
            for j in range(9):
                if not self.get(i, j) == 0:
                    fs += 1
                
        if fs == 81:
            return True
        else:
            return False
    
    #startVals is a list of tuples (x-coordinate, y-coordinate, value) that
    # correspond to the initial values for the board    
    def setup(self, startVals):
        for v in startVals:
            self.put(v[0], v[1], v[2])
            #self.fullSpots += 1
            self.original.append((v[0], v[1]))
            
    def countFilled(self):
        return self.fullSpots
    
    def checkLine(self, axis, line):
        already = []
        for i in range(self.MAX):
            if axis == 'x':
                coord = (i, line)
            elif axis == 'y':
                coord = (line, i)
            if self.get(coord[0], coord[1]) in already or self.get(coord[0], coord[1]) == 0:
                return False
            else:
                already.append(self.get(coord[0], coord[1]))
        return True
                
        '''
        check = dict()
        for i in range(self.MAX):
            if axis == 'x':
                coord = (i, line)
            elif axis == 'y':
                coord = (line, i)
            val = self.board.get(coord, 0)
            if not check.get(val) == 0:
                return False
            else:
                check[val] = coord
        return True
        '''
    
    def checkSub(self, x, y):
        check = []
        for i in range(self.SUB_L):
            for j in range(self.SUB_L):
                coord = (x+i, y+j)
                val = self.board.get(coord, 0)
                if val in check or val == 0:
                    return False
                else:
                    check.append(val)
        return True
    
    def isOver(self):
        '''
        This is the most fun function in Board. Its purpose is to determine
        if a Sudoku game has been completed. This means that:
        1. The board is full
        2. No row has repeat numbers
        3. No column has repeat numbers
        4. None of the 9 3x3 sub-boxes has repeat numbers
        I ensure that no number is outside the range 1-9 or empty within other
        functions, so there is no need to check that here.
        '''
        if not self.isFull():
            return False
        for i in range(self.MAX):
            if not self.checkLine('x', i):
                return False
        for i in range(self.MAX):
            if not self.checkLine('y', i):
                return False
        for i in range(self.SUBS):
            for j in range(self.SUBS):
                if not self.checkSub(i*3, j*3):
                    return False
        return False
    
    