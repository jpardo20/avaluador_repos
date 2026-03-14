import json
from pathlib import Path


class ReposLocator:
    """
    Localitza els repositoris associats a cada unitat d'avaluació.
    """

    def __init__(self, map_file):

        self.map_file = Path(map_file)

        if not self.map_file.exists():
            raise FileNotFoundError(f"No s'ha trobat el fitxer {map_file}")

        with open(self.map_file) as f:
            self.repo_map = json.load(f)

    def get_all_units(self):
        """
        Retorna totes les unitats definides.
        """
        return list(self.repo_map.keys())

    def get_repo_path(self, unit):
        """
        Retorna el path del repositori associat a la unitat.
        """
        path = self.repo_map.get(unit)

        if not path:
            raise ValueError(f"No hi ha repositori definit per {unit}")

        return Path(path)