import pygame
import math
import scipy
import matplotlib
import numpy

wScreen = 1200
hScreen = 500

win = pygame.display.set_mode((wScreen,hScreen))

class roquette(object):
    def __init__(self,x,y,radius,color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
    def draw(self, win):
        pygame.draw.circle(win, (0,0,0), (self.x,self.y), self.radius)
        pygame.draw.circle(win, self.color, (self.x,self.y), self.radius-1)

    @staticmethod
    def air_resistance(v, r, Cd=0.4, rho=1.225):
        S = numpy.pi * r**2 /2  #surface d'un demi cercle
        return 0.5 * Cd * rho * S * v**2

    @staticmethod
    def ballPath(startx, starty, power, ang, time, mass = 1, r = 0.1):
        velx = numpy.cos(ang) * power
        vely = math.sin(ang) * power
        v = numpy.sqrt(velx ** 2 + vely ** 2)
        Fd = roquette.air_resistance(v, r)
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

    def redrawWindow():
        win.fill((64, 64, 64))
        Roquette.draw(win)
        pygame.draw.line(win, (0, 0, 0), line[0], line[1])
        pygame.display.update()

    def findAngle(pos):
        sX = Roquette.x
        sY = Roquette.y
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

#_______________________________________________________________________________________________________________________________________________________
class grenade(object):
    def __init__(self,x,y,radius,color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
    def draw(self, win):
        pygame.draw.circle(win, (0,0,0), (self.x,self.y), self.radius)
        pygame.draw.circle(win, self.color, (self.x,self.y), self.radius-1)

    @staticmethod
    def ballPath(startx, starty, power, ang, time):
        velx = (math.cos(ang) * power)
        vely = math.sin(ang) * power
        distX = velx * time
        distY = (vely * time) + ((-9.8 * (time * time)) / 2)
        newx = round(distX + startx)
        newy = round(starty - distY)
        return (newx, newy)
    def redrawWindow():
        win.fill((64,64,64))
        grenadeBall.draw(win)
        pygame.draw.line(win, (0,0,0),line[0], line[1])
        pygame.display.update()

    def findAngle(pos):
        sX = grenadeBall.x
        sY = grenadeBall.y
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

grenadeBall = grenade(300, 494, 5, (255, 255, 255))
Roquette = roquette(300, 494, 5, (255, 255, 255))


def air_resistance(v, r, Cd=0.47, rho=1.225):
    """
    Calcule la force de résistance de l'air sur une sphère en mouvement.

    :param v: Vitesse de l'objet (m/s)
    :param r: Rayon de l'objet (m)
    :param Cd: Coefficient de traînée (par défaut 0.47 pour une sphère)
    :param rho: Densité de l'air (kg/m^3, par défaut 1.225 au niveau de la mer)
    :return: Force de traînée (N)
    """
    A = numpy.pi * r ** 2  # Aire frontale de la sphère
    return 0.5 * Cd * rho * A * v ** 2

run = True
time = 0
power = 0
angle = 0


shoot = False
clock = pygame.time.Clock()
while run:
    clock.tick(200)
    if shoot:
        if Roquette.y < 500 - Roquette.radius:
            time += 0.05
            po = Roquette.ballPath(x, y, power, angle, time)
            Roquette.x = po[0]
            Roquette.y = po[1]
        else:
            shoot = False
            time = 0
            Roquette.y = 494

    line = [(Roquette.x, Roquette.y), pygame.mouse.get_pos()]
    roquette.redrawWindow()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if not shoot:
                x = Roquette.x
                y = Roquette.y
                pos = pygame.mouse.get_pos()
                shoot = True
                power = math.sqrt((line[1][1]-line[0][1])**2 +(line[1][0]-line[0][1])**2)
                angle = roquette.findAngle(pos)

pygame.quit()
