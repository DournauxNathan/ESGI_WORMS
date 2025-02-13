import pygame
import numpy as np
from perlin_noise import PerlinNoise

# Initialisation de Pygame
pygame.init()

# Paramètres de la fenêtre
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Terrain marron avec bruit de Perlin")

# Paramètres du bruit de Perlin
scale = 10  # Échelle du bruit
noise = PerlinNoise(octaves=6)

# Génération du terrain
def generate_terrain(width, height):
    terrain = np.zeros((height, width, 3), dtype=np.uint8)
    
    for y in range(height):
        for x in range(width):
            # Générer le bruit de Perlin
            noise_value = noise([x / scale, y / scale])
            # Normaliser la valeur de bruit entre 0 et 1
            normalized_value = (noise_value + 1) / 2
            
            # Déterminer la couleur marron en fonction de la valeur de bruit
            color_value = int(normalized_value * 255)
            terrain[y, x] = (color_value // 2, color_value // 4, color_value)  # Couleur marron
            
    return terrain

# Boucle principale
running = True
terrain = generate_terrain(width, height)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Affichage du terrain
    surface = pygame.surfarray.make_surface(terrain)
    screen.blit(surface, (0, 0))
    pygame.display.flip()

# Quitter Pygame
pygame.quit()