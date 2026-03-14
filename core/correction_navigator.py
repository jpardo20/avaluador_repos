class CorrectionNavigator:
    """
    Controla el flux de navegació de la correcció.

    Mode B:
    RA → unitats → evidències
    """

    def __init__(self, locator, scanner, rule_engine):
        self.locator = locator
        self.scanner = scanner
        self.rule_engine = rule_engine

    def run(self, ras):

        units = self.locator.get_all_units()

        for ra in ras:

            ra_id = ra["id"]
            expected_path = ra["expected_path"]
            evidence_type = ra["type"]

            print("\n================================")
            print(f"RA {ra_id}")
            print("================================")

            for unit in units:

                repo_path = self.locator.get_repo_path(unit)

                inventory = self.scanner.scan_repo(repo_path)

                result = self.rule_engine.evaluate(
                    repo_path,
                    inventory,
                    expected_path,
                    evidence_type
                )

                print(f"\nUnitat: {unit}")
                print("Resultat:", result)
                