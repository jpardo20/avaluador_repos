import json
import csv
from pathlib import Path
import glob

RULES_FILE = Path("data/rules.json")
REPOS_DIR = Path("repos/smx-sprint-t2")
OUTPUT_FILE = Path("data/notes_smx.csv")
OUTPUT_MD = Path("data/notes_smx.md")
REPOS_MAP = Path("data/repos_map.json")



def load_repos_map():

    with open(REPOS_MAP, "r", encoding="utf-8") as f:
        data = json.load(f)

    mapping = {}

    for key, info in data.items():

        nom = info["nom"]
        cognoms = info["cognoms"]

        mapping[key] = f"{nom} {cognoms}"

    return mapping

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

    result = {}
    total = 0

    for rule_name, rule in rules.items():

        patterns = rule["patterns"]
        punts = rule["punts"]

        if check_patterns(repo_path, patterns):
            result[rule_name] = 1
            total += punts
        else:
            result[rule_name] = 0

    result["nota"] = total

    return result

def write_markdown(results, rules, output_file):

    headers = ["Alumne"] + list(rules.keys()) + ["Nota"]

    with open(output_file, "w", encoding="utf-8") as f:

        # capçalera
        f.write("| " + " | ".join(headers) + " |\n")
        f.write("|" + "|".join(["---"] * len(headers)) + "|\n")

        for r in results:

            alumne = r["repo"].replace("smx-sprint-t2-", "")

            row = [alumne]

            for rule in rules.keys():

                if r[rule] == 1:
                    row.append("✔")
                else:
                    row.append("✘")

            row.append(str(r["nota"]))

            f.write("| " + " | ".join(row) + " |\n")


def main():

    repos_map = load_repos_map()

    rules = load_json(RULES_FILE)

    results = []

    for repo in sorted(REPOS_DIR.iterdir()):

        if not repo.is_dir():
            continue

        print("Avaluant:", repo.name)

        nota = evaluate_repo(repo, rules)
        repo_key = repo.name.replace("smx-sprint-t2-", "")

        alumne = repos_map.get(repo_key, repo_key)

        row = {"repo": alumne}
        row.update(nota)
        results.append(row)


    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:

        writer = csv.DictWriter(
            f,
            fieldnames=["repo"] + list(rules.keys()) + ["nota"]
        )

        writer.writeheader()

        for r in results:
            writer.writerow(r)

    print()
    print("Notes generades a:", OUTPUT_FILE)

    write_markdown(results, rules, OUTPUT_MD)


if __name__ == "__main__":
    main()

