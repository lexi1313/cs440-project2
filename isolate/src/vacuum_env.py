"""
Vacuum Robot Lab Environment Setup.
Note: T and R are intentionally omitted.
"""

# The grid layout and setup rules are delegated to the environment-agent.
# The AIMA GridMDP parameters are delegated to the q-learning-agent.

# TODO: Sub-agents will implement the environment setup here.

# hyperparameters
living_reward = -0.04
discount_factor = 0.9
learning_rate = 0.1
epsilon = 0.1
