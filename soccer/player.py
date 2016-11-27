import pygame
from settings import blue
from utils import pixelof, dist, size2pixels


class Player(object):

    def __init__(self, x, y, team=blue):
        self.pos = [x, y]
        self.team = team
        self.size = 0.025

    def draw(self, screen):
        size = size2pixels(self.size)
        pygame.draw.circle(screen, self.team, pixelof(*self.pos),
                           size / 3, 0)
        pygame.draw.circle(screen, self.team, pixelof(*self.pos), size, 1)

    def move(self, dpos):
        self.pos[0] += dpos[0]
        self.pos[1] += dpos[1]
        error = False
        if self.pos[0] > 1:
            self.pos[0] = 1
            error = True
        elif self.pos[0] < -1:
            self.pos[0] = -1
            error = True
        if self.pos[1] > 1:
            self.pos[1] = 1
            error = True
        elif self.pos[1] < -1:
            self.pos[1] = -1
            error = True
        return error

    def can_move_ball(self, ball):
        return dist(ball.pos, self.pos) < 0.05

    def kick(self, ball, power, angle):
        if self.can_move_ball(ball):
            ball.kick(power, angle)
