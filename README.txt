README

Author: Brendan Kelly
Version: 1.0

Usage: python sudoku.py -a <agent number> -f <game file>
-An agent number is 0 for keyboard and 1 for CSP solver
-A game file is the file that stores the start of a game of sudoku of
    of the name 'file'.sudoku
The output is a print of the solved game.

1. The problem I attempted to solve is using constraint satisfaction
problem methods to solve a game of sudoku. The problem requires satisfying
binary constraints between every one of the 81 variables and:
	Every other variable in its row
	Every other variable in its column
	Every other variable in its box
The inputs are the type of agent (in my program either keyboard or csp 
solver) and the file storing the game.

2. The algorithm I use is backtracking with forward checking and arc 
consistency. These algorithms are appropriate because this way we can
iterate through the puzzle, and if we run into a variable with no
options left we can easily go back and try a different set of variable
assignments.

3. The algorithm should successfully solve problems when a solution
exists. We can see the algorithm in action as compared to solving by
hand by running the puzzle in both the csp agent and the keyboard agent.
