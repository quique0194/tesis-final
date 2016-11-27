import pygame
import random
from pygame.locals import (
    K_LEFT,
    K_RIGHT,
    K_DOWN,
    K_UP,
    K_SPACE,
)
from settings import goals
from utils import angle_to


def auto_strategy(team, opp, ball, side=0, tic=0):
    for i, player in enumerate(team):
        if tic % 50 == 0:
            mv = [random.uniform(-0.01, 0.01), random.uniform(-0.01, 0.01)]
            auto_strategy.prev_moves[i] = mv
            player.move(mv)
        else:
            player.move(auto_strategy.prev_moves[i])
auto_strategy.prev_moves = [[0, 0]] * 3


def manual_strategy(team, opp, ball, side=0, tic=0):
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
    if keys[K_SPACE]:
        angle = angle_to(team[0].pos, goals[not side])
        team[0].kick(ball, 0.1, angle)
    team[0].move(mv)
