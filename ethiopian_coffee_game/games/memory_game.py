import random

class MemoryGame:
    def __init__(self, level):
        self.pairs = min(3 + level, 12)
        self.cards = list(range(self.pairs)) * 2
        random.shuffle(self.cards)
        self.flipped = []

    def flip_card(self, index):
        self.flipped.append(index)

    def check_match(self):
        if len(self.flipped) == 2:
            i1, i2 = self.flipped
            match = self.cards[i1] == self.cards[i2]
            self.flipped = []
            return match
        return False