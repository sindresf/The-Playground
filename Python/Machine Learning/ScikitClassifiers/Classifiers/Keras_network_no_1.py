from keras.models import Sequential
from keras.layers import Dense
import numpy as np
import pandas as pd

seed = 21
np.random.seed(seed)

url = "https://archive.ics.uci.edu/ml/machine-learning-databases/pima-indians-diabetes/pima-indians-diabetes.data"
names = ['preg', 'plas', 'pres', 'skin', 'test', 'mass', 'pedi', 'age', 'class']

df = pd.read_csv(url, names=names)
array = df.values
X = array[:,0:8]
y = array[:,8]

#Network definition
model = Sequential()
model.add(Dense(12, input_dim=8, activation='relu'))
model.add(Dense(8,activation='relu'))
model.add(Dense(1, activation='sigmoid'))

#Compiling model
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

#Fit the model
model.fit(X, y, epochs=50, batch_size=150, verbose=3)

#Evaluate it
scores = model.evaluate(X, y)
print("\n%s: % 2f%%" % (model.metrics_names[1], round(scores[1] * 100,2)))

#Predictions from the model
predictions = pd.DataFrame(model.predict(X))
predictions[predictions >= 0.5] = 1.0
predictions[predictions < 1] = 0.0
print(predictions)
hit = len(predictions[predictions[0] > 0.0])
rate = hit / len(predictions[0])
print("hitrate: " + str(rate)) #not rate, just nr. 1