import json
import csv


def export_notes(corrections_file, repos_map_file, output_csv, output_md):

    with open(corrections_file) as f:
        corrections = json.load(f)

    with open(repos_map_file) as f:
        repos = json.load(f)

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
            row[ra] = nota
            total += nota

        row["TOTAL"] = total

        rows.append(row)

    fieldnames = ["unitat", "alumne"] + ras + ["TOTAL"]

    # CSV
    with open(output_csv, "w", newline="") as f:

        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    # Markdown
    with open(output_md, "w") as f:

        f.write("# Notes SMX per RA\n\n")

        header = "| Alumne | " + " | ".join(ras) + " | TOTAL |\n"
        sep = "|---" * (len(ras) + 2) + "|\n"

        f.write(header)
        f.write(sep)

        for r in rows:

            vals = [str(r[ra]) for ra in ras]

            f.write(
                f"| {r['alumne']} | " +
                " | ".join(vals) +
                f" | {r['TOTAL']} |\n"
            )