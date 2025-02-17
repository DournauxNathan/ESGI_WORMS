import pygame
import math
import numpy

from terrain import generate_terrain, create_random_craters, draw_terrain, create_crater

class Roquette(object):
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.power = 0
        self.angle = 0
        self.time = 0
        self.radius = radius
        self.color = color
        self.on_ground = False  # État pour savoir si la roquette est au sol

    def draw(self, win):
        if not self.on_ground:  # Ne dessinez que si la roquette n'est pas au sol
            pygame.draw.circle(win, (0, 0, 0), (self.x, self.y), self.radius)
            pygame.draw.circle(win, self.color, (self.x, self.y), self.radius - 1)

    @staticmethod
    def air_resistance(v, r, Cd=0.1, rho=1.225):
        S = numpy.pi * r**2 / 2  # surface d'un demi cercle
        return 0.5 * Cd * rho * S * v**2

    @staticmethod
    def ballPath(startx, starty, power, ang, time, mass=1, r=0.1):
        velx = numpy.cos(ang) * power
        vely = math.sin(ang) * power
        v = numpy.sqrt(velx ** 2 + vely ** 2)
        Fd = Roquette.air_resistance(v, r)
        if v > 0:
            ax = - (Fd / mass) * (velx / v) / 7
            ay = - (Fd / mass) * (vely / v) / 4 - 2.81
        else:
            ax = 0
            ay = -2.81

        velx += ax * time
        vely += ay * time
        distX = velx * time
        distY = (vely * time)
        newx = round(distX + startx)
        newy = round(starty - distY)
        return (newx, newy)

    def findAngle(self, pos):
        sX = self.x
        sY = self.y
        try:
            angle = math.atan((sY - pos[1]) / (sX - pos[0]))
        except:
            angle = math.pi / 2
        if pos[1] < sY and pos[0] > sX:
            angle = abs(angle)
        elif pos[1] < sY and pos[0] < sX:
            angle = math.pi - angle
        elif pos[1] > sY and pos[0] < sX:
            angle = math.pi + abs(angle)
        elif pos[1] > sY and pos[0] > sX:
            angle = (math.pi * 2) - angle
        return angle

    def move(self, terrain, players):
        if not self.on_ground:  # Ne mettez à jour que si la roquette n'est pas au sol
            self.time += 0.05
            po = self.ballPath(self.x, self.y, self.power, self.angle, self.time)
            self.x = po[0]
            self.y = po[1]

            # Vérifiez si la roquette touche le terrain
            terrain_x = int(self.x)
            if 0 <= terrain_x < len(terrain):
                terrain_height = terrain[terrain_x]
                if self.y >= terrain_height - self.radius:  # Collision avec le sol
                    self.y = terrain_height - self.radius
                    self.on_ground = True  # La roquette est maintenant au sol
                    terrain[:] = create_crater(terrain, terrain_x, 25)  # Mise à jour du terrain
                    self.check_damage(players)  # Vérifie les dégâts
                    self.reposition_characters(players, terrain)  # Repositionne les personnages

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
                if distance <= 20:  # Rayon d'explosion
                    print(f"Character {character.player_number} takes damage!")  # Pour le débogage
                    character.take_damage(5)  # Inflige 5 de dégâts