import csv
import numpy as np 

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

def test():
        log(0.808396, 12.0695,[np.pi/2,3*np.pi/4,0,np.pi+.7,np.pi/2 + .38,0,0,0])

test()