import matplotlib.pyplot as plt
import numpy as np

files = ["soccerdata/_error.csv"]
# files = ["soccerdata/_cumulative_reward.csv"]
# files = ["soccerdata/_avg_reward.csv"]
styles = ["b", "r", "g"]
for i, file in enumerate(files):
    data = np.loadtxt(file, delimiter=",")
    plt.plot(data, styles[i], label=file.split(".")[0])
plt.legend(loc=2)
plt.show()
