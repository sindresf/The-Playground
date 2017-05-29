import pandas as pd
from sklearn import model_selection
from sklearn.ensemble import ExtraTreesClassifier

url = "https://archive.ics.uci.edu/ml/machine-learning-databases/pima-indians-diabetes/pima-indians-diabetes.data"
names = ['preg', 'plas', 'pres', 'skin', 'test', 'mass', 'pedi', 'age', 'class']

df = pd.read_csv(url, names=names)
array = df.values
X = array[:,0:8]
y = array[:,8]

seed = 21
num_trees = 100
max_features = 7

kfold = model_selection.KFold(n_splits=10, random_state=seed)
model = ExtraTreesClassifier(n_estimators=num_trees, max_features=max_features)
results = model_selection.cross_val_score(model, X, y, cv=kfold)
print('results: ')
print(results)
print()
print('mean: ' + str(results.mean()))