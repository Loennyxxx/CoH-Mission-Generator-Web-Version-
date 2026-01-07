
class Map:
    def __init__(self, name, size, map_type):
        """
        name: str, z. B. "Angoville"
        size: str, "small" | "medium" | "large"
        map_type: str, "urban" | "open" | "mixed"
        """
        self.name = name
        self.size = size
        self.map_type = map_type

    def __repr__(self):
        return f"<Map {self.name} | {self.size} | {self.map_type}>"
