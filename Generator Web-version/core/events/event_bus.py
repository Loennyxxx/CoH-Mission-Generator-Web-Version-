class EventBus:
    def __init__(self):
        self.listeners = []
        self.replay_recorder = None  # NEU: optionaler Recorder

    def attach_recorder(self, recorder):
        self.replay_recorder = recorder

    def subscribe(self, callback):
        self.listeners.append(callback)

    def emit(self, event, tick_id=None):
        # NEU: Event aufzeichnen
        if self.replay_recorder:
            self.replay_recorder.record_event(event, tick_id)

        for cb in self.listeners:
            cb(event)
