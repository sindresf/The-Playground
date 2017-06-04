import matplotlib.pyplot as plt
import numpy as np
import time


#DEFINE STARTING VALUES
range_start = 60
range_end = 1720
step = 20
data_range = np.arange(range_start,range_end,step)
rand_seed = 21
np.random.seed(rand_seed)

csv_path = 'W:\Datasets\synth_scoring\lines.csv'
lines = np.loadtxt(csv_path)

fig = plt.figure()
ax = fig.add_subplot(111)
axes = plt.gca()
axes.set_xlim([0,range_end])
axes.set_ylim([0,600])

# some X and Y data
x = data_range
y = np.zeros(len(x))
y[0] = 350

li, = ax.plot(x, y)

# draw and show it
ax.relim() 
ax.autoscale_view(True,True,True)
fig.canvas.draw()
plt.show(block=False)

def inv_log_func(x):
    return ((1 * 350) / (np.log(1 * x)))

# loop to update the data
count = 1
while count < len(y):
    try:
        y[count] = inv_log_func(count)

        # set the new data
        li.set_ydata(y)

        fig.canvas.draw()

        time.sleep(0.1)
        count += 1
    except KeyboardInterrupt:
        break