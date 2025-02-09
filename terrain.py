import pygame
import random
import numpy as np

# Couleur utilisée pour dessiner le terrain
GROUND_BROWN = (139, 69, 19)

def generate_terrain(width, height, min_height, max_height, smoothness):
    """
    Génère une liste représentant les hauteurs du terrain avec des courbes douces.
    """
    control_points = [
        random.randint(min_height, max_height) for _ in range(smoothness)
    ]
    control_x = np.linspace(0, width, num=smoothness)

    interpolator = np.interp(np.arange(width), control_x, control_points)

    return interpolator.astype(int)

def draw_terrain(screen, terrain, height):
    """
    Dessine le terrain sur l'écran.
    """
    for x, terrain_height in enumerate(terrain):
        pygame.draw.line(screen, GROUND_BROWN, (x, height), (x, height - terrain_height))

def create_crater(terrain, explosion_x, radius):
    """
    Modifie le terrain pour créer un cratère en forme plus circulaire avec des bords lissés.

    Args:
        terrain (list): Liste représentant les hauteurs du terrain.
        explosion_x (int): Position X du centre de l'explosion.
        radius (int): Rayon de l'explosion.

    Returns:
        list: Terrain modifié avec un cratère circulaire.
    """
    for x in range(max(0, explosion_x - radius), min(len(terrain), explosion_x + radius + 1)):
        dx = x - explosion_x  # Distance horizontale par rapport au centre
        if abs(dx) < radius:
            # Utilisation d'une équation parabolique pour créer un cratère plus circulaire
            depth = int((radius**2 - dx**2) ** 0.5)  # Forme circulaire
            terrain[x] = max(0, terrain[x] - depth)  # Empêche des valeurs négatives

            # Lissage des bords pour une transition plus naturelle
            if abs(dx) > radius * 0.7:  # Seulement aux bords du cratère
                terrain[x] += (abs(dx) - radius * 0.7) // 2  # Adoucit la pente

    return terrain

def smooth_terrain(terrain, strength=2):
    """
    Applique une moyenne glissante pour adoucir les variations abruptes du terrain.

    Args:
        terrain (list): Liste des hauteurs du terrain.
        strength (int): Nombre d'itérations de lissage.

    Returns:
        list: Terrain lissé.
    """
    for _ in range(strength):
        for i in range(1, len(terrain) - 1):
            terrain[i] = (terrain[i - 1] + terrain[i] + terrain[i + 1]) // 3
    return terrain
