import pygame
import math

wScreen = 1200
hScreen = 500

win = pygame.display.set_mode((wScreen,hScreen))

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
        angle = ang
        velx = math.cos(angle) * power
        vely = math.sin(angle) * power
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

run = True
time = 0
power = 0
angle = 0
shoot = False
clock = pygame.time.Clock()
while run:
    clock.tick(200)
    if shoot:
        if grenadeBall.y < 500 - grenadeBall.radius:
            time += 0.05
            po = grenade.ballPath(x, y, power, angle, time)
            grenadeBall.x = po[0]
            grenadeBall.y = po[1]
        else:
            shoot = False
            time = 0
            grenadeBall.y = 494

    line = [(grenadeBall.x, grenadeBall.y), pygame.mouse.get_pos()]
    redrawWindow()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if not shoot:
                x = grenadeBall.x
                y = grenadeBall.y
                pos = pygame.mouse.get_pos()
                shoot = True
                power = math.sqrt((line[1][1]-line[0][1])**2 +(line[1][0]-line[0][1])**2)/8
                angle = findAngle(pos)

pygame.quit()
