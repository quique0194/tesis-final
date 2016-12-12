#!/usr/bin/python

import sys
import matplotlib.pyplot as plt
import numpy as np


files = sys.argv[1:]
if len(files) > 3:
    print "Max 3 files allowed"
    sys.exit()
# files = ["soccerdata/_cumulative_reward.csv"]
# files = ["soccerdata/_avg_reward.csv"]
styles = ["b", "r", "g"]
for i, file in enumerate(files):
    data = np.loadtxt(file, delimiter=",")
    plt.plot(data, styles[i], label=file.split(".")[0])
plt.legend(loc=2)
plt.show()
