#patient.py

class Patient:
    def __init__(self, date, organClass, bloodType, praScore, visited):
        # date where kidney requirement for kidney starts (int)
        self.date = date
        # lifetime without transplant (int)
        self.dateMatched = -1
        # int
        self.organClass = organClass


        self.bloodType = bloodType

        self.praScore = praScore


        # boolean to implement TTC
        self.visited = visited

    def give_patient_features(self):
        print("My patient features are ", self.date, self.lifetime, self.type, self.waitingList, self.cured)
