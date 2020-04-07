import numpy as np
from base import Base

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
        
    def set_clusters(self, clusters):
        # Number of arms
        self.k = clusters.shape[0]
        
        # Step count for each arm
        self.k_n = np.zeros(self.k)
        # Mean reward for each arm
        self.k_reward = np.zeros(self.k)
        # Clusters
        self.clusters = clusters
        self.clusters_safe = clusters.copy()
            
    def pull_arm(self,last_reward = None):
        # Generate random number
        p = np.random.rand()
        if self.epsilon == 0 and self.n_pulls == 0:
            arm = np.random.choice(self.k)
        elif p < self.epsilon:
            # Randomly select an action
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
            
        temp = self.clusters.iloc[arm]
        temp = np.array(temp.drop('cluster'))
        rec_idx = np.argmax(temp) + 1 # +1 because the first column is for cluster name
        #movieIds = self.clusters.columns
        #rec = movieIds[rec_idx]
        rec = self.clusters.columns[rec_idx]
        #rec = self.clusters.iloc[p, rec_idx]
        #self.clusters.iloc[:, rec_idx] = 0
        
        return rec
            
    def reset(self):
        # Resets results while keeping settings
        self.n_pulls = 0
        self.k_n = np.zeros(self.k)
        self.mean_reward = 0
        self.k_reward = np.zeros(self.k)
        self.clusters = self.clusters_safe.copy()
