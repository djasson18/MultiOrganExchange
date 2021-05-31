import patient
import random
import numpy as np
from random import randrange
from donor import Donor
from patient import Patient
from collections import deque
import time


#GLOBAL PARAMETERS FOR GENERATION:
NUM_PATIENTS = 100 #number of patients to generate
CHANCE_KIDNEY = .5 #chance of needing a kidney vs liver
CHANCE_LEFT = .5 #chance of being left lobe (or organ type 1)
LIFETIME_AVG = 365*5 #average lifespan for someone after discovering needed organ
LIFETIME_STDDEV = 365*2 #std dev on lifespan ^
DATE_RANGE = 365 #upper bound on dates to discover needing organ
NUM_ORGANS = 3 # number of uniquely matchable organs
ORGAN_TYPES = 4 # number of compatability types within an organ class
BLOOD_TYPES = 4 # number of blood types

#This is for tissue-type compatability
ZERO_PROB, HUN_PROB = .2, .15
UNI_PROB = 1 - ZERO_PROB + HUN_PROB
PRA_PROBS = []
PRA = []

# called by matching algorithm, prints various stats about that algorithm.
def analyze(dead, matched, name):
    deadCount = len(dead)
    matchCount = len(matched)

    matchTime = 0
    for patient in matched:
        matchTime += patient.first.cured
    matchTime /= matchCount

    print("Algorithm " + name)
    print("Number cured: " + matchCount)
    print("Number died: " + deadCount)
    print("Success rate: " + matchCount/(matchCount + deadCount))
    print("Average time for match: " + matchTime)
    print()

    return 0

# top trading cycles. not yet implemented
# toDiscover now: {x, y} {a, b}
# toDiscover want: {x, b} {a, y}
def ttc(toDiscover):
    print("Entering TTC...")
    startTime = time.time()

    q = []
    dead = []
    patients = []
    donors = []
    currIndex = 0
    date = 0
    matched = 0

    for t in range(DATE_RANGE):
        for pair in toDiscover:
            # print(pair)
            # if currIndex == 0:
                # currIndex += 1
                # continue
            # print(currIndex)
            # print((pair[0], currIndex))
            q.append((pair[0], currIndex))
            # print(q)
            patients.append(pair[0])
            donors.append(pair[1])
            currIndex += 1

        for currP in patients:
            if currP.date + currP.lifetime < date:
                dead.append(currP)
                patients.remove(currP)

        # for each patient in queue
        # print(q)
        for pair in q:
            if type(pair) is not tuple:
                break
            # print(pair)
            p = pair[0]
            currDonor = donors[(pair[1] -1)]
            if p.visited or isCompatible(p, currDonor):
                continue
            p.visited = True
            donorIndex = 0
            donor = Donor(113, 0)
            # find a donor match
            for d in donors:
                if isCompatible(pair[0], d):
                    donor = d
                    break
                donorIndex += 1
            # if donor is paired with unvisited patient j
            donorPatient = patients[donorIndex]
            if not donorPatient.visited:
                # move j before i in queue
                q.append(donorPatient)
            # else if donor is paired with visited patient j
            else:
                # patient's partner to become donor
                donors[(pair[1] -1)] = donor
                matched += 1
                # donorPatient partner to become currDonor
                donors[donorIndex] = donors[(pair[1] -1)]
        date += 1

    print("TTC: ")
    print("Time Elapsed", startTime - time.time())
    print("dead:", NUM_PATIENTS - matched)
    print("matched", matched)
    print("---------------")

    return 0

# straightforward RSD-type match. Iterates through trying to find bilateral pairs.
def pairedMatch(pdList):
    print("Entering Paired Match...")
    startTime = time.time()
    # people that currently need kidney
    toDiscover = []
    toDiscover.extend(pdList)
    toMatch = []
    #
    dead = []
    matched = []
    date = 0

    # daily update
    for t in range(DATE_RANGE):
        for pair in toDiscover:
            if (pair[0]).date <= date:
                toMatch.append(pair)
                toDiscover.remove(pair)
        for pair in toMatch:
            if (pair[0]).date + (pair[0]).lifetime < date:
                dead.append(pair)
                toMatch.remove(pair)

        # cycle through pairs of patients trying to find matches
        for pair1 in toMatch:
            for pair2 in toMatch:
                if isCompatible(pair1[0], pair2[1]) and isCompatible(pair2[0], pair1[1]): #if 1 needs 2's kidney
                    pair1[0].cured = date - pair1[0].date
                    pair2[0].cured = date - pair2[0].date
                    if pair1 in toMatch:
                        toMatch.remove(pair1)
                    if pair1 not in matched:
                        matched.append(pair1)
                    if pair1 != pair2:
                        toMatch.remove(pair2)
                        matched.append(pair2)

        date += 1

    dead.extend(toMatch)
    # analyze(dead, matched, "Free For All Paired Match")
    print("Paired Match: ")
    print("Elapsed Time:", startTime - time.time())
    print("dead:",len(dead))
    print("matched:",len(matched))
    print("---------------")
    return 0
