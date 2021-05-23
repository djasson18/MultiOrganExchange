import patient
import organ
import random
#import numpy
from random import randrange
from organ import Organ
from patient import Patient


#GLOBAL PARAMETERS FOR GENERATION:
NUM_PATIENTS = 2 #number of patients to generate
CHANCE_KIDNEY = .5 #chance of needing a kidney vs liver
CHANCE_LEFT = .5 #chance of being left lobe (or organ type 1)
LIFETIME_AVG = 365*5 #average lifespan for someone after discovering needed organ
LIFETIME_STDDEV = 365*2 #std dev on lifespan ^
DATE_RANGE = 365 #upper bound on dates to discover needing organ

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
def ttc(toMatch, toDiscover):
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
    while(toMatch.size != 0 and toDiscover.size != 0):
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

        return 0

# our novel approach. Not yet implemented.
def nft(toMatch, toDiscover):
    pass
    return 0

# generates list of patients according to global parameters up top
def generate():
    patients = []
    sampleList = [True, False]

    # create patients according to distributions defined by parameters
    for i in range(NUM_PATIENTS):
        kidney = random.choices(sampleList, weights = (CHANCE_KIDNEY, 1-CHANCE_KIDNEY))
        left = random.choices(sampleList, weights = (CHANCE_LEFT, 1-CHANCE_LEFT))
        organToGiveIsKidney = random.choices(sampleList, weights = (CHANCE_KIDNEY, 1-CHANCE_KIDNEY))
        organToGiveIsLeft = random.choices(sampleList, weights = (CHANCE_LEFT, 1-CHANCE_LEFT))


        # kidney = False
        # left = False
        # organToGiveIsKidney = True
        # organToGiveIsLeft = True

        faultyOrgan = Organ(kidney, left, True)
        print("faulty")
        faultyOrgan.give_features()
        donorOrgan = Organ(organToGiveIsKidney, organToGiveIsLeft, False)
        print("donor")
        donorOrgan.give_features()  # randoms in parenthesis is bad?

        lifetime = randrange(300)  # random.normal(LIFETIME_AVG, LIFETIME_STDDEV)
        date = randrange(DATE_RANGE)

        patient = Patient(date, lifetime, faultyOrgan, donorOrgan, i, False, False)
        print("patient")
        patient.give_features()  # don't know if organ ones work
        patients.append(patient)

    # print(patients)
    return patients



# generates patients, then runs each match.
def main():
    # date = 0
    patients = generate()
    print(patients)
    """
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
    """
    # pairedMatch(toMatch, toDiscover)
    # ttc(toMatch, toDiscover)
    # nft(toMatch, toDiscover)


if __name__ == "__main__":
    main()
