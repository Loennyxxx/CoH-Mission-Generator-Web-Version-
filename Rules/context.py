class Context:
    def __init__(self, map_obj=None, player_count=None, ai_difficulty=None):
        """
        map_obj: Map-Instanz
        player_count: int
        ai_difficulty: str
        """
        self.map_size = map_obj.size if map_obj else None
        self.map_type = map_obj.map_type if map_obj else None
        self.map_name = map_obj.name if map_obj else None
        self.player_count = player_count
        self.ai_difficulty = ai_difficulty
