# core/engine.py
from core.utils.rng import DeterministicRNG

class Engine:
    def __init__(self, tick_rate=60, use_jobs=True, max_workers=None, rng_seed=42):
        from core.time.clock import EngineClock
        from core.jobs import JobSystem

        self.clock = EngineClock(tick_rate)
        self.systems = []
        self.event_bus = None
        self.running = False
        self.replay_recorder = None

        self.use_jobs = use_jobs
        if use_jobs:
            self.job_system = JobSystem(max_workers=max_workers)

        # Deterministischer RNG mit Seed
        self.rng = DeterministicRNG(rng_seed)

    # ---------------- Systems ----------------
    def add_system(self, system):
        """Systeme registrieren"""
        self.systems.append(system)
        system.on_attach(self)

    # ---------------- EventBus ----------------
    def attach_event_bus(self, bus):
        self.event_bus = bus
        if self.replay_recorder:
            bus.attach_recorder(self.replay_recorder)

    # ---------------- Replay ----------------
    def enable_replay(self):
        from core.replay.recorder import ReplayRecorder
        self.replay_recorder = ReplayRecorder()
        if self.event_bus:
            self.event_bus.attach_recorder(self.replay_recorder)

    # ---------------- Engine Update ----------------
    def update(self, dt):
        """
        Haupt-Update pro Tick:
        - Tick-ID hochzählen
        - Jobsystem verwenden, wenn aktiviert
        - Alle Systeme updaten
        """
        self.clock.tick()  # Tick-ID erhöhen
        tick_id = self.clock.current_tick()

        if self.use_jobs:
            # Alle Systeme als Jobs in ThreadPool einreihen
            for system in self.systems:
                self.job_system.add_job(system.update, dt, tick_id)
            # Jobs ausführen
            self.job_system.execute_jobs()
        else:
            for system in self.systems:
                system.update(dt, tick_id)

    # ---------------- Save / Load ----------------
    def save(self, path):
        from core.save.load import SaveManager
        SaveManager.save(path, self)

    def load(self, path):
        from core.save.load import SaveManager
        SaveManager.load(path, self)

    # ---------------- Shutdown ----------------
    def shutdown(self):
        """Sauberes Beenden der Engine, Threads schließen"""
        if self.use_jobs:
            self.job_system.shutdown()
