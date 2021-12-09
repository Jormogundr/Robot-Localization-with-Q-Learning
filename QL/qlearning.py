import copy
import random
import matrix.matrix_utils as matrix_utils

# Initialize the learning frequency array as a 2D list where the elements are dictionaries with the element ij as the key
# and the the list [west, north, east, south] as the value. The matrix that is passed in to this function is directly modified.
def initializeN(matrix, ROWS, COLS):
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
def updateQ(traj, matrix, Q_Matrix, N_Matrix, GAMMA):
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
    q_prime = QPrime(s, a, Q_Matrix, matrix)
    q_tot = q[ind] + (1/n)*(r + GAMMA*q_prime - q[ind])
    q[ind] = q_tot
    Q_Matrix[i][j] = q

# Given a Q_Matrix and some state and action, find the maximum Q-Value of the adjacent state (i.e., the state we are moving
# in to). Returns the max value of that adjacent state.  
def QPrime(s, a, Q_Matrix, matrix):
    i = s[0]
    j = s[1]
    COLS = len(Q_Matrix[0])
    ROWS = len(Q_Matrix)
    
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
    
    if stateIsTerminal(loc, matrix) == True:
        return q
    else: 
        Q_Prime  = max(q)
        return Q_Prime

# Given a state, determines if the state is terminal. If terminal, return true.
def stateIsTerminal(loc, matrix):
    i = loc[0]
    j = loc[1]
    
    if matrix[i][j] == -100 or matrix[i][j] == 100: 
        return True # action is terminal
    
    else: return False # action does not result in terminal state

# State is the current element in the matrix. 
def updateTrajectory(loc, traj, Q_Matrix, matrix):
    i = loc[0]
    j = loc[1]
    # generate the next action using epsilon greedy
    t = random.choices(['Optimal', 'Random'], weights=[0.9, 0.1])
    
    if t[0] == 'Random':
        a = matrix_utils.selectRndDir(matrix, loc) # action is list in form [W, N, E, S]. Only nonzero element is the move element.
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
def initializeTrajectory(loc, traj, matrix):
    a = matrix_utils.selectRndDir(matrix, loc)
    
    # Generate the reward based on the action. Reward is the negative of the cost determined by windy condition
    x = a.index(1)
    
    if x == 0: r = -1 # action is move west
    if x == 1: r = -2 # action is move north
    if x == 2: r = -3 # action is move east
    if x == 3: r = -2 # action is move south
    update = [loc, a, r]
    traj.append(update)
    return traj