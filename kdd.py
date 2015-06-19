#-------------------------------------------------------------------------------
# Name:        kdd
# Purpose:
#
# Author:      Sapientia
#
# Created:     06/06/2015
# Copyright:   (c) Administrator 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import utilities
import csv
from sklearn import svm
from sklearn.linear_model import SGDClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn import linear_model


def fitAndTest(clf, X, Y, data_test, enroll_list, errors, name):
    train_size = 90000
    clf.fit(X[:train_size], Y[:train_size])
    resTrain = []
    resTest = []
    for item in X[train_size:]:
        tmpRes = clf.predict(item)
        resTrain.append(tmpRes)
    for item in data_test:
        tmpRes = clf.predict(item)
        resTest.append(tmpRes)
    utilities.normalizeResult(resTrain)
    utilities.normalizeResult(resTest)
    utilities.outputResult(enroll_list, resTest, '%s.csv' % name)
    errors[name] = utilities.checkError(Y[train_size:], resTrain)
    print('%s DONE!' % name)


def main():
##Preparation
    X = utilities.readCsv("tmpTrain.csv", range(1,6))
    Y = utilities.readCsv("truth_train.csv", range(1,2))
    data_test = utilities.readCsv("tmpTest.csv", range(1,6))
    enroll_list = utilities.readCsv("sampleSubmission.csv", range(0,1))

    print('Prepare DONE!')
    print("size of train data: %d" % len(X))
    print("size of train label: %d" % len(Y))
    print("size of test data: %d" % len(data_test))
    print("size of enroll list: %d" % len(enroll_list))
    errors = {}

##SVM
    # clf = svm.SVC()
    # clf = SGDClassifier(loss="hinge", penalty="l2")
    # fitAndTest(clf, X, Y, data_test, enroll_list, errors, 'SVM')

##SGD
    clf = SGDClassifier(loss="hinge", penalty="l2")
    fitAndTest(clf, X, Y, data_test, enroll_list, errors, 'SGD')

##Randomized Forest
    # clf = RandomForestClassifier(n_estimators=10)
    # fitAndTest(clf, X, Y, data_test, enroll_list, errors, 'RF')

##Linear Regression
    clf = linear_model.LinearRegression()
    fitAndTest(clf, X, Y, data_test, enroll_list, errors, 'LR')

##Bayes Regression
    clf = linear_model.BayesianRidge()
    fitAndTest(clf, X, Y, data_test, enroll_list, errors, 'BR')
##Output Errors
    print(errors)


if __name__ == '__main__':
    main()
