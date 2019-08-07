import csv
import settings as set
import matplotlib.pyplot as plt
import os

trial = 1
file = str(set.EXP_NAME) + '_' + str(set.FITNESS_FUNCTION)
parent_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
data = parent_path + "/data/" + file + "_trial_" + str(trial) + ".csv"
generations = []
best = []
average = []
min = []

with open(data, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        generations.append(row["Gen"])
        best.append(float(row["Max"]))
        average.append(float(row["Avg"]))
        min.append(float(row["Min"]))

plt.plot(generations, best, label="max")
plt.plot(generations, average, label="average")
plt.plot(generations, min, label="min")
axs = plt.gca()
axs.set_xticks(axs.get_xticks()[::7])
plt.legend()
plt.xlabel('Generations')
plt.ylabel('Fitness')

plt.savefig('../plot/plot_' + file + '_trial_' + str(trial) + '.png')
plt.show()
