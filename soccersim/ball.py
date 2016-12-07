import numpy as np
import pygame
from settings import black
from utils import pixelof, dist


class Ball(object):

    def __init__(self, x, y):
        self.pos = [x, y]
        self.traveled = 0
        self.speed = 0.015
        self.power = 0
        self.angle = 0

    @property
    def pypos(self):
        return pixelof(*self.pos)

    def draw(self, screen):
        pygame.draw.circle(screen, black, pixelof(*self.pos), 2, 0)
        pygame.draw.circle(screen, black, pixelof(*self.pos), 5, 1)

    def valid_move(self, mv):
        pos = list(self.pos)
        pos[0] += mv[0]
        pos[1] += mv[1]
        error = False
        if pos[0] > 1:
            pos[0] = 1
            error = True
        elif pos[0] < -1:
            pos[0] = -1
            error = True
        if pos[1] > 1:
            pos[1] = 1
            error = True
        elif pos[1] < -1:
            pos[1] = -1
            error = True
        return not error

    def move(self, mv):
        if not self.valid_move(mv):
            return False
        self.pos[0] += mv[0]
        self.pos[1] += mv[1]
        return True

    def update(self):
        # ball always move 0.01 units per tic
        if self.traveled < self.power:
            rad = np.radians(self.angle)
            mv = [self.speed * np.cos(rad), self.speed * np.sin(rad)]
            self.move(mv)
            self.traveled += dist([0, 0], mv)

    def kick(self, power, angle):
        # angle in degrees
        # check self.update()
        self.power = power
        self.angle = angle
        self.traveled = 0
