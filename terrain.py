import pygame
import numpy as np
import random

def generate_island(width, height, min_height, max_height, variation):
    """
    Génère un terrain en forme d'île avec un pic central et une pente douce vers l'eau.
    
    Paramètres :
      - width : largeur du terrain (nombre de colonnes)
      - height : hauteur totale de l'écran (pour référence)
      - min_height : hauteur minimale (niveau de l'eau)
      - max_height : hauteur maximale (au centre de l'île)
      - variation : amplitude des variations aléatoires à ajouter (non utilisée ici)
      
    Renvoie :
      Un tableau numpy de type int contenant la hauteur du terrain pour chaque colonne.
    """
    terrain = np.zeros(width)
    center = width // 2

    for x in range(width):
        # Calcul de la distance par rapport au centre
        distance = abs(x - center)
        
        # L'île commence haute au centre, puis descend progressivement vers les bords
        base_height = max_height - (max_height - min_height) * (distance / center) ** 2
        
        # Ajouter une pente douce vers le bas de l'écran
        height_factor = (height - 100 - base_height) / (height - 100)  # Gradient de la pente vers l'eau
        base_height += height_factor * (min_height - base_height)  # Ajuste la hauteur selon l'écran
        
        terrain[x] = base_height

    # Aucune variation aléatoire n'est ajoutée ici, l'île est maintenant lisse
    return terrain.astype(int)

def draw_terrain(screen, terrain, height):
    """
    Dessine le terrain avec l'eau au bas de l'écran.
    
    Paramètres :
      - screen : la surface Pygame où dessiner
      - terrain : tableau des hauteurs du terrain pour chaque colonne
      - height : hauteur totale de l'écran
    """
    # Dessiner l'île
    terrain_color = (34, 139, 34)  # Vert foncé pour représenter l'île
    for x in range(len(terrain)):
        pygame.draw.line(screen, terrain_color, (x, terrain[x]), (x, height))  # L'île s'arrête avant l'eau

def create_crater(terrain, x, radius):
    """
    Modifie le terrain pour créer un cratère circulaire à la position x avec le rayon spécifié.
    
    Paramètres :
      - terrain : tableau des hauteurs du terrain
      - x : position centrale du cratère (en index)
      - radius : rayon du cratère
      
    Renvoie :
      Le tableau du terrain modifié.
    """
    for i in range(max(0, x - radius), min(len(terrain), x + radius)):
        # Calcul de la distance horizontale par rapport au centre du cratère
        distance = abs(i - x)

        # Si la distance est inférieure au rayon, on applique la déformation
        if distance < radius:
            # Appliquer une fonction lissée pour la profondeur (courbe plus douce)
            depth = int((radius - distance) ** 0.87)  # Courbe quadratique plus douce

            # Appliquer la profondeur, mais éviter de dépasser une hauteur trop faible
            terrain[i] = max(terrain[i] + depth, 0)  # On déforme vers le bas (le terrain "descend")

    return terrain

