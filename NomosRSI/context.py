
class MapContext:
    def __init__(self, map_obj, player_count, ai_difficulty):
        """
        map_obj: z.B. aus Maps.examples
        player_count: int
        ai_difficulty: str
        """
        self.map_name = map_obj.name
        self.map_size = getattr(map_obj, "size", None)
        self.map_type = getattr(map_obj, "type", None)
        self.player_count = player_count
        self.ai_difficulty = ai_difficulty


class AnalysisReport:
    """
    Enthält Ergebnisse einer Map-Analyse (RuleSystem Output)
    """
    def __init__(self, map_context: MapContext, rule_results: list):
        """
        rule_results: [{'rule': 'RuleName', 'score': int, 'explanation': str}, ...]
        """
        self.map_context = map_context
        self.rule_results = rule_results

    @property
    def total_score(self):
        return sum(r['score'] for r in self.rule_results)
