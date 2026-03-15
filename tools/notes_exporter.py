import json
import csv
from core.rules_registry import RulesRegistry


def export_notes(corrections_file, repos_map_file, output_csv, output_md):

    with open(corrections_file) as f:
        corrections = json.load(f)

    with open(repos_map_file) as f:
        repos = json.load(f)

    rules = RulesRegistry()

    ras = list(corrections.keys())

    # construir estructura per alumne
    per_unit = {}

    for ra, units in corrections.items():

        for unit, data in units.items():

            if unit not in per_unit:
                per_unit[unit] = {}

            per_unit[unit][ra] = data["nota"]

    rows = []

    for unit, ras_data in per_unit.items():

        nom = repos.get(unit, {}).get("nom", "")
        cognoms = repos.get(unit, {}).get("cognoms", "")
        alumne = f"{nom} {cognoms}".strip()

        row = {
            "unitat": unit,
            "alumne": alumne
        }

        total = 0

        for ra in ras:

            nota = ras_data.get(ra, 0)
            label = rules.get_rule(ra)["nom"]
            row[label] = nota
            total += nota

        row["TOTAL"] = total

        rows.append(row)

    ras_labels = [rules.get_rule(ra)["nom"] for ra in ras]

    fieldnames = ["unitat", "alumne"] + ras_labels + ["TOTAL"]

    # CSV
    with open(output_csv, "w", newline="") as f:

        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    # Markdown
    with open(output_md, "w") as f:

        f.write("# Avaluació d'evidències del lliurament (SMX)\n\n")
        
        header = "| Alumne | " + " | ".join(ras_labels) + " | TOTAL |\n"
        sep = "|---" * (len(ras) + 2) + "|\n"

        f.write(header)
        f.write(sep)

        for r in rows:

            vals = [str(r[rules.get_rule(ra)["nom"]]) for ra in ras]

            f.write(
                f"| {r['alumne']} | " +
                " | ".join(vals) +
                f" | {r['TOTAL']} |\n"
            )