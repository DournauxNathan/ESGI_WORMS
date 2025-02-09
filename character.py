# character.py
import pygame
import random

# Constantes pour la gravité et la taille
GRAVITY = 0.5

class Character:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False
        self.move_start_time = None  # Temps de début du déplacement
        self.color = color  # Couleur du personnage
        self.radius = 15  # Rayon du personnage (taille)

    def apply_gravity(self, terrain):
        if not self.on_ground:
            self.vel_y += GRAVITY
            new_y = self.y + self.vel_y
    
            # Vérification de la collision avec le terrain
            terrain_x = int(self.x)
            if 0 <= terrain_x < len(terrain):  # Vérification que x est dans les limites
                terrain_height = terrain[terrain_x]  # Hauteur du terrain à la position x
                if new_y >= terrain_height - self.radius:  # Ajustement avec le rayon du personnage
                    self.y = terrain_height - self.radius  # Le personnage se place au niveau du sol
                    self.vel_y = 0
                    self.on_ground = True
                else:
                    self.y = new_y

    def move(self, direction, terrain, WIDTH):
        new_x = self.x + direction  # Incrémentation du mouvement horizontal

        # Vérification que le personnage ne dépasse pas les bords de l'écran
        if 0 <= new_x < WIDTH:  # Limite du terrain
            self.x = new_x
            
            # Vérification si le personnage est au sol avant de mettre à jour la position y
            if self.on_ground:
                terrain_height = terrain[int(self.x)]  # Hauteur du terrain à la position x
                self.y = terrain_height - self.radius  # Mettre à jour la position Y
        else:
            # Si on dépasse les bords, on empêche le mouvement
            self.x = max(0, min(self.x, WIDTH - 1))  # Rendre la position valide

    def jump(self):
        if self.on_ground:
            self.vel_y = -10
            self.on_ground = False

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)  # Dessin du personnage avec le rayon
