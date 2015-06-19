
import csv

def readCsv(csvName, cols):
    data = []
    file = open(csvName, 'rt')
    lines_csv = csv.reader(file)
    for line in lines_csv:
        item_data = []
        for col in cols:
            item_data.append(int(line[col]))
        if len(cols) == 1:
            item_data = item_data[0]
        data.append(item_data)
    return data

def normalizeResult(result):
    for i in range(len(result)):
        result[i] = result[i][0]
        result[i] = max(result[i], 0)
        result[i] = min(result[i], 1)

def checkError(label, result):
    error = 0
    for i in range(len(label)):
        if label[i] == 1:
            error += result[i]
        else:
            error += 1 - result[i]
    error = 1.0 * error /len(label)
    return error

def outputResult(enroll_list, result, filename):
    csvfile = open(filename, 'w', newline='')
    writer = csv.writer(csvfile)
    for i in range(len(enroll_list)):
        writer.writerow([enroll_list[i], result[i]])
    csvfile.close()

