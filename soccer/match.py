import pygame
from player import Player
from ball import Ball
from settings import red, blue


class Match(object):

    def __init__(self, red_players=3, blue_players=3, red_strategy=None,
                 blue_strategy=None):
        self.red_team = [
            Player(-0.9, 0, red),
            Player(-0.5, 0, red),
            Player(-0.1, 0, red),
        ]
        self.blue_team = [
            Player(0.1, 0.1, blue),
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
            self.red_strategy(self.red_team, self.blue_team, self.ball,
                              tic=self.tic)
        if self.blue_strategy:
            self.blue_strategy(self.blue_team, self.red_team, self.ball,
                               tic=self.tic)
        self.ball.update()
        self.tic += 1
