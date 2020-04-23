import numpy as np
from .base import Base

'''
Inspired by:

https://www.datahubbs.com/multi_armed_bandits_reinforcement_learning_1/
'''

class EGreedy(Base):
    '''
    epsilon-greedy k-bandit problem
    
    Inputs
    =====================================================
    k: number of arms (int)
    eps: probability of random action 0 < eps < 1 (float)
    '''

    def __init__(self, epsilon=.1):
        # Step count
        self.n_pulls = 0
        # Total mean reward
        self.mean_reward = 0
        # Previous arm pulled
        self.last_arm = -1
        self.epsilon = epsilon
        self.rewards = None
        self.rewards_hist = list()
        
    def __str__(self):
        return "EGreedy"

    def set_rewards(self, rewards):
        # Number of arms
        self.k = rewards.shape[0]
        
        # Step count for each arm
        self.k_n = np.zeros(self.k)
        # Mean reward for each arm
        self.k_reward = np.zeros(self.k)
        # Clusters
        self.rewards = rewards
        self.rewards_safe = rewards.copy()
    
    def pull_arm(self,last_reward = None):
        # Generate random number
        p = np.random.rand()
        
        if self.epsilon == 0 and self.n_pulls == 0:
            arm = np.random.choice(self.k)
        elif p < self.epsilon:
            # Randomly select an action (cluster)            
            arm = np.random.choice(self.k)
        else:
            # Take greedy action
            arm = np.argmax(self.k_reward)

        # Update number of pulls from arm
        self.n_pulls += 1
        self.k_n[arm] += 1
    
        # Update total
        self.mean_reward += (last_reward - self.mean_reward) / self.n_pulls
        
        # Update results for a_k
        self.k_reward[arm]  += (last_reward - self.k_reward[arm]) / self.k_n[arm]
        
        rec = self.rewards.index[arm]
        
        return rec
            
    def get_reward(self, item):
        reward = self.rewards[item]
        self.rewards_hist.append(reward)
        return reward

    def reset(self):
        # Resets results while keeping settings
        self.n_pulls = 0
        self.k_n = np.zeros(self.k)
        self.mean_reward = 0
        self.k_reward = np.zeros(self.k)
        self.rewards = self.rewards_safe.copy()
        self.rewards_hist = list()


class Greedy(EGreedy):

    def __init__(self):
        super(Greedy, self).__init__(0)

    def __str__(self):
        return "Greedy"

class EGreedyDecay(EGreedy):
    
    def __init__(self, epsilon, beta):
        self.epsilon_threshold = epsilon
        super(EGreedyDecay, self).__init__(epsilon=epsilon)
        self.beta = beta
        self.epsilon_hist = list()

    def __str__(self):
        return "EGreedyDecay"

    def update_epsilon(self):
        update = 1/(1 + self.n_pulls*self.beta)
        self.epsilon = update if update >= self.epsilon_threshold else self.epsilon_threshold
        self.epsilon_hist.append(self.epsilon)

    def pull_arm(self,last_reward = None):
        # Generate random number
        p = np.random.rand()
        
        self.update_epsilon()

        if self.epsilon == 0 and self.n_pulls == 0:
            arm = np.random.choice(self.k)
        elif p < self.epsilon:
            # Randomly select an action (cluster)            
            arm = np.random.choice(self.k)
        else:
            # Take greedy action
            arm = np.argmax(self.k_reward)

        # Update number of pulls from arm
        self.n_pulls += 1
        self.k_n[arm] += 1
    
        # Update total
        self.mean_reward += (last_reward - self.mean_reward) / self.n_pulls
        
        # Update results for a_k
        self.k_reward[arm]  += (last_reward - self.k_reward[arm]) / self.k_n[arm]
        
        rec = self.rewards.index[arm]
        
        return rec    


    