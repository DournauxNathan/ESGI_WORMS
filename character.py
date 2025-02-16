import pygame
import random
import settings

class Character:
    def __init__(self, x, y, color, player_number):
        self.x = x  # Position X du personnage
        self.y = y  # Position Y du personnage
        self.vel_x = 0  # Vitesse horizontale du personnage
        self.vel_y = 0  # Vitesse verticale du personnage
        self.on_ground = False  # Indique si le personnage est au sol
        self.has_shoot = False # Indique si le personnage a tirée
        self.move_start_time = None  # Temps de début du mouvement (non utilisé ici)
        self.color = color  # Couleur du personnage
        self.radius = 15  # Rayon du personnage (taille)
        self.health = settings.MAX_HEALTH  # Vie initiale du personnage
        self.player_number = player_number  # Numéro du joueur (1, 2, etc.)

    def take_damage(self, damage):
        """Inflige des dégâts au personnage."""
        self.health -= damage  # Réduit la vie du personnage
        if self.health <= 0:
            self.health = 0  # Assure que la vie ne soit pas négative
    
    #region MOUVEMENT
    def apply_gravity(self, terrain):
        """Applique la gravité au personnage."""
        if not self.on_ground:  # Si le personnage n'est pas au sol
            self.vel_y += settings.GRAVITY  # Applique la gravité à la vitesse verticale
            new_y = self.y + self.vel_y  # Calcule la nouvelle position Y

            # Vérification de la collision avec le terrain
            terrain_x = int(self.x)  # Position X arrondie pour accéder au terrain
            if 0 <= terrain_x < len(terrain):  # Vérification que x est dans les limites
                terrain_height = terrain[terrain_x]  # Hauteur du terrain à la position x
                if new_y >= terrain_height - self.radius:  # Vérifie si le personnage touche le sol
                    self.y = terrain_height - self.radius  # Place le personnage au niveau du sol
                    self.vel_y = 0  # Réinitialise la vitesse verticale
                    self.on_ground = True  # Le personnage est maintenant au sol
                else:
                    self.y = new_y  # Met à jour la position Y

    def move(self, direction, terrain, WIDTH):
        """Déplace le personnage dans la direction spécifiée."""
        new_x = self.x + direction  # Incrémentation du mouvement horizontal

        # Vérification que le personnage ne dépasse pas les bords de l'écran
        if 0 <= new_x < WIDTH:  # Limite du terrain
            self.x = new_x  # Met à jour la position X

            # Vérification si le personnage est au sol avant de mettre à jour la position Y
            if self.on_ground:
                terrain_height = terrain[int(self.x)]  # Hauteur du terrain à la position x
                self.y = terrain_height - self.radius  # Met à jour la position Y
        else:
            # Si on dépasse les bords, on empeche le mouvement
            self.x = max(0, min(self.x, WIDTH - 1))  # Rendre la position valide

    def jump(self):
        """Fait sauter le personnage."""
        if self.on_ground:  # Le personnage peut sauter seulement s'il est au sol
            self.vel_y = -9.81  # Definit la vitesse verticale pour le saut
            self.on_ground = False  # Le personnage est en l'air

    def update_position(self, x, y, terrain):
        """Met à jour la position du personnage"""
        if not self.on_ground:
            terrain_height = terrain[int(self.x)]  # Hauteur du terrain à la position x
            self.y = terrain_height - self.radius  # Met à jour la position Y
    #endregion

    #region Affichage
    def draw(self, screen):
        if self.health > 0:  # Vérifiez si le personnage est vivant
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)  # Dessin du personnage avec le rayon

    def draw_player_name(self, screen):
        if self.health > 0:  # Vérifiez si le personnage est vivant
            player_name = f"Player {self.player_number}"  # Crée le texte du nom du joueur
            name_text = pygame.font.SysFont("Arial", 18).render(player_name, True, (0, 0, 0))  # Rendu du texte
            screen.blit(name_text, (self.x - self.radius - 15, self.y - self.radius - 60))  # Affiche le texte

    def draw_health_bar(self, screen):
        if self.health > 0:  # Vérifiez si le personnage est vivant
            player_name = f"{self.health}"  # Crée le texte de la vie
            name_text = pygame.font.SysFont("Arial", 18).render(player_name, True, (0, 0, 0))  # Rendu du texte
            screen.blit(name_text, (self.x - self.radius, self.y - self.radius - 30))  # Affiche le texte
    #endregion