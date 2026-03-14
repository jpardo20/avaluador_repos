from core.repos_locator import ReposLocator
from core.repo_scanner import RepoScanner
from core.rule_engine import RuleEngine
from core.correction_navigator import CorrectionNavigator
from core.correction_registry import CorrectionRegistry
from core.rules_registry import RulesRegistry

def main():

    print("\n=== AVALUADOR DE REPOSITORIS ===\n")

    # Inicialitzar components

    locator = ReposLocator("data/repos_map.json")
    scanner = RepoScanner()
    engine = RuleEngine()
    navigator = CorrectionNavigator(locator, scanner, engine)
    registry = CorrectionRegistry()

    rules = RulesRegistry()

    units = locator.get_all_units()

    for unit in units:

        repo = locator.get_repo_path(unit)

        print(f"\n================================")
        print(f"Unitat: {unit}")
        print(f"Repo: {repo}")
        print(f"================================")

        files = scanner.scan_repo(repo)

        ra = "AE05"

        rule = rules.get_rule(ra, unit)

        expected_path = rule["expected_path"]
        evidence_type = rule["type"]

        result = engine.evaluate(repo, files, expected_path, evidence_type)

        unitat = unit

        print(f"\nUnitat: {unitat}")
        print(f"Resultat: {result}")

        # mirar si ja està corregit
        existing = registry.get_correction(ra, unitat)

        if existing:
            print("Ja corregit:")
            print(existing)
            continue

        # assignació automàtica simple
        if result["status"] == "exact_match":
            nota = 2
            comentari = "evidència correcta"

        elif result["status"] == "partial_match":
            nota = 1
            comentari = "evidència parcial"

        else:
            nota = 0
            comentari = "sense evidència"

        registry.set_correction(ra, unitat, nota, comentari)

        print("Correcció guardada:")
        print({
            "nota": nota,
            "comentari": comentari
        })


if __name__ == "__main__":
    main()