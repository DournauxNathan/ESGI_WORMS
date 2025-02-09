import pygame
import subprocess
import sys

# Initialisation de pygame
pygame.init()

# Définition des couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# Définition de la fenêtre
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Main Menu")

# Chargement de la police
font = pygame.font.Font(None, 36)

# Bouton générique
class Button:
    def __init__(self, text, x, y, width, height, action=None):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = GRAY
        self.action = action

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        text_surface = font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# Création des boutons
buttons = [
    Button("Play", 300, 200, 200, 50, action="play"),
    Button("Crédits", 300, 300, 200, 50, action="credits"),
    Button("Quit", 300, 400, 200, 50, action="quit")
]

# Scène active
current_scene = "menu"

# Liste des crédits
developers = ["Nathan DOURNAUX", "Sarobidy RAHARIMANANA", "Adam NESSAIBIA", "Théo Breton"]
assets_text = ["Assets utilisés :"]

def draw_main_menu():
    screen.fill(WHITE)
    for button in buttons:
        button.draw(screen)

def draw_credits():
    screen.fill(WHITE)
    
    # Affichage des développeurs
    for i, text in enumerate(developers):
        text_surface = font.render(text, True, BLACK)
        screen.blit(text_surface, (50, 50 + i * 40))

    # Affichage des assets
    for i, text in enumerate(assets_text):
        text_surface = font.render(text, True, BLACK)
        screen.blit(text_surface, (50, 300 + i * 30))

    # Bouton retour
    back_button = Button("Retour", 50, 500, 150, 50, action="menu")
    back_button.draw(screen)
    return back_button

running = True
while running:
    screen.fill(WHITE)
    pos = pygame.mouse.get_pos()

    if current_scene == "menu":
        draw_main_menu()
    elif current_scene == "credits":
        back_button = draw_credits()

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if current_scene == "menu":
                for button in buttons:
                    if button.is_clicked(event.pos):
                        if button.action == "play":
                            subprocess.run(["python", "main.py"])  # Exécute main.py
                            running = False  # Ferme le menu après lancement
                            print("Lancer le jeu...")
                        elif button.action == "credits":
                            current_scene = "credits"
                        elif button.action == "quit":
                            running = False
            elif current_scene == "credits" and back_button.is_clicked(event.pos):
                current_scene = "menu"

pygame.quit()
sys.exit()
