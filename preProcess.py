import csv
from utilities import timeShift
from scipy.sparse import csr_matrix
from scipy.io import mmwrite


def featureProcess(filename):

    data = []

    last_time = []
    time_split =[]
    
    file = open(filename, 'rt')
    file.readline()
    log = csv.reader(file)
    enroll_id = 0
    line_idx = -1
    for line in log:
        if enroll_id != int(line[0]):
            enroll_id = int(line[0])
            last_time.append('0')
            line_idx += 1
        last_time[line_idx] = max(last_time[line_idx], line[1])
    file.close()
    print('%s last_time calculate finish' % filename)

    for lt in last_time:
        tmp_split = []
        for days  in range(-58, 0, 2):
            tmp_split.append(timeShift(lt, days))
        time_split.append(tmp_split)
    print('%s time_split calculate finish: %d' % (filename, len(time_split)))

    # n points splitting n+1 peices
    # time_split = []
    # for days  in range(-145, 0, 5):
    #     time_split.append(timeShift("2014-08-01T00:00:00", days))


    # n points splitting n+1 peices
    lag_split = []
    for lag in range(30, 900, 30):
        lag_split.append(lag)
        
    csvfile = open(filename, 'rt')
    csvfile.readline()
    log = csv.reader(csvfile)

    # enroll_id = 0
    # line_idx = -1
    # for line in log:
    #     if enroll_id != int(line[0]):
    #         ## complete for last line

    #         ## init for new line
    #         enroll_id = int(line[0])
    #         data.append([0] * 750)
    #         line_idx += 1

    #     idx_time = 0 # from 0 to len(time_split) + 1
    #     while idx_time < len(time_split) and time_split[idx_time] < line[1]:
    #         idx_time += 1
    #     lag = (0 if line[4]=='null' else float(line[4]))
    #     idx_lag = 0 # from 0 to len(lag_split) + 1
    #     while idx_lag < len(lag_split) and lag_split[idx_lag] < lag:
    #         idx_lag += 1 
    #     bias = idx_time * (len(lag_split) + 1) + idx_lag
    #     bias *= 5

    #     if line[3]=='navigate':
    #         data[line_idx][bias+1]+=1

    #     if line[3]=='access':
    #         data[line_idx][bias+2]+=1

    #     if line[3]=='problem':
    #         data[line_idx][bias+3]+=1

    #     if line[3]=='page_close':
    #         data[line_idx][bias+4]+=1

    #     if line[3]=='video':
    #         data[line_idx][bias+5]+=1
 
    # preparation for sparse matrix
    rows = []
    cols = []
    values = []
    row_cnt = 0
    row_value = []
    enroll_id = 0
    for line in log:
        if enroll_id != int(line[0]):
            ## complete for last line
            if row_cnt > 0:
                for i in range(len(row_value)):
                    if row_value[i] != 0:
                        rows.append(row_cnt-1)
                        cols.append(i)
                        values.append(row_value[i])
            ## init for new line
            enroll_id = int(line[0])
            row_value = [0] * 4500
            row_cnt += 1

        idx_time = 0 # from 0 to len(time_split)
        while idx_time < len(time_split[row_cnt-1]) and time_split[row_cnt-1][idx_time] < line[1]:
            idx_time += 1
        lag = (0 if line[4]=='null' else float(line[4]))
        idx_lag = 0 # from 0 to len(lag_split)
        while idx_lag < len(lag_split) and lag_split[idx_lag] < lag:
            idx_lag += 1 
        bias = idx_time * (len(lag_split) + 1) + idx_lag
        bias *= 5

        if line[3]=='navigate':
            row_value[bias]+=1

        if line[3]=='access':
            row_value[bias+1]+=1

        if line[3]=='problem':
            row_value[bias+2]+=1

        if line[3]=='page_close':
            row_value[bias+3]+=1

        if line[3]=='video':
            row_value[bias+4]+=1

    data_sparse = csr_matrix((values, (rows, cols)), shape=(row_cnt, 4500))

    csvfile.close()
    print('%s feature calculate finish' % filename)

    # for i in range(len(data)):
    #     for j in range(46, len(data[i])):
    #         data[i][j] = data[i][j-40] - data[i][j-45]

    return data_sparse


def preProcess():
##enrollment_train:['enrollment_id', 'username', 'course_id']
    file = open('enrollment_train.csv', 'rt')
    file.readline()
    enrollment_train = csv.reader(file)
##    for line in enrollment_train:
##        print(line)
##log_train:['enrollment_id', 'time', 'source', 'event', 'object']
    file = open('log_train.csv', 'rt')
    file.readline()
    log_train = csv.reader(file)
##    for line in log_train:
##       print(line)
##truth_train:[id,0/1]
    truth_train = csv.reader(open('truth_train.csv', 'rt'))
##    for line in truth_train:
##        print(line)
    file = open('enrollment_test.csv', 'rt')
    file.readline()
    enrollment_test = csv.reader(file)
##    for line in enrollment_test:
##        print(line)
    file = open('log_test.csv', 'rt')
    file.readline()
    log_test = csv.reader(file)
##    for line in log_test:
##        print(line)
##cobject:['course_id','module_id','category','children','start']
    file = open('object.csv', 'rt')
    file.readline()
    cobject = csv.reader(file)
##    for line in cobject:
##        print(line)

    data_train = featureProcess('new_log_train.csv')
    data_test = featureProcess('new_log_test.csv')

    mmwrite('tmpTrain', data_train)
    mmwrite('tmpTest', data_test)

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
