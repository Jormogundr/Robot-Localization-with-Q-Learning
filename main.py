import copy
import random
from matrix.matrix import createMatrix
import QL.qlearning as ql
import matrix.matrix_utils as matrix_utils

# Create the matrix!
matrix, ROWS, COLS = createMatrix()

# Constants
GAMMA = 0.9
EPSILON = 0.1
SAMPLES = 50000 # number of trials, including aborted trials

def main():
    ql.initializeN(matrix, ROWS, COLS)
    N_Matrix = copy.deepcopy(matrix) # initialize learning freq matrix all elements are [0,0,0,0]
    Q_Matrix = copy.deepcopy(matrix)  # initialize Q-value matrix all elements are [0,0,0,0]
    Pi_Matrix = copy.deepcopy(matrix) # initialize optimal action matrix all elements are [0,0,0,0]
    loc = matrix_utils.rndLocation(matrix)
    traj = []
    traj = ql.initializeTrajectory(loc, traj, matrix) # generate first element in trajectory (consists of a state, action, and reward)
    sample_count = 0 
    q = 0 # counter used for trajectory indexing
    
    print('Finding Optimal Policy...')
    
    while sample_count < SAMPLES:
        a = traj[q][1] # note that traj[q] is the current (state, action, reward), and traj[q][1] gives the action
        n = ql.updateN(traj[q],  N_Matrix)
        ql.updateQ(traj[q], matrix, Q_Matrix, N_Matrix, GAMMA) 
        ql.updatePolicy(Pi_Matrix, Q_Matrix, traj[q]) 
        
        
        TERMINAL = ql.stateIsTerminal(loc, matrix) # boolean value - if True, the move function has placed us in a terminal state
        
        # terminal state reached - end the current trajectory and start a new one
        if TERMINAL == True:
            traj = []
            loc = matrix_utils.rndLocation(matrix)
            ql.initializeTrajectory(loc, traj, matrix) 
            q = 0
            sample_count += 1
            continue
        
        traj = ql.updateTrajectory(loc, traj, Q_Matrix, matrix) # update the trajectory with (state, action, reward)
        loc = matrix_utils.move(a, loc, matrix) # move to the element in the matrix determined by action a
        q += 1
        
        # avoid getting bogged down in a loop by terminating sample if it loops more than 100 times
        if q > 100:
            q = 0
            sample_count += 1
            traj = []
            loc = matrix_utils.rndLocation(matrix)
            ql.initializeTrajectory(loc, traj, matrix) # end the current trajectory and start a new one
            
    print("Learning Complete.")
    
    # Print the matrices.
    # TODO: Output to a file, tidy the print out.
    print('Learning Frequency Matrix')
    matrix_utils.printM(N_Matrix)
    print('Q-Value Matrix')
    matrix_utils.printM(Q_Matrix)
    print('Optimal Action Matrix')
    matrix_utils.printM(Pi_Matrix)

if __name__ == '__main__':
    main()
        

