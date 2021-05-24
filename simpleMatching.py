import patient
import organ
import random
#import numpy as np
from random import randrange
from organ import Organ
from donor import Donor
from patient import Patient


#GLOBAL PARAMETERS FOR GENERATION:
NUM_PATIENTS = 2 #number of patients to generate
CHANCE_KIDNEY = .5 #chance of needing a kidney vs liver
CHANCE_LEFT = .5 #chance of being left lobe (or organ type 1)
LIFETIME_AVG = 365*5 #average lifespan for someone after discovering needed organ
LIFETIME_STDDEV = 365*2 #std dev on lifespan ^
DATE_RANGE = 365 #upper bound on dates to discover needing organ
NUM_ORGANS = 8 # number of uniquely matchable organs
ORGAN_TYPES = 2
BLOOD_TYPES = 4

# called by matching algorithm, prints various stats about that algorithm.
def analyze(dead, matched, name):
    deadCount = dead.size
    matchCount = matched.size

    matchTime = 0
    for patient in matched:
        matchTime += patient.cured
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
def pairedMatch(toDiscover):
    # people that currently need kidney
    toMatch = []
    #
    dead = []
    matched = []
    date = 0

    # daily update
    while(len(toDiscover) != 0):
        for patient in toDiscover:
            if patient.date <= date:
                toMatch.append(patient)
                toDiscover.remove(patient)
        for patient in toMatch:
            if patient.date + patient.age > date:
                dead.append(patient)
                toMatch.remove(patient)

        # cycle through pairs of patients trying to find matches
        for patient1 in toDiscover:
            for patient2 in toDiscover:
                if patient1.faulty.kidney == patient2.donor.kidney and patient1.faulty.right == patient2.donor.right: #if 1 needs 2's kidney
                    if patient2.faulty.kidney == patient1.donor.kidney and patient2.faulty.right == patient1.donor.right: #if 2 needs 1's kidney
                        patient1.faulty = patient2.donor
                        patient2.faulty = patient1.donor

                        patient1.cured = date - patient1.date
                        patient2.cured = date - patient2.date
                        toMatch.remove(patient1)
                        matched.append(patient1)
                        toMatch.remove(patient2)
                        matched.append(patient2)

        date += 1
        analyze(dead, matched, "Free For All Match")
        #
        return 0
#Determines whether or not a patient and donor are compatible
def isCompatible(patient, donor):
    patient = str(patient.type)
    donor = str(donor.type)

    # check if organs same
    if patient[0] != donor[0]:
        return false

    # check if organ types same, say odd and even must match
    if (patient[1])%2 != (donor[1])%2:
        return false

    # check if blood types match and each blood type is comparable with numbers lower than it
    if (patient[2] > donor[2]):
        return false

    return true



# Akbarpour's single organ case
# Parameters: toDiscover, a stack of tuples representing a patient donor pair (p,d)
def unpaired_simple(toDiscover):
    pd_index = 0
    pending_donors = []
    pending_patients = []


    for t in range(DATE_RANGE):
        while(pd_index < len(toDiscover) and toDiscover[pd_index][0].date == t):
            #try to find a donor for toDiscover[pd_index].patient in pending_donors
            patient = toDiscover[pd_index][0]
            isPatientMatched = False
            for donor in pending_donors:
                if donor.type == patient.type:
                    pending_donors.remove(donor)
                    isPatientMatched = True
                    matched.append((patient, donor))
                    print("Log: ", patient.id, " matched with ", donor.id)
            #if no match, add patient to pending_patients
            if(not isPatientMatched):
                pending_patients.append(patient)


            #try to find a patient for toDiscover[pd_index].donor
            donor = toDiscover[pd_index][1]
            isDonorMatched = False
            for patient in pending_patients:
                if donor.type == patient.type:
                    pending_patients.remove(patient)
                    isDonorMatched = True
                    matched.append((patient, donor))
                    print("Log: ", patient.id, " matched with ", donor.id)
            #if no match, add patient to pending_patients
            if(not isPatientMatched):
                pending_patients.append(patient)

            pd_index += 1



# generates list of patients according to global parameters up top
def generate():
    patients = []
    donors = []
    sampleList = [True, False]
    pairs = []
    # create patients according to distributions defined by parameters
    for i in range(NUM_PATIENTS):
        patientType = 100*randrange(NUM_ORGANS) + 10*randrange(ORGAN_TYPES) + randrange(BLOOD_TYPES)
        donorType = 100*randrange(NUM_ORGANS) + 10*randrange(ORGAN_TYPES) + randrange(BLOOD_TYPES)
        date = randrange(DATE_RANGE)
        lifetime =  300 ## TODO: change this to randomize lifespan later

        patient = Patient(date, lifetime, type, i, False)
        donor = Donor(donorType, i)

        patients.append(patient)
        donors.append(donor)
        pairs.append((patient, donor))

    print("patients:", patients)
    print("donors:", donors)
    print("pairs:", pairs)

    return pairs

# generates patients, then runs each match.
def main():
    # date = 0
    toDiscover = generate()
    print(toDiscover)
    #pairedMatch(patients)
    ttc(toDiscover)
    unpaired_simple(toDiscover)
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
