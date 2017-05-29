import pandas as pd
from sklearn import model_selection
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.ensemble import VotingClassifier

url = "https://archive.ics.uci.edu/ml/machine-learning-databases/pima-indians-diabetes/pima-indians-diabetes.data"
names = ['preg', 'plas', 'pres', 'skin', 'test', 'mass', 'pedi', 'age', 'class']

df = pd.read_csv(url,names=names)
array = df.values
X = array[:,0:8]
y = array[:, 8]
seed = 21
kfold = model_selection.KFold(n_splits=10, random_state=seed)

#SUB-models
estimators = []
LR_model = LogisticRegression()
estimators.append(('logistic', LR_model))
DT_model = DecisionTreeClassifier()
estimators.append(('cart', DT_model))
SV_model = SVC()
estimators.append(('svm', SV_model))

#Ensemble creation
ensemble = VotingClassifier(estimators)
results = model_selection.cross_val_score(ensemble, X, y, cv=kfold)

print('results: ')
print(results)
print()
print('mean: ' + str(results.mean()))