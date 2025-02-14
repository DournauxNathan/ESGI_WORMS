import pygame
import random
import math

# Initialisation de Pygame
pygame.init()

# Dimensions de la fenêtre
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Terrain Modifier")

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GROUND_COLOR = (139, 69, 19)  # Couleur du sol (marron)
GRENADE_COLOR = (255, 0, 0)  # Couleur de la grenade (rouge)

# Paramètres du terrain
min_height = 50
max_height = 300
num_craters = 5
previous_num_craters = num_craters  # Pour suivre le nombre de cratères précédent

# Classe pour la grenade
class Grenade:
    def __init__(self, x, y, timer):
        self.x = x
        self.y = y
        self.timer = timer
        self.active = True
        self.start_time = pygame.time.get_ticks()
        self.velocity_y = 0  # Vitesse verticale
        self.velocity_x = 0  # Vitesse horizontale
        self.gravity = 0.5  # Force de gravité
        self.bounce_factor = 0.7  # Facteur de rebond

    def update(self, terrain):
        if self.active:
            # Appliquer la gravité
            self.velocity_y += self.gravity
            self.y += self.velocity_y
            self.x += self.velocity_x

            # Vérifier si la grenade touche le sol
            terrain_height = terrain[int(self.x)]
            if self.y >= terrain_height:
                self.y = terrain_height  # Réinitialiser la position à la hauteur du terrain
                self.handle_bounce(terrain, int(self.x))

            # Vérifier si le temps est écoulé pour l'explosion
            if (pygame.time.get_ticks() - self.start_time >= self.timer * 1000):
                self.explode(terrain)

    def handle_bounce(self, terrain, x):
        # Calculer la pente (normale) à la position de la grenade
        if x > 0 and x < len(terrain) - 1:
            slope = (terrain[x + 1] - terrain[x - 1]) / 2.0  # Pente entre les deux points adjacents
            normal_angle = math.atan(slope)  # Angle de la normale

            # Calculer la nouvelle direction de la vitesse
            speed = math.sqrt(self.velocity_x ** 2 + self.velocity_y ** 2)
            angle_of_incidence = math.atan2(self.velocity_y, self.velocity_x)

            # Calculer l'angle de réflexion
            angle_of_reflection = 2 * normal_angle - angle_of_incidence

            # Mettre à jour les vitesses
            self.velocity_x = speed * math.cos(angle_of_reflection)
            self.velocity_y = -speed * math.sin(angle_of_reflection) * self.bounce_factor

    def explode(self, terrain):
        self.active = False
        return self.x, self.y  # Retourne la position de l'explosion

def generate_terrain(width, height, min_height, max_height):
    terrain = []
    center = width // 2

    for x in range(width):
        distance = abs(x - center)
        base_height = max_height - (max_height - min_height) * (distance / center) ** 2
        terrain.append(int(height - base_height))

    return terrain

def create_random_craters(terrain, num_craters, width):
    for _ in range(num_craters):
        x = random.randint(5, width - 5)
        radius = random.randint(50, 75)
        terrain = create_crater(terrain, x, radius)

    return terrain

def draw_terrain(screen, terrain, height):
    for x in range(len(terrain)):
        pygame.draw.line(screen, GROUND_COLOR, (x, terrain[x]), (x, height))

def create_crater(terrain, x, radius):
    for i in range(max(0, int(x) - radius), min(len(terrain), int(x) + radius)):
        distance = abs(i - x)
        if distance < radius:
            depth = int((radius - distance) ** 0.87)
            terrain[i] = max(terrain[i] + depth, 0)

    return terrain

def draw_slider(screen, x, y, width, value, min_value, max_value):
    pygame.draw.rect(screen, BLACK, (x, y, width, 20))
    pygame.draw.rect(screen, WHITE, (x + value * width / (max_value - min_value), y, 10, 20))

def draw_grenade(screen, grenade):
    if grenade.active:
        pygame.draw.circle(screen, GRENADE_COLOR, (int(grenade.x), int(grenade .y)), 10)

def draw_button(screen, x, y, width, height, text):
    pygame.draw.rect(screen, BLACK, (x, y, width, height))
    font = pygame.font.Font(None, 36)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(text_surface, text_rect)

def main():
    global min_height, max_height, num_craters, previous_num_craters
    clock = pygame.time.Clock()
    running = True
    terrain = generate_terrain(WIDTH, HEIGHT, min_height, max_height)
    grenade = None  # Initialiser la grenade

    while running:
        screen.fill(WHITE)

        # Dessiner le terrain
        draw_terrain(screen, terrain, HEIGHT)

        # Dessiner les sliders
        draw_slider(screen, 50, 50, 200, min_height, 0, 500)
        draw_slider(screen, 50, 100, 200, max_height, 0, 500)
        draw_slider(screen, 50, 150, 200, num_craters, 0, 20)

        # Dessiner le bouton pour faire apparaître la grenade
        draw_button(screen, 50, 200, 200, 40, "Spawn Grenade")

        # Dessiner la grenade
        if grenade:
            draw_grenade(screen, grenade)

        # Événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Clic gauche
                    mouse_x, mouse_y = event.pos
                    if 50 <= mouse_x <= 250:
                        if 50 <= mouse_y <= 70:
                            min_height = int((mouse_x - 50) / 200 * 500)
                        elif 100 <= mouse_y <= 120:
                            max_height = int((mouse_x - 50) / 200 * 500)
                        elif 150 <= mouse_y <= 170:
                            new_num_craters = int((mouse_x - 50) / 200 * 20)
                            if new_num_craters != previous_num_craters:  # Vérifier si le nombre de cratères a changé
                                num_craters = new_num_craters
                                terrain = generate_terrain(WIDTH, HEIGHT, min_height, max_height)
                                terrain = create_random_craters(terrain, num_craters, WIDTH)
                                previous_num_craters = num_craters  # Mettre à jour le nombre de cratères précédent
                        elif 200 <= mouse_y <= 240:  # Zone pour faire apparaître la grenade
                            grenade = Grenade((random.randrange(100, WIDTH - 100)), HEIGHT // 2, 3)  # Créer une grenade au centre de l'écran

        # Mettre à jour la grenade
        if grenade:
            grenade.update(terrain)  # Passer le terrain à la méthode update
            if not grenade.active:  # Si la grenade a explosé
                explosion_position = grenade.explode(terrain)
                if explosion_position:
                    x, y = explosion_position
                    radius = 50  # Rayon de l'explosion
                    for i in range(max(0, int(x) - radius), min(WIDTH, int(x) + radius)):
                        terrain = create_crater(terrain, i, radius)  # Détruire le terrain autour de l'explosion
                grenade = None  # Réinitialiser la grenade après l'explosion

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()