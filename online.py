global pt1, pt2, gap  # pt1,2: processing time of dose 1 and 2 gap:fixed time gap
global hospitals  # a set of existing hospitals

"""
function name:
    arrange
arguments names and types:
    st: start time of feasible interval
    dt: end time of feasible interval
    delay: patient-dependent delay
    interval: the length of the second feasible interval 
description:
    arrange each patient
"""


def arrange(st, dt, delay, interval):
    global pt1, pt2, gap, hospitals
    real_st_does1 = 0  # the real start time of does1
    real_st_does2 = 0  # the real start time of does2
    id_hospital_does1 = 0
    st_dose2 = 0  # the start available time of does2
    dose1_is_arranged = 0
    #  arrange first does
    for i in range(0, len(hospitals)):
        real_st_does1_t, real_st_does2_t, id_hospital_does1_t, st_dose2_t = arrange_hospital1(i, st, dt, delay,
                                                                                              interval)
        if real_st_does1_t == 0:
            continue
        else:
            if real_st_does2_t == 0:
                if dose1_is_arranged == 0:
                    real_st_does1 = real_st_does1_t
                    st_dose2 = st_dose2_t
                    id_hospital_does1 = id_hospital_does1_t
                    dose1_is_arranged = 1
            else:
                return
    #  first dose can be arranged but no hospital for the second dose
    if real_st_does1 != 0 and real_st_does2 == 0:
        # have hospital for dose1 but no for dose 2
        hospitals[id_hospital_does1 - 1].append([real_st_does1, real_st_does1 + pt1 - 1])
        hospital = [st_dose2, st_dose2 + pt2 - 1]
        hospitals.append([hospital])
        real_st_does2 = st_dose2
        id_hospital_does2 = len(hospitals)
        # print the detail
        print(real_st_does1, id_hospital_does1, real_st_does2, id_hospital_does2)
    #  no hospital for the first dose
    if real_st_does1 == 0:
        # no hospital for does1, create new hospital
        hospital = [st, st + pt1 - 1]
        hospitals.append([hospital])
        real_st_does1 = st
        id_hospital_does1 = len(hospitals)
        st_dose2 = st + pt1 + gap + delay
        #  arrange second does
        real_st_does2, id_hospital_does2 = arrange_hospital2(interval, st_dose2)
        if real_st_does2 == 0:
            # no hospital for does2, create new hospital
            hospital = [st_dose2, st_dose2 + pt2 - 1]
            hospitals.append([hospital])
            real_st_does2 = st_dose2
            id_hospital_does2 = len(hospitals)
        # print the detail
        print(real_st_does1, id_hospital_does1, real_st_does2, id_hospital_does2)


"""
function name:
    arrange_hospital1
arguments names and types:
    i: the hospital id
    st: start time of feasible interval
    dt: end time of feasible interval
    delay: patient-dependent delay
    interval: the length of the second feasible interval 
function return:
    real_st_does1: real start time of dose1
    real_st_does2: real start time of dose2 (0 means no available hospital for dose 2)
    id_hospital_does1: the id of hospital where first dose is arranged
    st_dose2: possible start time of dose2
description:
    check weather one patient can be arranged choosing hospital i as the first dose hospital
"""


def arrange_hospital1(i, st, dt, delay, interval):
    global pt1, pt2, gap, hospitals
    real_st_does1 = 0  # the real start time of does1
    real_st_does2 = 0
    id_hospital_does1 = 0
    st_dose2 = 0  # the start available time of does2
    res_does1 = hospital_available(i, st, dt, pt1)
    if res_does1[0] == 0:
        #  no hospital for the first dose
        return real_st_does1, real_st_does2, id_hospital_does1, st_dose2
    else:
        #  there is available hospital for dose1, arrange the dose2
        real_st_does1 = res_does1[1]
        id_hospital_does1 = i + 1
        st_dose2 = res_does1[2] + gap + delay + 1
        real_st_does2, id_hospital_does2 = arrange_hospital2(interval, st_dose2)
        if real_st_does2 != 0:
            #  no hospital for does2, check other possible interval of dose1
            hospital = hospitals[i]
            hospital.append([res_does1[1], res_does1[2]])
            # print the detail
            print(real_st_does1, id_hospital_does1, real_st_does2, id_hospital_does2)
            return real_st_does1, real_st_does2, id_hospital_does1, st_dose2
        else:
            #  both dose1 and dose2 can be arranged, return the result
            if dt - real_st_does1 >= pt1:
                res = arrange_hospital1(i, real_st_does1 + 1, dt, delay, interval)
                if res[1] == 0:
                    return real_st_does1, real_st_does2, id_hospital_does1, st_dose2
                else:
                    return res
            else:
                return real_st_does1, real_st_does2, id_hospital_does1, st_dose2


