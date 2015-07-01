
import csv
import datetime
from numpy import *
from scipy.sparse import csr_matrix
import matplotlib.pyplot as plt
import math

def getDayTime(time):
    year = int(time[0:4])
    month = int(time[5:7])
    day = int(time[8:10])
    hour = int(time[11:13])
    minu = int(time[14:16])
    sec = int(time[17:19])
    return datetime.datetime(year,month,day,hour,minu,sec)

def getDayTime2(time):
    year = int(time[0:4])
    month = int(time[5:7])
    day = int(time[8:10])
    hour = 23
    minu = 59
    sec = 59
    return datetime.datetime(year,month,day,hour,minu,sec)

## return the hours of t1 - t2
def timeSubtract(t1, t2):
    dt1 = getDayTime(t1)
    dt2 = getDayTime(t2)

    return (dt1-dt2).total_seconds()/3600

## return a string for time + days
def timeShift(time, days):
    dt = getDayTime(time)
    ds = dt + datetime.timedelta(days)
    return ds.strftime('%Y-%m-%dT%H:%M:%S')

## return a string for time + days
def timeShift2(time, days):
    dt = getDayTime2(time)
    ds = dt + datetime.timedelta(days)
    return ds.strftime('%Y-%m-%dT%H:%M:%S')

def readCsv(csvName, cols):
    data = []
    file = open(csvName, 'rt')
    lines_csv = csv.reader(file)
    for line in lines_csv:
        item_data = []
        for col in cols:
            item_data.append(float(line[col]))
        if len(cols) == 1:
            item_data = item_data[0]
        data.append(item_data)
    return data

def normalizeResult(result):
    for i in range(len(result)):
        result[i] = result[i][0]
        if type(result[i]) is ndarray:
            result[i] = result[i][1]
        result[i] = max(result[i], 0)
        result[i] = min(result[i], 1)

def checkError(label, result):
    error = 0
    for i in range(len(label)):
        if label[i] == 1:
            error += result[i]
        else:
            error += 1 - result[i]
    if len(label)>0:
        error = 1.0 * error /len(label)
    return error

def outputResult(enroll_list, result, filename):
    csvfile = open(filename, 'w', newline='')
    writer = csv.writer(csvfile)
    for i in range(len(enroll_list)):
        writer.writerow([int(enroll_list[i]), result[i]])
    csvfile.close()

# the splitted matrix share the same indices and data with original csr
# changing the elements will change both
def splitCsr(csr, row):
    assert row < csr.shape[0]
    indptr_1 = csr.indptr[:row + 1].copy()
    indices_1 = csr.indices[:csr.indptr[row]]
    data_1 = csr.data[:csr.indptr[row]]
    indptr_2 = csr.indptr[row:].copy()
    indices_2 = csr.indices[csr.indptr[row]:]
    data_2 = csr.data[csr.indptr[row]:]
    for i in range(len(indptr_2) - 1, 0, -1):
        indptr_2[i] -= indptr_2[0]
    indptr_2[0] = 0

    mat_1 = csr_matrix((data_1,indices_1, indptr_1), shape=(row, csr.shape[1]))
    mat_2 = csr_matrix((data_2,indices_2, indptr_2), shape=(csr.shape[0] - row, csr.shape[1]))

    return mat_1, mat_2

def drawVector(vec, rows, cols, depth):
    plt.figure(figsize=(16, 10))
    vec_all = []
    for d in range(depth):
        vec_new = [([0]*cols) for i in range(rows)]
        for i in range(rows):
            for j in range(cols):
                vec_new[i][j] = vec[depth*(i*cols+j)+d]
        vec_all.append(vec_new)

    for d in range(depth):
        plot = plt.subplot(math.ceil(depth/4), 4, d + 1)
        mat = abs(array(vec_all[d]))
        # mat = array([([0.5]*cols) for i in range(rows)]) + 0.5 * mat
        plot.imshow( mat, interpolation='nearest',
                       cmap='binary', vmax=1, vmin=0)
        plot.set_xticks(())
        plot.set_yticks(())
    plt.show()