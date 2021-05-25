# -*- coding: utf-8 -*-
"""
Created on Fri Feb 26 12:37:01 2021

CIS479 - Program 3 - Reinforcement Learning
@author: Nate Pierce UMID 94712233
"""

import copy
import random


matrix = [[-100,0,0,0,0,0,0],
             [-100,'#',0,0,'#',0,0],
             [-100,0,0,0,0,0,0],
             [-100,'#',0,0,'#',0,0],
             [-100,0,0,0,0,0,-100],
             [-100,0,0,0,0,0,100]]

"""
0 is open space
# is an obstacle. Consider the walls of the maze to be an obstacle
-100, 100 are terminal states
"""

# Constants
GAMMA = 0.9
EPSILON = 0.1
ROWS = 6
COLS = 7
SAMPLES = 50000 # number of trials, including aborted trials

# Initialize the learning frequency array as a 2D list where the elements are dictionaries with the element ij as the key
# and the the list [west, north, east, south] as the value. The matrix that is passed in to this function is directly modified.
def initializeN(matrix):
    arr = [0,0,0,0]
    for i in range(0, ROWS):
        for j in range(0, COLS):
            if matrix[i][j] != '#' and matrix[i][j] != -100 and matrix[i][j] != 100: # check for valid state
                matrix[i][j] = arr
              

def updateN(traj, N_Matrix):
    s = traj[0] # current state in trajectory
    a = traj[1] # current action in trajectory
    
    i = s[0] # extract ith row from state
    j = s[1] # extract jth col from state
    
    sum_list = []
    for k in range(0, len(a)):
        t = N_Matrix[i][j][k] + a[k]
        sum_list.append(t)
    
    N_Matrix[i][j] = sum_list
    return sum(sum_list)
    
# The n passed in is already calculated for the current trajectory state and action. Updates the Q_Matrix stored in memory
# (i.e. no need to return anything). The action associated with the current item in the trajectory is the based on the
# epsilon greedy (90% it's optimal, 10% it's random) for the all trajectory indices n > 2 (the first element in the
# trajectory is totally random - the location AND the action).
def updateQ(traj, Q_Matrix):
    s = traj[0] # extract state from trajectory 
    a = traj[1] # extract action from trajectory
    r = traj[2] # extract reward function term from trajectory
    i = s[0]
    j = s[1]
    
    # Determine the Q-Value for the given state and the associated action
    q = copy.deepcopy(Q_Matrix[i][j])
    ind = a.index(1)
    
    n = N_Matrix[i][j][ind]
    
    
    # Apply the formula
    q_prime = QPrime(s, a, Q_Matrix)
    q_tot = q[ind] + (1/n)*(r + GAMMA*q_prime - q[ind])
    q[ind] = q_tot
    Q_Matrix[i][j] = q

   
# Given a Q_Matrix and some state and action, find the maximum Q-Value of the adjacent state (i.e., the state we are moving
# in to). Returns the max value of that adjacent state.  
def QPrime(s, a, Q_Matrix):
    i = s[0]
    j = s[1]
    
    if j > 0:
        if a == [1,0,0,0] and Q_Matrix[i][j-1] != '#': 
            Q_Matrix[i][j] = Q_Matrix[i][j-1]
            j = j - 1
    if i > 0:
        if a == [0,1,0,0] and Q_Matrix[i-1][j] != '#': 
            Q_Matrix[i][j] = Q_Matrix[i-1][j]
            i = i - 1
    if j + 1 < COLS :
        if a == [0,0,1,0] and Q_Matrix[i][j+1] != '#': 
            Q_Matrix[i][j] = Q_Matrix[i][j+1]
            j = j + 1
    if i + 1 < ROWS :
        if a == [0,0,0,1] and Q_Matrix[i+1][j] != '#':  
            Q_Matrix[i][j] = Q_Matrix[i+1][j]
            i = i + 1
    
    q = Q_Matrix[i][j] # q is a state, [i,j]
    loc = [i,j]
    
    if stateIsTerminal(loc) == True:
        return q
    else: 
        Q_Prime  = max(q)
        return Q_Prime
    

def updatePolicy(Pi_Matrix, Q_Matrix, traj): 
    s = traj[0]
    i = s[0]
    j = s[1]
    
    q = Q_Matrix[i][j]
    q_max = max(q)
    ind = q.index(q_max)
    
    if ind == 0: 
        Pi_Matrix[i][j] = '<<<<<'
    if ind == 1: 
        Pi_Matrix[i][j] = '^^^^^'
    if ind == 2: 
        Pi_Matrix[i][j] = '>>>>>'
    if ind == 3: 
        Pi_Matrix[i][j] = 'vvvvv'

