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
    
    def move(self, terrain, delta_time):  
        if not self.exploded:  # Ne met à jour que si la grenade n'a pas explosé
            self.launch_time += delta_time  # Incrémente le temps de lancement
            if self.launch_time >= 2.5:  # Vérifie si X secondes se sont écoulées
                self.explode(terrain)  # Appelle la méthode d'explosion
                return  # Ne met pas à jour la position si elle a explosé

            if not self.on_ground:  # Ne mettez à jour que si la grenade n'est pas au sol
                self.x, new_y, self.velx, self.vely = Grenade.ballPath(self.x, self.y, self.velx, self.vely, 0.05)
                
                terrain_x = int(self.x)  
                if 0 <= terrain_x < len(terrain):  
                    terrain_height = terrain[terrain_x]  
                    if new_y >= terrain_height - self.radius:  # Collision avec le sol
                        self.y = terrain_height - self.radius  
                        self.vely = -self.vely * self.restitution  # Inverser la vitesse et appliquer le facteur de restitution
                        if abs(self.vely) < 1:  # Arrêt du rebond si vitesse trop faible
                            self.vely = 0
                            self.on_ground = True  # La grenade est maintenant au sol
                    else:
                        self.y = new_y  # Met à jour la position Y
                else:
                    self.y = new_y  # Met à jour la position Y si hors des limites du terrain
            else:
                self.y = terrain[int(self.x)] - self.radius  # Assurez-vous que la grenade reste au-dessus du terrain

    def explode(self, terrain):
        """ Gère l'explosion de la grenade. """
        self.exploded = True
        # Vérifiez si la roquette touche le terrain
        terrain_x = int(self.x)
        if 0 <= terrain_x < len(terrain):
            terrain_height = terrain[terrain_x]
            if self.y >= terrain_height - self.radius:  # Collision avec le sol
                self.y = terrain_height - self.radius
                self.on_ground = True  # La roquette est maintenant au sol
                terrain[:] = create_crater(terrain, terrain_x, 50)  # Mise à jour du terrain
        print("BOOM! La grenade a explosé.")