import time
import random
from core.engine import Engine
from __init__ import MAPS
from __init__ import Context
from __init__ import RuleSystem
from __init__ import (
    LargeMapDefensiveRule,
    UrbanMapInfantryRule,
    ExpertAICautionRule,
    EasyAIExperimentRule,
    TwoPlayerSynergyRule,
    MultiPlayerMapControlRule,
    NoEarlyLightVehicleRule,
    LateGameArtilleryRule,
    MGNestChokeRule,
    BunkerVPRule,
    MinefieldFlankRule,
    ReconPriorityRule,
    TrenchLineRule,
    MortarSuppressionRule,
    ATGunnerCoverRule,
    FuelRushEconomyRule
)

class MapEvaluationEngine(Engine):
    def __init__(self, maps, player_count, difficulty_function, tick_rate=60, fixed_step=1.0, callback=None, progress_callback=None):
        """
        maps: Liste von Map-Objekten
        player_count: Anzahl der Spieler
        difficulty_function: callable(map_obj, index) -> str
        callback: callable(context, results) z.B. NomosRSI.ingest_report
        progress_callback: callable(message) für GUI-Log
        """
        super().__init__(tick_rate=tick_rate, use_jobs=False)  # disable job system für simplicity
        self.maps = maps
        self.player_count = player_count
        self.difficulty_function = difficulty_function
        self.fixed_step = fixed_step
        self.callback = callback
        self.progress_callback = progress_callback
        self.current_index = 0

        # RuleSystem vorbereiten
        self.rule_system = RuleSystem()
        self.rule_system.add_rule(LargeMapDefensiveRule())
        self.rule_system.add_rule(UrbanMapInfantryRule())
        self.rule_system.add_rule(ExpertAICautionRule())
        self.rule_system.add_rule(EasyAIExperimentRule())
        self.rule_system.add_rule(TwoPlayerSynergyRule())
        self.rule_system.add_rule(MultiPlayerMapControlRule())
        self.rule_system.add_rule(NoEarlyLightVehicleRule())
        self.rule_system.add_rule(LateGameArtilleryRule())
        self.rule_system.add_rule(MGNestChokeRule())
        self.rule_system.add_rule(BunkerVPRule())
        self.rule_system.add_rule(MinefieldFlankRule())
        self.rule_system.add_rule(ReconPriorityRule())
        self.rule_system.add_rule(TrenchLineRule())
        self.rule_system.add_rule(MortarSuppressionRule())
        self.rule_system.add_rule(ATGunnerCoverRule())
        self.rule_system.add_rule(FuelRushEconomyRule())

    def fixed_update(self, dt):
        if self.current_index >= len(self.maps):
            if self.progress_callback:
                self.progress_callback(
                    f"[Engine] Map-Generierung abgeschlossen.\n"
                )
            self.stop()
            return

        map_obj = self.maps[self.current_index]
        ai_difficulty = self.difficulty_function(map_obj, self.current_index)

        context = Context(
            map_obj=map_obj,
            player_count=self.player_count,
            ai_difficulty=ai_difficulty
        )

        results = self.rule_system.evaluate(context)

        if self.callback:
            self.callback(context, results)

        # 🔥 LIVE PROGRESS → GUI
        if self.progress_callback:
            self.progress_callback(
                f"[Engine] Karte {self.current_index + 1}/{len(self.maps)} "
                f"generiert: {map_obj.name} "
                f"(Difficulty: {ai_difficulty})\n"
            )

        self.current_index += 1


    @staticmethod
    def choose_difficulty(map_obj, index):
        difficulties = ["easy", "normal", "hard", "expert"]
        return random.choice(difficulties)
    
    def reset(self):
        """Setzt die Engine zurück, damit sie erneut laufen kann"""
        self.current_index = 0
        self.running = False