import pygame
import random
import numpy as np
import math
import settings
import pygame_gui
from character import Character
from terrain import generate_terrain, create_random_craters, draw_terrain, create_crater
from inventory import Inventory
import Roquette, Grenade 

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
        self.winner = None  # Variable pour stocker le vainqueur
        self.roquette_instance = None
        self.grenade_instance = None
    #endregion
    
    #region DEMANDE_NOMBRE_JOUEURS
    def ask_number_of_players(self):
        """
        Demande à l'utilisateur d'entrer le nombre de joueurs (2-6) et le valide.
        """
        running = True
        input_text = "2"
        color = (0, 0, 0)
        
        while running:
            self.screen.fill(settings.SKY_COLOR)
            prompt_text = self.font.render(f"Entrez le nombre de joueurs (2-6): {input_text}", True, color)
            self.screen.blit(prompt_text, (settings.WIDTH // 4, settings.HEIGHT // 2))
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and input_text.isdigit():
                        num_players = int(input_text)
                        if 2 <= num_players <= 6:  # Modifié pour accepter 2 à 6 joueurs
                            return num_players
                        else:
                            input_text = ""
                            color = (255, 0, 0)
                    elif event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    elif event.unicode.isdigit():
                        input_text += event.unicode
            
            pygame.display.flip()
        
        return 2  # Valeur par défaut
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
    
    #region REINITIALISATION_DU_JEU
    def reset_game(self):
        """
        Réinitialise l'état du jeu pour recommencer une nouvelle partie.
        """
        self.current_player = 0
        self.current_character_index = 0
        self.num_players = self.ask_number_of_players()
        self.terrain = generate_terrain(settings.WIDTH, settings.HEIGHT, settings.MIN_HEIGHT, settings.MAX_HEIGHT)
        self.terrain = create_random_craters(self.terrain, 20, settings.WIDTH)
        self.players = self.initialize_players()
        self.winner = None
    #endregion

    #region BOUCLE_PRINCIPALE
    def start(self):
        """ Démarre la boucle principale du jeu. """
        self.running = True  # Réinitialise l'état de la variable running
        while True:  # Boucle infinie pour relancer le jeu
            while self.running:
                self.update()
                self.check_game_over()  # Vérifie si la partie est terminée
            
            if self.winner is not None:  # Afficher le vainqueur seulement si un joueur a gagné
                self.display_winner()

            # Vérifie si le joueur veut rejouer
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    self.reset_game()  # Relance une nouvelle partie
                    break
                elif event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    return  # Quitte proprement le programme

    #endregion
    
    #region MISE_A_JOUR
    def update(self):
        """ Met à jour l'état du jeu, gère les entrées et affiche les éléments. """
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
        
        #region USER INPUT
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
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_F4:
                    self.current_player = (self.current_player + 1) % self.num_players
                elif event.key == pygame.K_F5:
                    self.terrain = create_crater(self.terrain, random.randint(1, settings.WIDTH - 1), random.randint(25, 50))
                elif event.key == pygame.K_1:
                    self.inventory.current_weapon_index = 0
                elif event.key == pygame.K_2:
                    self.inventory.current_weapon_index = 1
                elif event.key == pygame.K_3:
                    self.inventory.current_weapon_index = 2
                
                elif event.key == pygame.K_RETURN and not current_character.has_shoot:
                    if self.inventory.current_weapon_index == 1: 
                        self.roquette_instance = Roquette.Roquette(current_character.x, current_character.y, 5, (255, 0, 0))
                        mousePos = pygame.mouse.get_pos()
                        self.roquette_instance.power = math.sqrt((mousePos[1] - self.roquette_instance.y) ** 2 + (mousePos[0] - self.roquette_instance.x) ** 2)    
                        self.roquette_instance.angle = self.roquette_instance.findAngle(mousePos)
                        print(f" \n Roquette tirée, avec :\n - une puissance de {self.roquette_instance.power} \n - Un angle de {self.roquette_instance.angle} \n")
                    
                    elif self.inventory.current_weapon_index == 2: 
                        self.grenade_instance = Grenade.Grenade(current_character.x, current_character.y, 5, (255, 0, 0))
                        mousePos = pygame.mouse.get_pos()
                        self.grenade_instance.power = math.sqrt((mousePos[1] - self.grenade_instance.y) ** 2 + (mousePos[0] - self.grenade_instance.x) ** 2)
                        self.grenade_instance.angle = self.grenade_instance.findAngle(mousePos, self.grenade_instance.x, self.grenade_instance.y)
                        self.grenade_instance.velx = math.cos(self.grenade_instance.angle) *  self.grenade_instance.power
                        self.grenade_instance.vely = math.sin(self.grenade_instance.angle) *  self.grenade_instance.power

                        print(f" \n Grenade lancée, avec :\n - une puissance de {self.grenade_instance.power} \n - Un angle de {self.grenade_instance.angle} \n")
                        print(f"- Velocité[{self.grenade_instance.velx}, {self.grenade_instance.vely}]")
                    current_character.has_shoot = True

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
        #endregion
        
        if self.inventory.current_weapon_index == 1 or self.inventory.current_weapon_index == 2:
            # Dessiner une ligne en pointillés entre la roquette et le curseur
            self.draw_dashed_line(current_character.x, current_character.y, pygame.mouse.get_pos())

        if self.roquette_instance:
            self.roquette_instance.move(self.terrain, self.players)  # Passez les joueurs
            self.roquette_instance.draw(self.screen)
            if current_character.has_shoot:
                current_character.has_shoot = False

        if self.grenade_instance:
            delta_time = self.clock.tick(60) / 1000.0  # Temps écoulé depuis la dernière image
            self.grenade_instance.move(self.terrain, delta_time, self.players)  # Passez les joueurs
            self.grenade_instance.draw(self.screen)  # Dessinez la grenade

            if current_character.has_shoot:
                current_character.has_shoot = False

        self.manager.update(self.clock.tick(60) / 1000.0)
        self.manager.draw_ui(self.screen)
        pygame.display.flip()
        self.clock.tick(60)
    #endregion

    #region 
    def draw_dashed_line(self, start_x, start_y, end_pos, dash_length=5):
        """ Dessine une ligne en pointillés entre deux points. """
        # Calculer la distance et l'angle
        distance = math.hypot(end_pos[0] - start_x, end_pos[1] - start_y)
        angle = math.atan2(end_pos[1] - start_y, end_pos[0] - start_x)

        # Dessiner des segments de ligne
        for i in range(0, int(distance), dash_length * 2):
            start_segment_x = start_x + math.cos(angle) * i
            start_segment_y = start_y + math.sin(angle) * i
            end_segment_x = start_x + math.cos(angle) * (i + dash_length)
            end_segment_y = start_y + math.sin(angle) * (i + dash_length)
            pygame.draw.line(self.screen, (0, 0, 0), (start_segment_x, start_segment_y), (end_segment_x, end_segment_y), 2)
    #endregion

    #region VERIFICATION_FIN_DE_JEU
    def check_game_over(self):
        """
        Vérifie si la partie est terminée et met à jour le vainqueur.
        """
        alive_players = [i for i, player in enumerate(self.players) if any(character.health > 0 for character in player)]
        
        if len(alive_players) == 1:
            self.winner = alive_players[0] + 1  # Le joueur gagnant (1-indexé)
            self.running = False  # Arrête le jeu
    #endregion

    #region AFFICHAGE_VAINQUEUR
    def display_winner(self):
        """ Affiche le vainqueur au centre de l'écran et attend que l'utilisateur appuie sur Entrée. """
        self.screen.fill(settings.SKY_COLOR)
        winner_text = f"Le Vainqueur est le Joueur {self.winner}!"
        text_surface = self.font.render(winner_text, True, (255, 0, 0))
        text_rect = text_surface.get_rect(center=(settings.WIDTH // 2, settings.HEIGHT // 2))
        self.screen.blit(text_surface, text_rect)
        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        waiting = False  # Sort de la boucle d'attente
                        self.restart_game()  # Relance le jeu dans une nouvelle fenêtre
    #endregion

    def restart_game(self):
        """ Relance le jeu dans une nouvelle fenêtre. """
        pygame.quit()  # Ferme l'ancienne fenêtre
        WormsGame().start()  # Crée une nouvelle instance et démarre le jeu

if __name__ == "__main__":
    WormsGame().start()
    pygame.quit()