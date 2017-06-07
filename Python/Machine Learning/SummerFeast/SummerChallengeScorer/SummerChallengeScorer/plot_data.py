import numpy as np
from bokeh.plotting import figure, output_file, show

#DEFINE INNER FUNCTIONS
def plot_sin(steps):
    sin = sin_vals(steps)

    output_file("sine_line.html")
    sp = figure(width=1800, height=800)
    sin_step = (np.pi * 2.0) / steps
    x_range = np.arange(0,np.pi * 2.0 + 0.1,sin_step)
    sp.line(x_range,sin,legend='sin_bump', alpha=0.7, line_width=4, color='green')
    show(sp)

    
def add_trio_to_plot(plot, trio):
    plot.line(data_range,trio[0], alpha=0.4 + np.random.normal(0,0.35), line_width=int(np.random.uniform(low=2.4, high=5.1)), color='green')
    plot.line(data_range,trio[1], alpha=0.4 + np.random.normal(0,0.35), line_width=int(np.random.uniform(low=2.4, high=5.1)), color = 'navy')
    plot.line(data_range,trio[2], alpha=0.4 + np.random.normal(0,0.35), line_width=int(np.random.uniform(low=2.4, high=5.1)), color='red')

#DEFINE STARTING VALUES
range_start = 60
range_end = 1200
step = 15
data_range = np.arange(range_start,range_end,step)
rand_seed = 21
np.random.seed(rand_seed)

#PUT IT ALL TOGETHE
output_file("base_line_bCoef.html")
plot = figure(width = 1400, height = 800)

csv_path = 'W:\Datasets\synth_scoring\lines.csv'
lines = np.loadtxt(csv_path)
trios = []
for i in range(2,len(lines),3):
    trio = [lines[i - 2][1:],lines[i - 1][1:],lines[i][1:]]
    trios.append(trio)
np.random.shuffle(trios)
for trio in trios:
    add_trio_to_plot(plot,trio)
    
plot.title.text = "All lines extracted from csv file"
plot.legend.location = "top_right"
plot.grid.grid_line_alpha = 0
plot.xaxis.axis_label = 'Seconds'
plot.yaxis.axis_label = 'Score'
plot.ygrid.band_fill_color = "olive"
plot.ygrid.band_fill_alpha = 0.1
show(plot)

def highlight_plot(plot, lines, hli=0):
    for line in lines:
        plot.line(data_range,line[1:], alpha=0.05 + np.random.normal(0,0.18), line_width=2, color='gray')
    plot.line(data_range,lines[hli][1:], line_width=3, color='red')
    show(plot)
    
output_file("highlight_plot.html")
hlplot = figure(width = 1400, height = 800)
hlplot.legend.location = "top_right"
hlplot.grid.grid_line_alpha = 0
hlplot.xaxis.axis_label = 'Seconds'
hlplot.yaxis.axis_label = 'Score'
hlplot.ygrid.band_fill_color = "olive"
hlplot.ygrid.band_fill_alpha = 0.1
highlight_plot(hlplot,lines,np.random.randint(0,len(lines)))