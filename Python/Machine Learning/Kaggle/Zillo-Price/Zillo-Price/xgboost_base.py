import numpy as np
import pandas as pd
import xgboost as xgb
import gc

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
split = int(len(x_train) * 0.88)
print("split: " + str(split))
x_train, y_train, x_valid, y_valid = x_train[:split], y_train[:split], x_train[split:], y_train[split:]

print('Building DMatrix...')
d_train = xgb.DMatrix(x_train, label=y_train)
d_valid = xgb.DMatrix(x_valid, label=y_valid)

del x_train, x_valid
gc.collect()

print('Training ...')
params = {}
params['seed'] = 21
params['eta'] = 0.02
params['objective'] = 'reg:linear'
params['eval_metric'] = 'mae'
params['silent'] = 1
params['max_depth'] = 4
params['min_child_weight'] = 1
params['gamma'] = 0.0
#div
params['max_delta_step'] = 0
params['silent'] = 1
params['lambda'] = 1
params['alpha'] = 0
params['lambda_bias'] = 0
params['subsample'] = 1.0
params['colsample_bytree '] = 1.0

watchlist = [(d_train, 'train'), (d_valid, 'valid')]
clf = xgb.train(params, d_train, 10000, watchlist, early_stopping_rounds=100, verbose_eval=10)
print("saving model")
clf.save_model("first.model")
del d_train, d_valid

print('Building test set ...')
sample['parcelid'] = sample['ParcelId']
df_test = sample.merge(prop, on='parcelid', how='left')

del prop
gc.collect()

x_test = df_test[train_columns]
for c in x_test.dtypes[x_test.dtypes == object].index.values:
    x_test[c] = (x_test[c] == True)

del df_test, sample
gc.collect()

d_test = xgb.DMatrix(x_test)

del x_test
gc.collect()

print('Predicting on test ...')
p_test = clf.predict(d_test)

del d_test
gc.collect()

sub = pd.read_csv('W:/Datasets/Zillo/sample_submission.csv')
for c in sub.columns[sub.columns != 'ParcelId']:
    sub[c] = p_test

#print('Writing csv ...')
#sub.to_csv('xgb_starter.csv', index=False, float_format='%.4g')
print()
print([params['eta'],params['max_depth'],params['gamma'],params['subsample'],params['colsample_bytree '],clf.best_score])