# organ.py
# faulty or not (bool)
# liver or kidney (bool)
# left lobe or right lobe (bool)

class Organ:
    def __init__(self, faulty, kidney, left):
        self.kidney = kidney
        self.left = left
        self.faulty = faulty

    def give_features(self):
        print("My features are ", self.kidney, self.left, self.faulty)
