import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
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

scaler = MinMaxScaler(feature_range=(0,1))
lines_scaled = scaler.fit_transform(lines.T)

#training splitt
train_size = int(len(lines_scaled) * 0.67)
test_size = int(len(lines_scaled)) - train_size
train, test = lines_scaled[0:train_size,:].T, lines_scaled[train_size:,:].T


# convert an array of values into a dataset matrix
def create_dataset(dataset, look_back=1):
	dataX, dataY = [], []
	for i in range(len(dataset) - look_back - 1):
		a = dataset[i:(i + look_back), 0]
		dataX.append(a)
		dataY.append(dataset[i + look_back, 0])
	return np.array(dataX), np.array(dataY)

look_back = 4
trainX, trainY = create_dataset(train,look_back)
testX, testY = create_dataset(test,look_back)

#print(trainX[0])
#print(trainY[0])
#print()
#print(trainX[1])
#plt.plot(trainX)
#plt.show()

#unscaled
utrain_size = int(len(lines) * 0.67)
utest_size = int(len(lines)) - utrain_size
utrain, utest = lines[0:utrain_size,:].T, lines[utrain_size:,:].T

ulook_back = 6
utrainX, utrainY = create_dataset(utrain,ulook_back)
utestX, utestY = create_dataset(utest,ulook_back)

#print(utrainX[0])
#print(utrainY[0])
#print()
#print(utrainX[1])
#plt.plot(utrainX)
#plt.show()

# reshape input to be [samples, time steps, features]
trainX = np.reshape(trainX, (trainX.shape[0], 1, trainX.shape[1]))
testX = np.reshape(testX, (testX.shape[0], 1, testX.shape[1]))

# unscalded reshape input to be [samples, time steps, features]
utrainX = np.reshape(utrainX, (utrainX.shape[0], 1, utrainX.shape[1]))
utestX = np.reshape(utestX, (utestX.shape[0], 1, utestX.shape[1]))

# create and fit the LSTM network
model = Sequential()
model.add(LSTM(10, input_shape=(1, look_back)))
model.add(Dense(1))
model.compile(loss='mean_squared_error', optimizer='adam')
model.fit(trainX, trainY, epochs=20, batch_size=5, verbose=2)

# unscaled create and fit the LSTM network
umodel = Sequential()
umodel.add(LSTM(15, input_shape=(1, ulook_back)))
umodel.add(Dense(1))
umodel.compile(loss='mean_squared_error', optimizer='adam')
umodel.fit(utrainX, utrainY, epochs=10, batch_size=5, verbose=2)
print()
print()
print('scoring!')
print()
# make predictions
trainPredict = model.predict(trainX)
testPredict = model.predict(testX)
# calculate root mean squared error
trainScore = math.sqrt(mean_squared_error(trainY, trainPredict))
print('Train Score: %.2f RMSE' % (trainScore))
testScore = math.sqrt(mean_squared_error(testY, testPredict))
print('Test Score: %.2f RMSE' % (testScore))
print()
# make unscaled predictions
utrainPredict = umodel.predict(utrainX)
utestPredict = umodel.predict(utestX)
# calculate root mean squared error
utrainScore = math.sqrt(mean_squared_error(utrainY, utrainPredict))
print('Train Score: %.2f RMSE' % (utrainScore))
utestScore = math.sqrt(mean_squared_error(utestY, utestPredict))
print('Test Score: %.2f RMSE' % (utestScore))
print()
# shift train predictions for plotting
trainPredictPlot = np.empty_like(lines_scaled.T)
trainPredictPlot[:] = np.nan
trainPredictPlot[look_back:len(trainPredict) + look_back] = trainPredict
# shift test predictions for plotting
#testPredictPlot = np.empty_like(lines_scaled.T)
#testPredictPlot[:] = np.nan
#testPredictPlot[len(trainPredict) + (look_back * 2) + 1:len(lines_scaled.T) -
#1] = testPredict
# plot baseline and predictions
plt.plot(lines_scaled)
plt.plot(trainPredictPlot)
#plt.plot(testPredictPlot)
plt.show()
#print()
# shift unscaled train predictions for plotting
utrainPredictPlot = np.empty_like(lines.T)
utrainPredictPlot[:] = np.nan
utrainPredictPlot[ulook_back:len(utrainPredict) + ulook_back] = utrainPredict
## shift test predictions for plotting
#utestPredictPlot = np.empty_like(lines.T)
#utestPredictPlot[:, :] = np.nan
#utestPredictPlot[len(utrainPredict) + (ulook_back * 2) + 1:len(lines.T) - 1,
#:] = utestPredict
## plot baseline and predictions
#plt.plot(lines[0].T)
plt.plot(utrainPredictPlot.T)
#plt.plot(utestPredictPlot)
plt.show()