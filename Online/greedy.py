"""
Just a simple greedy online algorithm. The program assumes nothing is wrong with the data.
"""


# --- Initialisation --- #


# Imports
import os

# Globals
i = 0 # Patient number. Corresponds to line i+3 in the lines of the file
hospitals = [] # List of list corresponding to each hospitals schedule
separator = '\t' # Separator used in the input file
paddingChar = '_' # Character used for padding when printing to the terminal
inputFileName = "instance_online_1.txt" # Input file name in the Instances folder. Can be set to ""
outputFileName = "output_1.txt" # Output file name. Set to "" for no output 

# Ask for file name if not defined beforehand
if inputFileName == "":
    inputFileName = input()

# Read all input file lines
lines = []
with open(os.path.join("Instances", inputFileName), 'r') as inputFile:
    lines = inputFile.read().splitlines()

# Open output file
outputFile = None
if outputFileName != "":
    open(outputFileName, 'w').close() # Clear the file before use
    outputFile = open(os.path.join("Outputs", outputFileName), 'a')

# Extracted global parameters
p1 = int(lines[0]) # Processing time of the first dose
print("Processing time p1: " + str(p1))
p2 = int(lines[1]) # Processing time of the second dose
print("Processing time p2: " + str(p2))
g = int(lines[2]) # Minimum gap between first and second dose
print("Gap g: " + str(g))


# --- Useful functions --- #


# Searches the soonest available timeslot of length p in the timeslot [ri, di] and schedules it for patient i.
# If no hospital is available a new one is created.
# Returns the beginning of the scheduled slot ti
def findSchedule (ri, di, p):
    global i, hospitals
    found = False
    c = 0 # Counts the hospitals

    # Find first available schedule for patient i by going through all existing hospitals
    for h in hospitals:
        # Add hospital availability if there is some missing
        if (len(h) < di):
            h += [-1] * (di+1-len(h))

        # Check availability for the first dose in the current hospital
        for j in range(ri, di-p):
            if h[j] == -1 and h[j+p-1] == -1:
                # Found an available schedule
                found = True
                for k in range(j, j+p):
                    h[k] = i
                return (j, c)
        c += 1
        
    # If we didn't find an available hospital in [ri, di] we create a new one and schedule [ri-1, ri+p]
    if not found:
        hospitals += [[-1]*(ri-1) + [i]*p]
        return (ri-1, len(hospitals)-1)

# Pretty prints all schedules in the terminal. Each line represents one hospital
def printSchedules ():
    global paddingChar
    # We find the length of the longest number to print in order to correctly pad
    longest = len(str(len(lines)-3))

    for h in hospitals:
        for schedule in h:
            if schedule == -1:
                print(paddingChar.rjust(longest, paddingChar), end=' ')
            else:
                print(str(schedule).rjust(longest, paddingChar), end=' ')
        print('') # Newline

    print("Total number of patients: " + str(len(lines)-3))
    print("Total number of hospitals: " + str(len(hospitals)))

# Add the patient to the output file f as defined in the assignment sheet :
# ti1/ti2: starting time of the first/second dose
# mi1/mi2: hospital of the first/second dose
def outputToFile (f, ti1, mi1, ti2, mi2):
    global outputFile

    if f != None:
        f.write(separator.join([str(ti1), str(mi1), str(ti2), str(mi2)]) + "\n")


# --- Main loop --- #


while (lines[i+3].strip() != "X"):
    # Get data on patient i
    patientData = lines[i+3].split(separator)
    ri = int(patientData[0]) # First available time slot of the first dose
    di = int(patientData[1]) # Last available time slot of the first dose
    xi = int(patientData[2]) # Patient-dependent delay between the first and the second dose
    li = int(patientData[3]) # Length of the second dose feasible interval

    # Schedule first dose
    ti1, mi1 = findSchedule(ri, di, p1)

    # Schedule second dose
    ti2, mi2 = findSchedule(ti1+p1+g+xi, ti1+p1+g+xi+li, p2)

    # Write to output file
    outputToFile(outputFile, ti1, mi1, ti2, mi2)

    i += 1

# --- Finalization --- #

printSchedules()

# Add the minimum number of hospitals needed add the end of the output file
if outputFile:
    outputFile.write(str(len(hospitals)))
    outputFile.close()