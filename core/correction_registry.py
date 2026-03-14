"""
CorrectionRegistry
Gestió persistent de les correccions del sistema d'avaluació.

Aquest mòdul carrega i desa el fitxer data/corrections.json.
Permet consultar i actualitzar correccions de forma estructurada.

Estructura esperada del JSON:

{
  "AE05": {
    "unitat-1": {
      "nota": 2,
      "comentari": "correcte"
    }
  }
}
"""

import json
import os


class CorrectionRegistry:

    def __init__(self, corrections_file="data/corrections.json"):
        self.corrections_file = corrections_file
        self.data = {}
        self._load()

    def _load(self):
        """Carrega el fitxer de correccions si existeix."""
        if os.path.exists(self.corrections_file):
            with open(self.corrections_file, "r", encoding="utf-8") as f:
                self.data = json.load(f)
        else:
            self.data = {}

    def _save(self):
        """Desa el fitxer de correccions."""
        with open(self.corrections_file, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)

    def get_correction(self, ra, unitat):
        """
        Retorna la correcció existent per una unitat concreta.

        :param ra: resultat d'aprenentatge (ex: AE05)
        :param unitat: unitat concreta (ex: unitat-1)
        """
        return self.data.get(ra, {}).get(unitat)

    def set_correction(self, ra, unitat, nota, comentari=""):
        """
        Desa o actualitza una correcció.

        :param ra: resultat d'aprenentatge
        :param unitat: unitat concreta
        :param nota: puntuació
        :param comentari: comentari opcional
        """
        if ra not in self.data:
            self.data[ra] = {}

        self.data[ra][unitat] = {
            "nota": nota,
            "comentari": comentari
        }

        self._save()

    def list_ra(self):
        """Retorna els RA registrats."""
        return list(self.data.keys())

    def list_unitats(self, ra):
        """Retorna les unitats registrades per un RA."""
        return list(self.data.get(ra, {}).keys())


if __name__ == "__main__":

    print("=== TEST CorrectionRegistry ===")

    registry = CorrectionRegistry()

    registry.set_correction("AE05", "unitat-1", 2, "correcte")

    print(registry.get_correction("AE05", "unitat-1"))