import csv
import numpy as np
from scipy.sparse import csr_matrix
import utilities


def appendRow(csr, row):
    assert len(row) == csr.shape[1]
    indices = [] 
    data = []
    for col,value in enumerate(row):
        indices.append(col)
        data.append(value)

    ind_last = csr.indptr[len(csr.indptr)-1]
    csr.indptr = np.append(csr.indptr, np.array([ind_last + len(row)]))
    csr.indices = np.append(csr.indices, np.array(indices))
    csr.data = np.append(csr.data, np.array(data))
    csr.set_shape((csr.shape[0] + 1, csr.shape[1]))


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

# file_log = open('new_log_train.csv_2', 'rt')
# file_log.readline()
# log = csv.reader(file_log)
# file_train = open('tmpTrain.csv', 'rt')
# train = csv.reader(file_train)
# file_truth = open('truth_train.csv', 'rt')
# truth = csv.reader(file_truth)



# while True:
#     row_train = next(train)
#     row_truth = next(truth)
#     print (row_truth[1], end=': ')
#     print('')
#     for i in range(5,311,10):
#             print (int(float(row_train[i])), end=' ')
#     print('')
#     for i in range(10,311,10):
#             print (int(float(row_train[i])), end=' ')
#     print('')


c = [0.3, 0.0 , 0.5 ,0.1, 0.6, 0.2 , 0.9 ,0.3]
utilities.drawVector(c, 2 ,2, 2)