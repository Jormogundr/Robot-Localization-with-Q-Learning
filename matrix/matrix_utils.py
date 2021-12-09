import random

def printM(matrix):
    COLS = len(matrix[0])
    ROWS = len(matrix)
    for i in range(0, ROWS):
        print('\n','-'*100)
        for j in range(0, COLS):
            k = matrix[i][j]
            if k == '#': k = '#####'
            print(k, end=" "*4)
    print('\n','-'*100)

# Given a movement command [west, north, east, south] and current location, move to that location and return the updated
# location.
def move(a, loc, matrix):
    x = a.index(1) # extract the move command
    i = loc[0]
    j = loc[1]
    t = []
    COLS = len(matrix[0])
    ROWS = len(matrix)

    # movement command is west
    if x == 0:
        t = random.choices(['West', 'North', 'East', 'South'], weights=(0.8, 0.1, 0.0, 0.1))
        
    # movement command is north
    if x == 1:
        t = random.choices(['West', 'North', 'East', 'South'], weights=(0.1, 0.8, 0.1, 0.0))
        
    # movement command is east
    if x == 2:
        t = random.choices(['West', 'North', 'East', 'South'], weights=(0.0, 0.1, 0.8, 0.1))
    
    # movement command is south
    if x == 3:
        t = random.choices(['West', 'North', 'East', 'South'], weights=(0.1, 0.0, 0.1, 0.8))
            
    # evaluate the selected drift probability
    if j > 0:
        if t[0] == 'West' and matrix[i][j-1] != '#':
            j = j - 1
    if i > 0:
        if t[0] == 'North' and matrix[i-1][j] != '#':
            i = i - 1
    if j < COLS - 1:
        if t[0] == 'East' and matrix[i][j+1] != '#':
            j = j + 1
    if i < ROWS - 1:
        if t[0] == 'South' and matrix[i+1][j] != '#':
            i = i + 1
    
    # Assign the new location based on drift probability
    loc = [i, j] 
    return loc     

# Generate random starting element in matrix
def rndLocation(matrix):
    g = False
    COLS = len(matrix[0])
    ROWS = len(matrix)

    while g == False:
        i = random.randrange(0,ROWS)
        j = random.randrange(0,COLS)
        loc = [i,j] # location
        
        if matrix[i][j] != '#' and matrix[i][j] != -100 and matrix[i][j] != 100:
            g = True # a valid location was randomly selected, so break the loop
        
    return loc

def selectRndDir(matrix, loc):    
    a = random.randrange(0, 4)

    if a == 0: action = [1,0,0,0] # west
    if a == 1: action  = [0,1,0,0] # north
    if a == 2: action = [0,0,1,0] # east
    if a == 3: action = [0,0,0,1] # south
    
    return action