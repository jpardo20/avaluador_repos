import json
from pathlib import Path


class ReposLocator:
    """
    Localitza els repositoris associats a cada unitat d'avaluació.
    Llegeix el fitxer data/repos_map.json.
    """

    def __init__(self, repos_root="repos", map_file="data/repos_map.json"):
        self.repos_root = Path(repos_root)
        self.map_file = Path(map_file)

        if not self.map_file.exists():
            raise FileNotFoundError(f"No s'ha trobat el fitxer {self.map_file}")

        with open(self.map_file, "r", encoding="utf-8") as f:
            self.repo_map = json.load(f)

    def get_repo_path(self, unitat):
        """
        Retorna la ruta del repositori associat a una unitat d'avaluació.
        """
        if unitat not in self.repo_map:
            raise KeyError(f"No hi ha repositori definit per la unitat '{unitat}'")

        repo_name = self.repo_map[unitat]
        repo_path = self.repos_root / repo_name

        if not repo_path.exists():
            raise FileNotFoundError(f"El repositori '{repo_path}' no existeix")

        return repo_path

    def list_unitats(self):
        """
        Retorna la llista de totes les unitats d'avaluació.
        """
        return list(self.repo_map.keys())

if __name__ == "__main__":
    print("Test repos locator")

    try:
        locator = ReposLocator()

        print("Unitats detectades:")
        for unitat in locator.list_unitats():
            path = locator.get_repo_path(unitat)
            print(f"{unitat} -> {path}")

    except Exception as e:
        print("Error:", e)