# Location is guaranteed to not be an obstacle or a terminal - because the location that is passed in here is generated
# in the rndLocation function which checks to see that a random position in the matrix is NOT an obstacle or a 
# terminal. 
def initializeTrajectory(loc, traj):
    a = selectRndDir(matrix, loc)
    
    # Generate the reward based on the action. Reward is the negative of the cost determined by windy condition
    x = a.index(1)
    
    if x == 0: r = -1 # action is move west
    if x == 1: r = -2 # action is move north
    if x == 2: r = -3 # action is move east
    if x == 3: r = -2 # action is move south
    update = [loc, a, r]
    traj.append(update)
    return traj

def selectRndDir(matrix, loc):    
    a = random.randrange(0, 4)

    if a == 0: action = [1,0,0,0] # west
    if a == 1: action  = [0,1,0,0] # north
    if a == 2: action = [0,0,1,0] # east
    if a == 3: action = [0,0,0,1] # south
    
    return action


# State is the current element in the matrix. 
def updateTrajectory(loc, traj, Q_Matrix):
    i = loc[0]
    j = loc[1]
    
    # generate the next action using epsilon greedy
    t = random.choices(['Optimal', 'Random'], weights=[0.9, 0.1])
    
    if t[0] == 'Random':
        a = selectRndDir(matrix, loc) # action is list in form [W, N, E, S]. Only nonzero element is the move element.
    if t[0] == 'Optimal': # choose the optimal action for a given state
        q = Q_Matrix[i][j]
        q_max = max(q)
        ind = q.index(q_max)
        a = [0,0,0,0]
        a[ind] = 1
        
    x = a.index(1)
    
    # Generate the reward based on the action. Reward is the negative of the cost determined by windy condition
    
    if x == 0: r = -1 # action is move west
    if x == 1: r = -2 # action is move north
    if x == 2: r = -3 # action is move east
    if x == 3: r = -2 # action is move south
    
    update = [loc, a, r]
    traj.append(update)
    
    return traj

# Given a state, determines if the state is terminal. If terminal, return true.
def stateIsTerminal(loc):
    i = loc[0]
    j = loc[1]
    
    if matrix[i][j] == -100 or matrix[i][j] == 100: 
        return True # action is terminal
    
    else: return False # action does not result in terminal state
    
# Generate random starting element in matrix
def rndLocation(matrix):
    g = False
    while g == False:
        i = random.randrange(0,ROWS)
        j = random.randrange(0,COLS)
        loc = [i,j] # location
        
        if matrix[i][j] != '#' and matrix[i][j] != -100 and matrix[i][j] != 100:
            g = True # a valid location was randomly selected, so break the loop
        
    return loc
                 
def printM(matrix):
    for i in range(0, ROWS):
        print('\n','-'*100)
        for j in range(0, COLS):
            k = matrix[i][j]
            if k == '#': k = '#####'
            print(k, end=" "*4)
    print('\n','-'*100)

# Given a movement command [west, north, east, south] and current location, move to that location and return the updated
# location.
def move(a, loc):
    x = a.index(1) # extract the move command
    i = loc[0]
    j = loc[1]
    t = []
    
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
                
if __name__ == '__main__':

    initializeN(matrix)
    N_Matrix = copy.deepcopy(matrix) # initialize learning freq matrix all elements are [0,0,0,0]
    Q_Matrix = copy.deepcopy(matrix)  # initialize Q-value matrix all elements are [0,0,0,0]
    Pi_Matrix = copy.deepcopy(matrix) # initialize optimal action matrix all elements are [0,0,0,0]
    loc = rndLocation(matrix)
    
    traj = []
    traj = initializeTrajectory(loc, traj) # generate first element in trajectory (consists of a state, action, and reward)
    
    sample_count = 0 
    q = 0 # counter used for trajectory indexing
    
    print('Performing...')
    
    while sample_count < SAMPLES:
        a = traj[q][1] # note that traj[q] is the current (state, action, reward), and traj[q][1] gives the action
        n = updateN(traj[q],  N_Matrix)
        updateQ(traj[q], Q_Matrix) 
        updatePolicy(Pi_Matrix, Q_Matrix, traj[q]) 
        
        
        TERMINAL = stateIsTerminal(loc) # boolean value - if True, the move function has placed us in a terminal state
        
        # terminal state reached - end the current trajectory and start a new one
        if TERMINAL == True:
            traj = []
            loc = rndLocation(matrix)
            initializeTrajectory(loc, traj) 
            q = 0
            sample_count += 1
            continue
        
        traj = updateTrajectory(loc, traj, Q_Matrix) # update the trajectory with (state, action, reward)
        loc = move(a, loc) # move to the element in the matrix determined by action a
        
        q += 1
        
        
        # avoid getting bogged down in a loop by terminating sample if it loops more than 100 times
        if q > 100:
            q = 0
            sample_count += 1
            traj = []
            loc = rndLocation(matrix)
            initializeTrajectory(loc, traj) # end the current trajectory and start a new one
            
    
    print("Learning Complete.")
    
    print('Learning Frequency Matrix')
    printM(N_Matrix)
    print('Q-Value Matrix')
    printM(Q_Matrix)
    print('Optimal Action Matrix')
    printM(Pi_Matrix)
        

