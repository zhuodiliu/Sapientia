
import csv
import utilities

def searchTime(table, module):
    course = ''
    for line in table:
        if line[1] == module:
            course = line[0]
        if line[3].find(module)!=-1:
            if line[4]!='null':
                return line[4]
            else:
                return searchTime(table, line[1])
    return 'null'

def objectTime():
    table_old = []
    table_new = []

    csvfile = open('object.csv', 'rt')
    csvfile.readline()
    lines_csv = csv.reader(csvfile)
    for line in lines_csv:
        table_old.append(line)

    for line in table_old:
        module = line[1]
        time = line[4]
        if time == 'null':
            time = searchTime(table_old, module)
        table_new.append([module,time])
        # print([module, time])

    csvfile = open('objectTime_2.csv', 'w', newline='')
    writer = csv.writer(csvfile)
    writer.writerows(table_new)
    csvfile.close()


def logLag(logfile):

    object_time = {}
    log_new = []
    log_new.append(['','','','',''])

    csvfile = open('objectTime.csv', 'rt')
    lines_csv = csv.reader(csvfile)
    for line in lines_csv:
        object_time[line[0]] = line[1]
    csvfile.close()

    csvfile = open(logfile, 'rt')
    csvfile.readline()
    lines_csv = csv.reader(csvfile)

    csvfile_w = open("new_%s_2" % logfile, 'w', newline='')
    writer = csv.writer(csvfile_w)
    writer.writerow(['','','','',''])

    for line in lines_csv:
        if line[4] in object_time:
            if object_time[line[4]] != 'null':
                line[4] = utilities.timeSubtract(line[1], object_time[line[4]])
            else:
                line[4] = 'null'
        else:
            line[4] = 'null'
        writer.writerow(line)
        # log_new.append(line)

    csvfile.close()
    csvfile_w.close()

    

def endTime():
    end_time = [ ['0'] for i in range (200905) ]

    csvfile = open('date.csv', 'rt')
    csvfile.readline()
    date=csv.reader(csvfile)
    datebyid={}
    for line in date:
        datebyid[line[0]]=line[2]


    csvfile = open('enrollment_test.csv', 'rt')
    csvfile.readline()
    log = csv.reader(csvfile)
    for line in log:
        line_idx = int(line[0]) - 1
        end_time[line_idx][0] = datebyid[line[2]]
    csvfile.close()

    csvfile = open('enrollment_train.csv', 'rt')
    csvfile.readline()
    log = csv.reader(csvfile)
    for line in log:
        line_idx = int(line[0]) - 1
        end_time[line_idx][0] = datebyid[line[2]]
    csvfile.close()

    csvfile = open("end_time.csv", 'w', newline='')
    writer = csv.writer(csvfile)
    writer.writerows(end_time)



if __name__ == '__main__':
    # objectTime()
    logLag('log_train.csv')
    logLag('log_test.csv')
    # endTime()