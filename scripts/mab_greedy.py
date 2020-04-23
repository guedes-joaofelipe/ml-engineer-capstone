import os 
import sys
import pandas as pd
source_path = "./../sources"
if source_path not in sys.path:
    sys.path.append(source_path)
import utils
from mab.greedy import EGreedy, Greedy, EGreedyDecay
import random
import numpy as np

# def get_reward(df_offers, item):    
#     return random.choice(df_offers[df_offers[item] == 1]["reward"].values)

def get_reward(df_clusters, item):    
    return random.choice(df_clusters[item].values)

if __name__ == "__main__":
    data_dir = "./../data"

    df_clusters_rewards = pd.read_csv(os.path.join(data_dir, "df_clusters_rewards.csv"), 
        sep=';')
    df_clusters_rewards.set_index("cluster", inplace=True)

    mab = EGreedy(epsilon=.3)
    # mab = Greedy()
    mab = EGreedyDecay(epsilon=.3, beta=.1)
    mab.set_rewards(df_clusters_rewards.loc[0])


    last_reward = 0
    T = 10000
    print ('Starting MAB Training for ' + str(mab))
    
    for i in range(1,T):        
        item = mab.pull_arm(last_reward) 
        last_reward = mab.get_reward(item) 
       

    print (mab.k_n)
    print ('K reward: ', mab.k_reward)
    print ('Mean reward: ', mab.mean_reward)
    print (np.array(mab.epsilon_hist))