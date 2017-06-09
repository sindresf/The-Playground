import numpy as np
import matplotlib.pyplot as plt
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
csv_path = 'W:\Datasets\synth_scoring\lines.csv'
lines = np.loadtxt(csv_path)
alcos = lines[:,0]
lines = lines[:,1:]

#output_file("alco_hist_plot.html")
#hist_plt = figure(width = 1400, height = 800)
#hist,edges = np.histogram(alcos,bins=60)
#print(hist)
#print()
#print(edges)
##yes = input('yes')
#hist_plt.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:],
#        fill_color="#036564", line_color="#033649")
#show(hist_plt)
def histedges_equalN(x, nbin):
    npt = len(x)
    return np.interp(np.linspace(0, npt, nbin + 1),
                     np.arange(npt),
                     np.sort(x))

n, bins, patches = plt.hist(alcos, histedges_equalN(alcos, 45))
#output_file("alco_equal_hist_plot.html")
#hist_plt = figure(width = 1400, height = 800)
#hist_plt.quad(top=n, bottom=0, left=bins[:-1], right=bins[1:],
#        fill_color="#036564", line_color="#033649")
#show(hist_plt)
def get_alco_bin(alco,bins):
    if(alco < bins[0]): return 1
    for i in range(1, len(bins)):
        if alco < bins[i]:
            return i
    return 1

def get_alcos_in_bin(bins,bin,alcos):
    bin_min = 0
    if(bin > 0):
        bin_min = bins[bin - 1]
    bin_max = bins[bin]
    alcs = []
    for i in range(len(alcos)):
        if(alcos[i] >= bin_min and alcos[i] < bin_max):
            alcs.append(i)
    return alcs

busdf = get_alcos_in_bin(bins,26,alcos)
print(busdf)
input()

def get_bin_alco_lines(alcos_i,lines):
    alc_lines = []
    for i in alcos_i:
        alc_lines.append(lines[i])
    return alc_lines

alc = 1.061623
bin = get_alco_bin(alc, bins)
bin_alcos = get_alcos_in_bin(bins,bin,alcos)
alco_lines = get_bin_alco_lines(bin_alcos,lines)

def get_bin_avgs(bin_lines):
    avg_line = np.zeros(len(bin_lines[0]))
    for line in bin_lines:
        avg_line += line
    for i in range(len(avg_line)):
        avg_line[i] /= len(bin_lines)
    for i in range(len(avg_line)):
        for line in bin_lines:
            avg_line[i] += ((abs(line[i] - avg_line[i])) * 0.075)
        
    return avg_line
score_line = get_bin_avgs(alco_lines)
def plot_alco_lines_in_bin(plot,lines,avg_line):
    for line in lines:
        color = 'gray'
        aplha = 0.15
        if np.random.rand() < 0.45:
            color = '#aaacaf'
        if np.random.rand() < 0.2:
            color = '#cacbcd'
            aplha = 0.3
        plot.line(data_range,line, alpha=aplha + np.random.normal(0,0.23), line_width=2, color=color)
    plot.line(data_range,avg_line, line_width = 3, color = 'red')
    
def plot_score(plot,x,y):
    plot.quad(top=y, bottom=0, left= x, right= x + 2,
        fill_color='blue', line_color="#33333d")
    plot.circle_x(x=x + 1,y=y,size=25,color='purple', fill_alpha=0.2, line_width=3)

def alco_based_plot(plot, alco):
    bin = get_alco_bin(alco, bins)
    bin_alcos = get_alcos_in_bin(bins,bin,alcos)
    alco_lines = get_bin_alco_lines(bin_alcos,lines)
    score_line = get_bin_avgs(alco_lines)
    plot_alco_lines_in_bin(hlaplot,alco_lines,score_line)

output_file("highlight_alco_plot.html")
hlaplot = figure(width = 1400, height = 800)
hlaplot.title.text = "highlightet alcohol lvl bin selection, alc: " + str(alc)
hlaplot.legend.location = "top_right"
hlaplot.grid.grid_line_alpha = 0
hlaplot.xaxis.axis_label = 'Seconds'
hlaplot.yaxis.axis_label = 'Score'
hlaplot.ygrid.band_fill_color = "olive"
hlaplot.ygrid.band_fill_alpha = 0.1

plot_alco_lines_in_bin(hlaplot,alco_lines,score_line)
time_taken = np.round((76 * 4 * 3) / step)
x = int(time_taken)
y = score_line[x]
print('YOUR TEAM SCORE: ' + str(y))
x = range_start + x * step
plot_score(hlaplot,x,y + 0.01)
show(hlaplot)


trios = []
output_file("all_lines_trio_plot.html")
plot = figure(width = 1400, height = 800)
for i in range(2,len(lines),3):
    trio = [lines[i - 2],lines[i - 1],lines[i]]
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
        color = 'gray'
        aplha = 0.05
        if np.random.rand() < 0.45:
            color = '#83858b'
        if np.random.rand() < 0.2:
            color = '#bbbdbf'
            aplha = 0.2
        plot.line(data_range,line, alpha=aplha + np.random.normal(0,0.13), line_width=4, color=color)
    plot.line(data_range,lines[hli], line_width = 3, color = 'red')
    show(plot)

#highlight = 214
#output_file("highlight_plot.html")
#hlplot = figure(width = 1400, height = 800)
#hlplot.title.text = "highlightet alcohol lvl " + str(highlight)
#hlplot.legend.location = "top_right"
#hlplot.grid.grid_line_alpha = 0
#hlplot.xaxis.axis_label = 'Seconds'
#hlplot.yaxis.axis_label = 'Score'
#hlplot.ygrid.band_fill_color = "olive"
#hlplot.ygrid.band_fill_alpha = 0.1