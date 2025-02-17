import pygame
import numpy
import math
from terrain import generate_terrain, create_random_craters, draw_terrain, create_crater

class Grenade(object):
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.velx = 0
        self.vely = 0
        self.power = 0
        self.angle = 0
        self.time = 0
        self.on_ground = False
        self.restitution = 0.6  # Facteur de restitution pour le rebond
        self.launch_time = 0  # Temps de lancement
        self.exploded = False  # État d'explosion

    def draw(self, win):
        if not self.exploded:  # Ne dessinez que si la grenade n'a pas explosé
            pygame.draw.circle(win, (0, 0, 0), (self.x, self.y), self.radius)
            pygame.draw.circle(win, self.color, (self.x, self.y), self.radius - 1)

    @staticmethod
    def ballPath(startx, starty, velx, vely, time, mass=1, r=0.1):
        v = numpy.sqrt(velx ** 2 + vely ** 2)
        Fd = Grenade.air_resistance(v, r)
        if v > 0:
            ax = - (Fd / mass) * (velx / v) / 7
            ay = - (Fd / mass) * (vely / v) / 4 - 9.81
        else:
            ax = 0
            ay = -9.81

        velx += ax * time
        vely += ay * time

        newx = startx + velx * time
        newy = starty - vely * time  # Notez le signe négatif pour le mouvement vers le bas

        return newx, newy, velx, vely

    @staticmethod
    def air_resistance(v, r, Cz=0.094, rho=1.225):
        """
        Calcule la force de résistance de l'air sur une sphère en mouvement.
        """
        A = numpy.pi * r ** 2  # Aire frontale de la sphère
        return 0.5 * Cz * rho * A * v ** 2

    @staticmethod
    def findAngle(pos, startx, starty):
        try:
            angle = math.atan2(starty - pos[1], pos[0] - startx)
        except:
            angle = math.pi / 2
        return angle

    def move(self, terrain, delta_time, players):
        # Ne met à jour que si la grenade n'a pas explosé
        if not self.exploded:
            # Incrémente le temps de lancement de la grenade
            self.launch_time += delta_time

            # Si plus de 2.5 secondes se sont écoulées, faire exploser la grenade
            if self.launch_time >= 2.5:
                self.explode(terrain, players)
                return  # Ne met pas à jour la position si la grenade a explosé

            # Ne met à jour la position que si la grenade n'est pas au sol
            if not self.on_ground:
                # Calculer la nouvelle position à l'aide de la méthode ballPath
                self.x, new_y, self.velx, self.vely = Grenade.ballPath(self.x, self.y, self.velx, self.vely, 0.05)

                # Vérifier la collision avec le terrain
                terrain_x = int(self.x)
                if 0 <= terrain_x < len(terrain):
                    terrain_height = terrain[terrain_x]

                    # Si la grenade touche le sol, appliquer la collision
                    if new_y >= terrain_height - self.radius:
                        self.y = terrain_height - self.radius  # Positionner la grenade au sol
                        self.vely = -self.vely * self.restitution  # Inverser la vitesse verticale et appliquer la restitution

                        # Si la vitesse verticale devient trop faible, la grenade s'immobilise
                        if abs(self.vely) < 1:
                            self.vely = 0
                            self.on_ground = True  # La grenade est maintenant au sol
                    else:
                        self.y = new_y  # Mettre à jour la position Y si aucune collision
                else:
                    # Si la grenade est en dehors des limites du terrain, mettre à jour Y normalement
                    self.y = new_y
            else:
                # Si la grenade est déjà au sol, la position Y est ajustée pour rester au-dessus du terrain
                self.y = terrain[int(self.x)] - self.radius

    def explode(self, terrain, players):
        """ Gère l'explosion de la grenade. """
        self.exploded = True
        # Vérifiez si la grenade touche le terrain
        terrain_x = int(self.x)
        if 0 <= terrain_x < len(terrain):
            terrain_height = terrain[terrain_x]
            if self.y >= terrain_height - self.radius:  # Collision avec le sol
                self.y = terrain_height - self.radius
                self.on_ground = True  # La grenade est maintenant au sol
                terrain[:] = create_crater(terrain, terrain_x, 50)  # Mise à jour du terrain
                self.check_damage(players)  # Vérifie les dégâts
                self.reposition_characters(players, terrain)  # Repositionne les personnages
        print("BOOM! La grenade a explosé.")

    def reposition_characters(self, players, terrain):
        """ Repositionne les personnages après une explosion. """
        for player in players:
            for character in player:
                terrain_x = int(character.x)
                if 0 <= terrain_x < len(terrain):
                    terrain_height = terrain[terrain_x]
                    # Vérifiez si le personnage est sous le terrain
                    if character.y + character.radius > terrain_height:  # Si le bas du personnage est sous le terrain
                        character.y = terrain_height - character.radius  # Repositionne le personnage au-dessus du terrain
                        character.on_ground = True  # Le personnage est maintenant au sol
                    else:
                        character.on_ground = False  # Si le personnage n'est pas sous le terrain, il n'est pas au sol

    def check_damage(self, players):
        for player in players:
            for character in player:
                distance = math.hypot(character.x - self.x, character.y - self.y)
                print(f"Distance to character: {distance}")  # Pour le débogage
                if distance <= 50:  # Rayon d'explosion
                    print(f"Character {character.player_number} takes damage!")  # Pour le débogage
                    character.take_damage(10)  # Inflige 5 de dégâts