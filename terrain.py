import pygame
import random
import settings 

def generate_terrain(width, height, min_height, max_height):
    """
    Génère un terrain avec une forme de pic central et une pente douce vers le bas.
    
    Paramètres :
      - width : largeur du terrain (nombre de colonnes)
      - height : hauteur totale de l'écran (pour référence)
      - min_height : hauteur minimale (niveau le plus bas du terrain)
      - max_height : hauteur maximale (au centre du terrain)
      
    Renvoie :
      Une liste contenant la hauteur du terrain pour chaque colonne.
    """
    terrain = []  # Initialise une liste vide pour le terrain
    center = width // 2  # Calcule la position centrale du terrain

    for x in range(width):
        # Calcul de la distance par rapport au centre
        distance = abs(x - center)
        
        # Le terrain commence haut au centre, puis descend progressivement vers les bords
        base_height = max_height - (max_height - min_height) * (distance / center) ** 2
        
        # Inverser la hauteur pour que le pic soit en bas
        terrain.append(int(height - base_height))  # Ajoute la hauteur dans la liste

    return terrain  # Renvoie la liste des hauteurs


# Permet d'apporté de l'irrégularite au terrain
def create_random_craters(terrain, num_craters, width):
    for _ in range(num_craters):
        # Choisir une position aléatoire sur le terrain
        x = random.randint(5, width - 5)
        radius = random.randint(50, 75)  # Rayon aléatoire pour le cratère
        terrain = create_crater(terrain, x, radius)  # Créer le cratère

    return terrain # Renvoie le terrain modifié

def draw_terrain(screen, terrain, height):
    """
    Dessine le terrain sur la surface Pygame, avec le bas de l'écran représentant le niveau le plus bas.
    
    Paramètres :
      - screen : la surface Pygame où dessiner le terrain
      - terrain : liste des hauteurs du terrain pour chaque colonne
      - height : hauteur totale de l'écran
    """
    for x in range(len(terrain)):
        # Dessine une ligne verticale pour chaque colonne du terrain
        pygame.draw.line(screen, settings.GROUND_COLOR, (x, terrain[x]), (x, height))  # Le terrain s'arrête au bas de l'écran

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

    return terrain  # Renvoie le terrain modifié
