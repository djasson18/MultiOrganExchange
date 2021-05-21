# patient.py
# date where kidney requirement for kidney starts (int)
# lifetime without transplant (int)
# liver or kidney (bool)
# left lobe or right lobe (bool)
# faultyOrgan (organ)
# donorOrgan (organ)
# place on waiting list (int) [consistent across all patients]
# token (bool)
# cured (bool)


class Patient:
    def __init__(self, date, lifetime, kidney, right, faulty, donor, waitingList, token, cured):
        self.date = date
        self.lifetime = lifetime
        self.kidney = kidney
        self.right = right
        self.faulty = faulty
        self.donor = donor
        self.waitingList = waitingList
        self.token = token
        self.cured = cured