class ReplayPlayer:
    def __init__(self, events):
        # Sortiert nach Tick
        self.events = sorted(events, key=lambda x: x[0])
        self.current_index = 0

    def get_events_for_tick(self, tick_id):
        events_to_play = []
        while self.current_index < len(self.events) and self.events[self.current_index][0] == tick_id:
            _, event = self.events[self.current_index]
            events_to_play.append(event)
            self.current_index += 1
        return events_to_play
