import numpy as np
import pygame
from settings import black
from utils import pixelof, dist


class Ball(object):

    def __init__(self, x, y):
        self.pos = [x, y]
        self.traveled = 0
        self.power = 0
        self.angle = 0

    def draw(self, screen):
        pygame.draw.circle(screen, black, pixelof(*self.pos), 2, 0)
        pygame.draw.circle(screen, black, pixelof(*self.pos), 5, 1)

    def move(self, dpos):
        self.pos[0] += dpos[0]
        self.pos[1] += dpos[1]

    def update(self):
        # ball always move 0.01 units per tic
        if self.traveled < self.power:
            rad = np.radians(self.angle)
            mv = [0.01 * np.sin(rad), 0.01 * np.cos(rad)]
            self.move(mv)
            self.traveled += dist([0, 0], mv)

    def kick(self, power, angle):
        # angle in degrees
        self.power = power
        self.angle = angle
        self.traveled = 0
