import random
import numpy as np
import pygame
from pygame.locals import (
    K_LEFT,
    K_RIGHT,
    K_DOWN,
    K_UP,
    # K_SPACE,
)
from settings import goals, goal_width, goal_height
from utils import (
    angle_diff,
    dist,
    angle_to,
    normalize_vector,
    tonp,
    vector_to
)


class StrategyBase(object):
    def __init__(self):
        self.lagged_ball_pos = None
        self.next_lagged_bal_pos = None
        self.ball_lag = 0

        self.attacker1_last_move = None

    def auto_goalkeeper(self, team, role, opp, ball, side=0, tic=0):
        # role = idx of player in team
        if side == 0:
            delta = 2 * goal_width
        else:
            delta = - 2 * goal_width
        goal_keeper_points = [
            goals[side] + np.array([delta, goal_height]),
            goals[side] + np.array([delta, -goal_height]),
        ]
        if not hasattr(self, 'curr_point'):
            self.curr_point = 0
        dest = goal_keeper_points[self.curr_point]
        if dist(team[role].pos, dest) < 0.01:
            self.curr_point = (self.curr_point + 1) % 2
        team[role].move_to(dest)
        if side == 0:
            team[role].kick(ball, 0.5, 0)
        else:
            team[role].kick(ball, 0.5, 180)

    def auto_goalkeeper2(self, team, role, opp, ball, side=0, tic=0):
        if side == 0:
            delta = 2 * goal_width
        else:
            delta = - 2 * goal_width
        if self.ball_lag % 50 == 0:
            self.ball_lag = 0
            self.lagged_ball_pos = self.next_lagged_bal_pos
            self.next_lagged_bal_pos = list(ball.pos)
        self.ball_lag += 1
        if self.lagged_ball_pos:
            dy = self.lagged_ball_pos[1]
        else:
            dy = 0
        dest = goals[side] + np.array([delta, dy])
        team[role].move_to(dest)
        team[role].kick(ball, 0.5, 0)

    def auto_attacker(self, team, role, opp, ball, side=0, tic=0):
        # Go to ball
        if tic % 50 == 0:
            team[role].move_to(ball.pos)
        else:
            team[role].repeat_last_move()
        noise = random.uniform(-20, 20)

        # Kick to goal or to front
        if team[role].pos[0] < 0.5:
            target = [team[role].pos[0] + 0.1,
                      team[role].pos[1] + random.uniform(-0.3, 0.3)]
        else:
            target = goals[not side]
        team[role].kick(ball, 0.15,
                        angle_to(team[role].pos, target) + noise)

    def auto_attacker3(self, team, role, opp, ball, side=0, tic=0):
        team[role].move_to(ball.pos)

    def auto_attacker2(self, team, role, opp, ball, side=0, tic=0):
        """Strategy for an attacker working with DQN."""
        angle_to_ball = angle_to(team[role].pos, ball.pos)
        angle_to_goal = angle_to(team[role].pos, goals[not side])
        angle_ball_to_goal = angle_to(team[role].pos, goals[not side])
        dist_ball_to_goal = dist(ball.pos, goals[not side])
        dist_to_goal = dist(team[role].pos, goals[not side])
        dist_to_ball = dist(team[role].pos, ball.pos)

        print "angle_to_ball", angle_to_ball
        print "angle_to_goal", angle_to_goal
        print "angle_ball_to_goal", angle_ball_to_goal
        print "dist_ball_to_goal", dist_ball_to_goal
        print "dist_to_goal", dist_to_goal
        print "dist_to_ball", dist_to_ball

        # Decision tree
        target = None
        if abs(angle_diff(angle_to_goal, angle_ball_to_goal)) < 1 and \
                dist_ball_to_goal < dist_to_goal:
            # run to score!
            target = ball.pos
            print "GO KICK"
        else:
            if team[role].pos[0] < ball.pos[0]:
                # go behind ball, aligned with goal
                vec = vector_to(goals[not side], ball.pos)
                vec = normalize_vector(vec, 0.7)
                target = tonp(ball.pos) + vec
                print "PREPARE TO KICK"
            else:
                # go behind goal
                target = list(ball.pos)
                if angle_to_ball > 0:
                    target[1] -= 0.5
                else:
                    target[0] += 0.5
                target[0] += 0.1
                print "GO BEHIND BALL"

        print team[role].pos, ball.pos, target
        team[role].move_to(target)

    def run(self, team, opp, ball, side=0, tic=0):
        self.auto_goalkeeper2(team, 0, opp, ball, side, tic)
        if len(team) > 1:
            self.auto_attacker(team, 1, opp, ball, side, tic)
        if len(team) > 2:
            self.auto_attacker(team, 2, opp, ball, side, tic)

    def manual_player(self, team, role, opp, ball, side=0, tic=0):
        keys = pygame.key.get_pressed()
        mv = ""
        if keys[K_DOWN]:
            mv += "bottom"
        if keys[K_UP]:
            mv += "top"
        if keys[K_LEFT]:
            mv += "left"
        if keys[K_RIGHT]:
            mv += "right"
        team[1].move_dir(mv)
        # To activate long kick:
        # if keys[K_SPACE]:
        #     team[1].walk_kick(ball, full_power=True)
        # else:
        #     team[1].walk_kick(ball)
        # To desactivate long kick:
        team[1].walk_kick(ball)


class ManualStrategy(StrategyBase):

    def run(self, team, opp, ball, side=0, tic=0):
        self.auto_goalkeeper(team, 0, opp, ball, side, tic)
        if len(team) > 1:
            self.manual_player(team, 1, opp, ball, side, tic)
