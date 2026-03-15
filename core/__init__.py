class RulesRegistry:

    def __init__(self, rules_file="data/rules.json"):

        with open(rules_file, "r") as f:
            data = json.load(f)

        self.config = data.get("config", {})
        self.rules = data.get("rules", {})

        # aplicar valors per defecte
        default_points = self.config.get("default_points", 1)
        default_penalty = self.config.get("default_structure_penalty", 0)

        for rule_id, rule in self.rules.items():

            rule.setdefault("max_score", default_points)
            rule.setdefault("structure_penalty", default_penalty)
            rule.setdefault("extensions", [])
            rule.setdefault("ra_pes", {})