#!/usr/bin/env python3

from core.repos_locator import ReposLocator
from core.repo_scanner import RepoScanner
from core.rule_engine import RuleEngine
from core.correction_navigator import CorrectionNavigator


ras = [
    {
        "id": "AE05",
        "expected_path": "05_comunicacio/correu_enviat.png",
        "type": "image"
    }
]


def main():

    print("\n=== AVALUADOR DE REPOSITORIS ===\n")

    locator = ReposLocator("data/repos_map.json")
    scanner = RepoScanner()
    rule_engine = RuleEngine()

    navigator = CorrectionNavigator(
        locator,
        scanner,
        rule_engine
    )

    navigator.run(ras)


if __name__ == "__main__":
    main()