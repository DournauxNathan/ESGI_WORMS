import pygame
import random
import numpy as np
import math
import settings
import pygame_gui
from character import Character
from terrain import generate_terrain, create_random_craters, draw_terrain, create_crater
from inventory import Inventory

class WormsGame:
    #region INITIALISATION
    def __init__(self):
        """
        Initialisation du jeu : Pygame, écran, terrain, joueurs, interface et boucle de jeu.
        """
        pygame.init()
        
        # Initialisation de l'écran
        self.screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
        pygame.display.set_caption("Worms Game")
        
        # Police pour afficher le texte
        self.font = pygame.font.SysFont("Arial", 24)
        
        # Variables de jeu
        self.current_player = 0  # Joueur actuel
        self.current_character_index = 0  # Personnage actuel
        self.num_players = self.ask_number_of_players()
        
        # Génération du terrain
        self.terrain = generate_terrain(settings.WIDTH, settings.HEIGHT, settings.MIN_HEIGHT, settings.MAX_HEIGHT)
        self.terrain = create_random_craters(self.terrain, 20, settings.WIDTH)
        
        # Initialisation des joueurs
        self.players = self.initialize_players()
        
        # Gestion de l'interface et de l'inventaire
        self.manager = pygame_gui.UIManager((settings.WIDTH, settings.HEIGHT))
        self.inventory = Inventory(self.manager)
        
        # Boucle de jeu
        self.running = True
        self.clock = pygame.time.Clock()
    #endregion
    
    #region DEMANDE_NOMBRE_JOUEURS
    def ask_number_of_players(self):
        """
        Demande à l'utilisateur d'entrer le nombre de joueurs (1-6) et le valide.
        """
        running = True
        input_text = "1"
        color = (0, 0, 0)
        
        while running:
            self.screen.fill(settings.SKY_COLOR)
            prompt_text = self.font.render(f"Entrez le nombre de joueurs (1-6): {input_text}", True, color)
            self.screen.blit(prompt_text, (settings.WIDTH // 4, settings.HEIGHT // 2))
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and input_text.isdigit():
                        num_players = int(input_text)
                        if 1 <= num_players <= 6:
                            return num_players
                        else:
                            input_text = ""
                            color = (255, 0, 0)
                    elif event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    elif event.unicode.isdigit():
                        input_text += event.unicode
            
            pygame.display.flip()
        
        return 1
    #endregion
    
    #region INITIALISATION_JOUEURS
    def initialize_players(self):
        """
        Initialise les joueurs avec leurs personnages et couleurs respectives.
        """
        players = []
        for i in range(self.num_players):
            player_color = settings.PLAYER_COLORS[i % len(settings.PLAYER_COLORS)]
            player_characters = [Character(random.randint(50, settings.WIDTH - 100) + 25, 100 + j * 50, player_color, i + 1) 
                                 for j in range(settings.CHARA_NUMBER)]
            players.append(player_characters)
        return players
    #endregion
    
    #region BOUCLE_PRINCIPALE
    def start(self):
        """
        Démarre la boucle principale du jeu.
        """
        while self.running:
            self.update()
    #endregion
    
    #region MISE_A_JOUR
    def update(self):
        """
        Met à jour l'état du jeu, gère les entrées et affiche les éléments.
        """
        self.screen.fill(settings.SKY_COLOR)
        draw_terrain(self.screen, self.terrain, settings.HEIGHT)
        self.inventory.draw(self.screen)
        
        # Affichage des personnages
        for player in self.players:
            for character in player:
                character.apply_gravity(self.terrain)
                character.draw(self.screen)
                character.draw_player_name(self.screen)
                character.draw_health_bar(self.screen)
        
        # Gestion des mouvements des personnages
        keys = pygame.key.get_pressed()
        current_character = self.players[self.current_player][self.current_character_index]
        if keys[pygame.K_LEFT] and current_character.x > 0:
            current_character.move(-1, self.terrain, settings.WIDTH)
        if keys[pygame.K_RIGHT] and current_character.x < settings.WIDTH - 1:
            current_character.move(1, self.terrain, settings.WIDTH)
        
        # Gestion des événements clavier
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F4:
                    self.current_player = (self.current_player + 1) % self.num_players
                elif event.key == pygame.K_F5:
                    self.terrain = create_crater(self.terrain, random.randint(1, settings.WIDTH - 1), random.randint(25, 50))
                elif event.key == pygame.K_RETURN:
                    print("Tirer")
                elif event.key == pygame.K_SPACE:
                    current_character.jump()
                elif event.key == pygame.K_TAB:
                    self.current_character_index = (self.current_character_index + 1) % len(self.players[self.current_player])
                elif event.key == pygame.K_F1:  # Choisir un personnage aléatoire pour infliger des dégâts
                    random_player_index = random.randint(0, self.num_players - 1)
                    random_character_index = random.randint(0, len(self.players[random_player_index]) - 1)
                    damage = random.randint(5, 20)  # Dégâts aléatoires entre 5 et 20
                    self.players[random_player_index][random_character_index].take_damage(damage)
                
                self.manager.process_events(event)
        
        self.manager.update(self.clock.tick(60) / 1000.0)
        self.manager.draw_ui(self.screen)
        pygame.display.flip()
        self.clock.tick(60)
    #endregion
    
if __name__ == "__main__":
    WormsGame().start()
    pygame.quit()
