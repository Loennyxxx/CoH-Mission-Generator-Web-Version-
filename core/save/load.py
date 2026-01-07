import pickle

class SaveManager:
    @staticmethod
    def save(path, engine):
        # Sammle State von Engine und Systemen
        state = {
            "tick_id": engine.clock.tick_id,
            "rng_state": engine.rng.rng.getstate() if hasattr(engine, "rng") else None,
            "systems": {type(s).__name__: s.get_state() for s in engine.systems}
        }
        with open(path, "wb") as f:
            pickle.dump(state, f)

    @staticmethod
    def load(path, engine):
        with open(path, "rb") as f:
            state = pickle.load(f)

        engine.clock.tick_id = state["tick_id"]

        if hasattr(engine, "rng") and state["rng_state"] is not None:
            engine.rng.rng.setstate(state["rng_state"])

        for s in engine.systems:
            s_state = state["systems"].get(type(s).__name__)
            if s_state:
                s.set_state(s_state)
