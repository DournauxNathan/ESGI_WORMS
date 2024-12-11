import pygame
import random

# Couleur utilisée pour dessiner le terrain
GROUND_BROWN = (139, 69, 19)

# Génération du terrain
def generate_terrain(width, height, min_height, max_height, smoothness):
    """
    Génère une liste représentant les hauteurs du terrain.
    
    Args:
        width (int): Largeur totale du terrain (en pixels).
        height (int): Hauteur de la fenêtre (non utilisée directement ici).
        min_height (int): Hauteur minimale du terrain.
        max_height (int): Hauteur maximale du terrain.
        smoothness (int): Facteur de lissage pour limiter les variations entre les hauteurs.

    Returns:
        list: Une liste contenant les hauteurs du terrain à chaque pixel horizontal.
    """
    terrain = []
    last_height = random.randint(min_height, max_height)  # Hauteur initiale aléatoire
    for x in range(width):
        # Calcul d'une nouvelle hauteur avec une variation limitée par "smoothness"
        new_height = last_height + random.randint(-smoothness, smoothness)
        # Assure que la hauteur reste dans les limites spécifiées
        new_height = max(min_height, min(max_height, new_height))
        terrain.append(new_height)  # Ajoute la hauteur au terrain
        last_height = new_height  # Met à jour la dernière hauteur
    return terrain

# Dessin du terrain
def draw_terrain(screen, terrain, height):
    """
    Dessine le terrain sur l'écran.

    Args:
        screen (Surface): Surface Pygame sur laquelle dessiner.
        terrain (list): Liste des hauteurs du terrain.
        height (int): Hauteur totale de la fenêtre.
    """
    for x, terrain_height in enumerate(terrain):
        # Dessine une ligne verticale pour chaque pixel horizontal du terrain
        pygame.draw.line(screen, GROUND_BROWN, (x, height), (x, height - terrain_height))
