# Define the matrix here. 

"""
0 is open space
# is an obstacle. Consider the walls of the maze to be an obstacle
-100, 100 are terminal states
"""

def createMatrix():
    matrix = [[-100,0,0,0,0,0,0],
             [-100,'#',0,0,'#',0,0],
             [-100,0,0,0,0,0,0],
             [-100,'#',0,0,'#',0,0],
             [-100,0,0,0,0,0,-100],
             [-100,0,0,0,0,0,100]]
    cols = len(matrix[0])
    rows = len(matrix)

    return matrix, rows, cols