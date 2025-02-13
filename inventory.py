import pygame  # Assurez-vous d'importer pygame
import pygame_gui
from settings import HEIGHT

# inventory.py
class Inventory:
    def __init__(self, manager):
        self.weapons = ["Weapon 1", "Weapon 2", "Weapon 3"]
        self.current_weapon_index = 0
        self.manager = manager  # Pygame GUI manager

        # Créer des boutons pour chaque arme
        self.weapon_buttons = []
        for i, weapon in enumerate(self.weapons):
            button = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(50 + i * 150, HEIGHT - 100, 140, 50),
                text=weapon,
                manager=self.manager
            )
            self.weapon_buttons.append(button)

    def select_weapon(self, index):
        if 0 <= index < len(self.weapons):
            self.current_weapon_index = index

    def get_current_weapon(self):
        return self.weapons[self.current_weapon_index]

    def draw(self, screen):
        # Affichage de l'inventaire
        for i, button in enumerate(self.weapon_buttons):
            # Mettre en surbrillance l'arme sélectionnée
            if i == self.current_weapon_index:
                button.set_text(f"> {self.weapons[i]} <")  # Indiquer l'arme sélectionnée
            else:
                button.set_text(self.weapons[i])  # Texte normal

        # Dessiner les éléments de l'interface utilisateur
        self.manager.draw_ui(screen)

    def process_events(self, event):
        self.manager.process_events(event)  # Traiter les événements de l'interface utilisateur