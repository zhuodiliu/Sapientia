#-------------------------------------------------------------------------------
# Name:        濠碘槅鍨埀顒冩珪閸?
# Purpose:
#
# Author:      Administrator
#
# Created:     06/06/2015
# Copyright:   (c) Administrator 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import csv
from sklearn import svm
from sklearn.linear_model import SGDClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn import linear_model

def main():
####enrollment_train:['enrollment_id', 'username', 'course_id']
##    file = open('enrollment_train.csv', 'rt')
##    file.readline()
##    enrollment_train = csv.reader(file)
####    for line in enrollment_train:
####        print(line)
##log_train:['enrollment_id', 'time', 'source', 'event', 'object']
    file = open('log_train.csv', 'rt')
    file.readline()
    log_train = csv.reader(file)
    for line in log_train:
        print(line)
##truth_train:[id,0/1]
    truth_train = csv.reader(open('truth_train.csv', 'rt'))
####    for line in truth_train:
####        print(line)
##    file = open('enrollment_test.csv', 'rt')
##    file.readline()
##    enrollment_test = csv.reader(file)
####    for line in enrollment_test:
####        print(line)
##    file = open('log_test.csv', 'rt')
##    file.readline()
##    log_test = csv.reader(file)
####    for line in log_test:
####        print(line)
####cobject:['course_id','module_id','category','children','start']
##    file = open('object.csv', 'rt')
##    file.readline()
##    cobject = csv.reader(file)
####    for line in cobject:
####        print(line)
##
##    data_train = [[0 for col in range(5)] for row in range(300000)]
##    for line in log_train:
##        if line[3]=='navigate':
##            data_train[int(line[0])][0]+=1;
##
##        if line[3]=='access':
##            data_train[int(line[0])][1]+=1;
##
##        if line[3]=='problem':
##            data_train[int(line[0])][2]+=1;
##
##        if line[3]=='page_close':
##            data_train[int(line[0])][3]+=1;
##
##        if line[3]=='video':
##            data_train[int(line[0])][4]+=1;
##    data_test = [[0 for col in range(5)] for row in range(300000)]
##    for line in log_test:
##        if line[3]=='navigate':
##            data_test[int(line[0])][0]+=1;
##
##        if line[3]=='access':
##            data_test[int(line[0])][1]+=1;
##
##        if line[3]=='problem':
##            data_test[int(line[0])][2]+=1;
##
##        if line[3]=='page_close':
##            data_test[int(line[0])][3]+=1;
##
##        if line[3]=='video':
##            data_test[int(line[0])][4]+=1;
##
##    csvfile = open('tmpTrain.csv', 'wt')
##    writer = csv.writer(csvfile)
##    writer.writerows(data_train)
##    csvfile.close()
##    csvfile = open('tmpTest.csv', 'wt')
##    writer = csv.writer(csvfile)
##    writer.writerows(data_test)
##    csvfile.close()

##Submission preparation
    SubNum = []
    file = open('sampleSubmission.csv', 'rt')
    tmp_train = csv.reader(file)
    j = 1
    for line in tmp_train:
        tmpa = int(line[0])
        SubNum.append(tmpa)
        if j>80362:
            break
        j+=1


    X=[]
    Y=[]

    file = open('tmpTrain.csv', 'rt')
    tmp_train = csv.reader(file)
    j = 0
    for line in tmp_train:
        if j%2==0:
            tmpa = [int(line[0]),int(line[1]),int(line[2]),int(line[3]),int(line[4])]
##            print(tmpa)
            X.append(tmpa)
        if j>=2*120541:
            break
        j+=1

    data_test = []
    file = open('tmpTest.csv', 'rt')
    tmp_test = csv.reader(file)
    j = 0
    for line in tmp_test:
        if j%2==0:
            tmpa = [int(line[0]),int(line[1]),int(line[2]),int(line[3]),int(line[4])]
            data_test.append(tmpa)
        if j>2*80362:
            break
        j+=1



    for line in truth_train:
##        X.append(data_train[int(line[0])]);
        if line[1]=='0':
            Y.append(0);
        if line[1]=='1':
            Y.append(1);

    print('Prepare DONE!')
##SVM
    clf = svm.SVC()
    clf.fit(X, Y)
    resSVC = []
    for item in data_test:
        tmpRes = clf.predict(item)
        if tmpRes == 0:
            resSVC.append(0)
        if tmpRes == 1:
            resSVC.append(1)
    csvfile = open('resSVM.csv', 'w',newline='')
    writer = csv.writer(csvfile)
    for i in range (1,80363):
        writer.writerow([SubNum[i-1],resSVC[i-1]])
    csvfile.close()
    print('SVM DONE!')

##SGD
    clf = SGDClassifier(loss="hinge", penalty="l2")
    clf.fit(X, Y)
    resSGD = []
    for item in data_test:
        tmpRes = clf.predict(item)
        if tmpRes == 0:
            resSGD.append(0)
        if tmpRes == 1:
            resSGD.append(1)
    csvfile = open('resSGD.csv', 'w',newline='')
    writer = csv.writer(csvfile)
    for i in range (1,80363):
        writer.writerow([SubNum[i-1],resSGD[i-1]])
    csvfile.close()
    print('SGD DONE!')

##Randomized Tree
    clf = RandomForestClassifier(n_estimators=10)
    clf.fit(X, Y)
    resRT = []
    for item in data_test:
        tmpRes = clf.predict(item)
        if tmpRes == 0:
            resRT.append(0)
        if tmpRes == 1:
            resRT.append(1)
    csvfile = open('resRT.csv', 'w',newline='')
    writer = csv.writer(csvfile)
    for i in range (1,80363):
        writer.writerow([SubNum[i-1],resRT[i-1]])
    csvfile.close()
    print('RT DONE!')

##Linear Regression
    clf = linear_model.LinearRegression()
    clf.fit(X, Y)
    resLR = []
    resLR_tmp = []
    totaltmp = 0
    for item in data_test:
        tmpRes = clf.predict(item)
        resLR_tmp.append(tmpRes)
        totaltmp += tmpRes
    avertmp = totaltmp / 80362.0
    for item in resLR_tmp:
        if item >= avertmp:
            resLR.append(1)
        if item < avertmp:
            resLR.append(0)

    csvfile = open('resLR.csv', 'w',newline='')
    writer = csv.writer(csvfile)
    for i in range (1,80363):
        writer.writerow([SubNum[i-1],resLR[i-1]])
    csvfile.close()
    print('LR DONE!')

##Bayes Regression
    clf = linear_model.BayesianRidge()
    clf.fit(X, Y)
    resBR = []
    resBR_tmp = []
    totaltmp = 0
    for item in data_test:
        tmpRes = clf.predict(item)
        resBR_tmp.append(tmpRes)
        totaltmp += tmpRes
    avertmp = totaltmp / 80362.0
    for item in resBR_tmp:
        if item >= avertmp:
            resBR.append(1)
        if item < avertmp:
            resBR.append(0)

    csvfile = open('resBR.csv', 'w',newline='')
    writer = csv.writer(csvfile)
    for i in range (1,80363):
        writer.writerow([SubNum[i-1],resBR[i-1]])
    csvfile.close()
    print('BR DONE!')


if __name__ == '__main__':
    main()
