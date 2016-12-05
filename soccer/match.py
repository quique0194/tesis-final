import random
import pygame
from pygame import Color
from player import Player
from ball import Ball
from settings import red, blue, black, white, goals
from utils import get_goal_rect
import settings
from PIL import Image


class Match(object):

    def reset(self):
        self.red_team = [
            Player(random.uniform(-1, 0), random.uniform(-1, 1), red),
            Player(random.uniform(-1, 0), random.uniform(-1, 1), red),
            Player(random.uniform(-1, 0), random.uniform(-1, 1), red),
        ]
        self.blue_team = [
            Player(random.uniform(0, 1), random.uniform(-1, 1), blue),
            Player(random.uniform(0, 1), random.uniform(-1, 1), blue),
            Player(random.uniform(0, 1), random.uniform(-1, 1), blue),
        ]
        self.red_team = self.red_team[:self.red_players]
        self.blue_team = self.blue_team[:self.blue_players]
        self.blue_score = 0
        self.red_score = 0
        self.ball = Ball(random.uniform(-1, 0), random.uniform(-1, 1))
        self.tic = 0

    def __init__(self, red_players=3, blue_players=3, red_strategy=None,
                 blue_strategy=None):
        self.red_players = red_players
        self.blue_players = blue_players
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

    def draw(self, screen, draw_to_img=False, fancy=True):
        if fancy:
            screen.blit(self.field, (0, 0))       # soccer field background
        else:
            screen.fill(Color("white"))     # white background
        for player in self.red_team + self.blue_team:
            player.draw(screen)
        font = pygame.font.Font(None, 30)
        if not draw_to_img:
            ren = font.render("Blue score: " + str(self.blue_score),
                              0, black, white)
            screen.blit(ren, (10, 10))
        self.ball.draw(screen)
        self.draw_goals(screen)
        if draw_to_img:
            data = pygame.image.tostring(screen, "RGBA")
            image = Image.fromstring("RGBA", (settings.width, settings.height),
                                     data)
            if random.random() < 0.0001:
                image.save("borrame.jpg")
            return image
        else:
            pygame.display.flip()

    def calculate_blue_score(self):
        if self.tic % 10 == 0:
            self.blue_score -= 1
        for player in self.blue_team:
            if player.kicked:
                player.kicked = False
                self.blue_score += 10
        for player in self.red_team:
            if player.kicked:
                player.kicked = False
                self.blue_score -= 10

    def run(self):
        if self.red_strategy:
            self.red_strategy(self.red_team, self.blue_team, self.ball, side=0,
                              tic=self.tic)
        if self.blue_strategy:
            self.blue_strategy(self.blue_team, self.red_team, self.ball,
                               side=1, tic=self.tic)
        self.ball.update()
        # TODO: calculate_red_score()
        gol_of = self.is_ball_in_goal()
        if gol_of is not None:
            print "GOL!!!!!!!!!!!", gol_of
            self.reset()
        self.calculate_blue_score()
        self.tic += 1
