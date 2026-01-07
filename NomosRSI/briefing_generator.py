# briefing_generator.py (KOMPLETT mit ALLEN 16 Rules)
import random
import re

class BriefingGenerator:
    def __init__(self):
        # Difficulty Templates
        self.difficulty_templates = {
            "easy": [
                "schwache Feindeinheit mit schlechter Moral",
                "grüne Rekruten ohne Kampferfahrung", 
                "überschaubare Kräfte mit schwacher Führung"
            ],
            "normal": [
                "solide Einheit mit durchschnittlicher Ausbildung",
                "ausgeglichene Kräfte in Standardformation", 
                "reguläre Truppen ohne besondere Vorbereitung"
            ],
            "hard": [
                "harte Feindeinheit mit Kampferfahrung",
                "Elite-Gegner mit überlegener Ausrüstung",
                "überlegene Kräfte mit starker Befehlsstruktur"
            ],
            "expert": [
                "fanatische Eliteeinheit mit Todesverachtung",
                "Veteranen mit jahrelanger Kampfpraxis",
                "Todesschwadron mit besonderer Härte"
            ]
        }
        
        # Style Templates
        self.style_templates = {
            "defensive": [
                "sichert eure Flanken mit Bunkern und MG-Nestern",
                "Position halten und den Feind zermürben", 
                "defensive Linie aufbauen, Ausdauer siegen lassen"
            ],
            "aggressive": [
                "sofortiger Vorstoß, keine Rücksicht!", 
                "Feind überrennen mit konzentriertem Druck",
                "Blitzangriff ohne Zögern durchführen"
            ],
            "control": [
                "Sichtlinien mit Aufklärern sichern",
                "Map-Kontrolle durch strategische Punkte",
                "Informationsüberlegenheit schaffen"
            ]
        }
        
        # **KOMPLETTES TACTIC SYSTEM für alle 16 Rules**
        self.tactic_templates = {
            # Bestehende Rules
            "artillery": [
                "Artillerie früh aufbauen für maximale Reichweite", 
                "Feuerunterstützung über offene Flächen lenken",
                "Gegner mit Bombardements weichklopfen"
            ],
            "infantry": [
                "Infanterie in Wellen vorantreiben",
                "Mann-gegen-Mann-Kampf im Nahbereich suchen",
                "Rush mit Granatwerfern und Bajonett"
            ],
            "vehicles": [
                "Panzerkeil durch feindliche Linien brechen",
                "Flankenangriffe mit gepanzerten Speerspitzen",
                "Fahrzeug-Synergie für Durchbruchsoperation"
            ],
            
            # LargeMapDefensiveRule
            "large_map_defensive": [
                "Große Flächen mit Defensive und Map Control dominieren",
                "Ausgedehnte Front mit Bunker und Artillerie sichern",
                "Langsame Expansion durch strategische Kontrolle"
            ],
            
            # UrbanMapInfantryRule  
            "urban_infantry": [
                "Infanterie dominiert urbane Engpässe",
                "Fahrzeuge eingeschränkt - Infanterie-Wellen schicken",
                "Haus-zu-Haus-Kampf mit Granatwerfern"
            ],
            
            # ExpertAICautionRule
            "expert_caution": [
                "Expert-AI bestraft frühe Aggression - Geduld",
                "Langsame Aufbau-Phase gegen smarte Gegner",
                "Keine vorschnellen Angriffe - AI kontert perfekt"
            ],
            
            # EasyAIExperimentRule
            "easy_experiment": [
                "Einfache AI erlaubt riskante Experimente",
                "Testet neue Taktiken ohne große Gefahr",
                "Early Game für Tech-Versuche nutzen"
            ],
            
            # TwoPlayerSynergyRule
            "two_player_synergy": [
                "Rollenverteilung mit Partner: einer hält, einer greift",
                "Team-Synergie durch Spezialisierung",
                "Koordinierter 2v2-Aufbau"
            ],
            
            # MultiPlayerMapControlRule
            "multiplayer_control": [
                "Map Control bei vielen Spielern zwingend",
                "Strategic Points früh sichern",
                "Multi-Front-Krieg durch Kontrolle vermeiden"
            ],
            
            # NoEarlyLightVehicleRule
            "no_early_vehicles": [
                "Frühe Light Vehicles riskant - Infanterie zuerst",
                "AI bestraft Halftracks und Jeeps hart",
                "Tech erst nach Stabilisierung"
            ],
            
            # LateGameArtilleryRule
            "late_artillery": [
                "Spätgame-Artillerie dominiert große Maps",
                "Teamplay verstärkt Artillerie-Effekt",
                "Langfristige Feuerunterstützung planen"
            ],
            
            # MGNestChokeRule
            "mg_nest": [
                "MG-Nester an Engpässen bauen",
                "Vickers/MG42 für Suppression nutzen", 
                "Maschinengewehr-Feuerlanzen schaffen"
            ],
            
            # BunkerVPRule
            "bunker": [
                "Bunker an VPs und Fuel Points",
                "Verstärkte Positionen mit Offizier halten",
                "Bunker-Traps mit Demo Charges"
            ],
            
            # MinefieldFlankRule
            "mines": [
                "Minen vor MG-Nestern legen",
                "Anti-Tank-Minen an Flanken",
                "Minefields für Mobile Defense"
            ],
            
            # ReconPriorityRule
            "recon": [
                "Aufklärer für Sicht und Prioritätstargets",
                "Scouts hinter feindliche Linien",
                "Recon für Artillery Spotting"
            ],
            
            # TrenchLineRule
            "trenches": [
                "Gräben vor Strategic Points",
                "Tommy Trenches mit Rifle Grenades",
                "Defensive Linie mit Officers"
            ],
            
            # MortarSuppressionRule
            "mortar": [
                "Mortar hinter Deckung für Smoke/Suppression",
                "Gegner aus Green Cover rauchen",
                "Mortar für Anti-Infantry"
            ],
            
            # ATGunnerCoverRule
            "at_gun": [
                "AT-Geschütze mit Deckung schützen",
                "Pak40/AT-Gun an Panzerwegen",
                "Flak36 für duale Bedrohung"
            ],
            
            # FuelRushEconomyRule
            "fuel_rush": [
                "Fuel Points priorisieren für Tech-Rush",
                "Schnelle Panzer sofort zu den Fuel-Caps",
                "Wirtschaftskampf durch Fuel dominieren"
            ]
        }
        
        self.closing_phrases = [
            # **DIREKTE BEFEHLE**
            "Kämpft mit eisernem Willen und tretet keinen Schritt zurück!",
            "Vorwärts mit aller Härte - der Feind bricht!",
            "Angriff ohne Erbarmen - Sieg oder Tod!",
            "Sturmangriff jetzt - keine Gefangenen!",
            
            # **DISZIPLIN & EHRE**
            "Sieg durch Disziplin und unerbittliche Präzision.",
            "Ehre und Pflicht fordern den totalen Sieg!",
            "Der Sieg gehört den Unbeugsamen!",
            "Pflicht und Ehre siegen über alles!",
            
            # **FÜHRUNG & GEHORSAM**
            "Führt meine Befehle aus - der Sieg ist gewiss!",
            "Befehle befolgen, Feind vernichten!",
            "Disziplin siegt - führt aus ohne Zögern!",
            "Kommandos ausführen - zum Sieg!",
            
            # **SCHICKSAL & BESTIMMUNG**
            "Das Schicksal ruft - der Sieg erwartet euch!",
            "Die Götter fordern Sieg - erobert ihn!",
            "Euer Schicksal ist Sieg - nehmt es!",
            "Bestimmung ruft - der Feind fällt!",
            
            # **KAMPFESWILLE**
            "Mit eiserner Härte und Todesverachtung!",
            "Unbeugsamer Wille erzwingt den Sieg!",
            "Kämpft wie Löwen - der Sieg ist euer!",
            "Unerbittlich voran - bis zum letzten Mann!",
            
            # **PATRIOTISMUS**
            "Für das Vaterland - keine Kompromisse!",
            "Blut für die Heimat - Sieg für das Reich!",
            "Ehre dem Vaterland - Tod dem Feind!",
            "Für Volk und Vaterland - totaler Sieg!",
            
            # **VERGLEICHE & MOTIVATION**
            "Wie Hannibal über die Alpen - zum Sieg!",
            "Wie Rommel in der Wüste - unaufhaltsam!",
            "Kursk neu schreiben - totaler Sieg!",
            "Stalingrad rächen - siegt jetzt!",
            
            # **AKTIONSORIENTIERT**
            "Vorwärts brechen - die Stellung halten!",
            "Angriff - Durchbruch - Sieg!",
            "Sturm - Eroberung - Herrschaft!",
            "Feind zermalmen - Position sichern!"
        ]

        # **NEUE FÜLLSATZ-SYSTEME** (AB Zeile 10 in __init__ HINZUFÜGEN)
        self.connectors = {
            "intro_connect": [
                "In dieser Schlacht treffen wir auf"
            ],
            "defensive_lead": [
                "Verteidigung dominiert diese Schlacht",
                "Festungen sind der Schlüssel zum Sieg",
                "Positionen sichern entscheidet alles",
                "Ausdauer schlägt feindliches Tempo",
                "Die Defensive bildet unsere Stärke",
                "Befestigungen gewinnen diesen Krieg",
                "Haltet die Stellung - der Feind zerbricht",
                "Verteidigung ist Angriffs beste Waffe"
            ],
            
            "offensive_lead": [
                "Der Angriff trägt den Sieg",
                "Mobilität entscheidet diesen Kampf",
                "Schnelligkeit übertrumpft feindliche Masse",
                "Der Vorstoß ist überlebenswichtig",
                "Offensive ist die einzige Sprache",
                "Blitzkrieg bricht jeden Widerstand",
                "Angriff siegt über jede Verteidigung",
                "Vorwärtskampf erzwingt den Durchbruch"
            ],
            
            "comparison": [
                "Hannibal über die Alpen",
                "Stalingrad 1942",
                "Kursk 1943",
                "Rommel in der Wüste",
                "Monte Cassino 1944",
                "Waterloo 1815",
                "Sedan 1870",
                "Verdun 1916"
            ],
            
        "conditionals": [
            "Solange die Flanken gesichert bleiben hält uns nichts auf",
            "Vorausgesetzt Artillerie deckt wird der Sieg unser sein",
            "Wenn Fuel frühzeitig gekappt wird bricht der Feind zusammen", 
            "Bei konsequenter Befehlsausführung ist Niederlage unmöglich",
            "Unter ständiger Aufklärung findet uns der Feind niemals",
            "Bei präziser Feuerunterstützung zermalmen wir den Widerstand",
            "Wenn Nachschub gesichert ist hält unsere Offensive ewig",
            "Unter einheitlicher Führung werden wir unaufhaltsam",
            
            "Solange MG-Nester stehen bleibt der Feind im Kugelhagel",
            "Vorausgesetzt die Bunker halten, dann bricht kein Angriff durch",
            "Wenn Recon die Feindlinien kennt schlagen wir blind zu",
            "Bei perfekter Koordination zerreißen wir ihre Front",
            
            "Solange Fuel fließt rollen unsere Panzer unaufhaltsam",
            "Vorausgesetzt Infanterie folgt zerbrechen wir jeden Widerstand",
            "Wenn die Linie hält zermürben wir den Feind tot",
            "Unter eiserner Disziplin siegt der stärkere Wille"
            ]
        }

        self.phrase_expander = {
            "defensive": [
                # **KOMPLETTE SÄTZE - Positionierung & Feuerkraft**
                "Disziplinierte Feueraufstellung zerbricht jeden Angriff",
                "Geschickte Positionierung macht uns unangreifbar", 
                "Natürliche Deckungen werden zur tödlichen Falle",
                "Methodische Ausdauer zwingt den Feind in die Knie",
                
                # **Befestigungen & Ausdauer**
                "Undurchdringliche Bunker halten jeden Sturm ab",
                "MG-gesicherte Stellungen werden zum Grab des Feindes",
                "Granaten und Minen vernichten jeden Vorstoß",
                "Zermürbende Verteidigung siegt über blinde Aggression",
                
                # **Führung & Disziplin**
                "Eiserne Kommandoführung erzwingt den Sieg",
                "Präzise Feuerlenkung richtet den Feind hin",
                "Perfekte Formation hält jeden Ansturm stand",
                "Unbeugsame Disziplin bricht jeden Widerstand"
            ],
            
            "offensive": [
                # **Angriffstempo & Durchbruch**
                "Erbarmungslose Präzision vernichtet den Feind",
                "Konzentrierte Schläge zerschlagen jede Verteidigung",
                "Geschlossene Formation durchbricht jede Linie",
                "Tempo und Überraschung machen uns unaufhaltsam",
                
                # **Feuerkraft & Manöver**
                "Artillerie-Feuerschutz ebnet unseren Weg",
                "Panzerkeile zermalmen feindliche Stellungen",
                "Flankenangriffe entscheiden die Schlacht",
                "Bajonett und Granate räumen jeden Widerstand weg",
                
                # **Führung & Aggression**
                "Blitzschneller Vorstoß lässt keine Zeit zum Atmen",
                "Gnadenlose Offensive kennt kein Erbarmen",
                "Eiserner Angriffswille erzwingt den Sieg",
                "Unerbittliche Durchschlagskraft bricht alles"
            ],
            
            "recon": [
                "Vorauseilende Aufklärung macht uns allwissend",
                "Ständige Feindbeobachtung verhindert Überraschungen", 
                "Überlegene Sichtkontrolle gewinnt jedes Gefecht",
                "Präzise Zielaufklärung lenkt tödliches Feuer"
            ],
            
            "economy": [
                "Frühzeitige Fuel-Sicherung sichert unsere Überlegenheit",
                "Dominierende Ressourcenkontrolle erzwingt den Sieg",
                "Wirtschaftliche Überlegenheit erschlägt den Feind",
                "Tech-Vorsprung macht uns unaufhaltsam"
            ],
            
            "ai_caution": [
                "Äußerste Vorsicht besiegt jede Falle",
                "Gegen smarte Gegner gewinnt Geduld",
                "Permanente Wachsamkeit überlebt jeden Trick",
                "Geduldiges Aufbauspiel überlistet jede AI"
            ],
            
            "universal": [
                "Militärische Präzision schlägt jede Überzahl",
                "Taktische Überlegenheit erzwingt den Sieg", 
                "Konsequente Ausführung bricht jeden Widerstand",
                "Überlegene Gefechtsführung siegt immer"
            ]
        }

        self.grammar_rules = {
            "defensive": [
                "{ITEM} bildet eure Feuerlinie",
                "Mit {ITEM} haltet ihr die Stellung", 
                "{ITEM} sichert eure Positionen",
                "{ITEM} schützt eure Flanken"
            ],
            "offensive": [
                "{ITEM} eröffnet den Vorstoß", 
                "Durch {ITEM} brecht ihr durch",
                "{ITEM} führt zum Sieg",
                "{ITEM} erzwingt den Durchbruch"
            ],
            "recon": [
                "{ITEM} gewinnt entscheidende Sicht",
                "{ITEM} lokalisiert Prioritätstargets",
                "{ITEM} sichert eure Aufklärung"
            ]
        }

    def parse_rsi_output(self, map_name: str, advice: str):
        """Erweiterter Parser für alle Rules"""
        data = {
            "map": map_name,
            "players": "2",
            "difficulty": None,
            "style": None,
            "factors": [],
            "focus": None,
            "evaluation": None
        }
        
        lines = advice.strip().split('\n')
        for line in lines:
            line = line.strip()
            if "Schlachtfeld:" in line:
                data["map"] = line.split(":")[1].strip()
            elif "KI-Schwierigkeit:" in line:
                data["difficulty"] = line.split("KI-Schwierigkeit:")[1].strip()
            elif "begünstigt" in line.lower():
                data["style"] = line
            elif "▲" in line or "▼" in line:
                data["factors"].append(line)
            elif "Fokus auf" in line:
                data["focus"] = line.split("Fokus auf")[1].strip()
            elif "Missionsbewertung:" in line:
                data["evaluation"] = line.split(":")[1].strip()
        
        return data
    
    def generate_briefing(self, map_name: str, advice: str) -> str:
        data = self.parse_rsi_output(map_name, advice)
        
        # **SATZBAU-SYSTEM STARTET HIER** (ersetzt die 80 if-elif Zeilen)
        
        # 1. TOP-3 Faktoren extrahieren (nach Impact)
        factors = self._extract_top_factors(data["factors"])
        clusters = self._cluster_factors(factors)
        
        # 2. NOMOS kohärent sprechen lassen
        briefing = self._build_nomos_speech(data, clusters)
        
        return briefing

    def _extract_top_factors(self, factors):
        """Extrahiert Top-3 nach Score-Impact"""
        scored = []
        for factor in factors:
            # Score aus Text extrahieren (z.B. "Score: 4" → 4)
            import re
            score_match = re.search(r'Score:\s*([+-]?\d+)', factor)
            impact = int(score_match.group(1)) if score_match else 0
            scored.append({"text": factor, "impact": impact})
        return sorted(scored, key=lambda x: abs(x['impact']), reverse=True)[:3]

    def _cluster_factors(self, top_factors):
        """Gruppiert in Themen (Defensive/Offensive/AI)"""
        clusters = {
            'defensive': [],
            'offensive': [], 
            'ai_caution': [],
            'economy': []
        }
        
        for factor in top_factors:
            text = factor['text'].lower()
            if any(kw in text for kw in ['mg-nester', 'bunker', 'gräben', 'minen']):
                clusters['defensive'].append(factor['text'])
            elif any(kw in text for kw in ['recon', 'fuel-rush', 'infanterie']):
                clusters['offensive'].append(factor['text'])
            elif any(kw in text for kw in ['ai', 'expert', 'hard']):
                clusters['ai_caution'].append(factor['text'])
            elif 'fuel' in text:
                clusters['economy'].append(factor['text'])
        
        return clusters
    
    def _get_smart_expander(self, cluster_type, factor_text):
        """Wählt passenden phrase_expander basierend auf Inhalt"""
        text_lower = factor_text.lower()
        
        if cluster_type == 'defensive':
            return random.choice(self.phrase_expander["defensive"])
        elif cluster_type == 'offensive':
            return random.choice(self.phrase_expander["offensive"])
        elif cluster_type == 'economy':
            return random.choice(self.phrase_expander["economy"])
        elif 'ai' in text_lower or 'expert' in text_lower:
            return random.choice(self.phrase_expander["ai_caution"])
        elif 'recon' in text_lower or 'aufklärung' in text_lower:
            return random.choice(self.phrase_expander["recon"])
        else:
            return random.choice(self.phrase_expander["universal"])

    def _build_nomos_speech(self, data, clusters):
        """EPISCHES 10-12 Zeilen Briefing mit Füllsätzen, Vergleichen, Taktiken"""
        
        # 1. EPISCHE EINLEITUNG (2 Zeilen)
        difficulty = (data["difficulty"] or "normal").lower()
        intro = random.choice(self.difficulty_templates.get(difficulty, self.difficulty_templates["normal"]))
        lead_in = random.choice(self.connectors["intro_connect"])
        
        speech = f"NOMOS BEFIEHLT:\nAuf der Map: {data['map']}. {lead_in} {intro}."
        speech += f"\nDie Schlacht ähnelt {random.choice(self.connectors['comparison'])}."
        
        # 2. DEFENSIVE BLOCK (2-3 Zeilen mit Füllsätzen)
        if clusters['defensive']:
            def_items = [self._clean_factor(item) for item in clusters['defensive']]
            def_lead = random.choice(self.connectors["defensive_lead"])
            def_fill = self._get_smart_expander('defensive', def_items[0] if def_items else '')
            def_tactic = random.choice(self.tactic_templates["bunker"])
            
            speech += f" {def_lead}. {self._rich_connect(def_items)}. {def_fill}."
            speech += f"\n{def_tactic}!"
        
        # 3. OFFENSIVE BLOCK (2-3 Zeilen mit Füllsätzen)
        if clusters['offensive']:
            off_items = [self._clean_factor(item) for item in clusters['offensive']]
            off_lead = random.choice(self.connectors["offensive_lead"])
            off_fill = random.choice(self.phrase_expander["offensive"])
            off_tactic = random.choice(self.tactic_templates["fuel_rush"])
            
            speech += f"\n{off_lead}. {self._rich_connect(off_items)}. {off_fill}!"
            speech += f"\n{off_tactic}!"
        
        # 4. AI-GEFARH (1-2 Zeilen)
        if clusters['ai_caution']:
            ai_items = [self._clean_factor(item) for item in clusters['ai_caution']]
            ai_tactic = random.choice(self.tactic_templates["expert_caution"])
            conditional = random.choice(self.connectors["conditionals"])
            
            speech += f"\nGefahr: {self._rich_connect(ai_items)}. {conditional}."
            speech += f"\n{ai_tactic}."
        
        # 5. BEWERTUNG (1 Zeile)
        if data["evaluation"]:
            score = data["evaluation"].strip()
            if any(str(x) in score for x in [4, 5]):
                speech += "\nVICTORIA PROXIMA - Die Götter stehen zu uns!"
            elif any(str(x) in score for x in [-4, -5]):
                speech += "\nPERICULUM MAXIMUM - Jeder Fehler wird bestraft!"
            else:
                speech += "\nAUSDAUER ENTSCHEIDET - Geduld siegt über Hast!"
        
        # 6. EPISCHER SCHLUSS (1-2 Zeilen)
        closing = random.choice(self.closing_phrases)
        final_fill = random.choice(self.connectors["conditionals"])
        speech += f"\n\n{closing} {final_fill}."
        
        return speech

    def _get_difficulty_intro(self, data):
        """Saubere Difficulty-Auswahl"""
        difficulty = (data["difficulty"] or "normal").lower()
        return random.choice(self.difficulty_templates.get(difficulty, self.difficulty_templates["normal"]))

    def _rich_connect(self, items):
        """KOHÄRENTE VERBINDUNG - KEIN 'steht im Zentrum' mehr!"""
        if not items:
            return ""
        if len(items) == 1:
            return items[0]
        return f"{', '.join(items[:-1])} und {items[-1]}"

    def _clean_factor(self, factor_text):
        """'Gräben auf urban Maps vor Strategic Points. Score: 3' → 'Gräben vor Strategic Points'"""
        factor_text = re.sub(r'▲|▼|Score:\s*[+-]?\d+', '', factor_text).strip()
        factor_text = re.sub(r'\s+', ' ', factor_text)  # Multiple Spaces
        return factor_text.capitalize()
    
    def _capitalize_sentences(self, text):
        """Macht nach JEDEM Punkt den nächsten Buchstaben groß"""
        
        # Split nach Punkten, Leerzeichen trimmen, Großschreibung
        sentences = re.split(r'(?<=[.!?])\s+', text.strip())
        capitalized = [sentence[0].upper() + sentence[1:] if sentence else '' for sentence in sentences]
        
        return '. '.join(capitalized).strip()