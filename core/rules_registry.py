import json


class RulesRegistry:

    def __init__(self, rules_file="data/rules.json"):

        with open(rules_file, "r") as f:
            self.rules = json.load(f)

    def get_rule(self, ra, unit):

        if ra not in self.rules:
            return None

        if unit not in self.rules[ra]:
            return None

        return self.rules[ra][unit]