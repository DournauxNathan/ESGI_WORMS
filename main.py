import pygame
import random
from character import Character
from terrain import generate_terrain, draw_terrain, create_crater
import numpy as np
import math
from settings import WIDTH, HEIGHT, MIN_HEIGHT, MAX_HEIGHT, VARIATION, SKY_BLUE, PLAYER_COLORS, turn_time_limit

class WormsGame:
    def __init__(self):
        # Initialisation de Pygame
        pygame.init()
        
        # Initialisation de l'écran
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Worms Game")
        
        # Police pour afficher le texte
        self.font = pygame.font.SysFont("Arial", 24)

        # Initialisation des variables de jeu
        self.current_player = 0  # Le joueur actuellement en train de jouer
        self.current_character_index = 0  # L'index du personnage actuellement contrôlé
        self.turn_start_time = pygame.time.get_ticks()  # Le temps du début du tour

        # Demander le nombre de joueurs avant de commencer
        self.num_players = self.ask_number_of_players()

        # Initialisation du terrain
        self.terrain = generate_terrain(WIDTH, HEIGHT, MIN_HEIGHT, MAX_HEIGHT, VARIATION)

        # Initialisation des personnages et de leurs couleurs
        self.players = self.initialize_players()

        # Boucle principale du jeu
        self.running = True
        self.clock = pygame.time.Clock()

    def ask_number_of_players(self):
        running = True
        input_text = ""
        color = (0, 0, 0)

        while running:
            self.screen.fill(SKY_BLUE)
            # Afficher le texte demandant le nombre de joueurs
            prompt_text = self.font.render("Entrez le nombre de joueurs (1-6): " + input_text, True, color)
            self.screen.blit(prompt_text, (WIDTH // 4, HEIGHT // 2))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
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
                        input_text = input_text[:-1]
                    elif event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6]:
                        input_text += event.unicode

            pygame.display.flip()

        return 1  # Retourne un joueur si on quitte la fenêtre

    def initialize_players(self):
        players = []
        for i in range(self.num_players):
            spawn_x = 50 + (i * (WIDTH - 100) // self.num_players)
            player_color = PLAYER_COLORS[i % len(PLAYER_COLORS)]

            print(f"Création du joueur {i + 1} à la position {spawn_x}, couleur {player_color}")

            try:
                # Créer 2 personnages par joueur
                player_characters = [Character(spawn_x, 100 + j * 50, player_color, i + 1) for j in range(2)]
                players.append(player_characters)  # Ajouter les personnages à la liste
                print(f"Joueur {i + 1} créé avec succès avec {len(player_characters)} personnages")
            except Exception as e:
                print(f"Erreur lors de la création du joueur {i + 1}: {e}")
                self.running = False  # Arrêter la boucle en cas d'erreur
        return players

    def start(self):
        while self.running:
            self.update()

    def update(self):
        self.screen.fill(SKY_BLUE)
        draw_terrain(self.screen, self.terrain, HEIGHT)

        # Affichage et mise à jour des personnages
        for player_index in range(self.num_players):
            for character_index in range(len(self.players[player_index])):  # Plusieurs personnages par joueur
                current_character_obj = self.players[player_index][character_index]
                current_character_obj.apply_gravity(self.terrain)  # Le personnage utilise la gravité
                current_character_obj.draw(self.screen)  # Dessiner le personnage
                current_character_obj.draw_health_bar(self.screen)  # Dessiner la barre de vie
                current_character_obj.draw_player_name(self.screen)  # Afficher le nom du joueur

        # Affichage du temps restant pour le tour actuel
        elapsed_time = (pygame.time.get_ticks() - self.turn_start_time) // 1000
        remaining_time = max(0, turn_time_limit - elapsed_time)
        timer_text = self.font.render(f"Temps restant: {remaining_time}s", True, (0, 0, 0))
        self.screen.blit(timer_text, (WIDTH // 2 - timer_text.get_width() // 2, 20))

        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Jump
                    self.players[self.current_player][self.current_character_index].jump()  # Saut pour le personnage actuel
                elif event.key == pygame.K_RETURN:  # Passe au tour suivant
                    self.current_player = (self.current_player + 1) % self.num_players
                    self.current_character_index = 0  # Réinitialiser l'index du personnage
                    self.turn_start_time = pygame.time.get_ticks()  # Redémarre le chronomètre du tour
                elif event.key == pygame.K_TAB:  # Changer de personnage
                    self.current_character_index = (self.current_character_index + 1) % len(self.players[self.current_player])

        # Vérification des touches pour mouvement horizontal - pour le personnage actuel seulement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            if self.players[self.current_player][self.current_character_index].x > 0:
                self.players[self.current_player][self.current_character_index].move(-1, self.terrain, WIDTH)
        if keys[pygame.K_RIGHT]:
            if self.players[self.current_player][self.current_character_index].x < WIDTH - 1:
                self.players[self.current_player][self.current_character_index].move(1, self.terrain, WIDTH)

        # Si le temps du tour est écoulé, on passe au joueur suivant
        if remaining_time == 0:
            self.current_player = (self.current_player + 1) % self.num_players
            self.current_character_index = 0  # Réinitialiser l'index du personnage
            self.turn_start_time = pygame.time.get_ticks()  # Redémarre le chronomètre du tour

        pygame.display.flip()
        self.clock.tick(100)

if __name__ == "__main__":
    game = WormsGame()
    game.start()
    pygame.quit()