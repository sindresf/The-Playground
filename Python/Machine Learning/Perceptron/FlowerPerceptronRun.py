import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from Perceptron import Perceptron

eta = 0.02
epochs = 10
online_data_path = 'https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data'

def load_data(data_path):
    print('loading data')
    dataframe = pd.read_csv(data_path, header=None)
    return dataframe

data = load_data(online_data_path)
t = data.tail()

def extract_instances(dataframe, count,shape):
    print('extracting instances')
    instances = dataframe.iloc[0:count, shape].values
    return instances

y_batch = extract_instances(data, 100, 4)
y_batch = np.where(y_batch == 'Iris-setosa', -1, 1)
X_batch = extract_instances(data, 100, [0,2])

def plot_batch_scatter(split_point, x_label, y_label, legendLoc):
    print('constructing plot')
    plt.scatter(X_batch[:split_point, 0], X_batch[:split_point, 1],
                color='red', marker='o', label = 'setosa')
    plt.scatter(X_batch[split_point:len(X_batch), 0], X_batch[split_point:len(X_batch), 1],
                color='blue', marker='x', label='versicolor')
    plt.xlabel = x_label
    plt.ylabel = y_label
    plt.legend(legendLoc)
    print('displaying scatter plot')
    plt.show()

size_one = int(len(X_batch) / 2)
plot_batch_scatter(size_one, 'sepal length', 'petal length', 'upper left')
print()
print('constructing Perceptron')
NN = Perceptron(eta,epochs)
print('training network')
NN.fit(X_batch, y_batch)
print('plotting performance')
plt.plot(range(1,len(NN.errors_) + 1), NN.errors_, marker='o')
plt.xlabel = 'Epochs'
plt.ylabel = 'Number of misclassifications'
plt.show()
print()

