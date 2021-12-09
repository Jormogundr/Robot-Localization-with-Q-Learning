# Robot-Localization-with-Q-Learning
In this project, we aim to implement one of Reinforcement Learning algorithms: the Q-Learning algorithm.

Goal & Environment: The primary goal of this project is to implement the Q-learning reinforcement learning algorithm. The agent starts in some non-terminal, non-obstacle state within a 6 x 7 grid. Terminal states are defined by the -100, +100 blocks on the grid, and the black-filled blocks are obstacles, which the agent may not pass through. The agent may move west, north, east or south at any state s. These movements constitute the available agent actions a. Once reached, the agent cannot escape a terminal state.


Additionally, we consider that the maze is windy - that is, each action has an associated cost determined by the wind direction. The wind comes from the east. If the agent moves against the wind, it has an associated cost of 3. If the agent moves with the wind, the cost is 1, and if the agent moves perpendicular to the wind direction, the cost is 2. Once the agent has selected an action a, it may drift to the left or right each with probability 0.1. This simulates actuator error for a real-life agent. Note that if the agent moves into an obstacle or the outer wall of the maze, it simply gets bumped back and returned to its prior state.
