from pathlib import Path


class RepoScanner:
    """
    Escaneja un repositori i construeix un inventari de fitxers.
    """

    IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg"}
    DOCUMENT_EXTENSIONS = {".docx", ".pdf"}
    SPREADSHEET_EXTENSIONS = {".xlsx", ".ods"}
    PRESENTATION_EXTENSIONS = {".pptx", ".odp"}

    def scan_repo(self, repo_path):
        """
        Retorna un inventari de fitxers del repositori.

        Output exemple:
        {
            "images": [...],
            "documents": [...],
            "spreadsheets": [...],
            "presentations": [...],
            "others": [...]
        }
        """

        repo_path = Path(repo_path)

        inventory = {
            "images": [],
            "documents": [],
            "spreadsheets": [],
            "presentations": [],
            "others": [],
        }

        for path in repo_path.rglob("*"):

            if not path.is_file():
                continue

            ext = path.suffix.lower()

            if ext in self.IMAGE_EXTENSIONS:
                inventory["images"].append(str(path))

            elif ext in self.DOCUMENT_EXTENSIONS:
                inventory["documents"].append(str(path))

            elif ext in self.SPREADSHEET_EXTENSIONS:
                inventory["spreadsheets"].append(str(path))

            elif ext in self.PRESENTATION_EXTENSIONS:
                inventory["presentations"].append(str(path))

            else:
                inventory["others"].append(str(path))

        return inventory