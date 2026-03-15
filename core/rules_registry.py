import json


class RulesRegistry:

    def __init__(self, rules_file="data/rules.json"):

        with open(rules_file, "r") as f:
            data = json.load(f)

            self.config = data["config"]
            self.rules = data["rules"]

    def get_rule(self, ra, unit=None):

        if ra not in self.rules:
            return None

        return self.rules[ra]