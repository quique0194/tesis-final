#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Módulos
import time
import sys
import pygame
import random
import math
from pygame.locals import (
    QUIT,
    K_LEFT,
    K_RIGHT,
    K_DOWN,
    K_UP,
)


width = 544
height = 360


def pixelof(x, y):
    return int((x + 1) * width / 2.0), int((y + 1) * height / 2.0)


white = 255, 255, 255
black = 0, 0, 0
blue = 0, 0, 127
yellow = 200, 200, 0
green = 3, 153, 13
red = 200, 0, 0


class Ball(object):

    def __init__(self, x, y):
        self.pos = [x, y]

    def draw(self, screen):
        pygame.draw.circle(screen, black, pixelof(*self.pos), 2, 0)
        pygame.draw.circle(screen, black, pixelof(*self.pos), 5, 1)
        self.power = 0          # how much distance it must travel
        self.angle = 0
        self.traveled = 0       # distance already traveled

    def move(self, dpos):
        self.pos[0] += dpos[0]
        self.pos[1] += dpos[1]

    def update(self):
        pass

    def kick(self, power, angle):
        self.power = power
        self.angle = angle
        self.traveled = 0


class Player(object):

    def __init__(self, x, y, team=blue):
        self.pos = [x, y]
        self.team = team
        self.size = 10

    def draw(self, screen):
        pygame.draw.circle(screen, self.team, pixelof(*self.pos),
                           self.size / 3, 0)
        pygame.draw.circle(screen, self.team, pixelof(*self.pos), self.size, 1)

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
        dist = math.hypot(self.pos[0] - ball.pos[0], self.pos[1] - ball.pos[1])
        return dist < self.size

    def kick_ball(self, ball):
        pass


class Match(object):

    def __init__(self, red_players=3, blue_players=3, red_strategy=None,
                 blue_strategy=None):
        self.red_team = [
            Player(-0.9, 0, red),
            Player(-0.5, 0, red),
            Player(-0.1, 0, red),
        ]
        self.blue_team = [
            Player(0.1, 0, blue),
            Player(0.5, 0, blue),
            Player(0.9, 0, blue),
        ]
        self.ball = Ball(0, 0)
        self.field = pygame.image.load("soccer_field.png")
        self.tic = 0
        self.red_strategy = red_strategy
        self.blue_strategy = blue_strategy
        self.kick = [0, 0]      # power, angle

    def draw(self, screen):
        screen.blit(self.field, (0, 0))
        for player in self.red_team + self.blue_team:
            player.draw(screen)
        self.ball.draw(screen)
        pygame.display.flip()

    def run(self):
        if self.red_strategy:
            self.red_strategy(self.red_team, self.tic)
        if self.blue_strategy:
            self.blue_strategy(self.blue_team, self.tic)
        self.tic += 1


def auto_strategy(players, tic):
    for i, player in enumerate(players):
        if tic % 50 == 0:
            mv = [random.uniform(-0.01, 0.01), random.uniform(-0.01, 0.01)]
            auto_strategy.prev_moves[i] = mv
            player.move(mv)
        else:
            player.move(auto_strategy.prev_moves[i])
auto_strategy.prev_moves = [[0, 0]] * 3


def manual_strategy(players, tic):
    keys = pygame.key.get_pressed()
    mv = [0, 0]
    player1_speed = 0.01
    if keys[K_LEFT]:
        mv[0] -= player1_speed
    if keys[K_RIGHT]:
        mv[0] += player1_speed
    if keys[K_DOWN]:
        mv[1] += player1_speed
    if keys[K_UP]:
        mv[1] -= player1_speed
    players[0].move(mv)


def main():
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Soccer")
    match = Match(
        red_strategy=auto_strategy,
        blue_strategy=manual_strategy,
    )

    while True:
        time.sleep(0.01)
        match.run()
        match.draw(screen)
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()


if __name__ == '__main__':
    pygame.init()
    main()
