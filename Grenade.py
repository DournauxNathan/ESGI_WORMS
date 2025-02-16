import pygame
import math
import scipy
import matplotlib
import numpy

wScreen = 1200
hScreen = 500

win = pygame.display.set_mode((wScreen, hScreen))


class grenade(object):
    def __init__(self,x,y,radius,color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.velx = 0
        self.vely = 0
        self.restitution = 0.6  # Facteur de restitution pour le rebond

    def draw(self, win):
        pygame.draw.circle(win, (0,0,0), (self.x,self.y), self.radius)
        pygame.draw.circle(win, self.color, (self.x,self.y), self.radius-1)


    @staticmethod
    def ballPath(startx, starty, velx, vely, time, mass=1, r=0.1):
        v = numpy.sqrt(velx ** 2 + vely ** 2)
        Fd = grenade.air_resistance(v, r)
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

    def redrawWindow():
        win.fill((64,64,64))
        grenadeBall.draw(win)
        pygame.draw.line(win, (0,0,0),line[0], line[1])
        pygame.display.update()

    def findAngle(pos, startx, starty):
        try:
            angle = math.atan2(starty - pos[1], pos[0] - startx)
        except:
            angle = math.pi / 2
        return angle

grenadeBall = grenade(300, 494, 5, (255, 255, 255))

run = True
time = 0
power = 0
angle = 0
shoot = False
clock = pygame.time.Clock()
while run:
    clock.tick(200)
    if shoot:
        if shoot:
            grenadeBall.x, grenadeBall.y, velx, vely = grenade.ballPath(grenadeBall.x, grenadeBall.y, velx, vely, 0.05)
            if vely == 0 and velx == 0:
                shoot = False

    line = [(grenadeBall.x, grenadeBall.y), pygame.mouse.get_pos()]
    grenade.redrawWindow()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if not shoot:
                pos = pygame.mouse.get_pos()
                shoot = True
                power = math.sqrt((line[1][1] - line[0][1]) ** 2 + (line[1][0] - line[0][0]) ** 2) / 8
                angle = grenade.findAngle(pos, grenadeBall.x, grenadeBall.y)
                velx = math.cos(angle) * power
                vely = math.sin(angle) * power

pygame.quit()