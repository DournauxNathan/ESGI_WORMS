import pygame
import random
from character import Character
from terrain import generate_island, draw_terrain, create_crater
import numpy as np
import math

# Initialisation de Pygame
pygame.init()

# Paramètres du terrain (adaptables)
WIDTH, HEIGHT = 1080, 720
MIN_HEIGHT = 310  # Hauteur minimale (niveau de l'eau)
MAX_HEIGHT = 480  # Hauteur maximale (au centre de l'île)
VARIATION = 15  # Variation aléatoire

# Couleurs
SKY_BLUE = (135, 206, 235)

# Liste des couleurs disponibles pour les joueurs (ajoutez autant de couleurs que nécessaire)
PLAYER_COLORS = [
    (0, 0, 255),  # Bleu pour le Joueur 1
    (255, 0, 0),  # Rouge pour le Joueur 2
    (0, 255, 0),  # Vert pour le Joueur 3
    (255, 255, 0),  # Jaune pour le Joueur 4
    (255, 165, 0),  # Orange pour le Joueur 5
    (128, 0, 128),  # Violet pour le Joueur 6
]

# Initialisation de l'écran
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Worms Game")

# Police pour afficher le texte
font = pygame.font.SysFont("Arial", 24)

def inventory():
    current_weapon = 0
    input_text = ""
    running = True
    color = (0, 0, 0)

    while running:
        # Afficher l'inventaire des joueurs (NB : celui ci est commun)
        prompt_text = font.render("Inventory " + input_text, True, color)
        screen.blit(prompt_text, (WIDTH // 4, HEIGHT // 2))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    # Effacer le dernier caractère
                    input_text = input_text[:-1]
                elif event.key == pygame.K_1:
                    input_text += "Weapon 1"
                elif event.key == pygame.K_2:
                    input_text += "Weapon 2"
                elif event.key == pygame.K_3:
                    input_text += "Weapon 3"

def ask_number_of_players():
    running = True
    input_text = ""
    color = (0, 0, 0)

    while running:
        screen.fill(SKY_BLUE)
        # Afficher le texte demandant le nombre de joueurs
        prompt_text = font.render("Entrez le nombre de joueurs (1-6): " + input_text, True, color)
        screen.blit(prompt_text, (WIDTH // 4, HEIGHT // 2))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # Vérifier si l'entrée est un nombre valide
                    if input_text.isdigit():
                        num_players = int(input_text)
                        if 1 <= num_players <= 6:
                            return num_players  # Retourner le nombre de joueurs
                        else:
                            input_text = ""  # Réinitialiser si le nombre est invalide
                            color = (255, 0, 0)  # Rouge pour erreur
                    else:
                        input_text = ""  # Réinitialiser si l'entrée n'est pas un nombre
                        color = (255, 0, 0)  # Rouge pour erreur
                elif event.key == pygame.K_BACKSPACE:
                    # Effacer le dernier caractère
                    input_text = input_text[:-1]
                elif event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6]:
                    input_text += event.unicode

        pygame.display.flip()

    return 1  # Retourne un joueur si on quitte la fenêtre

# Demander le nombre de joueurs avant de commencer
NUM_PLAYERS = ask_number_of_players()

# Initialisation du terrain
terrain = generate_island(WIDTH, HEIGHT, MIN_HEIGHT, MAX_HEIGHT, VARIATION)

# Initialisation des variables de jeu
current_player = 0  # Le joueur actuellement en train de jouer
current_character_index = 0  # L'index du personnage actuellement contrôlé
turn_time_limit = 30  # Durée du tour en secondes
turn_start_time = pygame.time.get_ticks()  # Le temps du début du tour

# Initialisation des personnages et de leurs couleurs
players = []
for i in range(NUM_PLAYERS):
    spawn_x = 50 + (i * (WIDTH - 100) // NUM_PLAYERS)
    player_color = PLAYER_COLORS[i % len(PLAYER_COLORS)]

    print(f"Création du joueur {i + 1} à la position {spawn_x}, couleur {player_color}")

    try:
        # Créer 2 personnages par joueur
        player_characters = [Character(spawn_x, 100 + j * 50, player_color, i + 1) for j in range(2)]
        players.append(player_characters)  # Ajouter les personnages à la liste
        print(f"Joueur {i + 1} créé avec succès avec {len(player_characters)} personnages")
    except Exception as e:
        print(f"Erreur lors de la création du joueur {i + 1}: {e}")
        running = False  # Arrêter la boucle en cas d'erreur

# Si on arrive ici, on peut vérifier la structure de players pour chaque joueur
print(f"Liste des joueurs : {players}")

# Boucle principale du jeu
running = True
clock = pygame.time.Clock()
projectiles = []

def fire_projectile(x, y, angle, speed):
    """Crée un projectile avec un angle et une vitesse donnés."""
    rad_angle = math.radians(angle)
    vx = speed * math.cos(rad_angle)
    vy = -speed * math.sin(rad_angle)
    projectiles.append([[x, y], [vx, vy]])

while running:
    screen.fill(SKY_BLUE)
    draw_terrain(screen, terrain, HEIGHT)

    # Affichage et mise à jour des personnages
    for player_index in range(NUM_PLAYERS):
        for character_index in range(len(players[player_index])):  # Plusieurs personnages par joueur
            current_character_obj = players[player_index][character_index]
            current_character_obj.apply_gravity(terrain)  # Le personnage utilise la gravité
            current_character_obj.draw(screen)  # Dessiner le personnage
            current_character_obj.draw_health_bar(screen)  # Dessiner la barre de vie
            current_character_obj.draw_player_name(screen)  # Afficher le nom du joueur

    # Affichage du temps restant pour le tour actuel
    elapsed_time = (pygame.time.get_ticks() - turn_start_time) // 1000
    remaining_time = max(0, turn_time_limit - elapsed_time)
    timer_text = font.render(f"Temps restant: {remaining_time}s", True, (0, 0, 0))
    screen.blit(timer_text, (WIDTH // 2 - timer_text.get_width() // 2, 20))

    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  # Jump
                players[current_player][current_character_index].jump()  # Saut pour le personnage actuel
            elif event.key == pygame.K_RETURN:  # Passe au tour suivant
                current_player = (current_player + 1) % NUM_PLAYERS
                current_character_index = 0  # Réinitialiser l'index du personnage
                turn_start_time = pygame.time.get_ticks()  # Redémarre le chronomètre du tour
            elif event.key == pygame.K_TAB:  # Changer de personnage
                current_character_index = (current_character_index + 1) % len(players[current_player])
            #elif event.key == pygame.K_SPACE:  # Création d'un cratère
            #create_crater(terrain, 50, 25)

    # Vérification des touches pour mouvement horizontal - pour le personnage actuel seulement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        if players[current_player][current_character_index].x > 0:
            players[current_player][current_character_index].move(-1, terrain, WIDTH)
    if keys[pygame.K_RIGHT]:
        if players[current_player][current_character_index].x < WIDTH - 1:
            players[current_player][current_character_index].move(1, terrain, WIDTH)

    # Si le temps du tour est écoulé, on passe au joueur suivant
    if remaining_time == 0:
        current_player = (current_player + 1) % NUM_PLAYERS
        current_character_index = 0  # Réinitialiser l'index du personnage
        turn_start_time = pygame.time.get_ticks()  # Redémarre le chronomètre du tour

    pygame.display.flip()
    clock.tick(100)

pygame.quit()