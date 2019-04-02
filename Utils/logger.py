import csv 

def log(t0, tf, phis):
    """
    import Utils.logger as logger

    t = trajectory  #do fancy computations 

    logger.log(t.t0, t.tf, t.phases)
    #and your good
    """
    a = [["Log Data"],[t0,tf], phis]
    with open("../solarsys/main/data/log.csv","w+") as my_csv:
        csvWriter = csv.writer(my_csv,delimiter=',')
        csvWriter.writerows(a)

