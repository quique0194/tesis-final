import pygame
from utils import (
    pixelof,
    dist,
    size2pixels,
    normalize_vector,
    vector_to,
    angle_of,
)


class Player(object):

    def __init__(self, x, y, max_speed=0.01):
        self.pos = [x, y]
        self.size = 0.025
        self.kicked = False    # Used to calculate score
        self.max_speed = max_speed
        self.prev_move = None

    def draw(self, screen, color):
        size = size2pixels(self.size)
        pygame.draw.circle(screen, color, pixelof(*self.pos),
                           size / 3, 0)
        pygame.draw.circle(screen, color, pixelof(*self.pos), size, 1)

    def move_to(self, dest, speed=None):
        if speed is None:
            speed = self.max_speed
        speed = min(speed, self.max_speed)
        mv = vector_to(self.pos, dest)
        mv = normalize_vector(mv, speed)
        return self.move(mv)

    def move_dir(self, direc):
        direc = direc.lower()
        ms = self.max_speed
        direc_to_mv = {
            "none": [0, 0],
            "top": [0, -ms],
            "left": [-ms, 0],
            "right": [ms, 0],
            "bottom": [0, ms],
            "topleft": [-ms, -ms],
            "topright": [ms, -ms],
            "bottomleft": [-ms, ms],
            "bottomright": [ms, ms],
        }
        mv = [0, 0]
        if direc in direc_to_mv.keys():
            mv = direc_to_mv[direc]
        self.move(mv)

    def repeat_last_move(self):
        if self.prev_move is not None:
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
        mv = normalize_vector(mv, self.max_speed)
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

    def walk_kick(self, ball, full_power=False):
        """Kick the ball in the direction it is walking."""
        if self.prev_move is None:
            return
        if self.can_move_ball(ball):
            self.kicked = True
            power = 0.15
            if full_power:
                power = 0.5
            ball.kick(power, angle_of(self.prev_move))
