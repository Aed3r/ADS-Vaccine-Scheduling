"""
Just a simple greedy online algorithm. 
The program assumes nothing is wrong with the data.
Author: Gustav Hubert
"""


# --- Initialisation --- #


# Imports
import os

# Globals
i = 0 # Patient number. Corresponds to line i+3 in the lines of the file
hospitals = [] # List of list corresponding to each hospitals schedule
patients = 0 # Counts the amount of patients 
separator = ',' # Separator used in the input file
paddingChar = '_' # Character used for padding when printing to the terminal
inputFileName = "5-2.txt" # Input file name in the Instances folder. Can be set to ""
outputFileName = "output.txt" # Output file name. Set to "" for no output 
printInTerminal = False # Whether or not to print information in the terminal

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
    open(os.path.join("Outputs", outputFileName), 'w').close() # Clear the file before use
    outputFile = open(os.path.join("Outputs", outputFileName), 'a')

# Extracted global parameters
p1 = int(lines[0]) # Processing time of the first dose
if printInTerminal:
    print("Processing time p1: " + str(p1))
p2 = int(lines[1]) # Processing time of the second dose
if printInTerminal:
    print("Processing time p2: " + str(p2))
g = int(lines[2]) # Minimum gap between first and second dose
if printInTerminal:
    print("Gap g: " + str(g))


# --- Useful functions --- #


# Searches the soonest available timeslot of length p in the timeslot [ri, di] and schedules it for patient i.
# If no hospital is available a new one is created.
# Returns the beginning of the scheduled slot ti as well as the chosen hospital's number
def findSchedule (ri, di, p):
    global i, hospitals
    c = 0 # Counts the hospitals

    # Find first available schedule for patient i by going through all existing hospitals
    for h in hospitals:
        # Check availability for the first dose in the current hospital
        for j in range(ri, di-p+2):
            found = True
            for k in range(j, j+p):
                if len(h) > k and h[k] != -1:
                    found = False
                    break
            if found:
                # Add hospital availability if there is some missing
                h += [-1] * (j+p-len(h))

                # Found an available schedule
                for k in range(j, j+p):
                    h[k] = i
                return (j, c)
        c += 1
        
    # If we didn't find an available hospital in [ri, di] we create a new one and schedule [ri, ri+p]
    hospitals += [[-1]*(ri) + [i]*p]
    return (ri, len(hospitals)-1)

# Pretty prints all schedules in the terminal. Each line represents one hospital
def printSchedules ():
    global paddingChar, patients
    # We find the length of the longest number to print in order to correctly pad
    longest = max(len(str(patients)), len(str(len(hospitals))))

    c = 1
    for h in hospitals:
        print(str(c).rjust(longest, ' ') + '.', end=' ')
        c += 1
        for schedule in h:
            if schedule == -1:
                print(paddingChar.rjust(longest, paddingChar), end=' ')
            else:
                print(str(schedule).rjust(longest, paddingChar), end=' ')
        print('') # Newline

    print("Total number of patients: " + str(patients))
    print("Total number of hospitals: " + str(len(hospitals)))

# Add the patient to the output file f as defined in the assignment sheet :
# ti1/ti2: starting time of the first/second dose
# mi1/mi2: hospital of the first/second dose
def outputToFile (f, ti1, mi1, ti2, mi2):
    global outputFile

    if f != None:
        f.write(separator.join([str(ti1), str(mi1+1), str(ti2), str(mi2+1)]) + "\n")


# --- Main loop --- #


while (lines[i+3].strip() != "x" and lines[i+3].strip() != "X"):
    # Get data on patient i
    patientData = lines[i+3].split(separator)
    ri = int(patientData[0]) # First available time slot of the first dose
    di = int(patientData[1]) # Last available time slot of the first dose
    xi = int(patientData[2]) # Patient-dependent delay between the first and the second dose
    li = int(patientData[3]) # Length of the second dose feasible interval
    patients += 1

    # Schedule first dose
    # ti1 is the time of the first dose for patient i
    # mi1 is the hospital for the first dose of patient i
    ti1, mi1 = findSchedule(ri, di, p1)

    # Schedule second dose
    # ti2 is the time of the second dose for patient i
    # mi2 is the hospital for the second dose of patient i
    ti2, mi2 = findSchedule(ti1+p1+g+xi, ti1+p1+g+xi+li, p2)

    # Write to output file
    outputToFile(outputFile, ti1, mi1, ti2, mi2)

    i += 1

# --- Finalization --- #

if printInTerminal:
    printSchedules()

# Add the minimum number of hospitals needed at the end of the output file
if outputFile:
    outputFile.write(str(len(hospitals)))
    outputFile.close()