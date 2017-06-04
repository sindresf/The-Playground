import numpy as np
from bokeh.plotting import figure, output_file, show

#DEFINE INNER FUNCTIONS
def inv_log_func(x, a, b):
    return (a / (np.log(b * x)))

def bump_func(x,e):
    return (e * np.sin(x - np.pi / 2)) + e

def plot_sin(steps):
    sin = sin_vals(steps)

    output_file("sine_line.html")
    sp = figure(width=800, height=800)
    sin_step = (np.pi * 2.0) / steps
    x_range = np.arange(0,np.pi * 2.0 + 0.1,sin_step)
    sp.line(x_range,sin,legend='sin_bump', alpha=0.7, line_width=4, color='green')
    show(sp)

def sin_vals(ampl,steps):
    sin_step = (np.pi * 2.0) / steps
    x_range = np.arange(0,np.pi * 2.0 + 0.1,sin_step)
    sin_vals = [bump_func(x,ampl) for x in x_range]
    return sin_vals

def make_line_trio_data(ami,a,ama,bmi,b,bma):
    min_data = [inv_log_func(x,ami,bmi) for x in plot_range]
    mid_data = [inv_log_func(x,a,b) for x in plot_range]
    max_data = [inv_log_func(x,ama,bma) for x in plot_range]
    return min_data,mid_data,max_data

def add_bump_func(vals,ampl,frm,to):
    bump_vals = sin_vals(ampl,to - frm)
    sini = 0
    for i in range(frm,to):
        sini += 1
        vals[i] += bump_vals[sini] * 0.5

def add_bump_trio(ampl,xmi,x,xma,frm,to):
    add_bump_func(xmi,ampl,frm,to)
    add_bump_func(x,ampl,frm,to)
    add_bump_func(xma,ampl,frm,to)

def add_trio_to_plot(plot, ymi,y,yma):
    pb.line(plot_range,ymi, alpha=0.6 + np.random.normal(0,0.2), line_width=4, color='green')
    pb.line(plot_range,y, alpha = 0.6 + np.random.normal(0,0.2), line_width = 4, color = 'navy')
    pb.line(plot_range,yma, alpha=0.6 + np.random.normal(0,0.2), line_width=4, color='red')

def make_trio(a,b,c,d,ampl,plot):
    mini,mid,maxi = make_line_trio_data(a[0],a[1],a[2],b[0],b[1],b[2])
    bump_start = int(len(mid) * c)
    bump_end = len(mid) - d
    add_bump_trio(ampl,mini,mid,maxi,bump_start,bump_end)
    add_trio_to_plot(plot,mini,mid,maxi)

def make_trios(count,plot):
    az = [a_min,a,a_max]
    bz = [b_min,b,b_max]
    c = 0.62
    d = 6
    e = 10
    for i in range(count):
        make_trio(az,bz,c,d,e,pb)
        ami = a * np.random.uniform(low=0.6, high=0.9)
        amd = a * np.random.uniform(low=0.9, high=1.1)
        ama = a * np.random.uniform(low=1.1, high=1.4)
        az = [ami,amd,ama]
        bmi = b * np.random.uniform(low=0.8, high=0.95)
        bmd = b * np.random.uniform(low=0.95, high=1.05)
        bma = b * np.random.uniform(low=1.75, high=1.225)
        bz = [bmi,bmd,bma]
        c = np.random.uniform(low=0.23, high=0.85)
        d = int(np.random.uniform(low=2, high=28))
        e = int(np.random.uniform(low=7, high=14))



#DEFINE STARTING VALUES
a = 350.0
b = 0.05

a_max = a * 1.2
b_max = b * 1.15

a_min = a * 0.8
b_min = b * 0.85

e = 10
line_count = 20

plot_start = 60
plot_end = 720
step = 8
plot_range = np.arange(plot_start,plot_end,step)

rand_seed = 21
np.random.seed(rand_seed)

#PUT IT ALL TOGETHE
output_file("base_line_bCoef.html")
pb = figure(width = 1200, height = 600)
#mini,mid,max  = make_line_trio_data(a_min,a,a_max,b_min,b,b_max)
#add_bump_trio(mini,mid,max,bump_start,bump_end)
#add_trio_to_plot(pb,mini,mid,max)

make_trios(line_count,pb)

pb.title.text = "Min Max scale on B"
pb.legend.location = "top_left"
pb.grid.grid_line_alpha = 0
pb.xaxis.axis_label = 'Seconds'
pb.yaxis.axis_label = 'Score'
pb.ygrid.band_fill_color = "olive"
pb.ygrid.band_fill_alpha = 0.1
show(pb)