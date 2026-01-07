from Rules.rule import Rule
import random


# ALTE 8 Rules (bleiben unverändert - funktionieren)
class LargeMapDefensiveRule(Rule):
    def __init__(self):
        super().__init__("Large Map favors Defensive Play")

    def evaluate(self, context):
        if context.map_size == "large":
            score = 1 + context.player_count
            return score, f"Große Karten begünstigen Defensive und Map Control. Score skaliert mit Spielern: {score}"
        elif context.map_size == "medium":
            return 1, "Mittlere Karten begünstigen leicht defensive Spielweise"
        return 0, "Kleine Karten haben keinen defensiven Vorteil"


class UrbanMapInfantryRule(Rule):
    def __init__(self):
        super().__init__("Urban Map favors Infantry")

    def evaluate(self, context):
        if context.map_type == "urban":
            score = 2 + max(0, 2 - context.player_count)
            return score, f"Urban Maps schränken Fahrzeuge ein. Score angepasst an Spielerzahl: {score}"
        elif context.map_type == "mixed":
            return 1, "Mixed Maps haben leichte Infanterie-Vorteile"
        return 0, "Open Maps begünstigen keine Infanterie besonders"


class ExpertAICautionRule(Rule):
    def __init__(self):
        super().__init__("Expert AI discourages Early Aggression")

    def evaluate(self, context):
        if context.ai_difficulty == "expert":
            score = random.randint(-5, -3)
            return score, f"Expert AI bestraft frühe Aggression stark Score: {score}"
        elif context.ai_difficulty == "hard":
            return -2, "Starke AI warnt vor vorschnellen Angriffen"
        return 0, "Leichte AI erlaubt aggressives Early Game"


class EasyAIExperimentRule(Rule):
    def __init__(self):
        super().__init__("Easy AI allows Experimental Play")

    def evaluate(self, context):
        if context.ai_difficulty == "easy":
            score = random.choice([1,2,3])
            return score, f"Einfache AI erlaubt Experimente. Score zufällig: {score}"
        return 0, "AI zu stark für riskante Experimente"


class TwoPlayerSynergyRule(Rule):
    def __init__(self):
        super().__init__("2v2 favors Role-Based Play")

    def evaluate(self, context):
        if context.player_count == 2:
            score = 2 + random.randint(0,1)
            return score, f"Zwei Spieler erlauben Rollenverteilung. Score: {score}"
        return 0, "Spieleranzahl erzwingt keine Rollen"


class MultiPlayerMapControlRule(Rule):
    def __init__(self):
        super().__init__("Multiple Players require Strong Map Control")

    def evaluate(self, context):
        if context.player_count >= 3:
            score = context.player_count
            return score, f"Mehr Spieler → stärkerer Map Control Fokus. Score: {score}"
        return 0, "Map Control ist nicht überdurchschnittlich wichtig"


class NoEarlyLightVehicleRule(Rule):
    def __init__(self):
        super().__init__("No Early Light Vehicles")

    def evaluate(self, context):
        if context.ai_difficulty in ("hard", "expert"):
            score = -2 - (context.player_count - 1)
            return score, f"Frühe Light Vehicles riskant. Score: {score}"
        return 0, "Light Vehicles vertretbar"


class LateGameArtilleryRule(Rule):
    def __init__(self):
        super().__init__("Late Game favors Artillery")

    def evaluate(self, context):
        if context.map_size == "large":
            score = 1 + context.player_count
            if context.player_count >= 2:
                score += 1
            return score, f"Artillery-Nutzen steigt mit Map-Größe & Teamplay. Score: {score}"
        return 0, "Artillery nicht zwingend erforderlich"


# NEUE 8 Rules (STRUKTUR WIE DIE ALTEN - nur map_size, map_type, ai_difficulty, player_count)
class MGNestChokeRule(Rule):
    def __init__(self):
        super().__init__("MG Nests dominate Choke Points")
    
    def evaluate(self, context):
        if context.map_size in ["large", "medium"]:
            score = 3 if context.map_size == "large" else 2
            return score, f"▲ MG-Nester dominieren Engpässe auf {context.map_size} Maps Score: {score}"
        return 0, "Kleine Maps benötigen keine MG-Nester"


class BunkerVPRule(Rule):
    def __init__(self):
        super().__init__("Bunkers essential for VP Defense")
    
    def evaluate(self, context):
        if context.ai_difficulty in ["hard", "expert"]:
            score = 4 if context.ai_difficulty == "expert" else 3
            return score, f"▲ Bunker gegen {context.ai_difficulty} AI zwingend Score: {score}"
        elif context.map_size == "large":
            return 2, "Große Maps brauchen Bunkers an Schlüsselpositionen"
        return 0, "Bunkers nicht primär erforderlich"


class MinefieldFlankRule(Rule):
    def __init__(self):
        super().__init__("Minefields protect Flanks")
    
    def evaluate(self, context):
        if context.map_size == "large":
            score = -3 if context.ai_difficulty == "expert" else -2
            return score, f"▼ Flanken ohne Minen auf {context.map_size} Maps riskant Score: {score}"
        return 0, "Kleine Maps haben geringe Flankenrisiken"


class ReconPriorityRule(Rule):
    def __init__(self):
        super().__init__("Recon for High-Value Targets")
    
    def evaluate(self, context):
        if context.player_count == 2:
            score = 3
            return score, f"▲ Recon für 2v2 Fuel-Scouting zwingend Score: {score}"
        elif context.map_size == "large":
            return 2, f"Recon auf {context.map_size} Maps für Sicht wichtig"
        return 0, "Recon nicht überdurchschnittlich erforderlich"


class TrenchLineRule(Rule):
    def __init__(self):
        super().__init__("Trench Lines for Forward Defense")
    
    def evaluate(self, context):
        if context.map_type in ["mixed", "urban"]:
            score = 3
            return score, f"▲ Gräben auf {context.map_type} Maps vor Strategic Points Score: {score}"
        return 0, "Open Maps benötigen keine Gräben"


class MortarSuppressionRule(Rule):
    def __init__(self):
        super().__init__("Mortars counter Green Cover")
    
    def evaluate(self, context):
        if context.map_type == "mixed":
            score = 2 + random.randint(0,1)
            return score, f"▲ Mortars gegen Green Cover auf {context.map_type} Maps Score: {score}"
        elif context.ai_difficulty == "easy":
            return 1, "Mortars gegen schwache AI effektiv"
        return 0, "Mortars nicht primär"


class ATGunnerCoverRule(Rule):
    def __init__(self):
        super().__init__("AT Guns need Cover")
    
    def evaluate(self, context):
        if context.ai_difficulty in ["hard", "expert"]:
            score = -2 - (context.player_count - 1)
            return score, f"▼ AT-Geschütze ohne Deckung gegen {context.ai_difficulty} AI verwundbar Score: {score}"
        return 0, "AT-Geschütze sicher gegen leichte AI"


class FuelRushEconomyRule(Rule):
    def __init__(self):
        super().__init__("Fuel Points determine Tech Race")
    
    def evaluate(self, context):
        if context.player_count == 2:
            score = 4
            return score, f"▲ Fuel-Rush für 2v2 Tech-Vorteil entscheidend Score: {score}"
        elif context.map_size == "large":
            return 3, f"Fuel-Kontrolle auf {context.map_size} Maps wichtig"
        return 0, "Fuel-Rush nicht zwingend erforderlich"
