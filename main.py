from core.repos_locator import ReposLocator
from core.repo_scanner import RepoScanner
from core.rule_engine import RuleEngine
from core.correction_navigator import CorrectionNavigator
from core.correction_registry import CorrectionRegistry
from core.rules_registry import RulesRegistry
from tools.notes_exporter import export_notes
from tools.feedback_exporter import export_feedback

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

        for ra in rules.rules:

            rule = rules.get_rule(ra)

            nom_regla = rule.get("nom", ra)

            print("Regla:", nom_regla)
            print("ID:", ra)

            print("RULE:", rule)

            if not rule:
                continue

            expected_path = rule["expected_files"][0]
            extensions = rule.get("extensions", [])

            evidence_type = "document"

            result = engine.evaluate(repo, files, expected_path, extensions)

            unitat = unit

            print(f"\nUnitat: {unitat}")
            print(f"Resultat: {result}")

            # mirar si ja està corregit
            existing = registry.get_correction(ra, unitat)

            if existing:
                print("Ja corregit:")
                print(existing)
                continue

            max_score = rule.get("max_score", 1)

            # assignació automàtica simple
            if result["status"] == "exact_match":
                nota = max_score
                comentari = "evidència correcta"

            elif result["status"] == "alternatives":
                if rules.config.get("allow_partial_credit", False):
                    nota = max_score / 2
                    comentari = "evidència parcial"
                else:
                    nota = 0
                    comentari = "evidència no vàlida"

            else:
                nota = 0
                comentari = "sense evidència"

            registry.set_correction(
                ra,
                unitat,
                nota,
                comentari,
                result
            )

            print("Correcció guardada:")
            print({
                "nota": nota,
                "comentari": comentari
            })

    print("\n=== Generant informes finals ===\n")

    export_notes(
        corrections_file="data/corrections.json",
        repos_map_file="data/repos_map.json",
        output_csv="data/notes_smx.csv",
        output_md="data/notes_smx.md"
    )

    print("✔ notes_smx.csv generat")
    print("✔ notes_smx.md generat")

    export_feedback(
        corrections_file="data/corrections.json",
        repos_map_file="data/repos_map.json",
        output_md="data/feedback_smx.md"
    )

    print("✔ feedback_smx.md generat")

if __name__ == "__main__":
    main()