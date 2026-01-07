import random

class DeterministicRNG:
    def __init__(self, seed):
        self.seed = seed
        self.random = random.Random(seed)  # <-- self.random, nicht self.rng

    def randint(self, a, b):
        return self.random.randint(a, b)

    def random_value(self):
        return self.random.random()

    def choice(self, seq):
        return self.random.choice(seq)
