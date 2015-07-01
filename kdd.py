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
import preProcess
import csv
from sklearn import preprocessing
from sklearn.decomposition import PCA
from sklearn import svm
from sklearn.linear_model import SGDClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn import linear_model
from sklearn.naive_bayes import GaussianNB
from sklearn import neighbors
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.neural_network import BernoulliRBM
from sklearn.pipeline import Pipeline
from sklearn.metrics import roc_auc_score
from scipy.io import mmread



def fitAndTest(clf, X, Y, data_test, enroll_list, errors, name):
    # train_size = 90000
    # clf.fit(X[:train_size], Y[:train_size])
    # resTrain = []
    # resTest = []
    # print('%s fitted' % name)
    # for item in X[train_size:]:
    #     tmpRes = clf.predict(item)
    #     resTrain.append(tmpRes)
    # for item in data_test:
    #     tmpRes = clf.predict(item)
    #     resTest.append(tmpRes)
    # utilities.normalizeResult(resTrain)
    # utilities.normalizeResult(resTest)
    # utilities.outputResult(enroll_list, resTest, '%s.csv' % name)
    # errors[name] = roc_auc_score(Y[train_size:], resTrain)


    train_size = 90000
    X_new, X_reserve = utilities.splitCsr(X,train_size)
    clf.fit(X_new, Y[:train_size])
    resTrain = []
    resTest = []
    print('%s fitted' % name)
    for row in X_reserve:
        tmpRes = clf.predict(row)
        resTrain.append(tmpRes)
    for row in data_test:
        tmpRes = clf.predict(row)
        resTest.append(tmpRes)
    utilities.normalizeResult(resTrain)
    utilities.normalizeResult(resTest)
    utilities.outputResult(enroll_list, resTest, '%s.csv' % name)
    errors[name] = roc_auc_score(Y[train_size:], resTrain)

    print('%s DONE!' % name)

def fitAndTestProba(clf, X, Y, data_test, enroll_list, errors, name):
    # train_size = 90000
    # clf.fit(X[:train_size], Y[:train_size])
    # resTrain = []
    # resTest = []
    # print('%s fitted' % name)
    # for item in X[train_size:]:
    #     tmpRes = clf.predict_proba(item)
    #     resTrain.append(tmpRes)
    # for item in data_test:
    #     tmpRes = clf.predict_proba(item)
    #     resTest.append(tmpRes)
    # utilities.normalizeResult(resTrain)
    # utilities.normalizeResult(resTest)
    # utilities.outputResult(enroll_list, resTest, '%s.csv' % name)
    # errors[name] = roc_auc_score(Y[train_size:], resTrain)
    # print('%s DONE!' % name)

    train_size = 90000
    X_new, X_reserve = utilities.splitCsr(X,train_size)
    clf.fit(X_new, Y[:train_size])
    resTrain = []
    resTest = []
    print('%s fitted' % name)
    for row in X_reserve:
        tmpRes = clf.predict_proba(row)
        resTrain.append(tmpRes)
    for row in data_test:
        tmpRes = clf.predict_proba(row)
        resTest.append(tmpRes)
    utilities.normalizeResult(resTrain)
    utilities.normalizeResult(resTest)
    utilities.outputResult(enroll_list, resTest, '%s.csv' % name)
    errors[name] = roc_auc_score(Y[train_size:], resTrain)

    print('%s DONE!' % name)


def main():
##Preparation
    # X, data_test = preProcess.preProcess()
    X = mmread('tmpTrain_2').tocsr()
    data_test = mmread('tmpTest_2').tocsr()
    # X = utilities.readCsv("tmpTrain.csv", range(0,300))
    # data_test = utilities.readCsv("tmpTest.csv", range(0,300))
    Y = utilities.readCsv("truth_train.csv", range(1,2))
    enroll_list = utilities.readCsv("sampleSubmission.csv", range(0,1))

    # min_max_scaler = preprocessing.MinMaxScaler()
    # X = min_max_scaler.fit_transform(X)

    # pca = PCA(n_components=10)
    # X = pca.fit_transform(X)
    # data_test = pca.transform(data_test)
    # print(pca.explained_variance_ratio_)

    print('Prepare DONE!')
    print("size of train data: %d x %d" % (X.shape[0], X.shape[1]))
    print("size of test data: %d x %d" % (data_test.shape[0], data_test.shape[1]))
    # print("size of train data: %d x %d" % (len(X), len(X[0])))
    # print("size of train data: %d x %d" % (len(data_test), len(data_test[0])))
    print("size of train label: %d x %d" % (len(Y), 1))
    print("size of enroll list: %d x %d" % (len(enroll_list), 1))
    errors = {}

##SVM
    # clf =  svm.SVC(gamma=2, C=1, probability=True)
    # fitAndTestProba(clf, X, Y, data_test, enroll_list, errors, 'SVM')

##SGD
    clf = SGDClassifier(loss="log")
    fitAndTestProba(clf, X, Y, data_test, enroll_list, errors, 'SGD')

##Randomized Forest
    # clf = RandomForestClassifier(n_estimators=30)
    # fitAndTestProba(clf, X, Y, data_test, enroll_list, errors, 'RF')

##Naive Bayes
    # clf = GaussianNB()
    # fitAndTestProba(clf, X, Y, data_test, enroll_list, errors, 'NB')

##Logistic Regression
    c = 0.005
    clf = linear_model.LogisticRegression(C=c)
    fitAndTestProba(clf, X, Y, data_test, enroll_list, errors, 'LOG %f' % c)

##Linear Regression
    # clf = linear_model.LinearRegression()
    # fitAndTest(clf, X, Y, data_test, enroll_list, errors, 'LR')

##Linear Regression Lasso
    # clf = linear_model.Lasso(alpha = 0.001)
    # fitAndTest(clf, X, Y, data_test, enroll_list, errors, 'Las')

##Bayes Regression
    # clf = linear_model.BayesianRidge()
    # fitAndTest(clf, X, Y, data_test, enroll_list, errors, 'BR')

##Neural Network
    # logistic = linear_model.LogisticRegression(C = 1)
    # rbm = BernoulliRBM(random_state=0, verbose=True)
    # rbm.n_components = 10
    # rbm.learning_rate = 0.0001
    # rbm.n_iter = 20
    # clf = Pipeline(steps=[('rbm', rbm), ('logistic', logistic)])
    # fitAndTestProba(clf, X, Y, data_test, enroll_list, errors, 'NN')

##KNN
    # for n in range(3, 15, 3):
    #     clf = neighbors.KNeighborsClassifier(n, weights='uniform')
    #     fitAndTestProba(clf, X, Y, data_test, enroll_list, errors, 'KNN %d' % n)

##Boost
    # clf = GradientBoostingClassifier(n_estimators=100, learning_rate=0.01, random_state=0)
    # fitAndTestProba(clf, X, Y, data_test, enroll_list, errors, 'BS')


##Output Errors
    print(errors)
    utilities.drawVector(clf.coef_[0], 30, 30, 7)


if __name__ == '__main__':
    main()
