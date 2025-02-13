import pygame
import random
from character import Character
from terrain import generate_terrain, create_random_craters, draw_terrain, create_crater
import numpy as np
import math
import settings
from interface import Inventory
import pygame_gui

class WormsGame:
    #region FONCTIONS
    def __init__(self):
        #region INITIALISATION
        # Initialisation de Pygame
        pygame.init()
        
        # Initialisation de l'écran
        self.screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
        pygame.display.set_caption("Worms Game")
        
        # Police pour afficher le texte
        self.font = pygame.font.SysFont("Arial", 24)

        # Initialisation des variables de jeu
        self.current_player = 0  # Le joueur actuellement en train de jouer
        self.current_character_index = 0  # L'index du personnage actuellement contrôlé

        # Demander le nombre de joueurs avant de commencer
        self.num_players = self.ask_number_of_players()

        # Initialisation du terrain & Créer des cratères aléatoires sur le terrain
        self.terrain = generate_terrain(settings.WIDTH, settings.HEIGHT, settings.MIN_HEIGHT, settings.MAX_HEIGHT)
        self.terrain = create_random_craters(self.terrain, 20, settings.WIDTH)

        # Initialisation des personnages et de leurs couleurs
        self.players = self.initialize_players()

        # Initialisation de pygame_gui & de l'inventaire avec le gestionnaire
        self.manager = pygame_gui.UIManager((settings.WIDTH, settings.HEIGHT))
        self.inventory = Inventory(self.manager)
        #endregion

        # Boucle principale du jeu
        self.running = True
        self.clock = pygame.time.Clock()

    def ask_number_of_players(self):
        running = True
        input_text = "1"
        color = (0, 0, 0)

        while running:
            self.screen.fill(settings.SKY_COLOR)
            # Afficher le texte demandant le nombre de joueurs
            prompt_text = self.font.render("Entrez le nombre de joueurs (1-6): " + input_text, True, color)
            self.screen.blit(prompt_text, (settings.WIDTH // 4, settings.HEIGHT // 2))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event .key == pygame.K_RETURN:
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

        return 1

    def initialize_players(self):
        players = []
        
        for i in range(self.num_players):
            player_color = settings.PLAYER_COLORS[i % len(settings.PLAYER_COLORS)]
            print(f"Création du joueur {i + 1}, couleur {player_color}")

            try:
                player_characters = []
                for j in range(settings.CHARA_NUMBER):  # Créer X personnages par joueur
                    randomPosition = random.randint(50, settings.WIDTH - 100)  # Générer une position aléatoire
                    player_characters.append(Character(randomPosition + 25, 100 + j * 50, player_color, i + 1))

                players.append(player_characters)  # Ajouter les personnages à la liste
                print(f"Joueur {i + 1} créé avec succès avec {len(player_characters)} personnages")
            except Exception as e:
                print(f"Erreur lors de la création du joueur {i + 1}: {e}")
                self.running = False  # Arrêter la boucle en cas d'erreur

        return players
    #endregion

    def start(self):
        while self.running:
            self.update()

    def update(self):
        self.screen.fill(settings.SKY_COLOR)
        draw_terrain(self.screen, self.terrain, settings.HEIGHT)
        # Dessiner l'interface de l'inventaire
        self.inventory.draw(self.screen)

        #region Affichage et mise à jour des personnages
        for player_index in range(self.num_players):
            for character_index in range(len(self.players[player_index])):  # Plusieurs personnages par joueur
                current_character_obj = self.players[player_index][character_index]
                
                # Appliquer la gravité
                current_character_obj.apply_gravity(self.terrain)  # Le personnage utilise la gravité
                
                # Vérifier la position Y par rapport au terrain
                
                terrain_height = self.terrain[int(current_character_obj.x)]  # Hauteur du terrain à la position X
                if current_character_obj.y < terrain_height and current_character_obj.on_ground:  # Si le personnage est au-dessus du terrain
                    current_character_obj.y = terrain_height  # Ajuster la position Y au niveau du terrain
                
                current_character_obj.draw(self.screen)  # Dessiner le personnage
                current_character_obj.draw_player_name(self.screen)  # Afficher le nom du joueur    
                current_character_obj.draw_health_bar(self.screen)  # Dessiner la barre de vie
        #endregion

        #region Vérification des touches pour mouvement horizontal - pour le personnage actuel seulement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            if self.players[self.current_player][self.current_character_index].x > 0:
                self.players[self.current_player][self.current_character_index].move(-1, self.terrain, settings.WIDTH)
        if keys[pygame.K_RIGHT]:
            if self.players[self.current_player][ self.current_character_index].x < settings.WIDTH - 1:
                self.players[self.current_player][self.current_character_index].move(1, self.terrain, settings.WIDTH)
        if keys[pygame.K_UP]:
            print("+") # Modifie l'angle de tir en positif
        if keys[pygame.K_DOWN]:
            print("-")  # Modifie l'angle de tir en négatif
        #endregion

        #region Gestion des événements [APPUIE SUR UNE TOUCHE]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                # DEBUG
                if event.key == pygame.K_F4:  # Passe au tour suivant
                    self.current_player = (self.current_player + 1) % self.num_players
                elif event.key == pygame.K_F5:  # Créer une explosion
                    self.terrain = create_crater(self.terrain, random.randint(1, settings.WIDTH-1), random.randint(25,50)) #Création d'un cratère
                # PLAYER INPUT
                elif event.key == pygame.K_RETURN:  # FIRE
                    print("Tirer")
                
                elif event.key == pygame.K_SPACE:  # Jump
                    self.players[self.current_player][self.current_character_index].jump()

                elif event.key == pygame.K_TAB:  # Changer de personnage
                    self.current_character_index = (self.current_character_index + 1) % len(self.players[self.current_player])

                # SELECTION DES ARMES
                elif event.key == pygame.K_1:
                    self.inventory.select_weapon(0)
                
                elif event.key == pygame.K_2:
                    self.inventory.select_weapon(1)
                
                elif event.key == pygame.K_3:
                    self.inventory.select_weapon(2)
            
            self.manager.process_events(event)  # Process pygame_gui events
        #endregion    

        self.manager.update(self.clock.tick(60) / 1000.0)  # Mettre à jour le gestionnaire
        self.manager.draw_ui(self.screen)  # Dessiner l'interface utilisateur
        pygame.display.flip()  # Mettre à jour l'affichage
        self.clock.tick(60)  # Limiter le nombre de frames par seconde

if __name__ == "__main__":
    WormsGame().start()
    pygame.quit()