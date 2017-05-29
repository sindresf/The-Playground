import pandas as pd
import numpy as np
pd.options.mode.chained_assignment = None  # default='warn'
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from sklearn.model_selection import train_test_split
from sklearn import model_selection
from sklearn import svm
import seaborn as sns
sns.set(color_codes=True)


def mean_split(data, std_weight):
    dt = data.copy()
    midVal = dt[dt > 0].mean()
    std_width = dt[dt > 0].std() * std_weight
    lowerVal = midVal - std_width
    higherVal = midVal + std_width
    dt[(dt < lowerVal) & (dt > 0)] = 1
    dt[((dt < higherVal) & (dt >= lowerVal))] = 2
    dt[dt >= higherVal] = 3
    return dt

labeled_images = pd.read_csv('W:/Datasets/MNIST/train.csv')
images = labeled_images.iloc[:15000,1:]
labels = labeled_images.iloc[:15000,:1]
train_images, test_images, train_labels, test_labels = train_test_split(images, labels, train_size=0.8, random_state=0)
i = 1
std_weight = 0.1
bt_tst_imgs = mean_split(test_images,std_weight)
bt_trn_imgs = mean_split(train_images,std_weight)
img = bt_trn_imgs.iloc[i].as_matrix().reshape((28,28))
plt.clf()
plt.imshow(img, cmap='viridis')

clf_bucket = svm.SVC()
clf_bucket.fit(bt_trn_imgs, train_labels.values.ravel())
score = clf_bucket.score(bt_tst_imgs,test_labels)
print('bucket score ' + str(score))
print()