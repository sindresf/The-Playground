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

line = lines[0]

plt.plot(line)
plt.show()

plt.hist(alco)
plt.show()

#scaler = MinMaxScaler(feature_range=(0,1))
#lines_scaled = scaler.fit_transform(lines.T)

##training splitt
#train_size = int(len(lines_scaled) * 0.67)
#test_size = int(len(lines_scaled)) - train_size
#train, test = lines_scaled[0:train_size,:].T, lines_scaled[train_size:,:].T


## convert an array of values into a dataset matrix
#def create_dataset(dataset, look_back=1):
#	dataX, dataY = [], []
#	for i in range(len(dataset) - look_back - 1):
#		a = dataset[i:(i + look_back), 0]
#		dataX.append(a)
#		dataY.append(dataset[i + look_back, 0])
#	return np.array(dataX), np.array(dataY)

#look_back = 4
#trainX, trainY = create_dataset(train,look_back)
#testX, testY = create_dataset(test,look_back)

##print(trainX[0])
##print(trainY[0])
##print()
##print(trainX[1])
##plt.plot(trainX)
##plt.show()

##unscaled
#utrain_size = int(len(lines) * 0.67)
#utest_size = int(len(lines)) - train_size
#utrain, utest = lines[0:utrain_size,:].T, lines[utrain_size:,:].T

#ulook_back = 6
#utrainX, utrainY = create_dataset(utrain,ulook_back)
#utestX, utestY = create_dataset(utest,ulook_back)

##print(utrainX[0])
##print(utrainY[0])
##print()
##print(utrainX[1])
##plt.plot(utrainX)
##plt.show()

## reshape input to be [samples, time steps, features]
#trainX = np.reshape(trainX, (trainX.shape[0], 1, trainX.shape[1]))
#testX = np.reshape(testX, (testX.shape[0], 1, testX.shape[1]))

## unscalded reshape input to be [samples, time steps, features]
#utrainX = np.reshape(utrainX, (utrainX.shape[0], 1, utrainX.shape[1]))
#utestX = np.reshape(utestX, (utestX.shape[0], 1, utestX.shape[1]))