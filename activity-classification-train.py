# -*- coding: utf-8 -*-
"""
This is the script used to train an activity recognition 
classifier on accelerometer data.

"""

import os
import sys
import numpy as np
import sklearn
from sklearn.tree import export_graphviz
from features import extract_features
from util import slidingWindow, reorient, reset_vars
import pickle

from sklearn import model_selection
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier


from sklearn.model_selection import StratifiedKFold

from sklearn.metrics import confusion_matrix, accuracy_score

# %%---------------------------------------------------------------------------
#
#		                 Load Data From Disk
#
# -----------------------------------------------------------------------------

print("Loading data...")
sys.stdout.flush()
data_file = 'brand-new-merged-activity.csv'
data = np.genfromtxt(data_file, delimiter=',')
print("Loaded {} raw labelled activity data samples.".format(len(data)))
sys.stdout.flush()

# %%---------------------------------------------------------------------------
#
#		                    Pre-processing
#
# -----------------------------------------------------------------------------

print("Reorienting accelerometer data...")
sys.stdout.flush()
reset_vars()
reoriented = np.asarray([reorient(data[i,1], data[i,2], data[i,3]) for i in range(len(data))])
reoriented_data_with_timestamps = np.append(data[:,0:1],reoriented,axis=1)
data = np.append(reoriented_data_with_timestamps, data[:,-1:], axis=1)

# %%---------------------------------------------------------------------------
#
#		                Extract Features & Labels
#
# -----------------------------------------------------------------------------

offset = 2
mins = 5
window_size = 25 * 60 * offset * mins # ~5 minutes assuming 25 Hz sampling rate
step_size = window_size # no overlap


# sampling rate should be about 25 Hz; you can take a brief window to confirm this
n_samples = 1000

time_elapsed_seconds = (data[n_samples,0] - data[0,0]) / 1000
sampling_rate = n_samples / time_elapsed_seconds

# TODO: list the class labels that you collected data for in the order of label_index (defined in collect-labelled-data.py)
class_names = ["vigil", "sleeping"] #...


print("Extracting features and labels for window size {} and step size {}...".format(window_size, step_size))
sys.stdout.flush()

X = []
Y = []

for i,window_with_timestamp_and_label in slidingWindow(data, window_size, step_size):
    window = window_with_timestamp_and_label[:,1:-1]   
    feature_names, x = extract_features(window)
    X.append(x)
    Y.append(window_with_timestamp_and_label[10, -1])
    
X = np.asarray(X)
Y = np.asarray(Y)
n_features = len(X)

    
print("Finished feature extraction over {} windows".format(len(X)))
print("Unique labels found: {}".format(set(Y)))
print("\n")

# print("******************************** X data ******************************** ")
# print(X)
# print("******************************** Y data ******************************** ")
# print(Y)
# sys.stdout.flush()

# %%---------------------------------------------------------------------------
#
#		                Train & Evaluate Classifier
#
# -----------------------------------------------------------------------------


# TODO: split data into train and test datasets using 10-fold cross validation

# cv = model_selection.KFold(n_splits=10, random_state=None, shuffle=True)
cv = StratifiedKFold(n_splits=10, random_state=None, shuffle=True)

"""
TODO: iterating over each fold, fit a decision tree classifier on the training set.
Then predict the class labels for the test set and compute the confusion matrix
using predicted labels and ground truth values. Print the accuracy, precision and recall
for each fold.
"""
total_accuracy = 0.0
total_precision = 0.0
total_recall = 0.0

# Iterate over the cv and fit the decision tree using the training set
# https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.KFold.html

for i, (train_index, test_index) in enumerate(cv.split(X, Y)):
	X_train, X_test = X[train_index], X[test_index]
	y_train, y_test = Y[train_index], Y[test_index]
	tree = DecisionTreeClassifier(criterion="entropy", max_depth=3)
	print("Fold {} : Training decision tree classifier over {} points...".format(i, len(y_train)))
	sys.stdout.flush()
	tree.fit(X_train, y_train)
	print("Evaluating classifier over {} points...".format(len(y_test)))

	# predict the labels on the test data
	y_pred = tree.predict(X_test)

	# show the comparison between the predicted and ground-truth labels
	conf = confusion_matrix(y_test, y_pred, labels=[0,1])

	accuracy = np.sum(np.diag(conf)) / float(np.sum(conf))
	precision = np.nan_to_num(np.diag(conf) / np.sum(conf, axis=1).astype(float))
	recall = np.nan_to_num(np.diag(conf) / np.sum(conf, axis=0).astype(float))

	total_accuracy += accuracy
	total_precision += precision
	total_recall += recall
   
print("The average accuracy is {}".format(total_accuracy/10.0))  
print("The average precision is {}".format(total_precision/10.0))
print("The average recall is {}".format(total_recall/10.0))


# Set this to the best model you found, trained on all the data:
best_classifier = RandomForestClassifier(n_estimators=100)
best_classifier.fit(X,Y) 

export_graphviz(tree, out_file='tree-random.dot', feature_names = feature_names)

classifier_filename='classifier.pickle'

print("Saving best classifier")

with open(classifier_filename, 'wb') as f:
    pickle.dump(best_classifier, f)
