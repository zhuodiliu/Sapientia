#-------------------------------------------------------------------------------
# Name:        模块1
# Purpose:
#
# Author:      Administrator
#
# Created:     07/06/2015
# Copyright:   (c) Administrator 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import csv
def main():
    X = []
    file = open('resSGD.csv', 'rt')
    tmp_train = csv.reader(file)
    j = 0
    for line in tmp_train:
        if j%2==0:
            tmpa = int(line[0])
            X.append(tmpa)
        if j>160724:
            break
        j+=1
    Y = []
    file = open('sampleSubmission.csv', 'rt')
    tmp_train = csv.reader(file)
    j = 1
    for line in tmp_train:
        tmpa = int(line[0])
        Y.append(tmpa)
        if j>80362:
            break
        j+=1
    csvfile = open('sub2.csv', 'w',newline='')
    writer = csv.writer(csvfile)
    for i in range (1,80362):
        writer.writerow([Y[i-1],X[i-1]])
    writer.writerow([200903,1])
    csvfile.close()



if __name__ == '__main__':
    main()
