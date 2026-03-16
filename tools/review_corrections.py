#!/usr/bin/env python3

import json
import subprocess
from pathlib import Path

CORRECTIONS_FILE = Path("data/corrections.json")
RULES_FILE = Path("data/rules.json")

def load_rules():
    with open(RULES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)["rules"]

def open_file(filepath):
    try:
        subprocess.run(
            ["xdg-open", filepath],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    except Exception:
        pass


def load_corrections():
    with open(CORRECTIONS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_corrections(data):
    with open(CORRECTIONS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def review_entry(ra, alumne, entry, rules):

    expected = rules.get(ra, {}).get("expected_files", [])
    alternatives = entry.get("alternatives", [])

    if not alternatives:
        return entry

    print("\n====================================")
    print(f"RA: {ra}")
    print(f"Alumne: {alumne}")
    print("\n------------------------------------")

    if expected:
        print("Evidència esperada:")
        for f in expected:
            print("  ", f)
    print("====================================\n")

    print("Mostrant alternatives...\n")

    for i, alt in enumerate(alternatives, start=1):

        print(f"{i}/{len(alternatives)}  {alt}")

        open_file(alt)

        input("ENTER → següent")

    print("\nQuin fitxer és correcte?\n")

    for i, alt in enumerate(alternatives, start=1):
        print(f"[{i}] {alt}")

    print("[0] cap és correcte")

    while True:
        try:
            choice = int(input("\nSelecció: "))
            if 0 <= choice <= len(alternatives):
                break
        except ValueError:
            pass

    if choice == 0:

        entry["nota"] = 0
        entry["comentari"] = input("Comentari: ")
        entry["status"] = "manual_no_evidence"

        return entry

    selected = alternatives[choice - 1]

    while True:
        try:
            nota = float(input("Nota: "))
            break
        except ValueError:
            pass

    comentari = input("Comentari: ")

    entry["nota"] = nota
    entry["comentari"] = comentari
    entry["status"] = "manual_review"
    entry["file"] = selected

    return entry


def main():

    data = load_corrections()
    rules = load_rules()

    revisats = 0

    for ra, alumnes in data.items():

        for alumne, entry in alumnes.items():

            if entry.get("status") == "alternatives":

                updated = review_entry(ra, alumne, entry, rules)

                data[ra][alumne] = updated

                revisats += 1

    save_corrections(data)

    print("\n================================")
    print(f"Revisions fetes: {revisats}")
    print("corrections.json actualitzat")
    print("================================")


if __name__ == "__main__":
    main()