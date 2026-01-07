import time

class EngineClock:
    def __init__(self, tick_rate=60):
        self.tick_rate = tick_rate
        self.tick_time = 1.0 / tick_rate
        self.last_time = time.perf_counter()
        self.accumulator = 0.0
        self.tick_id = 0  # NEU: Tick-ID für Determinismus

    def tick(self):
        now = time.perf_counter()
        delta = now - self.last_time
        self.last_time = now
        self.accumulator += delta

        ticks_this_frame = 0
        while self.accumulator >= self.tick_time:
            self.accumulator -= self.tick_time
            self.tick_id += 1      # Tick-ID hochzählen
            ticks_this_frame += 1

        return ticks_this_frame

    def current_tick(self):
        return self.tick_id
