import pygame
from terrain import generate_terrain, draw_terrain

# Initialisation de Pygame
pygame.init()

# Dimensions de l'écran
WIDTH, HEIGHT = 800, 600

# Couleur du ciel
SKY_BLUE = (135, 206, 235)

# Initialisation de l'écran
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Crée une fenêtre Pygame
pygame.display.set_caption("Worms Terrain")  # Définit le titre de la fenêtre

def main():
    """
    Fonction principale qui gère la boucle du jeu.
    """
    clock = pygame.time.Clock()  # Horloge pour limiter les FPS

    # Génère un terrain
    terrain = generate_terrain(WIDTH, HEIGHT, 100, 300, 10)

    running = True  # Variable pour maintenir la boucle du jeu
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Vérifie si l'utilisateur ferme la fenêtre
                running = False

        # Efface l'écran en remplissant avec la couleur du ciel
        screen.fill(SKY_BLUE)

        # Dessine le terrain
        draw_terrain(screen, terrain, HEIGHT)

        # Met à jour l'affichage
        pygame.display.flip()
        clock.tick(60)  # Limite la boucle à 60 images par seconde

    pygame.quit()  # Ferme Pygame proprement

if __name__ == "__main__":
    main()  # Lance le jeu si le fichier est exécuté directement
