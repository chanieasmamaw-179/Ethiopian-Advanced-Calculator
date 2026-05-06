import random

class SpeedTapGame:
    def __init__(self, level):
        self.level = level
        self.speed = max(0.5, 2 - level * 0.1)
        self.targets = random.randint(3, 6 + level)

    def spawn_target(self):
        return random.randint(0, 5)

    def check_hit(self, target, tap):
        return target == tap