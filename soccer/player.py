import pygame
from settings import blue
from utils import pixelof, dist, size2pixels, normalize_vector, vector_to


class Player(object):

    def __init__(self, x, y, team=blue, max_speed=0.01):
        self.pos = [x, y]
        self.team = team
        self.size = 0.025
        self.kicked = False    # Used to calculate score
        self.max_speed = max_speed

    def draw(self, screen):
        size = size2pixels(self.size)
        pygame.draw.circle(screen, self.team, pixelof(*self.pos),
                           size / 3, 0)
        pygame.draw.circle(screen, self.team, pixelof(*self.pos), size, 1)

    def move_to(self, dest, speed=0.005):
        speed = min(speed, self.max_speed)
        mv = vector_to(self.pos, dest)
        mv = normalize_vector(mv, speed)
        return self.move(mv)

    def repeat_last_move(self):
        if hasattr(self, 'prev_move') and self.prev_move is not None:
            return self.move(self.prev_move)
        else:
            return self.move([0, 0])

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
        self.prev_move = mv
        self.pos[0] += mv[0]
        self.pos[1] += mv[1]
        return True

    def can_move_ball(self, ball):
        return dist(ball.pos, self.pos) < 0.05

    def kick(self, ball, power, angle):
        if self.can_move_ball(ball):
            self.kicked = True
            ball.kick(power, angle)
