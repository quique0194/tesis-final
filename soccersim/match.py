from PIL import Image
import random
import pygame
from pygame import Color
from player import Player
from ball import Ball
from settings import red, blue, black, white, goals
from utils import get_goal_rect
import settings
from soccersim.utils import dist


class Match(object):

    def get_state(self):
        return {
            "red_team": self.red_team,
            "blue_team": self.blue_team,
            "ball": self.ball,
        }

    def set_state(self, state):
        self.red_team = state["red_team"]
        self.blue_team = state["blue_team"]
        self.ball = state["ball"]

    def reset(self):
        self.red_team = [
            Player(-0.8, 0),
            Player(-0.2, 0),
            Player(random.uniform(-1, 0), random.uniform(-1, 1)),
        ]
        self.blue_team = [
            Player(random.uniform(0, 1), random.uniform(-1, 1)),
            Player(random.uniform(0, 1), random.uniform(-1, 1)),
            Player(random.uniform(0, 1), random.uniform(-1, 1)),
        ]
        # self.ball = Ball(random.uniform(0, 1), random.uniform(-1, 1))
        self.ball = Ball(0, 0)
        while dist(self.blue_team[1].pos, self.ball.pos) > 0.2:
            self.blue_team[1] = Player(random.uniform(0, 1),
                                       random.uniform(-1, 1))
        self.red_team = self.red_team[:self.red_players]
        self.blue_team = self.blue_team[:self.blue_players]

    def new_match(self):
        self.reset()
        self.blue_score = 0
        self.red_score = 0
        self.tic = 0

    def __init__(self, red_players=3, blue_players=3, red_strategy=None,
                 blue_strategy=None):
        self.red_players = red_players
        self.blue_players = blue_players
        self.new_match()
        self.field = pygame.image.load("soccersim/soccer_field.png")
        self.red_strategy = red_strategy
        self.blue_strategy = blue_strategy
        self.last_blue_score = 0    # blue point earned on the last tic
        self.team_scored = None
        self.blue_kicked_at_tic = 0

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
        for player in self.red_team:
            player.draw(screen, red)
        for player in self.blue_team:
            player.draw(screen, blue)
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
        self.last_blue_score = 0
        if self.tic % 10 == 0:
            self.last_blue_score = -1
        for player in self.blue_team:
            if player.kicked:
                self.blue_kicked_at_tic = self.tic
                player.kicked = False
                self.last_blue_score = 10
        for player in self.red_team:
            if player.kicked:
                player.kicked = False
                self.last_blue_score = -10
        if self.team_scored == 1:
            self.last_blue_score = 1000
        elif self.team_scored == 0:
            self.last_blue_score = -1000
        self.blue_score = self.blue_score + self.last_blue_score

    def run(self):
        if self.tic == 5001:
            self.new_match()
        if self.team_scored is not None:
            self.team_scored = None
            self.reset()
        if self.red_strategy:
            self.red_strategy.run(self.red_team, self.blue_team, self.ball,
                                  side=0, tic=self.tic)
        if self.blue_strategy:
            self.blue_strategy.run(self.blue_team, self.red_team, self.ball,
                                   side=1, tic=self.tic)
        self.ball.update()
        # TODO: calculate_red_score()
        gol_of = self.is_ball_in_goal()
        if gol_of is not None:
            self.team_scored = not gol_of
            print "GOL!!!!!!!!!!!", not gol_of
        self.calculate_blue_score()
        self.tic += 1

    def is_finished(self):
        return self.tic == 5000
