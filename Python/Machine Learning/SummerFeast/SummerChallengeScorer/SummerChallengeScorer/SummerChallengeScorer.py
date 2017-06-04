import numpy as np
from keras.layers import LSTM
from bokeh.plotting import figure, output_file, show

def base_func(x):
    return 200.0 / (np.log(0.05 * x))

base_plot_x = range(60,421,30)
base_plot_data = [base_func(x) for x in base_plot_x]

output_file("base_line.html")

print("plotting data")
p = figure(width=1200, height=400)
p.line(base_plot_x,base_plot_data, color='navy', legend='score')

p.title.text = "Base func scoring"
p.legend.location = "top_left"
p.grid.grid_line_alpha = 0
p.xaxis.axis_label = 'Seconds'
p.yaxis.axis_label = 'Score'
p.ygrid.band_fill_color = "olive"
p.ygrid.band_fill_alpha = 0.1
show(p)

print("plotting function")

#first time setup
#make ranges with a larger time step
#make stepwise sampling of expo-func
#fuck with it manually to create slight bump around "some timing"
#save in csv file for later runs

#Second time setup, or: how to train your LSTM
#train lstm on ranges and expo-func
#save lstm for direct questioning on other computers
#make automatic primer given alcohol level

#Third time setup
#have network trained
#prime it
#live plot second for second the output with bokeh
#have a pause or something to Mark the time actually taken through user input
# update is via while loop i think, so can interrupt there, or check for "marker input"
#keep the finalized plots for later revue by participants.