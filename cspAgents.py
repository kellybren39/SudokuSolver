import sudoku, sys, board


class CSPAgent():
    
    def __init__(self, board):
        self.board = board
        #possible values for sudoku
        self.domain = [1,2,3,4,5,6,7,8,9]
        '''
        This is used in forward checking and maintaining arc consistency. There are 27 value pools,
        9 for each row, column, and box. When a variable is assigned a value, that value is removed
        from the corresponding row, column, and box pool. The first 9 are the 9 rows, then columns,
        then boxes. If a failure is returned, we put the value back in the pools and continue on as
        part of our backtracking.
        '''
        self.valPools = []
        for i in range(27):
            self.valPools.append([])
            for j in range(1, 10):
                self.valPools[i].append(j)
        
        #an easy look up for which valPools a location (x, y) belongs to        
        self.vPIndex = dict()
        for i in range(9):
            for j in range(9):
                b = self.getB(i, j)
                self.vPIndex[(i, j)] = (i, j + 9, b)
                
        self.vars = []
        
        for i in range(9):
            for j in range(9):
                val = self.board.get(i, j)
                self.vars.append(((i, j), val))
        print "first self vars", self.vars
                
        self.varInd = 0
        
        self.immut = []
        for m in self.board.startVals:
            self.immut.append((m[0], m[1]))
        
        
        
    def run(self):
        self.backtrackingSearch()
        
    def backtrackingSearch(self):
        #print self.board
        for m in self.board.startVals:
            self.removeFromPool((m[0], m[1]), self.board.get(m[0], m[1]))
            self.vars[(9*m[0] + m[1])] = ((m[0], m[1]), m[2])
        print "self.vars =", self.vars
        #print self.valPools
        #print "domain is", self.domain
        if not self.backtracking():
            print "This board is unsolvable"
            sys.exit(1)
        #print self.vars
        self.assign()
        
    def backtracking(self):
        if self.varInd >= 81:
            return True
        tInd = self.varInd
        var = self.vars[tInd][0]
        self.varInd += 1
        if var in self.immut:
            print "PoopyButt", var
            result = self.backtracking()
            if result:
                return True
        #if not var in self.immut:
        else:
            for v in self.domain:
                if self.inValPool(var, v):
                    self.vars[tInd] = (var, v)
                    self.removeFromPool(var, v)
                    result = self.backtracking()
                    if result:
                        return True
                self.vars[tInd] = (var, 0)
                self.addToPool(var, v)
        self.varInd -= 1
        return False
        
        
    def getNextVar(self):
        for i in range(9):
            for j in range(9):
                if self.board.get(i, j) == 0:
                    return(i, j)
                
    def getB(self, i, j):
        if i < 3:
            if j < 3:
                b = 18
            elif j < 6:
                b = 19
            else:
                b = 20
        elif i < 6:
            if j < 3:
                b = 21
            elif j < 6:
                b = 22
            else:
                b = 23
        else:
            if j < 3:
                b = 24
            elif j < 6:
                b = 25
            else:
                b = 26
        return b
                
    def inValPool(self, var, v):
        for i in range(9):
            if (((i, var[1]), v) in self.vars):
                return False
            if (((var[0], i), v) in self.vars):
                return False
        if var[0] < 3:
            for i in range(3):
                if var[1] < 3:
                    for j in range(3):
                        if (((i, j), v) in self.vars):
                            return False
                elif var[1] < 6:
                    for j in range(3, 6):
                        if (((i, j), v) in self.vars):
                            return False
                else:
                    for j in range(6, 9):
                        if (((i, j), v) in self.vars):
                            return False
        elif var[0] < 6:
            for i in range(3, 6):
                if var[1] < 3:
                    for j in range(3):
                        if (((i, j), v) in self.vars):
                            return False
                elif var[1] < 6:
                    for j in range(3, 6):
                        if (((i, j), v) in self.vars):
                            return False
                else:
                    for j in range(6, 9):
                        if (((i, j), v) in self.vars):
                            return False
        else:
            for i in range(6, 9):
                if var[1] < 3:
                    for j in range(3):
                        if (((i, j), v) in self.vars):
                            return False
                elif var[1] < 6:
                    for j in range(3, 6):
                        if (((i, j), v) in self.vars):
                            return False
                else:
                    for j in range(6, 9):
                        if (((i, j), v) in self.vars):
                            return False
                    
        rowHuh = (not (0 == self.valPools[var[0]][v-1]))
        colHuh = (not (0 == self.valPools[var[1] + 9][v-1]))
        b = self.getB(var[0], var[1])
        boxHuh = (not (0 == self.valPools[b][v-1]))
        return (rowHuh and colHuh and boxHuh)
        
        #return True
    
    def removeFromPool(self, var, v):
        self.valPools[var[0]][v-1] = 0
        self.valPools[var[1] + 9][v-1] = 0
        b = self.getB(var[0], var[1])
        self.valPools[b][v-1] = 0
        
    def addToPool(self, var, v):
        self.valPools[var[0]][v-1] = v
        self.valPools[var[1] + 9][v-1] = v
        b = self.getB(var[0], var[1])
        self.valPools[b][v-1] = v
        
    def assign(self):
        for m in range(len(self.vars)):
            self.board.put(self.vars[m][0][0], self.vars[m][0][1], self.vars[m][1])
        
        
        
        
        
        
        