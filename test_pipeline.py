from core.repos_locator import ReposLocator
from core.repo_scanner import RepoScanner
from core.rule_engine import RuleEngine


def main():

    print("\n=== TEST PIPELINE ===\n")

    locator = ReposLocator("data/repos_map.json")
    scanner = RepoScanner()
    rule_engine = RuleEngine()

    units = locator.get_all_units()

    for unit in units:

        repo_path = locator.get_repo_path(unit)

        print(f"\nUnitat: {unit}")
        print(f"Repo: {repo_path}")

        inventory = scanner.scan_repo(repo_path)

        result = rule_engine.evaluate(
            repo_path,
            inventory,
            "05_comunicacio/correu_enviat.png",
            "image"
        )

        print("Resultat:", result)


if __name__ == "__main__":
    main()