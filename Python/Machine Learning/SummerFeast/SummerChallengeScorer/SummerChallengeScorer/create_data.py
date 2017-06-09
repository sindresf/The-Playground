import numpy as np

#DEFINE INNER FUNCTIONS
def inv_log_func(x, a, b):
    return ((a * starting_score) / (2 + np.log(b * x)))

def bump_func(x,e):
    return (e * np.sin(x - np.pi / 2)) + e

def sin_vals(ampl,steps):
    if (steps < 1): steps = 1
    sin_step = (np.pi * 2.0) / steps
    x_range = np.arange(0,np.pi * 2.0 + 0.1,sin_step)
    sin_vals = [bump_func(x,ampl) for x in x_range]
    return sin_vals

def make_line_trio_data(ami,a,ama,bmi,b,bma):
    min_data = [int(inv_log_func(x,ami,bmi)) if x <= 360 else int(inv_log_func(x,ami,bmi) + 0.003 * x) for x in data_range]
    mid_data = [int(inv_log_func(x,a,b)) if x < 120 else int(inv_log_func(x,a,b) - 0.017 * x) for x in data_range]
    max_data = [int(inv_log_func(x,ama,bma) - 0.029 * x) for x in data_range]
    return min_data,mid_data,max_data

def add_bump_func(vals,ampl,frm,to):
    bump_vals = sin_vals(ampl,to - frm)
    sini = 0
    for i in range(frm,to):
        sini += 1
        vals[i] += bump_vals[sini] * 0.5
        vals[i] = int(vals[i])

def add_bump_trio(ampl,xmi,x,xma,frm,to):
    add_bump_func(xmi,ampl,frm,to)
    add_bump_func(x,ampl,frm,to)
    add_bump_func(xma,ampl,frm,to)

def make_trio(a,b,c,d,ampl):
    mini,mid,maxi = make_line_trio_data(a[0],a[1],a[2],b[0],b[1],b[2])
    bump_start = int(len(mid) * c)
    bump_end = len(mid) - d
    add_bump_trio(ampl,mini,mid,maxi,bump_start,bump_end)
    return [a[0]] + mini,[a[1]] + mid,[a[2]] + maxi

def get_az():
    ami = np.random.uniform(low=0.39, high=0.7)
    amd = np.random.uniform(low=0.71, high=0.98)
    ama = np.random.uniform(low=0.985, high=1.205)
    return [ami,amd,ama]

def get_bz():
    bmi = b * np.random.uniform(low=0.9, high=0.95)
    bmd = b * np.random.uniform(low=0.96, high=1.1)
    bma = b * np.random.uniform(low=1.15, high=1.67)
    return [bmi,bmd,bma]

def make_trios(count):
    all_lines = []
    az = [a_min,a,a_max]
    bz = [b_min,b,b_max]
    c = 0.62
    d = 6
    e = 10
    for i in range(count):
        all_lines.extend(make_trio(az,bz,c,d,e))
        az = get_az()
        bz = get_bz()
        c = np.random.uniform(low=0.21, high=0.9)
        d = int(np.random.uniform(low=1, high=30))
        e = int(np.random.uniform(low=5, high=13))
    return all_lines

#DEFINE STARTING VALUES
starting_score = 342.5

a = 1.0
b = 0.025

a_max = 1.2
b_max = b * 1.15

a_min = 0.8
b_min = b * 0.85

e = 10
line_count = 150

range_start = 60
range_end = 1200
step = 15
data_range = np.arange(range_start,range_end,step)

rand_seed = 21
np.random.seed(rand_seed)

csv_path = 'W:\Datasets\synth_scoring\lines.csv'

#PUT IT ALL TOGETHER
all_lines = make_trios(line_count)

for line in all_lines:
    line = np.asarray(line)

all_lines = np.asarray(all_lines)
np.savetxt(csv_path,all_lines)