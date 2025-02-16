import pygame
import math
import scipy
import matplotlib
import numpy

class Grenade(object):
    def __init__(self,x,y,radius,color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.velx = 0
        self.vely = 0
        self.power = 0
        self.angle = 0
        self.time = 0
        self.restitution = 0.6  # Facteur de restitution pour le rebond

    def draw(self, win):
        pygame.draw.circle(win, (0,0,0), (self.x,self.y), self.radius)
        pygame.draw.circle(win, self.color, (self.x,self.y), self.radius-1)


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
        newy = starty - vely * time

        if newy >= 500 - 5:
            newy = 500 - 5
            vely = -vely * 0.6  # Rebond
            if abs(vely) < 1:  # Arrêt du rebond si vitesse trop faible
                vely = 0
                velx = 0

        return newx, newy, velx, vely

    @staticmethod
    def air_resistance(v, r, Cz=0.094, rho=1.225):
        """
        Calcule la force de résistance de l'air sur une sphère en mouvement.

        :param v: Vitesse de l'objet (m/s)
        :param r: Rayon de l'objet (m)
        :param Cz: Coefficient de traînée (par défaut 0.47 pour une sphère)
        :param rho: Densité de l'air (kg/m^3, par défaut 1.225 au niveau de la mer)
        :return: Force de traînée (N)
        """
        A = numpy.pi * r ** 2  # Aire frontale de la sphère
        return 0.5 * Cz * rho * A * v ** 2

    def findAngle(pos, startx, starty):
        try:
            angle = math.atan2(starty - pos[1], pos[0] - startx)
        except:
            angle = math.pi / 2
        return angle
    
    def move(self, terrain):
        self.x, self.y, self.velx, self.vely = Grenade.ballPath(self.x, self.y, self.velx, self.vely, 0.05)
        
        """
        terrain_height = terrain[int(self.x)]  # Hauteur du terrain à la position x
        self.y = terrain_height - self.radius  # Met à jour la position Y   
        """
            