# Determines whether or not a patient and donor are compatible
def isCompatible(patient, donor):
    patientString = str(patient.type)
    donorString = str(donor.type)

    # check if organs same
    if patientString[0] != donorString[0]:
        return False

    # check if organ types same, say odd and even must match
    if (int(patientString[1])) != (int(donorString[1])): # took out %2
        return False

    # check if blood types match and each blood type is comparable with numbers lower than it
    if (patientString[2] > donorString[2]):
        return False

    return True



# unpaired_complex
# Parameters: toDiscover, a stack of tuples representing a patient donor pair (p,d)
def unpaired_complex(toDiscover):
    pd_index = 0
    pending_donors = []
    pending_patients = []
    matched = []

    for t in range(DATE_RANGE):
        while(pd_index < len(toDiscover) and toDiscover[pd_index][0].date == t):
            #try to find a donor for toDiscover[pd_index].patient in pending_donors
            patient = toDiscover[pd_index][0]
            isPatientMatched = False
            for donor in pending_donors:
                if isCompatible(patient, donor):
                    pending_donors.remove(donor)
                    isPatientMatched = True
                    matched.append((patient, donor))
                    break
                    #print("Log: ", patient.id, " matched with ", donor.id)
            #if no match, add patient to pending_patients
            if(not isPatientMatched):
                pending_patients.append(patient)

            #try to find a patient for toDiscover[pd_index].donor
            donor = toDiscover[pd_index][1]
            isDonorMatched = False
            for patient in pending_patients:
                if isCompatible(patient, donor):
                    pending_patients.remove(patient)
                    isDonorMatched = True
                    matched.append((patient, donor))
                    break
                    #print("Log: ", patient.id, " matched with ", donor.id)
            #if no match, add patient to pending_patients
            if(not isDonorMatched):
                pending_donors.append(donor)

            pd_index += 1
            #print(pd_index)
    print("Unpaired Complex: ")
    print("Unmatched:",len(pending_patients))
    print("Matched:", len(matched))
    print("---------------")


#Run this only at the beginning
def create_HLA_distribution():
  PRA = [i for i in range(1,100)]
  PRA.append(0); PRA.append(100) #bimodal values

  PRA_PROBS = [UNI_PROB/99 for i in range(1,100)] #uniform probs from PRA: 1-99
  PRA_PROBS.append(ZERO_PROB); PRA_PROBS.append(HUN_PROB) #bimodal probs

# generates list of patients according to global parameters up top
def generate():
    patients = []
    donors = []
    sampleList = [True, False]
    pairs = []
    blood_probs = [.40,.11,.04,.45]
    organProbs = [.78, .11, .11]
    organs = [1,2,3]
    # create patients according to distributions defined by parameters
    for i in range(NUM_PATIENTS):
        #numpy random choice and manually assign mass values
        patientType = 100*np.random.choice(a = organs, size = 1, replace = True, p = organProbs) + 10*randrange(1,ORGAN_TYPES) + randrange(1,BLOOD_TYPES)
        donorType = 100*randrange(1,NUM_ORGANS) + 10*randrange(1,ORGAN_TYPES) + randrange(1,BLOOD_TYPES)
        date = randrange(DATE_RANGE)
        lifetime =  300 ## TODO: change this to randomize lifespan later

        patient = Patient(date, lifetime, patientType, i, False, False)
        donor = Donor(donorType, i)

        patients.append(patient)
        donors.append(donor)
        pairs.append((patient, donor))

    #print("patients:", patients)
    #print("donors:", donors)
    #print("pairs:", pairs)

    return pairs

# generates patients, then runs each match.
def main():
    # date = 0
    print("Running matches: ")
    toDiscover = generate()
    toDiscover.sort(key = lambda x: x[0].date)
    # print(toDiscover)
    pairedMatch(toDiscover)
    #ttc(toDiscover)
    unpaired_complex(toDiscover)
    '''
    toMatch = []
    toDiscover = [] # generated people who don't need a kidney now but will later
    for patient in patients:
        if patient.date <= date:
            toMatch.append(patient)
        else:
            toDiscover.append(patient)
    print("toMatch: ")
    print(toMatch)
    print("toDiscover: ")
    print(toDiscover)
    # pairedMatch(toMatch, toDiscover)
    # ttc(toMatch, toDiscover)
    # nft(toMatch, toDiscover)
    '''

if __name__ == "__main__":
    main()
