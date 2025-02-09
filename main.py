import pygame
import random
import numpy as np
from terrain import generate_terrain, draw_terrain, create_crater

# Initialisation de Pygame
pygame.init()

# Dimensions de l'écran
WIDTH, HEIGHT = 800, 600

# Couleurs
SKY_BLUE = (135, 206, 235)
PLAYER1_COLOR = (0, 0, 255)  # Bleu pour Joueur 1
PLAYER2_COLOR = (255, 0, 0)  # Rouge pour Joueur 2

# Initialisation de l'écran
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Worms Game")

# Paramètres du jeu
NUM_PLAYERS = 2
CHARACTERS_PER_PLAYER = 1  # Un seul personnage par joueur
GRAVITY = 0.5
TURN_TIME_LIMIT = 30  # 30 secondes par personnage
GLOBAL_TIME_LIMIT = 300  # 5 minutes de temps de jeu global

# Police pour afficher le temps
font = pygame.font.SysFont("Arial", 24)

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
            terrain_height = terrain[int(self.x)]  # Hauteur du terrain à la position x
            if new_y >= terrain_height - self.radius:  # Ajustement avec le rayon du personnage
                self.y = terrain_height - self.radius  # Le personnage se place au niveau du sol
                self.vel_y = 0
                self.on_ground = True
            else:
                self.y = new_y

    def move(self, direction, terrain):
        new_x = self.x + direction * 5
        if 0 <= new_x < WIDTH:
            self.x = new_x
            # Mise à jour de la position Y en fonction du terrain et du rayon
            terrain_height = terrain[int(self.x)]
            self.y = terrain_height - self.radius  # Position Y ajustée selon le terrain
            self.move_start_time = pygame.time.get_ticks()  # Met à jour le temps du déplacement

    def jump(self):
        if self.on_ground:
            self.vel_y = -10
            self.on_ground = False

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)  # Dessin du personnage avec le rayon

    def get_move_time(self):
        if self.move_start_time is None:
            return 0  # Si le déplacement n'a pas encore commencé
        return (pygame.time.get_ticks() - self.move_start_time) / 1000  # Temps écoulé depuis le début du déplacement en secondes

    def reset_move_time(self):
        self.move_start_time = pygame.time.get_ticks()  # Réinitialiser le temps du déplacement


# Génération du terrain
terrain = generate_terrain(WIDTH, HEIGHT, 100, 300, 8)

# Placement des personnages (un par joueur)
# Les personnages auront une position différente pour chaque joueur
players = [
    [Character(random.randint(50, WIDTH - 100), terrain[random.randint(50, WIDTH - 100)], PLAYER1_COLOR)],  # Joueur 1 (bleu)
    [Character(random.randint(50, WIDTH - 100), terrain[random.randint(50, WIDTH - 100)], PLAYER2_COLOR)]   # Joueur 2 (rouge)
]

# Variables de jeu
current_player = 0
current_character = 0
turn_start_time = pygame.time.get_ticks()  # Temps du début du tour
turn_time_left_player1 = TURN_TIME_LIMIT  # Temps restant pour le joueur 1
turn_time_left_player2 = TURN_TIME_LIMIT  # Temps restant pour le joueur 2
player_turn = 0  # 0 pour Joueur 1, 1 pour Joueur 2
global_time_left = GLOBAL_TIME_LIMIT  # Temps global restant

# Boucle principale du jeu
running = True
clock = pygame.time.Clock()

# Fonction pour convertir le temps en secondes en format 00:00
def format_time(seconds):
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes:02}:{seconds:02}"

while running:
    screen.fill(SKY_BLUE)
    draw_terrain(screen, terrain, HEIGHT)
    
    # Calcul du temps restant pour chaque joueur
    if player_turn == 0:  # Tour du Joueur 1
        current_time_player1 = pygame.time.get_ticks() - turn_start_time
        turn_time_left_player1 = max(0, TURN_TIME_LIMIT - current_time_player1 / 1000)
    else:  # Tour du Joueur 2
        current_time_player2 = pygame.time.get_ticks() - turn_start_time
        turn_time_left_player2 = max(0, TURN_TIME_LIMIT - current_time_player2 / 1000)
    
    # Calcul du temps global restant
    global_time_left = max(0, GLOBAL_TIME_LIMIT - (pygame.time.get_ticks() - turn_start_time) / 1000)

    # Affichage du temps global et du temps de chaque joueur
    global_time_text = font.render(f"Temps global restant : {format_time(global_time_left)}", True, (255, 255, 255))
    screen.blit(global_time_text, (WIDTH // 2 - global_time_text.get_width() // 2, 20))

    # Affichage du temps restant pour chaque joueur
    player1_time_text = font.render(f"Joueur 1 : {format_time(turn_time_left_player1)}", True, (255, 255, 255))
    player2_time_text = font.render(f"Joueur 2 : {format_time(turn_time_left_player2)}", True, (255, 255, 255))
    screen.blit(player1_time_text, (20, HEIGHT - 40))
    screen.blit(player2_time_text, (WIDTH - player2_time_text.get_width() - 20, HEIGHT - 40))

    # Affichage des personnages de chaque joueur
    for player_index in range(NUM_PLAYERS):
        for character_index in range(CHARACTERS_PER_PLAYER):
            current_character_obj = players[player_index][character_index]
            current_character_obj.apply_gravity(terrain)
            current_character_obj.draw(screen)
    
    # Logique pour le contrôle du personnage du joueur actuel
    current_character_obj = players[player_turn][current_character]
    current_character_obj.apply_gravity(terrain)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                current_character_obj.move(-1, terrain)
            elif event.key == pygame.K_RIGHT:
                current_character_obj.move(1, terrain)
            elif event.key == pygame.K_UP:
                current_character_obj.jump()
            elif event.key == pygame.K_RETURN:  # Appui sur Entrée pour finir le tour
                # Passer au personnage suivant
                current_character = (current_character + 1) % CHARACTERS_PER_PLAYER
                if current_character == 0:
                    # Passer au joueur suivant
                    player_turn = (player_turn + 1) % NUM_PLAYERS
                    turn_start_time = pygame.time.get_ticks()  # Réinitialiser le temps au début du tour

    # Détection des touches maintenues enfoncées pour le mouvement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        current_character_obj.move(-1, terrain)
    if keys[pygame.K_RIGHT]:
        current_character_obj.move(1, terrain)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