"""
function name:
    arrange_hospital2
arguments names and types:
    interval: the length of the second feasible interval
    st_dose2: start time of second feasible interval
function return:
    real_st_does2: the real start time of dose2
    id_hospital_does2: id of hospital where dose is arranged
description:
    check weather the second dose of one patient can be arranged among existing hospitals
"""


def arrange_hospital2(interval, st_dose2):
    real_st_does2 = 0  # the real start time of does2
    id_hospital_does2 = 0
    for i in range(0, len(hospitals)):
        res_does2 = hospital_available(i, st_dose2, st_dose2 + interval - 1, pt2)
        if res_does2[0] == 0:
            #  dose2 cannot be arranged
            continue
        else:
            #  available interval for dose2
            hospital = hospitals[i]
            hospital.append([res_does2[1], res_does2[2]])
            real_st_does2 = res_does2[1]
            id_hospital_does2 = i + 1
            break
    return real_st_does2, id_hospital_does2


"""
function name:
    hospital_available
arguments names and types:
    i: hospital id 
    s: start time of the feasible hospital
    e: end time of the feasible hospital
    pro_time: processing time of the dose
function return:
    first: 1-can be arranged 0-cannot arrange
    second: real start time of the dose
    third: real end time of the dose 
description:
    check weather one dose with a feasible interval[s,e] can be arranged among existing hospitals
"""


def hospital_available(i, s, e, pro_time):
    global hospitals
    hospital = hospitals[i]
    hospital.sort()
    #  process the slot before first occupied slot
    if hospital[0][0] - 1 >= pro_time:
        temp_slot = [1, hospital[0][0] - 1]
        if s + pro_time - 1 <= temp_slot[1]:
            return [1, s, s + pro_time - 1]
    #  process the slot between every two occupied slots
    for k in range(0, len(hospital) - 1):
        temp_slot = [hospital[k][1] + 1, hospital[k + 1][0] - 1]
        if temp_slot[1] - temp_slot[0] + 1 >= pro_time:
            for m in range(temp_slot[0], temp_slot[1] + 1):
                if m >= s and m + pro_time - 1 <= e:
                    if m + pro_time - 1 <= temp_slot[1]:
                        return [1, m, m + pro_time - 1]
    #  process the slot after last occupied slot
    last_time = hospital[len(hospital) - 1][1]
    if last_time + 1 >= s and last_time + pro_time <= e:
        return [1, last_time + 1, last_time + pro_time]
    if s >= last_time + 1:
        return [1, s, s + pro_time - 1]
    return [0, 0, 0]


"""
function name:
    read_data
arguments names and types:
    file_name: the name of the file to be read
description:
    read the data of p1,p2,gap and the information of each job
"""


def read_data(file_name):
    global pt1, pt2, gap, hospitals
    f = open(file_name, "r")
    lines = f.readlines()
    pt1 = int(lines[0])
    pt2 = int(lines[1])
    gap = int(lines[2])
    hospitals = []
    if lines[3] == "x":
        return
    #  process the first job
    job_data = lines[3].split(",")
    st = int(job_data[0])  # start time of does 1
    delay = int(job_data[2])  # patient delay
    hospital = [[st, st + pt1 - 1], [st + pt1 + gap + delay, st + pt1 + gap + delay + pt2 - 1]]
    hospitals = [hospital]
    print(st, 1, st + pt1 + gap + delay, 1)
    #  process following jobs
    i = 4
    while lines[i][0] != 'x':
        job_data = lines[i].split(",")
        st = int(job_data[0])  # start time of does 1
        et = int(job_data[1])  # end time of does 1
        delay = int(job_data[2])  # patient delay
        interval = int(job_data[3])  # interval of does2
        arrange(st, et, delay, interval)
        i = i + 1


if __name__ == '__main__':
    read_data("./Provided test instances/50000.txt")
    print(len(hospitals))  # print the number of hospitals
