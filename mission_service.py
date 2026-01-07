import time
import random

from Maps.examples import MAPS
from map_evaluation_engine import MapEvaluationEngine
from NomosRSI.nomos import NomosRSI
from NomosRSI.briefing_generator import BriefingGenerator


# --------------------------------------------------
# Difficulty-Funktion (aus main.py übernommen)
# --------------------------------------------------

def choose_difficulty(map_obj, index):
    return random.choice(["easy", "normal", "hard", "expert"])


# --------------------------------------------------
# Missionslauf (Web / CLI / GUI-unabhängig)
# --------------------------------------------------

def run_mission(progress_cb=None):
    """
    Führt eine komplette Missionsgenerierung aus.

    progress_cb: callable(str) | None
        Wird für Statusmeldungen aufgerufen (GUI / Web Logs)
    """

    def log(msg):
        if progress_cb:
            progress_cb(msg)

    log("System >> Starte Map Evaluation Engine...\n\n")

    nomos = NomosRSI()
    generator = BriefingGenerator()

    engine = MapEvaluationEngine(
        maps=MAPS,
        player_count=2,
        difficulty_function=choose_difficulty,
        fixed_step=0.1,
        callback=nomos.ingest_report,
        progress_callback=log
    )

    # --------------------------------------------------
    # Engine Loop (aus GUI + CLI vereinheitlicht)
    # --------------------------------------------------

    while engine.current_index < len(engine.maps):
        engine.fixed_update(engine.fixed_step)
        time.sleep(engine.fixed_step)

    # --------------------------------------------------
    # Mission auswählen + Briefing
    # --------------------------------------------------

    map_name, advice = nomos.choose_mission_random()

    if not map_name:
        return "Nomos >> Keine Map verfügbar.\n"

    briefing = generator.generate_briefing(map_name, advice)

    return (
        "\n🎖️  MISSIONSBRIEFING 🎖️\n"
        + "=" * 50 + "\n\n"
        + briefing + "\n\n"
        + "=" * 50 + "\n"
    )
