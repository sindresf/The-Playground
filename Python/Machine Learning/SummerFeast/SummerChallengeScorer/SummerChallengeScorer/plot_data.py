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
#output_file("all_lines_trio_plot.html")
#plot = figure(width = 1400, height = 800)
csv_path = 'W:\Datasets\synth_scoring\lines.csv'
lines = np.loadtxt(csv_path)
alcos = lines[:,0]
lines = lines[:,1:]

output_file("alco_hist_plot.html")
hist_plt = figure(width = 1400, height = 800)
hist,edges = np.histogram(alcos,bins=77)
hist_plt.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:],
        fill_color="#036564", line_color="#033649")
show(hist_plt)
#trios = []
#for i in range(2,len(lines),3):
#    trio = [lines[i - 2],lines[i - 1],lines[i]]
#    trios.append(trio)
#np.random.shuffle(trios)
#for trio in trios:
#    add_trio_to_plot(plot,trio)
    
#plot.title.text = "All lines extracted from csv file"
#plot.legend.location = "top_right"
#plot.grid.grid_line_alpha = 0
#plot.xaxis.axis_label = 'Seconds'
#plot.yaxis.axis_label = 'Score'
#plot.ygrid.band_fill_color = "olive"
#plot.ygrid.band_fill_alpha = 0.1
#show(plot)
def highlight_plot(plot, lines, hli=0):
    for line in lines:
        color = 'gray'
        aplha = 0.05
        if np.random.rand() < 0.45:
            color = '#83858b'
        if np.random.rand() < 0.2:
            color = '#bbbdbf'
            aplha = 0.2
        plot.line(data_range,line, alpha=aplha + np.random.normal(0,0.13), line_width=4, color=color)
    plot.line(data_range,lines[hli], line_width=3, color='red')
    show(plot)

highlight = 214
output_file("highlight_plot.html")
hlplot = figure(width = 1400, height = 800)
hlplot.title.text = "highlightet alcohol lvl " + str(highlight)
hlplot.legend.location = "top_right"
hlplot.grid.grid_line_alpha = 0
hlplot.xaxis.axis_label = 'Seconds'
hlplot.yaxis.axis_label = 'Score'
hlplot.ygrid.band_fill_color = "olive"
hlplot.ygrid.band_fill_alpha = 0.1
highlight_plot(hlplot,lines,highlight)