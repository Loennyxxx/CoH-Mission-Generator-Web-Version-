import pickle

class ReplayRecorder:
    def __init__(self):
        self.events = []

    def record_event(self, event, tick_id):
        self.events.append((tick_id, event))

    def save(self, path):
        with open(path, "wb") as f:
            pickle.dump(self.events, f)

    def load(self, path):
        with open(path, "rb") as f:
            self.events = pickle.load(f)
