"""
Algorithm for online problem
Yunming Hui
29/09/2021
"""
global pt1, pt2, gap  # pt1,2: processing time of dose 1 and 2 gap:fixed time gap
global hospitals

"""
function: arrange
usage: arrange the detail for patient
input:
st: start time of does 1
et: end time of does 1
delay: patient delay
interval: interval of does2
"""


def arrange(st, dt, delay, interval):
    global pt1, pt2, gap, hospitals
    real_st_does1 = 0  # the real start time of does1
    real_st_does2 = 0
    id_hospital_does1 = 0
    st_dose2 = 0  # the start available time of does2
    #  arrange first does
    for i in range(0, len(hospitals)):
        real_st_does1_t, real_st_does2_t, id_hospital_does1_t, st_dose2_t = arrange_hospital1(i, st, dt, delay,
                                                                                              interval)
        if real_st_does1_t == 0:
            continue
        else:
            if real_st_does2_t == 0:
                real_st_does1 = real_st_does1_t
                st_dose2 = st_dose2_t
                id_hospital_does1 = id_hospital_does1_t
            else:
                return
    if real_st_does1 != 0 and real_st_does2 == 0:
        # have hospital for dose1 but no for dose 2
        hospitals[id_hospital_does1 - 1].append([real_st_does1, real_st_does1 + pt1 - 1])
        hospital = [st_dose2, st_dose2 + pt2 - 1]
        hospitals.append([hospital])
        real_st_does2 = st_dose2
        id_hospital_does2 = len(hospitals)
        # print the detail
        print(real_st_does1, id_hospital_does1, real_st_does2, id_hospital_does2)

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


def arrange_hospital1(i, st, dt, delay, interval):
    global pt1, pt2, gap, hospitals
    real_st_does1 = 0  # the real start time of does1
    real_st_does2 = 0
    id_hospital_does1 = 0
    st_dose2 = 0  # the start available time of does2
    res_does1 = hospital_available(i, st, dt, pt1)
    if res_does1[0] == 0:
        return real_st_does1, real_st_does2, id_hospital_does1, st_dose2
    else:
        real_st_does1 = res_does1[1]
        id_hospital_does1 = i + 1
        st_dose2 = res_does1[2] + gap + delay + 1
        real_st_does2, id_hospital_does2 = arrange_hospital2(interval, st_dose2)
        if real_st_does2 != 0:
            hospital = hospitals[i]
            hospital.append([res_does1[1], res_does1[2]])
            # print the detail
            print(real_st_does1, id_hospital_does1, real_st_does2, id_hospital_does2)
            return real_st_does1, real_st_does2, id_hospital_does1, st_dose2
        else:
            if dt - real_st_does1 >= pt1:
                return arrange_hospital1(i, real_st_does1 + 1, dt, delay, interval)
            else:
                return real_st_does1, real_st_does2, id_hospital_does1, st_dose2


def arrange_hospital2(interval, st_dose2):
    real_st_does2 = 0  # the real start time of does2
    id_hospital_does2 = 0
    for i in range(0, len(hospitals)):
        res_does2 = hospital_available(i, st_dose2, st_dose2 + interval - 1, pt2)
        if res_does2[0] == 0:
            continue
        else:
            hospital = hospitals[i]
            hospital.append([res_does2[1], res_does2[2]])
            real_st_does2 = res_does2[1]
            id_hospital_does2 = i + 1
            break
    return real_st_does2, id_hospital_does2


"""
function: read_data
usage: read the data in txt file
"""


def read_data():
    global pt1, pt2, gap, hospitals
    f = open("instance_online_1.txt", "r")
    lines = f.readlines()
    pt1 = int(lines[0])
    pt2 = int(lines[1])
    gap = int(lines[2])
    #  process the first job
    job_data = lines[3].split(",")
    st = int(job_data[0])  # start time of does 1
    delay = int(job_data[2])  # patient delay
    hospital = [[st, st + pt1 - 1], [st + pt1 + gap + delay, st + pt1 + gap + delay + pt2 - 1]]
    hospitals = [hospital]
    print(st, 1, st + pt1 + gap + delay, 1)
    #  process following jobs
    i = 4
    while lines[i] != "X":
        job_data = lines[i].split(",")
        st = int(job_data[0])  # start time of does 1
        et = int(job_data[1])  # end time of does 1
        delay = int(job_data[2])  # patient delay
        interval = int(job_data[3])  # interval of does2
        arrange(st, et, delay, interval)
        i = i + 1


"""
function: hospital_available
usage: judge weather hospital is available
input: i-hospital ID, s-start of available slot, e-end of available slot, pro_time-process time
output: array[a,b,c] a-(1-arrangeable, 0 unarrangeable) b-start time, c-end time
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


if __name__ == '__main__':
    read_data()
    print(len(hospitals))  # print the number of hospitals
