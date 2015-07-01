import csv
from utilities import timeShift
from utilities import timeShift2
from utilities import drawVector
from scipy.sparse import csr_matrix
from scipy.io import mmwrite


def featureProcess(filename):

    data = []

    end_time=[]
    time_split =[]

    csvfile = open("end_time.csv", 'rt')
    end_csv = csv.reader(csvfile)

    end_time_all=[]
    for line in end_csv:
        end_time_all.append(line[0])
    csvfile.close()


    csvfile = open(filename, 'rt')
    csvfile.readline()
    log_csv = csv.reader(csvfile)

    enroll_id = 0
    line_idx = -1
    for line in log_csv:
        if enroll_id != int(line[0]):
            enroll_id = int(line[0])
            end_time.append('0')
            line_idx += 1
            end_time[line_idx] =end_time_all[enroll_id-1]
    csvfile.close()
    print('%s end_time calculate finish' % filename)

    for lt in end_time:
        tmp_split = []
        for days  in range(-58, 0, 2):
            tmp_split.append(timeShift2(lt, days/2))
        time_split.append(tmp_split)
    print('%s time_split calculate finish: %d' % (filename, len(time_split)))

    # n points splitting n+1 peices
    # time_split = []
    # for days  in range(-145, 0, 5):
    #     time_split.append(timeShift("2014-08-01T00:00:00", days))


    # n points splitting n+1 peices
    lag_split = []
    for lag in range(0, 870, 30):
        lag_split.append(lag)

    csvfile = open(filename, 'rt')
    csvfile.readline()
    log_csv = csv.reader(csvfile)

    # enroll_id = 0
    # line_idx = -1
    # for line in log_csv:
    #     if enroll_id != int(line[0]):
    #         ## complete for last line

    #         ## init for new line
    #         enroll_id = int(line[0])
    #         data.append([0] * 300)
    #         line_idx += 1

    #     idx_time = 0 # from 0 to len(time_split)
    #     while idx_time < len(time_split[line_idx]) and time_split[line_idx][idx_time] < line[1]:
    #         idx_time += 1
    #     lag = (0 if line[4]=='null' else float(line[4]))
    #     idx_lag = 0 # from 0 to len(lag_split)
    #     while idx_lag < len(lag_split) and lag_split[idx_lag] < lag:
    #         idx_lag += 1
    #     bias = idx_time * (len(lag_split) + 1) + idx_lag
    #     bias *= 3

    #     # if line[3]=='navigate':
    #     #     data[line_idx][bias+1] = 1

    #     if line[3]=='access':
    #         data[line_idx][bias+0] = 1

    #     if line[3]=='problem':
    #         data[line_idx][bias+1] = 1

    #     # if line[3]=='page_close':
    #     #     data[line_idx][bias+4] = 1

    #     if line[3]=='video':
    #         data[line_idx][bias+2] = 1

    # preparation for sparse matrix
    rows = []
    cols = []
    values = []
    row_cnt = 0
    row_value = []
    enroll_id = 0
    for line in log_csv:
        if enroll_id != int(line[0]):
            ## complete for last line
            if row_cnt > 0:
                for i in range(len(row_value)):
                    if row_value[i] != 0:
                        rows.append(row_cnt-1)
                        cols.append(i)
                        values.append(row_value[i])
                drawVector(row_value, 30, 30, 7)
            ## init for new line
            enroll_id = int(line[0])
            row_value = [0] * 6300
            row_cnt += 1

        idx_time = 0 # from 0 to len(time_split)
        while idx_time < len(time_split[row_cnt-1]) and time_split[row_cnt-1][idx_time] < line[1]:
            idx_time += 1
        lag = (-1 if line[4]=='null' else float(line[4]))
        idx_lag = 0 # from 0 to len(lag_split)
        while idx_lag < len(lag_split) and lag_split[idx_lag] < lag:
            idx_lag += 1
        bias = idx_time * (len(lag_split) + 1) + idx_lag
        bias *= 7

        if line[3]=='navigate':
            row_value[bias+0] = 1

        if line[3]=='access':
            row_value[bias+1] = 1

        if line[3]=='problem':
            row_value[bias+2] = 1

        if line[3]=='page_close':
            row_value[bias+3] = 1

        if line[3]=='video':
            row_value[bias+4] = 1

        if line[3]=='wiki':
            row_value[bias+5] = 1

        if line[3]=='discussion':
            row_value[bias+6] = 1

    data_sparse = csr_matrix((values, (rows, cols)), shape=(row_cnt, 6300))

    csvfile.close()
    print('%s feature calculate finish' % filename)

    # for i in range(len(data)):
    #     for j in range(46, len(data[i])):
    #         data[i][j] = data[i][j-40] - data[i][j-45]

    return data_sparse


def preProcess():
    data_train = featureProcess('new_log_train_2.csv')
    data_test = featureProcess('new_log_test_2.csv')

    mmwrite('tmpTrain_2', data_train)
    mmwrite('tmpTest_2', data_test)

    # csvfile = open('tmpTrain.csv', 'w', newline='')
    # writer = csv.writer(csvfile)
    # writer.writerows(data_train)
    # csvfile = open('tmpTest.csv', 'w', newline='')
    # writer = csv.writer(csvfile)
    # writer.writerows(data_test)
    # csvfile.close()

    return data_train, data_test

if __name__ == '__main__':
    preProcess()
