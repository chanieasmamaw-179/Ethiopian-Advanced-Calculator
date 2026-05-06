import random

class RememberOrderGame:
    def __init__(self, level):
        self.sequence_length = 3 + level
        self.sequence = [random.randint(0, 5) for _ in range(self.sequence_length)]
        self.user_input = []

    def add_input(self, value):
        self.user_input.append(value)

    def check_sequence(self):
        return self.user_input == self.sequence