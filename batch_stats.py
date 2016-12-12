import os
import pickle
import numpy as np

filename = "soccerdata/_batch.csv"

rewards = []

if os.path.exists(filename):
    print "LOADING BATCH FILE FROM", filename
    with open(filename, "rb") as f:
        D = pickle.load(f)
        print "Len(D):", len(D)
        print D[0]
        for i, row in enumerate(D):
            rewards.append(row[3])
else:
    print "File doesn't exist"

rewards = np.array(rewards)
print "rewards.mean():", rewards.mean()
print "rewards.max():", rewards.max()
print "rewards.min():", rewards.min()
print "rewards.sum():", rewards.sum()
print "len(rewards):", len(rewards)
