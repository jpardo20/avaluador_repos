import json
from core.rules_registry import RulesRegistry


def export_feedback(corrections_file, repos_map_file, output_md):

    with open(corrections_file) as f:
        corrections = json.load(f)

    with open(repos_map_file) as f:
        repos = json.load(f)

    rules = RulesRegistry()

    rules_ids = list(corrections.keys())

    # reorganitzar dades per alumne
    per_unit = {}

    for ra, units in corrections.items():

        for unit, data in units.items():

            if unit not in per_unit:
                per_unit[unit] = {}

            per_unit[unit][ra] = data

    with open(output_md, "w") as f:

        f.write("# Informe detallat per alumne\n\n")

        for unit, ras_data in per_unit.items():

            nom = repos.get(unit, {}).get("nom", "")
            cognoms = repos.get(unit, {}).get("cognoms", "")
            alumne = f"{nom} {cognoms}".strip()

            f.write(f"## {alumne}\n\n")

            f.write("| Evidència | Estat | Fitxer detectat | Nota |\n")
            f.write("|---|---|---|---|\n")

            for rule_id in rules_ids:

                rule = rules.get_rule(rule_id)

                if not rule:
                    continue

                label = rule["nom"]
                max_score = rule.get("max_score", 1)

                entry = ras_data.get(rule_id)

                if not entry:
                    continue

                nota = entry.get("nota", 0)
                status = entry.get("status", "")

                file_detected = entry.get("file")

                if file_detected:
                    file_detected = file_detected.split("/")[-1]
                else:
                    alts = entry.get("alternatives", [])
                    if alts:
                        file_detected = alts[0].split("/")[-1]
                    else:
                        file_detected = ""

                f.write(
                    f"| {label} | {status} | {file_detected} | {nota} / {max_score} |\n"
                )

            f.write("\n")