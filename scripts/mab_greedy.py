import os 
import sys
import pandas as pd
source_path = "./../sources"
if source_path not in sys.path:
    sys.path.append(source_path)
import utils
from mab.greedy import EGreedy
import random

# def get_reward(df_offers, item):    
#     return random.choice(df_offers[df_offers[item] == 1]["reward"].values)

def get_reward(df_clusters, item):    
    return random.choice(df_clusters[item].values)

if __name__ == "__main__":
    data_dir = "./../data"

    df_offers = pd.read_csv(os.path.join(data_dir, "clusters.csv"), 
        sep=';')

    df_offers["reward"] = df_offers["offer_viewed"] + \
        df_offers["offer_completed"]*df_offers["offered_reward"] + \
        2*df_offers["future_purchase"]

    # df_clusters = df_offers.groupby(["cluster_7"]).sum()[["social", "web", "mobile"]]
    # df_clusters = df_clusters.reset_index(drop=False).rename({"cluster_7": "cluster"}, axis=1)#.set_index("cluster")

    channels = ["email", "mobile", "social", "web"]
    df_clusters = pd.DataFrame(columns=["cluster"] + channels)
    for cluster in df_offers["cluster_7"].unique():
        df_temp = df_offers[df_offers["cluster_7"] == cluster]
        row = [cluster]
        for channel in channels:
            row.append(df_temp[df_temp[channel] == 1]["reward"].mean())
        
        df_clusters.loc[df_clusters.shape[0]] = row
        

    mab = EGreedy(epsilon=.1)
    mab.set_clusters(df_clusters)

    print(mab.clusters)
    
    last_reward = 0
    T = 50
    print ('Starting MAB Training')
    for i in range(1,T):
        
        item = mab.pull_arm(last_reward)
        
        # user fake review
        last_reward = get_reward(df_clusters, item) 
        # print("last_reward: ", last_reward)
        print("Item Recommended: {}\tReward: {:.02f}\tMean Reward: {}".format(item, last_reward, mab.mean_reward))

    print (mab.k_n)
    print ('K reward: ', mab.k_reward)
    print ('Mean reward: ', mab.mean_reward)