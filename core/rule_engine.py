from pathlib import Path
from difflib import SequenceMatcher
import os


def similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()


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

        repo_path = Path(repo_path)

        expected_file = repo_path / expected_path
        expected_name = os.path.basename(expected_path)
        expected_dir = os.path.dirname(expected_path)

        # ------------------------------------------------
        # 1️⃣ evidència exacta
        # ------------------------------------------------

        if expected_file.exists():

            return {
                "status": "exact_match",
                "file": str(expected_file),
                "alternatives": []
            }

        # ------------------------------------------------
        # 2️⃣ buscar candidats
        # ------------------------------------------------

        candidates = []

        for ext in evidence_extensions:
            candidates.extend(inventory["by_extension"].get(ext, []))

        best_match = None
        best_score = 0
        best_dir_match = False

        for f in candidates:

            filename = os.path.basename(f)
            filepath = Path(f)

            score = similarity(filename, expected_name)

            same_dir = expected_dir in str(filepath)

            if same_dir:
                score = min(score + 0.1, 1.0)

            if score > best_score:
                best_score = score
                best_match = f
                best_dir_match = same_dir

        # ------------------------------------------------
        # 3️⃣ match proper
        # ------------------------------------------------

        if best_match and best_score >= 0.9:

            status = "near_match"

            # si és el nom correcte però carpeta incorrecta
            if best_dir_match is False:
                status = "wrong_folder"

            return {
                "status": status,
                "file": best_match,
                "similarity": best_score,
                "alternatives": []
            }

        # ------------------------------------------------
        # 4️⃣ alternatives
        # ------------------------------------------------

        if candidates:
            return {
                "status": "alternatives",
                "file": None,
                "alternatives": candidates
            }

        # ------------------------------------------------
        # 5️⃣ no evidència
        # ------------------------------------------------

        return {
            "status": "no_evidence",
            "file": None,
            "alternatives": []
        }