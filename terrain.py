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
    Modifie le terrain pour ajouter un trou à une position donnée.
    
    Args:
        terrain (list): Liste représentant les hauteurs du terrain.
        explosion_x (int): Position X du centre de l'explosion.
        radius (int): Rayon de l'explosion.

    Returns:
        list: Terrain modifié avec un trou.
    """
    # Parcourt les indices dans une plage limitée par la taille de la liste
    for x in range(max(0, explosion_x - radius), min(len(terrain), explosion_x + radius + 1)):
        distance = abs(x - explosion_x)  # Distance entre x et le centre de l'explosion
        if distance < radius:
            depth = (radius - distance) ** 2 // radius  # Profondeur calculée
            terrain[x] = max(0, terrain[x] - depth)  # Diminue la hauteur du terrain sans aller sous 0
    return terrain

