class Donor:
    def __init__(self, type, id):
        # type of organ (int)
       self.type = type
	    # unique id matchable with associated patient
       self.id = id

    def give_donor_features(self):
        print("My donor features are Type:", self.type, "ID:", self.id)
