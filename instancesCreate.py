# _*_ coding:utf8 _*_

import random
import numpy as np

"""
this py file is used to create instances for project
"""

"""
the parameters is integer and greater or equal to 0
for every patients, 
the start time of first feasible interval between [1,patientsnum/2], use normal distribution
the length of FFI is equal or greater than first_dose, FI = first_dose +random(0,3*first_dose)
the patient delay time is randomn(0,6*first_dose),use normal distribution
the length of second feasible interval is equal or greater than second_dose, FI = random(second_dose,3*second_dose),
use normal distribution
"""
def normalInstance(first_dose, second_dose, gap, patientsnum):
    offlinedata = []
    onlinedata = []
    offlinedata.append(str(first_dose)), offlinedata.append(str(second_dose)), offlinedata.append(str(gap)), offlinedata.append(str(patientsnum))
    onlinedata.append(str(first_dose)), onlinedata.append(str(second_dose)), onlinedata.append(str(gap))
    for i in range(0,patientsnum):
        first_dose_interval_start = np.absolute(np.rint(np.random.normal(0.25*patientsnum,0.1*patientsnum,1)))[0]+1
        first_dose_interval_end = first_dose_interval_start + first_dose + random.randint(0,3*first_dose)
        delay = np.absolute(np.rint(np.random.normal(3*first_dose,3,1)))[0]
        second_dose_interval_length = np.absolute(np.rint(np.random.normal(second_dose,2,1)))[0]+second_dose
        offlinedata.append([str(int(first_dose_interval_start)), str(int(first_dose_interval_end)), str(int(delay)), str(int(second_dose_interval_length))])
    for i in range(0,patientsnum):
        first_dose_interval_start = np.absolute(np.rint(np.random.normal(0.25*patientsnum,1,1)))[0]+1
        first_dose_interval_end = first_dose_interval_start + first_dose + random.randint(0,3*first_dose)
        delay = np.absolute(np.rint(np.random.normal(3*first_dose,3,1)))[0]
        second_dose_interval_length = np.absolute(np.rint(np.random.normal(second_dose,2,1)))[0]+second_dose
        onlinedata.append([str(int(first_dose_interval_start)), str(int(first_dose_interval_end)), str(int(delay)), str(int(second_dose_interval_length))])
    onlinedata.append("x")
    return [offlinedata, onlinedata]


def writeToDocument(dataList):
    with open('offine_instance.txt', 'w') as f:
        for i in dataList[0]:
            if isinstance(i,list):
                f.write(",".join(i) + "\n")
            else:
                f.write(i + "\n")
    with open('onine_instance.txt', 'w') as f:
        for i in dataList[1]:
            if isinstance(i, list):
                f.write(",".join(i) + "\n")
            else:
                f.write(i + "\n")

if __name__=="__main__":
    writeToDocument(normalInstance(2, 2, 5, 100))


