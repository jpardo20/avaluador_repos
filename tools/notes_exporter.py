import json
import csv
from core.rules_registry import RulesRegistry


def export_notes(corrections_file, repos_map_file, output_csv, output_md):

    with open(corrections_file) as f:
        corrections = json.load(f)

    with open(repos_map_file) as f:
        repos = json.load(f)

    rules = RulesRegistry()

    rules_ids = list(corrections.keys())

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
        for rule_id in rules_ids:

            nota = ras_data.get(rule_id, 0)

            rule = rules.get_rule(rule_id)

            if not rule:
                continue

            label = rule["nom"]

            row[label] = nota
            total += nota

        row["TOTAL"] = total

        rows.append(row)

        ras_labels = [
            rules.get_rule(rule_id)["nom"]
            for rule_id in rules_ids
            if rules.get_rule(rule_id)
        ]
    fieldnames = ["unitat", "alumne"] + ras_labels + ["TOTAL"]

    # CSV
    with open(output_csv, "w", newline="") as f:

        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    # Markdown
    with open(output_md, "w") as f:

        f.write("# Avaluació d'evidències del lliurament (SMX)\n\n")
        
        rule_names = [
            rules.get_rule(r)["nom"]
            for r in rules_ids
            if rules.get_rule(r)
        ]

        ra_labels = []

        for rule_id in rules_ids:

            rule = rules.get_rule(rule_id)

            if not rule:
                continue

            ra_pes = rule.get("ra_pes", {})

            ra_labels.append("+".join(ra_pes.keys()))

        header = "|" + "|".join(["Alumne"] + rule_names + ["TOTAL"]) + "|\n"
        sep = "|---|" + "|".join(["---:"] * (len(rule_names) + 1)) + "|\n"

        max_scores = [
            rules.get_rule(r)["max_score"]
            for r in rules_ids
            if rules.get_rule(r)
        ]

        max_total = sum(max_scores)

        max_row = (
            "| **MAX** | " +
            " | ".join(str(x) for x in max_scores) +
            f" | {max_total} |\n"
        )


        f.write(header)
        f.write(sep)
        ra_row = (
            "| **RA** | " +
            " | ".join(ra_labels) +
            " | |\n"
        )

        f.write(ra_row)
        f.write(max_row)


        for r in rows:

            vals = [
                str(r[rules.get_rule(rule_id)["nom"]])
                for rule_id in rules_ids
                if rules.get_rule(rule_id)
            ]

            f.write(
                f"| {r['alumne']} | " +
                " | ".join(vals) +
                f" | {r['TOTAL']} |\n"
            )