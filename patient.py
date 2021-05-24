# don't know if organ is being imported properly

class Patient:
    def __init__(self, date, lifetime, type, waitingList, cured, visited):
        # date where kidney requirement for kidney starts (int)
        self.date = date
        # lifetime without transplant (int)
        self.lifetime = lifetime
        # int
        self.type = type
        # place on waiting list (int) [consistent across all patients]
        self.waitingList = waitingList
        # cured date is time to be cured (int)
        self.cured = cured
        # boolean to implement TTC
        self.visited = visited

    def give_patient_features(self):
        print("My patient features are ", self.date, self.lifetime, self.type, self.waitingList, self.cured)
