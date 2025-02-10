import pygame
import random

# Constantes pour la gravité et la taille
GRAVITY = 0.5

class Character:
    def __init__(self, x, y, color, player_number):
        self.x = x
        self.y = y
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False
        self.move_start_time = None
        self.color = color  # Couleur du personnage
        self.radius = 15  # Rayon du personnage (taille)
        self.health = 150  # Vie initiale
        self.player_number = player_number  # Numéro du joueur (1, 2, etc.)

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
            self.vel_y = -9.81  # Le saut est effectué en modifiant la vitesse verticale
            self.on_ground = False  # Le personnage est maintenant en l'air

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)),
                           self.radius)  # Dessin du personnage avec le rayon

    def draw_health_bar(self, screen):
        player_name = f"{self.health}"
        name_text = pygame.font.SysFont("Arial", 18).render(player_name, True, (0, 0, 0))
        screen.blit(name_text, (self.x - self.radius, self.y - self.radius - 60))

    def draw_player_name(self, screen):
        player_name = f"Player {self.player_number}"
        name_text = pygame.font.SysFont("Arial", 18).render(player_name, True, (0, 0, 0))
        screen.blit(name_text, (self.x - self.radius, self.y - self.radius - 30))
