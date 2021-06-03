import patient
import random
import numpy as np
from random import randrange
from donor import Donor
from patient import Patient
from collections import deque
import time


#GLOBAL PARAMETERS FOR GENERATION:
NUM_PATIENTS = 45000 #number of patients to generate
CHANCE_KIDNEY = .5 #chance of needing a kidney vs liver
CHANCE_LEFT = .5 #chance of being left lobe (or organ type 1)
LIFETIME_AVG = 365*5 #average lifespan for someone after discovering needed organ
LIFETIME_STDDEV = 365*2 #std dev on lifespan ^
DATE_RANGE = 365 #upper bound on dates to discover needing organ
NUM_ORGANS = 3 # number of uniquely matchable organs
ORGAN_TYPES = 4 # number of compatability types within an organ class
BLOOD_TYPES = 4 # number of blood types
LIVER = 0
KIDNEY = 1
BONE_MARROW = 3

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
	matched = []
	q = []
	dead = []
	patients = []
	donors = []
	currIndex = 0
	date = 0
	matched = 0

	for t in range(DATE_RANGE):
		if t % 60 == 0:
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

			#for currP in patients:
			#	if currP.date + currP.lifetime < date:
			#		dead.append(currP)
			#		patients.remove(currP)

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

				# find a donor match
				for d in donors:
					if isCompatible(pair[0], d):
						donor = d
						break
					donorIndex += 1
				# if donor is paired with unvisited patient j
				if(donorIndex == len(patients)):
					donorIndex = donorIndex - 1
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
	print("Time Elapsed", (time.time() - startTime)/60)
	print("matched", matched)
	print("unmatched:", NUM_PATIENTS - matched)
	print("---------------")

	return

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


		# cycle through pairs of patients trying to find matches
		for pair1 in toMatch:
			for pair2 in toMatch:
				if isCompatible(pair1[0], pair2[1]) and isCompatible(pair2[0], pair1[1]): #if 1 needs 2's kidney
					pair1[0].timeMatched = date - pair1[0].date
					pair2[0].timeMatched = date - pair2[0].date
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
	print("Elapsed Time:", (time.time() - startTime)/60)
	print("dead:",len(dead))
	print("matched:",len(matched))
	print("---------------")
	return 0
# Determines whether or not a patient and donor are compatible
def isCompatible(patient, donor):
	if(patient.organClass == "Kidney" and donor.organClass == "Kidney"):
		return bloodTypeCompatability(patient, donor) and HLACompatability(patient, donor)
	if(patient.organClass == "Livers" and patient.organClass == "Livers"):
		return bloodTypeCompatability(patient, donor)
	if(patient.organClass == "Marrow" and patient.organClass == "Marrow"):
		return bloodTypeCompatability(patient, donor) and HLACompatability(patient, donor)

def bloodTypeCompatability(patient, donor):
	if patient.bloodType == "A+":
		return donor.bloodType in ["A+", "A-", "O+", "O-"]
	elif patient.bloodType == "A-":
		return donor.bloodType in ["A-","O-"]
	elif patient.bloodType == "B+":
		return donor.bloodType in ["B+", "B-", "O+", "O-"]
	elif patient.bloodType == "B-":
		return donor.bloodType in ["B-", "O-"]
	elif patient.bloodType == "AB+":
		return True #compatable with all!
	elif patient.bloodType == "AB-":
		return donor.bloodType in ["AB-", "A-", "O+", "O-"]
	elif patient.bloodType == "O+":
		return donor.bloodType in ["O+", "O-"]
	elif patient.bloodType == "O-":
		return donor.bloodType in ["O+", "O-"]

def HLACompatability(patient, donor):
	return donor.praScore > patient.praScore

# unpaired_complex
# Parameters: toDiscover, a stack of tuples representing a patient donor pair (p,d)
def unpaired_complex(toDiscover):
	print(len(toDiscover))
	startTime = time.time()
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
	print("Elapsed Time:", (time.time() - startTime)/60)
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
	organs = ["Kidney", "Liver", "Marrow"]
	organProbs = [.78, .11, .11]
	blood = ["A+", "A-","B+", "B-", "AB+","AB-", "O+", "O-"]
	blood_probs = [.34, .06, .09, .02, .03, .01, .38, .07]
	patients = []
	donors = []
	pairs = []

	# create patients according to distributions defined by parameters
	for i in range(NUM_PATIENTS):
		#numpy random choice and manually assign mass values
		organ_classes = np.random.choice(organs, 2, True, organProbs)
		blood_types = np.random.choice(blood, 2, True, blood_probs)

		date = randrange(DATE_RANGE)
		patient_pra_score = random.randint(0, 100)
		donor_pra_score = random.randint(0, 100)
		if(patient_pra_score <= 20):
			patient_pra_score = 0
		elif(patient_pra_score > 10 and patient_pra_score <= 35):
			patient_pra_score = 100
		else:
			patient_pra_score = randrange(1,99)

		patient = Patient(date, organ_classes[0], blood_types[0], patient_pra_score, False)
		donor = Donor(organ_classes[1], blood_types[1], donor_pra_score, i)

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
	#pairedMatch(toDiscover)
	ttc(toDiscover)
	unpaired_complex(toDiscover)





if __name__ == "__main__":
	main()
