import csv 

def log(t0, tf, phis):
    a = [["Log Data"],[t0,tf], phis]
    with open("new_file.csv","w+") as my_csv:
        csvWriter = csv.writer(my_csv,delimiter=',')
        csvWriter.writerows(a)

