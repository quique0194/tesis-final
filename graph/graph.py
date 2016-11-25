import matplotlib.pyplot as plt
import numpy as np

files = ["dqn_ttt_4_error.csv"]
styles = ["b", "r", "g"]
for i, file in enumerate(files):
    data = np.loadtxt("graph/" + file, delimiter=",")
    plt.plot(data, styles[i], label=file.split(".")[0])
plt.legend(loc=2)
plt.show()
