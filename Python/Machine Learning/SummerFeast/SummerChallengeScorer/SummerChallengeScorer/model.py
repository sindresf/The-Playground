#import data for train
#fit
#store model
import numpy as np
from keras.layers import LSTM

#DEFINE STARTING VALUES
range_start = 60
range_end = 1720
step = 8
data_range = np.arange(range_start,range_end,step)
rand_seed = 21
np.random.seed(rand_seed)

csv_path = 'W:\Datasets\synth_scoring\lines.csv'
lines = np.loadtxt(csv_path)