import json
import csv
from pathlib import Path
import glob

RULES_FILE = Path("data/rules.json")
REPOS_DIR = Path("repos/smx-sprint-t2")
OUTPUT_FILE = Path("data/notes_smx.csv")


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def check_patterns(repo_path, patterns):

    for pattern in patterns:
        matches = glob.glob(str(repo_path / pattern))

        if matches:
            return True

    return False


def evaluate_repo(repo_path, rules):

    total = 0

    for rule_name, rule in rules.items():

        patterns = rule["patterns"]
        punts = rule["punts"]

        if check_patterns(repo_path, patterns):
            total += punts

    return total


def main():

    rules = load_json(RULES_FILE)

    results = []

    for repo in sorted(REPOS_DIR.iterdir()):

        if not repo.is_dir():
            continue

        print("Avaluant:", repo.name)

        nota = evaluate_repo(repo, rules)

        results.append({
            "repo": repo.name,
            "nota": nota
        })

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:

        writer = csv.DictWriter(
            f,
            fieldnames=["repo", "nota"]
        )

        writer.writeheader()

        for r in results:
            writer.writerow(r)

    print()
    print("Notes generades a:", OUTPUT_FILE)


if __name__ == "__main__":
    main()

