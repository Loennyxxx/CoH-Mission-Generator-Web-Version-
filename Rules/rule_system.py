class RuleSystem:
    def __init__(self):
        self.rules = []

    def add_rule(self, rule):
        self.rules.append(rule)

    def evaluate(self, context):
        results = []

        for rule in self.rules:
            score, explanation = rule.evaluate(context)
            results.append({
                "rule": rule.name,
                "score": score,
                "explanation": explanation
            })

        return results