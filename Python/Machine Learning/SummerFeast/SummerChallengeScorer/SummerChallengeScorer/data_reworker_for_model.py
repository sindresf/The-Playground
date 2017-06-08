import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math
from keras.models import Sequential
from keras.models import load_model
from keras.layers import *
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error

#DEFINE STARTING VALUES
range_start = 60
range_end = 1200
step = 15
data_range = np.arange(range_start,range_end,step)
rand_seed = 21
np.random.seed(rand_seed)
look_back = 5

csv_path = 'W:\Datasets\synth_scoring\lines.csv'
lines = np.loadtxt(csv_path)
alco = np.array([line[0] for line in lines])
lines = np.asarray([np.array(line[1:], dtype='float32') for line in lines])

val_scaler = MinMaxScaler(feature_range=(0.0,1.0))
time_scaler = MinMaxScaler(feature_range=(0.0,1.0))
all_vals = np.array([],dtype='float32')
for line in lines:
    all_vals = np.append(all_vals,line)
all_vals_scaled = val_scaler.fit_transform(all_vals.reshape(-1, 1))
data_range_scaled = time_scaler.fit_transform(data_range.reshape(-1, 1))

line_index_jump = 0
for i in range(0,len(lines)):
    for j in range(0,len(lines[i])):
        lines[i,j] = all_vals_scaled[j + line_index_jump]
    line_index_jump += len(lines[i])


def get_line_split(line,alco=1.0, look_back=1):
    line_look_back, line_pred = [],[]
    for i in range(1,len(line) - look_back - 2):
        xb = np.array(line[i:(i + look_back + 1)])
        xa = [np.array([v], dtype='float32') for v in xb]
        yb = line[i + look_back]
        for x in range(i, i + look_back + 1):
            if(x == 1):
                xa[x - i] = np.array([line[0], data_range_scaled[1], alco], dtype='float32')
            else:
                xa[x - i] = np.array([xb[x - i - 1],data_range_scaled[x], alco], dtype='float32')
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

lines_look_back, lines_pred = create_lines_splits(lines,alco,look_back)

def create_train_test_split(look_backs, preds, train_size=0.67):
    train_LB, train_pred, test_LB, test_pred = [],[],[],[]
    split_index = int(len(look_backs) * train_size)
    train_LB = look_backs[:split_index]
    train_pred = preds[:split_index]
    test_LB = look_backs[split_index:]
    test_pred = preds[split_index:]
    return np.array(train_LB),np.array(train_pred),np.array(test_LB), np.array(test_pred)

train_LB, train_pred, test_LB, test_pred = create_train_test_split(lines_look_back,lines_pred)

def get_LSTM_line_structure(line):
    return np.reshape(line, (line.shape[0], line.shape[2], line.shape[1]))

def get_all_LSTM_line_structures(lines):
    lines_reshaped = []
    for line in lines:
        ln = get_LSTM_line_structure(line)
        lines_reshaped.append(ln)
    return np.array(lines_reshaped)

train_LB_X = get_all_LSTM_line_structures(train_LB)
test_LB_X = get_all_LSTM_line_structures(test_LB)

def train_on_one_line(model, line, line_pred, epochs):
    model.fit(line, line_pred, epochs = epochs, batch_size =batch_size, verbose = 2)

def train_on_some_lines(model, lines, lines_preds, line_numbers=[], epochs=[]):
    epoch_index = 0
    for index in line_numbers:
        print('training on line no ' + str(index))
        train_on_one_line(model, lines[index], lines_preds[index], epochs[epoch_index])
        epoch_index = (epoch_index + 1) % len(epochs)
        print()

def train_on_all_lines(model, lines, lines_preds, epochs):
    for line,pred in zip(lines,lines_preds):
        train_on_one_line(model,line,pred,epochs)

#model train try
batch_size = 17
model = Sequential()
model.add(LSTM(100, stateful=True, return_sequences=True, input_shape=(3, look_back + 1), recurrent_activation="tanh", batch_size=batch_size))
model.add(Activation("tanh"))
model.add(Dropout(0.15))    
model.add(LSTM(110, stateful=True, return_sequences=True, recurrent_activation="tanh", batch_size=batch_size))
model.add(Activation("tanh"))
model.add(Dropout(0.15))
model.add(LSTM(80, stateful=True, return_sequences=False, recurrent_activation="tanh", batch_size=batch_size))
model.add(Activation("tanh"))
model.add(Dropout(0.15))
model.add(Dense(1))
model.add(Activation("relu"))
model.compile(loss='mean_squared_error', optimizer='rmsprop')

train_on_one_line(model,train_LB_X[214],train_pred[214],epochs=120)
train_on_one_line(model,train_LB_X[212],train_pred[212],epochs=120)
train_on_one_line(model,train_LB_X[9],train_pred[9],epochs=80)
train_on_all_lines(model,train_LB_X[3:30],train_pred[3:30],30)
train_on_all_lines(model,train_LB_X,train_pred,17)
train_on_some_lines(model,train_LB_X,train_pred,np.random.randint(0,len(train_LB_X),50),epochs=np.random.randint(15,35,15))
print('saving model as h5')
model_path = 'W:\Datasets\synth_scoring\model2.h5'
model.save(model_path)
print()
print('scoring!')
print()
# make predictions
trainPredict214 = model.predict(train_LB_X[214],batch_size = batch_size)
trainPredict165 = model.predict(train_LB_X[165],batch_size = batch_size)
trainPredict9 = model.predict(train_LB_X[9],batch_size = batch_size)
trainPredict280 = model.predict(train_LB_X[280],batch_size = batch_size)
testPredict49 = model.predict(test_LB_X[49],batch_size = batch_size)
# calculate root mean squared error
#trainPredict = scaler.inverse_transform(trainPredict)
#train_pred = scaler.inverse_transform([train_pred])
#testPredict = scaler.inverse_transform(testPredict)
#test_pred = scaler.inverse_transform([test_pred])
trainScore = math.sqrt(mean_squared_error(train_pred[214], trainPredict214))
trainScore += math.sqrt(mean_squared_error(train_pred[165], trainPredict165))
trainScore += math.sqrt(mean_squared_error(train_pred[9], trainPredict9))
trainScore += math.sqrt(mean_squared_error(train_pred[280], trainPredict280))
trainScore /= 4.0
print('Train Score: %.2f RMSE' % (trainScore))
testScore = math.sqrt(mean_squared_error(test_pred[49], testPredict49))
print('Test Score: %.2f RMSE' % (testScore))
print()
print('plotting prediction')

#plt.plot(train_LB_X_plot_vals,color='green', label='training data',
#linewidth=5)
plt.plot(trainPredict214,color = 'blue', label = '214')
plt.plot(trainPredict165,color = 'gray', label = '165')
plt.plot(trainPredict9,color = 'green', label = '9')
plt.plot(trainPredict280,color = 'gray', linewidth=3)
plt.plot(trainPredict280,color = 'yellow', label = '280')

#plt.plot(train_LB_X_plot_vals,color='orange', label='test data', linewidth=3)
plt.plot(testPredict49,color='red', label='test predictions')
plt.legend(loc = 'upper right')
plt.show()