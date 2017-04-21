import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap as lcm
from AdelineGD import AdelineGD as Adeline

epochs = 16
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

y = extract_instances(data, 100, 4)
y = np.where(y == 'Iris-setosa', -1, 1)
X = extract_instances(data, 100, [0,2])
X_std = np.copy(X)
X_std[:,0] = (X[:,0] - X[:,0].mean()) / X[:,0].std()
X_std[:,1] = (X[:,1] - X[:,1].mean()) / X[:,1].std()

def plot_decision_regions(X, y, classifier, resolution=0.02):
    #setup marker generator and color map
    markers = ('s','x','o','^','v')
    colors = ('red','blue','lightgreen','gray','cyan')
    cmap = lcm(colors[:len(np.unique(y))])

    #plot the decision surface
    x1_min, x1_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    x2_min, x2_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    xx1, xx2 = np.meshgrid(np.arange(x1_min,x1_max, resolution),
                           np.arange(x2_min, x2_max, resolution))
    Z = classifier.predict(np.array([xx1.ravel(), xx2.ravel()]).T)
    Z = Z.reshape(xx1.shape)

    plt.contourf(xx1,xx2,Z,alpha=0.4, cmap=cmap)
    plt.xlim(xx1.min(), xx1.max())
    plt.ylim(xx2.min(), xx2.max())

    #plot class samples
    for idx, cl in enumerate(np.unique(y)):
        plt.scatter(x=X[y == cl, 0], y=X[y == cl, 1],
                    alpha=0.8, c=cmap(idx),
                    marker=markers[idx], label=cl)

ada = Adeline(n_iter=epochs, eta=0.01)
ada.fit(X_std,y)
plot_decision_regions(X_std,y, classifier=ada)
plt.title = 'Adeline - Gradient Descent'
plt.xlabel = 'sepal length [std]'
plt.ylabel = 'petal length [std]'
plt.legend(loc='upper left')
plt.show()
plt.plot(range(1, len(ada.cost_) + 1), ada.cost_, marker='o')
plt.xlabel = 'Epochs'
plt.ylabel = 'SQE'
plt.show()