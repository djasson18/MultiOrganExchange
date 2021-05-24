import patient
import random
#import numpy as np
from random import randrange
from donor import Donor
from patient import Patient


#GLOBAL PARAMETERS FOR GENERATION:
NUM_PATIENTS = 100 #number of patients to generate
CHANCE_KIDNEY = .5 #chance of needing a kidney vs liver
CHANCE_LEFT = .5 #chance of being left lobe (or organ type 1)
LIFETIME_AVG = 365*5 #average lifespan for someone after discovering needed organ
LIFETIME_STDDEV = 365*2 #std dev on lifespan ^
DATE_RANGE = 365 #upper bound on dates to discover needing organ
NUM_ORGANS = 3 # number of uniquely matchable organs
ORGAN_TYPES = 3 # number of compatability types within an organ class
BLOOD_TYPES = 3 # number of blood types

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
def ttc(toDiscover):
    pass
    return 0

# straightforward RSD-type match. Iterates through trying to find bilateral pairs.
def pairedMatch(pdList):
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
                    toMatch.remove(pair1)
                    matched.append(pair1)
                    if pair1 != pair2:
                        toMatch.remove(pair2)
                        matched.append(pair2)

        date += 1

    dead.extend(toMatch)
    #analyze(dead, matched, "Free For All Paired Match")
    print("pairedMatch")
    print("dead:",len(dead))
    print("matched:",len(matched))
    return 0
#Determines whether or not a patient and donor are compatible
def isCompatible(patient, donor):
    patient = str(patient.type)
    donor = str(donor.type)

    # check if organs same
    if patient[0] != donor[0]:
        return False

    # check if organ types same, say odd and even must match
    if (int(patient[1]))%2 != (int(donor[1]))%2:
        return False

    # check if blood types match and each blood type is comparable with numbers lower than it
    if (patient[2] > donor[2]):
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
    print("unpaired_complex")
    print(len(matched))
    print(len(pending_patients))
    print(len(pending_donors))


# generates list of patients according to global parameters up top
def generate():
    patients = []
    donors = []
    sampleList = [True, False]
    pairs = []
    # create patients according to distributions defined by parameters
    for i in range(NUM_PATIENTS):
        patientType = 100*randrange(1,NUM_ORGANS) + 10*randrange(1,ORGAN_TYPES) + randrange(1,BLOOD_TYPES)
        donorType = 100*randrange(1,NUM_ORGANS) + 10*randrange(1,ORGAN_TYPES) + randrange(1,BLOOD_TYPES)
        date = randrange(DATE_RANGE)
        lifetime =  300 ## TODO: change this to randomize lifespan later

        patient = Patient(date, lifetime, patientType, i, False)
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

    toDiscover = generate()
    toDiscover.sort(key = lambda x: x[0].date)
    #print(toDiscover)
    pairedMatch(toDiscover)
    ttc(toDiscover)
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
