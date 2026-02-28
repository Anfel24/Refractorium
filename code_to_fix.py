"""Module pour calculer et afficher l'aire de cercles."""
import math


def calculate_circle_areas(diameters: list[float | int]) -> list[float]:
    """Calcule l'aire de cercles Ã  partir d'une liste de diamÃ¨tres.

    Args:
        diameters (list[float | int]): Une liste de diamÃ¨tres de cercles.

    Returns:
        list[float]: Une liste des aires calculÃ©es pour chaque cercle.
    """
    areas = []
    for d in diameters:
        radius = d / 2
        area = math.pi * (radius ** 2)
        areas.append(area)
    return areas


def display_circle_areas(areas: list[float]) -> None:
    """Affiche les aires de cercles formatÃ©es.

    Args:
        areas (list[float]): Une liste des aires de cercles Ã  afficher.
    """
    for i, area in enumerate(areas):
        print(f"Cercle {i} aire: {area}")


def f(d: list[float | int]) -> list[float]:
    """Orchestre le calcul et l'affichage des aires de cercles.

    Args:
        d (list[float | int]): Une liste de diamÃ¨tres de cercles.

    Returns:
        list[float]: Une liste des aires calculÃ©es pour chaque cercle.
    """
    areas = calculate_circle_areas(d)
    display_circle_areas(areas)
    return areas


if __name__ == "__main__":
    l = [10, 20, 30]
    calculated_areas = f(l)
