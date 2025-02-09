import pygame
import random
from character import Character
from terrain import generate_island, draw_terrain, create_crater

# Initialisation de Pygame
pygame.init()

# Paramètres du terrain (adaptables)
WIDTH, HEIGHT = 1080, 720
MIN_HEIGHT = 310    # Hauteur minimale (niveau de l'eau)
MAX_HEIGHT = 480    # Hauteur maximale (au centre de l'île)
VARIATION = 15      # Variation aléatoire

# Couleurs
SKY_BLUE = (135, 206, 235)

# Liste des couleurs disponibles pour les joueurs (ajoutez autant de couleurs que nécessaire)
PLAYER_COLORS = [
    (0, 0, 255),    # Bleu pour le Joueur 1
    (255, 0, 0),    # Rouge pour le Joueur 2
    (0, 255, 0),    # Vert pour le Joueur 3
    (255, 255, 0),  # Jaune pour le Joueur 4
    (255, 165, 0),  # Orange pour le Joueur 5
    (128, 0, 128),  # Violet pour le Joueur 6
]

# Initialisation de l'écran
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Worms Game")

# Police pour afficher le texte
font = pygame.font.SysFont("Arial", 24)

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
                elif event.key == pygame.K_1:
                    input_text += "1"
                elif event.key == pygame.K_2:
                    input_text += "2"
                elif event.key == pygame.K_3:
                    input_text += "3"
                elif event.key == pygame.K_4:
                    input_text += "4"
                elif event.key == pygame.K_5:
                    input_text += "5"
                elif event.key == pygame.K_6:
                    input_text += "6"
        
        pygame.display.flip()

    return 1  # Retourne un joueur si on quitte la fenêtre

# Demander le nombre de joueurs avant de commencer
NUM_PLAYERS = ask_number_of_players()

# Initialisation du terrain
terrain = generate_island(WIDTH, HEIGHT, MIN_HEIGHT, MAX_HEIGHT, VARIATION)

# Placement dynamique des personnages et attribution de couleurs en fonction du nombre de joueurs
players = []
for i in range(NUM_PLAYERS):
    spawn_x = 50 + (i * (WIDTH - 100) // NUM_PLAYERS)  # Position X en fonction du joueur
    player_color = PLAYER_COLORS[i % len(PLAYER_COLORS)]  # Choisir la couleur du joueur
    players.append([Character(spawn_x, 100, player_color)])

# Initialisation des variables de jeu
current_player = 0  # Le joueur actuellement en train de jouer
turn_time_limit = 30  # Durée du tour en secondes
turn_start_time = pygame.time.get_ticks()  # Le temps du début du tour

# Boucle principale du jeu
running = True
clock = pygame.time.Clock()

while running:
    screen.fill(SKY_BLUE)
    draw_terrain(screen, terrain, HEIGHT)
    
    # Affichage et mise à jour des personnages
    for player_index in range(NUM_PLAYERS):
        for character_index in range(1):  # Un personnage par joueur
            current_character_obj = players[player_index][character_index]
            current_character_obj.apply_gravity(terrain)  # Le personnage utilise le terrain
            current_character_obj.draw(screen)

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
            if event.key == pygame.K_UP:
                players[current_player][0].jump()  # Saut pour le joueur actuel
            
            elif event.key == pygame.K_RETURN: # Passe au tour suivant
            
                current_player = (current_player + 1) % NUM_PLAYERS
                turn_start_time = pygame.time.get_ticks()  # Redémarre le chronomètre du tour
            
            elif event.key == pygame.K_SPACE: # Création d'un cratère
                pass #create_crater(terrain, 50, 25)

    # Vérification des touches pour mouvement horizontal - pour le joueur actuel seulement
    keys = pygame.key.get_pressed()
    if current_player == 0:  # Si c'est au tour du joueur actif, Ne pas autoriser le joueur à sortir de l'écran
        if keys[pygame.K_LEFT]:
            if players[current_player][0].x > 0:  # Vérifie si le personnage ne sort pas de l'écran à gauche
                players[current_player][0].move(-1, terrain, WIDTH)
        if keys[pygame.K_RIGHT]:
            if players[current_player][0].x < WIDTH - 1:  # Vérifie si le personnage ne sort pas de l'écran à droite
                players[current_player][0].move(1, terrain, WIDTH)


    # Si le temps du tour est écoulé, on passe au joueur suivant
    if remaining_time == 0:
        current_player = (current_player + 1) % NUM_PLAYERS
        turn_start_time = pygame.time.get_ticks()  # Redémarre le chronomètre du tour

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
