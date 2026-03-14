from pathlib import Path


class DetectorEvidencies:
    """
    Detecta evidències dins d'un repositori.

    Aquesta primera versió busca fitxers amb extensions d'imatge
    que poden servir com a evidència.
    """

    EXTENSIONS_IMATGE = {".png", ".jpg", ".jpeg"}

    def __init__(self, repo_path):
        self.repo_path = Path(repo_path)

        if not self.repo_path.exists():
            raise FileNotFoundError(f"El repositori no existeix: {repo_path}")

    def find_images(self):
        """
        Retorna totes les imatges trobades al repositori.
        """
        images = []

        for path in self.repo_path.rglob("*"):
            if path.is_file() and path.suffix.lower() in self.EXTENSIONS_IMATGE:
                images.append(path)

        return images

    def find_expected(self, relative_path):
        """
        Comprova si existeix una evidència exacta.
        """
        target = self.repo_path / relative_path
        return target if target.exists() else None


if __name__ == "__main__":
    print("Test detector evidencies")

    repo = Path("repos/repo-alumne-1")

    detector = DetectorEvidencies(repo)

    images = detector.find_images()

    print("Imatges trobades:")
    for img in images:
        print("-", img)