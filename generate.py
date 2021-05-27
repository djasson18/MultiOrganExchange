import numpy as np

NO_PAIR_TRADE = True #No pair will be generated who can match within the pair
YEARS = 100
NUM_PATIENTS = 100 #patients per period
organs = ["Kidney", "Liver", "Marrow"]
organProbs = [.78, .11, .11]

blood = ["A+", "A-","B+", "B-", "AB+","AB-", "O+", "O-"]
blood_probs = [.34, .06, .09, .02, .03, .01, .38, .07]

#For generating patients without the AB positive possibility
no_ABP = ["A+", "A-","B+", "B-", "AB-", "O+", "O-"]
no_ABP_probs = [.34, .06, .09, .02, .01, .38, .07]/np.sum([.34, .06, .09, .02, .01, .38, .07]) #Bayesian adjustment

#Three Places dont know if this is the best spot for them
negative = []
positive = []
pairs = []

class pair:
  def __init__(self, patient, donor):
    self.patient = patient
    self.donor = donor

class new_patient:
  def __init__(self, organ, blood):
    self.organ = organ
    self.blood = blood
    balance = 0;

class new_donor:
  def __init__(self, blood):
    self.blood = blood
    donated = ""
    balance = 0;

def print_pairs():
  for i in pairs:
    print("Patient: ", i.patient.organ, i.patient.blood," Donor: " , i.donor.blood)

def incompatible_pair():
  #Ensures that the patients donor is unable to donate to the patient themselves, cannot be AB+ then
  patient = new_patient((np.random.choice(a = organs, size = 1, replace = True, p = organProbs)), (np.random.choice(a = no_ABP, size = 1, replace = True, p = no_ABP_probs)))

  #Make sure the donor cannot have a compatible bloodtype to the patient
  s = set(compatible_donors(patient))
  incompatible_blood_types = [x for x in blood if x not in s]
  incompatible_blood_probs = [blood_probs[blood.index(x)] for x in blood if x not in s]

  #Bayesian Adjustment
  incompatible_blood_probs /= np.sum(incompatible_blood_probs)
  donor = new_donor(np.random.choice(a = incompatible_blood_types, size = 1, replace = True, p = incompatible_blood_probs))

  pairs.append(pair(patient, donor))

def generate():
  if (NO_PAIR_TRADE): incompatible_pair()
  else:
    patient = new_patient((np.random.choice(a = organs, size = 1, replace = True, p = organProbs)), (np.random.choice(a = blood, size = 1, replace = True, p = blood_probs)))
  #Generated pairs could be compatible (37%, on average)
    donor = new_donor(np.random.choice(a = blood, size = 1, replace = True, p = blood_probs))
    pairs.append(pair(patient, donor))

#Add NUM_PATIENTS to the system
def inflow():
  for x in range(NUM_PATIENTS):
    generate()
  print_pairs()

#Bit manipulation
def bitfun(compatible, t):
  l = 'A+ O+ B+ AB+ A- O- B- AB-'.split()
  c = [9,15,12,8,153,255,204,136]
  i = l.index(t)
  for s in l:
    if c[l.index(s)] & (1 << i):
      compatible.append(s)

#Returns an array of compatible donor bloodtypes given a patient
def compatible_donors(patient):
  compatible = []
  bitfun(compatible, patient.blood)
  return compatible

def match():
  #First check for pair donating (they wouldn't be here if they could)
  counter = 0
  for i in pairs:
    if i.donor.blood in compatible_donors(i.patient):
      pairs.remove(i)
      counter += 1
  print(counter, "pairs already a match with themselves")

  #Check for matches between new arrivals and existing pairs, new arrivals

  l = len(pairs) - 1
  for i in range(0, l):
    for j in range(0, l):
      if pairs[i].donor.blood in compatible_donors(pairs[j].patient):
        break

  #Check debtors

def main():
  #for year in range(YEARS):
  inflow()
  match();





main()
