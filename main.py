import pygame
import random
from terrain import generate_terrain, draw_terrain, create_crater

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

    # Génère un terrain initial
    terrain = generate_terrain(WIDTH, HEIGHT, 100, 300, 8)

    running = True  # Variable pour maintenir la boucle du jeu
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Vérifie si l'utilisateur ferme la fenêtre
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F5:  # Régénère le terrain
                    terrain = generate_terrain(WIDTH, HEIGHT, 100, 300, 8)
                elif event.key == pygame.K_F4:  # Crée un trou aléatoire
                    explosion_x = random.randint(0, WIDTH - 1)  # Position X aléatoire
                    explosion_radius = random.randint(20, 50)  # Taille aléatoire du trou
                    terrain = create_crater(terrain, explosion_x, explosion_radius)

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
