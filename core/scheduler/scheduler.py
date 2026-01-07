import heapq
import time

class Scheduler:
    def __init__(self):
        self.tasks = []

    def schedule(self, delay, callback):
        heapq.heappush(self.tasks, (time.time() + delay, callback))

    def update(self):
        now = time.time()
        while self.tasks and self.tasks[0][0] <= now:
            _, cb = heapq.heappop(self.tasks)
            cb()
