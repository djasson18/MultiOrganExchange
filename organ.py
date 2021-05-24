# organ.py
# faulty or not (bool)
# liver or kidney (bool)
# left lobe or right lobe (bool)

class Organ:
    def __init__(self, faulty, kidney, left):
        # whether or not organ is kidney (bool)
        self.kidney = kidney
        # whether or not it is left lobe/type 1 liver (bool)
        self.left = left
        # whether organ is working properly (bool)
        self.faulty = faulty

    def give_organ_features(self):
        print("My organ features are ", self.kidney, self.left, self.faulty)
