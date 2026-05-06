import random

class CupShuffle:
    def __init__(self, level=1):
        self.level = level
        self.cups = min(3 + level // 5, 6)
        self.correct = random.randint(0, self.cups - 1)

    def shuffle(self):
        order = list(range(self.cups))
        random.shuffle(order)
        return order

    def check(self, choice):
        return choice == self.correct