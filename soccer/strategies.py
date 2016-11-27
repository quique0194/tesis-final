import numpy as np
import pygame
from pygame.locals import (
    K_LEFT,
    K_RIGHT,
    K_DOWN,
    K_UP,
    K_SPACE,
)
from settings import goals, goal_width, goal_height
from utils import angle_to, dist


def auto_goalkeeper(team, role, opp, ball, side=0, tic=0):
    # role = idx of player in team
    if side == 0:
        delta = 2 * goal_width
    else:
        delta = - 2 * goal_width
    goal_keeper_points = [
        goals[side] + np.array([delta, goal_height]),
        goals[side] + np.array([delta, -goal_height]),
    ]
    dest = goal_keeper_points[auto_goalkeeper.curr_point]
    if dist(team[role].pos, dest) < 0.01:
        auto_goalkeeper.curr_point = (auto_goalkeeper.curr_point + 1) % 2
    team[role].move_to(dest)
    team[role].kick(ball, 0.5, 0)
auto_goalkeeper.curr_point = 0


def auto_attacker(team, role, opp, ball, side=0, tic=0):
    if tic % 50 == 0:
        team[role].move_to(ball.pos)
    else:
        team[role].repeat_last_move()


def auto_strategy(team, opp, ball, side=0, tic=0):
    auto_goalkeeper(team, 0, opp, ball, side, tic)
    if len(team) > 1:
        auto_attacker(team, 1, opp, ball, side, tic)
    if len(team) > 2:
        auto_attacker(team, 2, opp, ball, side, tic)


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
