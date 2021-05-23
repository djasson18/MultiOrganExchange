# patient.py
# date where kidney requirement for kidney starts (int)
# lifetime without transplant (int)
# faultyOrgan (organ)
# donorOrgan (organ)
# place on waiting list (int) [consistent across all patients]
# token (bool)
# cured date is time to be cured (int)


class Patient:
    def __init__(self, date, lifetime, faulty, donor, waitingList, token, cured):
        self.date = date
        self.lifetime = lifetime
        self.faulty = faulty
        self.donor = donor
        self.waitingList = waitingList
        self.token = token
        self.cured = cured
