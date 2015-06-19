import csv
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

    data_train = []
    data_test = []
    
    enroll_id = 0
    line_idx = -1
    for line in log_train:
        if enroll_id != int(line[0]):
            enroll_id = int(line[0])
            data_train.append([0]*6)
            line_idx += 1
            data_train[line_idx][0] = enroll_id

        if line[3]=='navigate':
            data_train[line_idx][1]+=1

        if line[3]=='access':
            data_train[line_idx][2]+=1

        if line[3]=='problem':
            data_train[line_idx][3]+=1

        if line[3]=='page_close':
            data_train[line_idx][4]+=1

        if line[3]=='video':
            data_train[line_idx][5]+=1

    enroll_id = 0
    line_idx = -1
    for line in log_test:
        if enroll_id != int(line[0]):
            enroll_id = int(line[0])
            data_test.append([0]*6)
            line_idx += 1
            data_test[line_idx][0] = enroll_id

        if line[3]=='navigate':
            data_test[line_idx][1]+=1

        if line[3]=='access':
            data_test[line_idx][2]+=1

        if line[3]=='problem':
            data_test[line_idx][3]+=1

        if line[3]=='page_close':
            data_test[line_idx][4]+=1

        if line[3]=='video':
            data_test[line_idx][5]+=1

    csvfile = open('tmpTrain.csv', 'w', newline='')
    writer = csv.writer(csvfile)
    writer.writerows(data_train)
    csvfile = open('tmpTest.csv', 'w', newline='')
    writer = csv.writer(csvfile)
    writer.writerows(data_test)
    csvfile.close()

if __name__ == '__main__':
    preProcess()
