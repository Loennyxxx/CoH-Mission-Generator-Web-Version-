import concurrent.futures

class JobSystem:
    def __init__(self, max_workers=None):
        """
        max_workers: Anzahl paralleler Threads (None = CPU cores)
        """
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=max_workers)
        self.jobs = []

    def add_job(self, func, *args, **kwargs):
        """
        func: Callable
        args / kwargs: Argumente für die Funktion
        """
        self.jobs.append((func, args, kwargs))

    def execute_jobs(self):
        """
        Führt alle Jobs aus und wartet auf Ergebnis
        """
        futures = []
        for func, args, kwargs in self.jobs:
            futures.append(self.executor.submit(func, *args, **kwargs))
        # Warten bis alles fertig ist
        concurrent.futures.wait(futures)
        # Optional: Ergebnisse sammeln
        results = [f.result() for f in futures]
        self.jobs.clear()
        return results

    def shutdown(self):
        self.executor.shutdown(wait=True)
