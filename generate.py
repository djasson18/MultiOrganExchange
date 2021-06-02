#generate.py
#hello from a 3rd world country
import numpy as np

YEARS = 10
PPP = 10 #patients per period

organs = ["Kidney", "Liver", "Marrow"]
organProbs = [.78, .11, .11]

blood = ["A+", "A-","B+", "B-", "AB+","AB-", "O+", "O-"]
blood_probs = [.34, .06, .09, .02, .03, .01, .38, .07]

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

def generate():
  patient = new_patient((np.random.choice(a = organs, size = 1, replace = True, p = organProbs)), (np.random.choice(a = blood, size = 1, replace = True, p = blood_probs)))

  donor = new_donor(np.random.choice(a = blood,size = 1, replace = True, p = blood_probs))

  pairs.append(pair(patient, donor))


def inflow():
  for x in range(PPP):
    generate()

  for i in pairs:
    print("Patient: ", i.patient.organ, i.patient.blood," Donor: " , i.donor.blood)

def bitfun(compatible, t):
  l = 'A+ O+ B+ AB+ A- O- B- AB-'.split()
  c = [9,15,12,8,153,255,204,136]
  i = l.index(t)
  for s in l:
    if c[l.index(s)] & 1 << i:
      compatible.append(s)

def is_compatible(donor, patient):
  compatible = []
  bitfun(compatible, patient.blood)
  if donor.blood in compatible:
    return True



def match():
  #First check for pair donating (they wouldn't be here if they could)
  return

  #Run through debtors first

def main():
  #for year in range(YEARS):
  inflow()
  return
  #match();





main()
