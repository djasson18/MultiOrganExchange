# organ.py
# faulty or not (bool)
# liver or kidney (bool)
# left lobe or right lobe (bool)

class Organ:
    def __init__(self, faulty, kidney, right):
        self.kidney = kidney
        self.right = right
        self.faulty = faulty