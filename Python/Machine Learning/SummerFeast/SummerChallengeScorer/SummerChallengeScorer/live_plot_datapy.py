import numpy as np
import matplotlib.pyplot as plt
from bokeh.plotting import figure, output_file, show
from bokeh.plotting import ColumnDataSource
from bokeh.charts import Scatter
from bokeh.models import LabelSet
from pandas.core.frame import DataFrame

#DEFINE INNER FUNCTIONS
def histedges_equalN(x, nbin):
    npt = len(x)
    return np.interp(np.linspace(0, npt, nbin + 1),
                     np.arange(npt),
                     np.sort(x))

def get_alco_bin(alco):
    if(alco < bins[0]): return 1
    if(alco >= bins[-1]): return len(bins) - 1
    for i in range(1, len(bins)):
        if alco < bins[i]:
            return i
    return 1

def get_alcos_in_bin(bin):
    bin_min = 0
    if(bin > 0):
        bin_min = bins[bin - 1]
    bin_max = bins[bin]
    if(bin == len(bins) - 1):
        bin_max = 100
    alcs = []
    for i in range(len(alcos)):
        if(alcos[i] >= bin_min and alcos[i] < bin_max):
            alcs.append(i)
    return alcs

def get_bin_alco_lines(alcos_i):
    alc_lines = []
    for i in alcos_i:
        alc_lines.append(lines[i])
    return alc_lines

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
    plot.circle_x(x=x + 1,y=y,size=25,color='purple', fill_alpha=0.2, line_width=3, name=str(np.round(x,1)))
    plot.text(x + 23, y + 1.75, text=[str(np.round(y,1))],
           text_color="navy", text_align="center", text_font_size="18pt")

def plot_team_scores(teams,scores):
    output_file("team_scores.html")
    hist_plt = figure(width = 1200, height = 600)
    hist_plt.title.text = "Team Scores!"
    hist_plt.grid.grid_line_alpha = 0
    hist_plt.xaxis.axis_label = 'Team'
    hist_plt.yaxis.axis_label = 'Score'
    hist_plt.ygrid.band_fill_color = "olive"
    hist_plt.ygrid.band_fill_alpha = 0.1
    w = 20
    boxes_left = [w * 2 * x for x in range(len(scores))]
    boxes_right = [w * 2 * x for x in range(1,len(scores) + 1)]
    hist_plt.quad(top=scores, bottom=0, left=boxes_left, right=boxes_right,
            fill_color="#aaeeff", line_color="#5599ee")
    for i in range(len(teams)):
        hist_plt.text(boxes_left[i] + w,scores[i] + 3.2, text=[teams[i]],
               text_color="navy", text_align="center", text_font_size="14pt")
    show(hist_plt)

def alco_based_plot(plot, alco):
    bin = get_alco_bin(alco)
    bin_alcos = get_alcos_in_bin(bin)
    alco_lines = get_bin_alco_lines(bin_alcos)
    score_line = get_bin_avgs(alco_lines)
    plot_alco_lines_in_bin(plot,alco_lines,score_line)
    return score_line
    
def get_plot(teamNo, alco):
    output_file(plot_file_name + str(teamNo) + ".html")
    plot = figure(width = 1400, height = 800)
    plot.title.text = "scoring graph given alcohol: " + str(alco)
    plot.legend.location = "top_right"
    plot.grid.grid_line_alpha = 0
    plot.xaxis.axis_label = 'Time'
    plot.yaxis.axis_label = 'Score'
    plot.ygrid.band_fill_color = "olive"
    plot.ygrid.band_fill_alpha = 0.1
    return plot

def get_time_x(sec,team_count):
    scale = 7 - team_count
    time_taken = np.round((sec * scale) / step)
    x = min(int(time_taken), len(data_range) - 1)
    return x

def get_plot_x(x):
    x = min(range_start + x * step, range_end - step)
    return x

def get_score_line_point_from_time_x(score_line, time_x):
    y = score_line[time_x]
    return y

def still_going(command):
    return command[0] != "n"


#DEFINE STARTING VALUES
range_start = 60
range_end = 1200
step = 15
data_range = np.arange(range_start,range_end,step)

rand_seed = 21
np.random.seed(rand_seed)

csv_path = 'W:\Datasets\synth_scoring\lines.csv'
lines = np.loadtxt(csv_path)
alcos = lines[:,0]
lines = lines[:,1:]

n, bins, patches = plt.hist(alcos, histedges_equalN(alcos, 45))
plot_file_name = "scoring_and_final_score_team_"

team = ""


#PUT IT ALL TOGETHER
scores = []
teams = []
command = "letsgo!"
while still_going(command):
    team_name = input('team:')
    teams.append(team_name)
    team_alcos = input('alcos:')
    team_alcos = np.array(team_alcos.split('|'))
    team_alcos = team_alcos.astype(np.float)
    alco = np.mean(team_alcos)
    team_plot = get_plot(team_name,alco)
    score_line = alco_based_plot(team_plot,alco)
    show(team_plot)
    team_count = input('member count:')
    team_count = int(team_count)
    time = int(input('time:'))
    x = get_time_x(time, team_count)
    y = get_score_line_point_from_time_x(score_line, x)
    scores.append(y)
    x = get_plot_x(x)
    plot_score(team_plot,x,y)
    show(team_plot)
    command = input('moar?')

#ROUND IT UP AND DECLARE WINNER!
plot_team_scores(teams,scores)