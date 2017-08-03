import numpy as np
import pandas as pd
import xgboost as xgb
import gc
np.random.seed(21)
print('Loading data ...')
train = pd.read_csv('W:/Datasets/Zillo/train_2016_v2.csv')
prop = pd.read_csv('W:/Datasets/Zillo/properties_2016.csv')
sample = pd.read_csv('W:/Datasets/Zillo/sample_submission.csv')

print('Binding to float32')
for c, dtype in zip(prop.columns, prop.dtypes):
	if dtype == np.float64:
		prop[c] = prop[c].astype(np.float32)

print('Creating training set ...')
df_train = train.merge(prop, how='left', on='parcelid')

x_train = df_train.drop(['parcelid', 'logerror', 'transactiondate', 'propertyzoningdesc', 'propertycountylandusecode'], axis=1)
y_train = df_train['logerror'].values
print(x_train.shape, y_train.shape)

train_columns = x_train.columns

for c in x_train.dtypes[x_train.dtypes == object].index.values:
    x_train[c] = (x_train[c] == True)

del df_train
gc.collect()

#split = 80000
split = int(len(x_train) * 0.82)
print("split: " + str(split))
x_train, y_train, x_valid, y_valid = x_train[:split], y_train[:split], x_train[split:], y_train[split:]

print('Building DMatrix...')
d_train = xgb.DMatrix(x_train, label=y_train)
d_valid = xgb.DMatrix(x_valid, label=y_valid)

del x_train, x_valid
gc.collect()
bests = []
print('Training ...')
def param_search():
    params = {}
    params['seed'] = 21
    params['eta'] = 0.033432524004331464
    params['objective'] = 'reg:linear'
    params['eval_metric'] = 'mae'
    params['silent'] = 1
    params['max_depth'] = 2
    params['min_child_weight'] = 1
    params['gamma'] = 0.01518768274100421
    #div
    params['max_delta_step'] = 0
    params['silent'] = 1
    params['lambda'] = 1
    params['alpha'] = 0
    params['lambda_bias'] = 0
    params['subsample'] = 0.7741669639153989
    params['colsample_bytree '] = 0.7216379873552161
    watchlist = [(d_train, 'train'), (d_valid, 'valid')]
    num_boost_rounds = 10000
    early_stopping_rounds = 250
    best = 0.065522
    for i in range(1):
        print("model no" + str(i))
        model = xgb.train(params, d_train, num_boost_rounds, watchlist,early_stopping_rounds=early_stopping_rounds , verbose_eval=10)
        stats = [params['eta'],params['max_depth'],params['gamma'],params['subsample'],params['colsample_bytree '],model.best_iteration, model.best_score]
        print(stats)
        if model.best_score <= best:
            print("saving model " + str(i) + ", score: " + str(model.best_score))
            model.save_model("model_" + str(i) + ".model")
            best = model.best_score
            bests.append(stats)
        params['eta'] = 0.03417800674826878 - np.random.uniform(0.00009,0.013)
        #params['max_depth'] = 2
        #params['gamma'] = 0.01518768274100421 + np.random.uniform(-0.0025,0.0025)
        #params['subsample'] = 0.7741669639153989 + np.random.uniform(0.001,0.185)
        #params['colsample_bytree '] = 0.7216379873552161 + np.random.uniform(0.001,0.185)
param_search()
print(bests)