class Rule:
    def __init__(self, name):
        self.name = name

    def evaluate(self, context):
        """
        Returns:
            score (int): positive = spricht dafür, negativ = dagegen
            explanation (str): warum
        """
        raise NotImplementedError
