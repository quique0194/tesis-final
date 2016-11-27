import pygame
from player import Player
from ball import Ball
from settings import red, blue, black, goals
from utils import get_goal_rect


class Match(object):
    def reset(self):
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
        self.tic = 0

    def __init__(self, red_players=3, blue_players=3, red_strategy=None,
                 blue_strategy=None):
        self.reset()
        self.field = pygame.image.load("soccer_field.png")
        self.red_strategy = red_strategy
        self.blue_strategy = blue_strategy

    def draw_goals(self, screen):
        for goal in goals:
            pygame.draw.rect(screen, black, get_goal_rect(goal))

    def is_ball_in_goal(self):
        for i, goal in enumerate(goals):
            if get_goal_rect(goal).collidepoint(self.ball.pypos):
                return i

    def draw(self, screen):
        screen.blit(self.field, (0, 0))
        for player in self.red_team + self.blue_team:
            player.draw(screen)
        self.ball.draw(screen)
        self.draw_goals(screen)
        pygame.display.flip()

    def run(self):
        if self.red_strategy:
            self.red_strategy(self.red_team, self.blue_team, self.ball,
                              tic=self.tic)
        if self.blue_strategy:
            self.blue_strategy(self.blue_team, self.red_team, self.ball,
                               tic=self.tic)
        self.ball.update()
        if self.is_ball_in_goal() is not None:
            self.reset()
        self.tic += 1
