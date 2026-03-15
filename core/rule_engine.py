from pathlib import Path


class RuleEngine:
    """
    Compara l'evidència esperada amb els fitxers trobats al repositori.
    """

    TYPE_MAP = {
        "image": "images",
        "document": "documents",
        "spreadsheet": "spreadsheets",
        "presentation": "presentations"
    }

    def evaluate(self, repo_path, inventory, expected_path, evidence_extensions):
        """
        Avalua si existeix l'evidència esperada.

        Retorna:
        {
            "status": "exact_match" | "alternatives" | "no_evidence",
            "file": path o None,
            "alternatives": [...]
        }
        """

        repo_path = Path(repo_path)

        expected_file = repo_path / expected_path

        # 1️⃣ Evidència exacta
        if expected_file.exists():

            return {
                "status": "exact_match",
                "file": str(expected_file),
                "alternatives": []
            }

        # 2️⃣ Buscar alternatives segons tipus
        alternatives = []

        for ext in evidence_extensions:
            alternatives.extend(inventory["by_extension"].get(ext, []))

        if alternatives:
                return {
                    "status": "alternatives",
                    "file": None,
                    "alternatives": alternatives
                }

        # 3️⃣ Cap evidència
        return {
            "status": "no_evidence",
            "file": None,
            "alternatives": []
        }
    