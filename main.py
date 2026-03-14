#!/usr/bin/env python3

from core.repos_locator import ReposLocator
from core.detector_evidencies import DetectorEvidencies


def main():

    print("=== AVALUADOR DE REPOSITORIS ===")

    locator = ReposLocator("data/repos_map.json")

    unitats = locator.get_all_units()

    for unitat in unitats:

        repo_path = locator.get_repo_path(unitat)

        print(f"\nUnitat: {unitat}")
        print(f"Repo: {repo_path}")

        detector = DetectorEvidencies(repo_path)

        images = detector.find_images()

        if not images:
            print("  Cap evidència trobada")
        else:
            for img in images:
                print("  Evidència:", img)


if __name__ == "__main__":
    main()