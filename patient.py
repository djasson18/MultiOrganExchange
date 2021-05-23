# don't know if organ is being imported properly

class Patient:
    def __init__(self, date, lifetime, faulty, donor, waitingList, token, cured):
        # date where kidney requirement for kidney starts (int)
        self.date = date
        # lifetime without transplant (int)
        self.lifetime = lifetime
        # Organ
        self.faulty = faulty
        # Organ
        self.donor = donor
        # place on waiting list (int) [consistent across all patients]
        self.waitingList = waitingList
        # bool
        self.token = token
        # cured date is time to be cured (int)
        self.cured = cured

    def give_features(self):
        print("My patient features are ", self.date, self.lifetime, self.faulty, self.donor, self.waitingList, self.token, self.cured)
