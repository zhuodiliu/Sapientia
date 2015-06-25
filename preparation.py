
import csv
import utilities

def searchTimeCs(table, course):
    for line in table:
        if line[0] == course and line[4]!='null':
            return line[4]
    return 'null'

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
    return searchTimeCs(table, course)

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

    csvfile = open('objectTime.csv', 'w', newline='')
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

    csvfile = open(logfile, 'rt')
    csvfile.readline()
    lines_csv = csv.reader(csvfile)
    for line in lines_csv:
        if line[4] in object_time:
            line[4] = utilities.timeSubtract(line[1], object_time[line[4]])
        else:
            line[4] = 'null'
        log_new.append(line)
    csvfile.close()
    
    csvfile = open("new_%s" % logfile, 'w', newline='')
    writer = csv.writer(csvfile)
    writer.writerows(log_new)
    csvfile.close()

def lastLog():
    last_log = [ ['0'] for i in range (200905) ]
    csvfile = open('log_Train.csv', 'rt')
    csvfile.readline()
    log = csv.reader(csvfile)
    for line in log:
        line_idx = int(line[0]) - 1
        last_log[line_idx][0] = max(last_log[line_idx][0], line[1])
    csvfile.close()

    csvfile = open('log_Test.csv', 'rt')
    csvfile.readline()
    log = csv.reader(csvfile)
    for line in log:
        line_idx = int(line[0]) - 1
        last_log[line_idx][0] = max(last_log[line_idx][0], line[1])
    csvfile.close()

    csvfile = open("last_log.csv", 'w', newline='')
    writer = csv.writer(csvfile)
    writer.writerows(last_log)



if __name__ == '__main__':
    # objectTime()
    # logLag('log_train.csv')
    # logLag('log_test.csv')
    lastLog()