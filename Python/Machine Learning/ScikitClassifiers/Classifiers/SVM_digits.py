import pandas as pd
import numpy as np
pd.options.mode.chained_assignment = None  # default='warn'
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from sklearn.model_selection import train_test_split
from sklearn import svm
import seaborn as sns
sns.set(color_codes=True)

labeled_images = pd.read_csv('W:/Datasets/MNIST/train.csv')
images = labeled_images.iloc[0:5000,1:]
labels = labeled_images.iloc[0:5000,:1]
train_images, test_images, train_labels, test_labels = train_test_split(images, labels, train_size=0.8, random_state=0)
i = 1
std_weight = 0.1
bt_tst_imgs = test_images.copy()
midVal = bt_tst_imgs[bt_tst_imgs > 0].mean()
std_width = bt_tst_imgs[bt_tst_imgs > 0].std() * std_weight
lowerVal = midVal - std_width
higherVal = midVal + std_width
bt_tst_imgs[(bt_tst_imgs < lowerVal) & (bt_tst_imgs > 0)] = 1
bt_tst_imgs[((bt_tst_imgs < higherVal) & (bt_tst_imgs >= lowerVal))] = 2
bt_tst_imgs[bt_tst_imgs >= higherVal] = 3

bt_trn_imgs = train_images.copy()
midVal = bt_trn_imgs[bt_trn_imgs > 0].mean()
std_width = bt_trn_imgs[bt_trn_imgs > 0].std() * std_weight
lowerVal = midVal - std_width
higherVal = midVal + std_width
bt_trn_imgs[(bt_trn_imgs < lowerVal) & (bt_trn_imgs > 0)] = 1
bt_trn_imgs[((bt_trn_imgs < higherVal) & (bt_trn_imgs >= lowerVal))] = 2
bt_trn_imgs[bt_trn_imgs >= higherVal] = 3

img = bt_trn_imgs.iloc[i].as_matrix().reshape((28,28))
plt.clf()
plt.imshow(img, cmap='viridis')

clf_bucket = svm.SVC()
clf_bucket.fit(bt_trn_imgs, train_labels.values.ravel())
score = clf_bucket.score(bt_tst_imgs,test_labels)
print('bucket score ' + str(score))
print()
print('hard lines training')
hl_tst_imgs = test_images.copy()
std_weight = 0.12
midVal = hl_tst_imgs[hl_tst_imgs > 0].mean()
std_width = hl_tst_imgs[hl_tst_imgs > 0].std() * std_weight
higherVal = midVal + std_width
hl_tst_imgs[(hl_tst_imgs < higherVal) & (hl_tst_imgs > 0)] = 0
hl_tst_imgs[hl_tst_imgs >= higherVal] = 2

hl_trn_imgs = train_images.copy()
midVal = hl_trn_imgs[hl_trn_imgs > 0].mean()
std_width = hl_trn_imgs[hl_trn_imgs > 0].std() * std_weight
higherVal = midVal + std_width
hl_trn_imgs[(hl_trn_imgs < higherVal) & (hl_trn_imgs > 0)] = 0
hl_trn_imgs[hl_trn_imgs >= higherVal] = 2

img = hl_trn_imgs.iloc[i].as_matrix().reshape((28,28))
plt.clf()
plt.imshow(img, cmap='viridis')

clf_hard = svm.SVC()
clf_hard.fit(hl_trn_imgs, train_labels.values.ravel())
score = clf_hard.score(hl_tst_imgs,test_labels)
print('hard score ' + str(score))
print()
print('soft blob training')
sb_tst_imgs = test_images.copy()
std_weight = 0.85
midVal = sb_tst_imgs[sb_tst_imgs > 0].mean()
std_width = sb_tst_imgs[sb_tst_imgs > 0].std() * std_weight
lowerVal = midVal - std_width
sb_tst_imgs[sb_tst_imgs < lowerVal] = 0
sb_tst_imgs[sb_tst_imgs >= lowerVal] = 1

sb_trn_imgs = train_images.copy()
midVal = sb_trn_imgs[sb_trn_imgs > 0].mean()
std_width = sb_trn_imgs[sb_trn_imgs > 0].std() * std_weight
lowerVal = midVal - std_width
sb_trn_imgs[sb_trn_imgs < lowerVal] = 0
sb_trn_imgs[sb_trn_imgs >= lowerVal] = 1

img = sb_trn_imgs.iloc[i].as_matrix().reshape((28,28))
plt.clf()
plt.imshow(img, cmap='viridis')

clf_soft = svm.SVC()
clf_soft.fit(sb_trn_imgs, train_labels.values.ravel())
score = clf_soft.score(sb_tst_imgs,test_labels)
print('soft score ' + str(score))
print()
print('stacking SVCs')

test_data = pd.read_csv('W:/Datasets/MNIST/test.csv')
test_data[test_data > 0] = 1
pred1 = clf_bucket.predict(bt_trn_imgs + bt_tst_imgs)
pred2 = clf_hard.predict(hl_trn_imgs + hl_tst_imgs)
pred3 = clf_soft.predict(sb_trn_imgs + sb_tst_imgs)
stack_train_data = pd.DataFrame(np.column_stack([pred1,pred2,pred3]), columns=['bucket','hard','soft'])

clf_stack = svm.SVC()
clf_stack.fit(stack_train_data,train_labels.values.ravel() + stack_train_data.values.ravel())

test_pred1 = clf_bucket.predict(bt_tst_imgs)
test_pred2 = clf_hard.predict(hl_tst_imgs)
test_pred3 = clf_soft.predict(sb_tst_imgs)
stack_train_data = pd.DataFrame(np.column_stack([test_pred1,test_pred2,test_pred3]), columns=['bucket','hard','soft'])
print('stack: score data')
score = clf_stack.score(stack_train_data, test_labels)
print('stacked score: ' + str(score))

#test_data = pd.read_csv('W:/Datasets/MNIST/test.csv')
#test_data[test_data > 0] = 1
#results = clf_stack.predict(test_data[0:5000])
#df = pd.DataFrame(results)
#df.index.name = 'ImageId'
#df.index+=1
#df.columns = ['Label']
#df.to_csv('results.csv', header=True)