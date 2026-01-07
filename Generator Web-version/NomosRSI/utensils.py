class SpeechGenerator:
    """
    Erzeugt taktische Missionsberatung aus AnalysisReports
    """

    def generate_strategy_advice(self, report):
        context = report.map_context

        # --- Einordnung ---
        intro = (
            f"Analyse der OHL.\n"
            f"Schlachtfeld: {context.map_name}\n"
            f"Spieler: {context.player_count} | "
            f"KI-Schwierigkeit: {context.ai_difficulty.capitalize()}\n\n"
        )

        # --- Relevante Regeln filtern & sortieren ---
        impactful_rules = [
            r for r in report.rule_results if r["score"] != 0
        ]
        impactful_rules.sort(key=lambda r: abs(r["score"]), reverse=True)

        # --- Kernaussage ableiten ---
        total = report.total_score
        if total > 10:
            posture = "Diese Mission erfordert einen aggressiven und blitzschnellen Spielstil."
        elif 4 <= total <= 10:
            posture = "Diese Mission begünstigt einen kontrollierten, strukturierten Spielstil."
        elif total >= 4:
            posture = "Diese Mission begünstigt einen ausgewogenen, taktischen Spielstil."
        elif total <= -3:
            posture = "Diese Mission ist riskant – defensive Planung ist entscheidend."
        else:  # -2, -1, 0, 1, 2, 3
            posture = "Diese Mission ist ausgeglichen, Flexibilität wird entscheidend sein."

        body = posture + "\n\n"

        # --- Wichtigste Gründe (max. 3) ---
        if impactful_rules:
            body += "Entscheidende Faktoren:\n"
            for r in impactful_rules[:16]:
                direction = "▲" if r["score"] > 0 else "▼"
                body += f" {direction} {r['explanation']}\n"
        else:
            body += "Keine signifikanten strategischen Einschränkungen erkannt.\n"

        # --- Schlussfolgerung ---
        conclusion = (
            f"\nEmpfohlene Gesamtausrichtung:\n"
            f"→ Missionsbewertung: {report.total_score}\n"
            f"→ Fokus auf Anpassungsfähigkeit und Informationskontrolle.\n"
        )

        return intro + body + conclusion
