import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error

#DEFINE STARTING VALUES
range_start = 60
range_end = 1720
step = 24
data_range = np.arange(range_start,range_end,step)
rand_seed = 21
np.random.seed(rand_seed)

csv_path = 'W:\Datasets\synth_scoring\lines.csv'
lines = np.loadtxt(csv_path)
alco = np.asarray([line[0] for line in lines])
lines = np.asarray([line[1:] for line in lines])

def get_line_split(line,alco=1.0, look_back=1):
    line_look_back, line_pred = [],[]
    for i in range(1,len(line) - look_back - 2):
        xb = np.array(line[i:(i + look_back + 1)])
        xa = [np.array([v], dtype='float32') for v in xb]
        yb = line[i + look_back]
        for x in range(i, i + look_back + 1):
            if(x == 1):
                xa[x - i] = np.array([line[0], step, alco], dtype='float32')
            else:
                xa[x - i] = np.array([xb[x - i - 1],x * step, alco], dtype='float32')
        line_look_back.append(np.array(xa))
        line_pred.append(yb)
    return np.array(line_look_back), np.array(line_pred)

def create_lines_splits(lines, alcos, look_back=1):
    lines_look_back, lines_pred = [],[]
    alco_count = 0
    for line in lines:
        lb,pred = get_line_split(line,alcos[alco_count],look_back)
        lines_look_back.append(lb)
        lines_pred.append(pred)
        alco_count += 1
    return np.array(lines_look_back), np.array(lines_pred)

lines_look_back, lines_pred = create_lines_splits(lines,alco,look_back=4)

def create_train_test_split(look_backs, preds, train_size=0.67):
    train_LB, train_pred, test_LB, test_pred = [],[],[],[]
    split_index = int(len(look_backs) * train_size)
    train_LB = look_backs[:split_index]
    train_pred = preds[:split_index]
    test_LB = look_backs[split_index:]
    test_pred = preds[split_index:]
    return np.array(train_LB),np.array(train_pred),np.array(test_LB), np.array(test_pred)

train_LB, train_pred, test_LB, test_pred = create_train_test_split(lines_look_back,lines_pred)

def scale_data_down(scaler,): #not done for now
    return 1

## reshape input to be [samples, time steps, features]
#trainX = np.reshape(trainX, (trainX.shape[0], 1, trainX.shape[1]))
#testX = np.reshape(testX, (testX.shape[0], 1, testX.shape[1]))

## unscalded reshape input to be [samples, time steps, features]
#utrainX = np.reshape(utrainX, (utrainX.shape[0], 1, utrainX.shape[1]))
#utestX = np.reshape(utestX, (utestX.shape[0], 1, utestX.shape[1]))