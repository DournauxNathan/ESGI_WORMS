# Paramètres du terrain (adaptables)
WIDTH, HEIGHT = 1080, 720
MIN_HEIGHT = 310  # Hauteur minimale (niveau de l'eau)
MAX_HEIGHT = 480  # Hauteur maximale (au centre de l'île)
VARIATION = 15  # Variation aléatoire

# Couleurs
SKY_BLUE = (135, 206, 235)

# Liste des couleurs disponibles pour les joueurs
PLAYER_COLORS = [
    (0, 0, 255),  # Bleu pour le Joueur 1
    (255, 0, 0),  # Rouge pour le Joueur 2
    (0, 255, 0),  # Vert pour le Joueur 3
    (255, 255, 0),  # Jaune pour le Joueur 4
    (255, 165, 0),  # Orange pour le Joueur 5
    (128, 0, 128),  # Violet pour le Joueur 6
]

# Initialisation des variables de jeu
turn_time_limit = 30  # Durée du tour en secondes