class Donor:
	def __init__(self, organClass, bloodType, praScore, id):
		# type of organ (int)
		self.organClass = organClass
		self.bloodType = bloodType
		# unique id matchable with associated patient
		self.id = id
		self.praScore = praScore
		self.bloodType = bloodType
