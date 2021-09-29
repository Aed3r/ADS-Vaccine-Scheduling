# _*_ coding:utf8 _*_
from pulp import *


def offlineDataRead():
    data = []
    with open('offline_instance.txt', 'r') as f:
        for i in range(0,4):
            data.append(int(f.readline()))
        for i in range(0,data[3]):
            data.append(list(map(int,f.readline().split(","))))
    return data

def offlineSolveByPulp(data):
    #1. create a LP object, find the minimize value
    problem = LpProblem("ADSOfflineProject",sense=LpMinimize)

    #2. decide variables, hospital number 'n', for each patient first dose start time "dt1",
    #first dose start hospital "dh1", for each patient second dose start time "dt2",second dose start hospital "dh2",
    #so, there are 4n+1 variables totally
    HospitalNum = LpVariable(name="HospitalNum", lowBound=0, cat="Integer")
    PatientsVariablesList = []
    ValueName = ["FirstStartTime", "FirstHospital", "SecondStartTime", "SecondHospital"]
    for i in range(0,data[3]):
        PatientsVariablesList.append(LpVariable.dict("Patient"+str(i), ValueName, lowBound=0, cat="Integer" ))

    #3. Add Objective Function
    problem += HospitalNum*1.0

    #4. Add Constrains
    #for every patient
    for i in range(0,data[3]):
        # the describtion about data see the instanceCreate.py
        problem += PatientsVariablesList[i]["FirstStartTime"] >= data[4+i][0]#first_dose_interval_start
        problem += PatientsVariablesList[i]["FirstStartTime"] <= (data[4 + i][1] - data[0]+1) #first_dose_interval_end - dose1processTime
        # FirstDoseStartTime + dose1processTime + gap +delay
        problem += PatientsVariablesList[i]["SecondStartTime"] >= (PatientsVariablesList[i]["FirstStartTime"]+data[0]+data[2]+data[4+i][2])
        # FirstDoseStartTime + dose1processTime + gap +delay + second_dose_interval_length - dose2processTime
        problem += PatientsVariablesList[i]["SecondStartTime"] <= (PatientsVariablesList[i]["FirstStartTime"]+data[0]+data[2]+data[4+i][2]+data[4+i][3]-data[1])
        # FirstHospital and SecondHospital <= HospitalNum
        problem += PatientsVariablesList[i]["FirstHospital"] <= HospitalNum
        problem += PatientsVariablesList[i]["SecondHospital"] <= HospitalNum
    #the constraints between two patients
    M = 1000000
    AdditionalVariablesList = {} #variables used to create constrains
    AdditionalValueName = ["y1", "y2", "y3", "y4"]
    for i in range(0,data[3]-1):
        for j in range(i+1,data[3]):
            # [(patient_2 dose end time >= patient_1 dose start time) and (patient_2 dose start time <= patient_1 dose end time)] or (patient_2 dose hopsital != patient_1 dose hopsital)
            AdditionalVariablesList[str(i) + "_" + str(j)] = {}
            #i_dose1 and j_dose1
            #judge if two interval overlap
            if (data[i+4][1]>=data[j+4][0]) and (data[j+4][1]>=data[i+4][0]):
                AdditionalVariablesList[str(i) + "_" + str(j)]["11"] = LpVariable.dict("Additional_" + str(i) + "_" + str(j) + "_11", AdditionalValueName, lowBound=0, upBound=1,cat="Integer")
                #y1+y2+y3+y4>=1
                problem += AdditionalVariablesList[str(i)+"_"+str(j)]["11"]["y1"]+AdditionalVariablesList[str(i)+"_"+str(j)]["11"]["y2"]+AdditionalVariablesList[str(i)+"_"+str(j)]["11"]["y3"]+AdditionalVariablesList[str(i)+"_"+str(j)]["11"]["y4"] >=1
                #(is-je >0) or (js-ie >0) or (ih-jh >0) or (jh-ih >0)
                problem += (PatientsVariablesList[i]["FirstStartTime"] - PatientsVariablesList[j]["FirstStartTime"] -data[0]+1) >= 1.0+((-1.0)*M*(1.0-AdditionalVariablesList[str(i)+"_"+str(j)]["11"]["y1"]))
                problem += (PatientsVariablesList[j]["FirstStartTime"] - PatientsVariablesList[i]["FirstStartTime"] - data[0]+1) >= 1.0+((-1.0) * M * (1.0 - AdditionalVariablesList[str(i) + "_" + str(j)]["11"]["y2"]))
                problem += (PatientsVariablesList[i]["FirstHospital"] - PatientsVariablesList[j]["FirstHospital"]) >= 1.0+((-1.0) * M * (1.0 - AdditionalVariablesList[str(i) + "_" + str(j)]["11"]["y3"]))
                problem += (PatientsVariablesList[j]["FirstHospital"] - PatientsVariablesList[i]["FirstHospital"]) >= 1.0+((-1.0) * M * (1.0 - AdditionalVariablesList[str(i) + "_" + str(j)]["11"]["y4"]))
            #i_dose2 and j_dose1
            # judge if two interval overlap
            if ((data[i+4][1]+data[2]+data[i+4][2]+data[i+4][3]) >= data[j+4][0]) and (data[j+4][1] >= (data[i+4][0]+data[0]+data[2]+data[i+4][2])):
                AdditionalVariablesList[str(i) + "_" + str(j)]["21"] = LpVariable.dict("Additional_" + str(i) + "_" + str(j)+"_21", AdditionalValueName,lowBound=0,upBound=1, cat="Integer")
                # y1+y2+y3+y4>=1
                problem += AdditionalVariablesList[str(i) + "_" + str(j)]["21"]["y1"] + AdditionalVariablesList[str(i) + "_" + str(j)]["21"]["y2"] + AdditionalVariablesList[str(i) + "_" + str(j)]["21"]["y3"] + AdditionalVariablesList[str(i) + "_" + str(j)]["21"]["y4"] >= 1
                # (is-je >0) or (js-ie >0) or (ih-jh >0) or (jh-ih >0)
                problem += (PatientsVariablesList[i]["SecondStartTime"] - PatientsVariablesList[j]["FirstStartTime"] - data[0]+1) >= 1.0+((-1.0) * M * (1.0 - AdditionalVariablesList[str(i) + "_" + str(j)]["21"]["y1"]))
                problem += (PatientsVariablesList[j]["FirstStartTime"] - PatientsVariablesList[i]["SecondStartTime"] - data[1]+1) >= 1.0+((-1.0) * M * (1.0 - AdditionalVariablesList[str(i) + "_" + str(j)]["21"]["y2"]))
                problem += (PatientsVariablesList[i]["SecondHospital"] - PatientsVariablesList[j]["FirstHospital"]) >= 1.0+((-1.0) * M * (1.0 - AdditionalVariablesList[str(i) + "_" + str(j)]["21"]["y3"]))
                problem += (PatientsVariablesList[j]["FirstHospital"] - PatientsVariablesList[i]["SecondHospital"]) >= 1.0+((-1.0) * M * (1.0 - AdditionalVariablesList[str(i) + "_" + str(j)]["21"]["y4"]))
            #i_dose2 and j_dose2
            # judge if two interval overlap
            if ((data[i+4][1]+data[2]+data[i+4][2]+data[i+4][3]) >= (data[j+4][0]+data[0]+data[2]+data[j+4][2])) and ((data[j+4][1]+data[2]+data[j+4][2]+data[j+4][3]) >= (data[i+4][0]+data[0]+data[2]+data[i + 4][2])):
                AdditionalVariablesList[str(i) + "_" + str(j)]["22"] = LpVariable.dict("Additional_" + str(i) + "_" + str(j)+"_22", AdditionalValueName,lowBound=0,upBound=1, cat="Integer")
                # y1+y2+y3+y4>=1
                problem += AdditionalVariablesList[str(i) + "_" + str(j)]["22"]["y1"] + AdditionalVariablesList[str(i) + "_" + str(j)]["22"]["y2"] + AdditionalVariablesList[str(i) + "_" + str(j)]["22"]["y3"] + AdditionalVariablesList[str(i) + "_" + str(j)]["22"]["y4"] >= 1
                # (is-je >0) or (js-ie >0) or (ih-jh >0) or (jh-ih >0)
                problem += (PatientsVariablesList[i]["SecondStartTime"] - PatientsVariablesList[j]["SecondStartTime"] - data[1]+1) >= 1.0+((-1.0) * M * (1.0 - AdditionalVariablesList[str(i) + "_" + str(j)]["22"]["y1"]))
                problem += (PatientsVariablesList[j]["SecondStartTime"] - PatientsVariablesList[i]["SecondStartTime"] - data[1]+1) >= 1.0+((-1.0) * M * (1.0 - AdditionalVariablesList[str(i) + "_" + str(j)]["22"]["y2"]))
                problem += (PatientsVariablesList[i]["SecondHospital"] - PatientsVariablesList[j]["SecondHospital"]) >= 1.0+((-1.0) * M * (1.0 - AdditionalVariablesList[str(i) + "_" + str(j)]["22"]["y3"]))
                problem += (PatientsVariablesList[j]["SecondHospital"] - PatientsVariablesList[i]["SecondHospital"]) >= 1.0+((-1.0) * M * (1.0 - AdditionalVariablesList[str(i) + "_" + str(j)]["22"]["y4"]))
            # i_dose1 and j_dose2
            # judge if two interval overlap
            if (data[i+4][1] >= (data[j+4][0]+data[0]+data[2]+data[j+4][2])) and ((data[j+4][1]+data[2]+data[j+4][2]+data[j+4][3]) >= data[i+4][0]):
                AdditionalVariablesList[str(i) + "_" + str(j)]["12"] = LpVariable.dict("Additional_" + str(i) + "_" + str(j) + "_12", AdditionalValueName,lowBound=0,upBound=1, cat="Integer")
                # y1+y2+y3+y4>=1
                problem += AdditionalVariablesList[str(i) + "_" + str(j)]["12"]["y1"] + AdditionalVariablesList[str(i) + "_" + str(j)]["12"]["y2"] + AdditionalVariablesList[str(i) + "_" + str(j)]["12"]["y3"] + AdditionalVariablesList[str(i) + "_" + str(j)]["12"]["y4"] >= 1
                # (is-je >0) or (js-ie >0) or (ih-jh >0) or (jh-ih >0)
                problem += (PatientsVariablesList[i]["FirstStartTime"] - PatientsVariablesList[j]["SecondStartTime"] -data[1]+1) >= 1.0+((-1.0) * M * (1.0 - AdditionalVariablesList[str(i) + "_" + str(j)]["12"]["y1"]))
                problem += (PatientsVariablesList[j]["SecondStartTime"] - PatientsVariablesList[i]["FirstStartTime"] -data[0]+1) >= 1.0+((-1.0) * M * (1.0 - AdditionalVariablesList[str(i) + "_" + str(j)]["12"]["y2"]))
                problem += (PatientsVariablesList[i]["FirstHospital"] - PatientsVariablesList[j]["SecondHospital"]) >= 1.0+((-1.0) * M * (1.0 - AdditionalVariablesList[str(i) + "_" + str(j)]["12"]["y3"]))
                problem += (PatientsVariablesList[j]["SecondHospital"] - PatientsVariablesList[i]["FirstHospital"]) >= 1.0+((-1.0) * M * (1.0 - AdditionalVariablesList[str(i) + "_" + str(j)]["12"]["y4"]))
    #5. solve
    problem.solve()
    #6. result
    resultdata = []
    hospialnum = 0
    tempFirstHospital = 0
    tempFirstStartTime = 0
    tempSecondHospital = 0
    tempSecondStartTime = 0
    for v in problem.variables():
        print(str(v.name) + ":"+str(v.value()))
        if v.name == "HospitalNum":
            hospialnum = v.value() + 1
        elif "FirstHospital" in v.name:
            tempFirstHospital = v.value()+1
        elif "FirstStartTime" in v.name:
            tempFirstStartTime = v.value()
        elif "SecondHospital" in v.name:
            tempSecondHospital = v.value()+1
        elif "SecondStartTime" in v.name:
            tempSecondStartTime = v.value()
            resultdata.append([str(int(tempFirstStartTime)), str(int(tempFirstHospital)), str(int(tempSecondStartTime)), str(int(tempSecondHospital))])
    resultdata.append(int(hospialnum))
    return resultdata

def resultShow(resultdata):
    with open('offline_result.txt', 'w') as f:
        for item in resultdata:
            if isinstance(item, list):
                f.write(",".join(item) + "\n")
            else:
                f.write(str(item) + "\n")
    return None

if __name__=="__main__":
    data = offlineDataRead()
    result = offlineSolveByPulp(data)
    resultShow(result)