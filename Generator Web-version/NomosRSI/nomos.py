import random
from .parser import MEEResultParser
from .utensils import SpeechGenerator

class NomosRSI:
    def __init__(self):
        self.parser = MEEResultParser()
        self.speech = SpeechGenerator()

    def ingest_report(self, map_context, rule_results):
        self.parser.ingest(map_context, rule_results)

    def get_all_reports(self):
        return self.parser.get_reports()

    def get_report(self, map_name):
        return self.parser.get_report_for_map(map_name)

    def speak_strategy(self, map_name):
        report = self.get_report(map_name)
        if report:
            return self.speech.generate_strategy_advice(report)
        return f"Kein Report für Map {map_name} vorhanden."

    def choose_mission_random(self):
        """
        Wählt zufällig eine Map aus den bisherigen Reports aus
        UND gibt direkt die Empfehlung aus.
        """
        reports = self.get_all_reports()
        if not reports:
            return None, "Keine Maps verfügbar."

        chosen_report = random.choice(reports)
        map_name = chosen_report.map_context.map_name
        advice = self.speech.generate_strategy_advice(chosen_report)

        return map_name, advice
