import pygame
import math
import scipy
import matplotlib
import numpy

class Roquette(object):
    def __init__(self,x,y,radius,color):
        self.x = x
        self.y = y
        self.power = 0
        self.angle = 0
        self.time = 0
        self.radius = radius
        self.color = color
        
    def draw(self, win):
        pygame.draw.circle(win, (0,0,0), (self.x,self.y), self.radius)
        pygame.draw.circle(win, self.color, (self.x,self.y), self.radius-1)

    @staticmethod
    def air_resistance(v, r, Cd=0.1, rho=1.225):
        S = numpy.pi * r**2 /2  #surface d'un demi cercle
        return 0.5 * Cd * rho * S * v**2

    @staticmethod
    def ballPath(startx, starty, power, ang, time, mass = 1, r = 0.1):
        velx = numpy.cos(ang) * power
        vely = math.sin(ang) * power
        v = numpy.sqrt(velx ** 2 + vely ** 2)
        Fd = Roquette.air_resistance(v, r)
        if v > 0 :
            ax = - (Fd / mass) * (velx / v) /7
            ay = - (Fd / mass) * (vely / v) /4 - 2.81
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
    
    def move(self, terrain):
        if self.y < 500 - self.radius:
                self.time += 0.05
                po = self.ballPath(self.x, self.y, self.power, self.angle, self.time)
                self.x = po[0]
                self.y = po[1]
        else:
            shoot = False
            self.time = 0
            self.y = 494
        
def air_resistance(v, r, Cd=0.1, rho=1.225):
    """
    Calcule la force de résistance de l'air sur une sphère en mouvement.

    :param v: Vitesse de l'objet (m/s)
    :param r: Rayon de l'objet (m)
    :param Cd: Coefficient de traînée (par défaut 0.04 pour un corps profilé)
    :param rho: Densité de l'air (kg/m^3, par défaut 1.225 au niveau de la mer)
    :return: Force de traînée (N)
    """
    A = numpy.pi * r ** 2  # Aire frontale de la sphère
    return 0.5 * Cd * rho * A * v ** 2
