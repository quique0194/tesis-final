import os
import sys
import pygame
from pygame.locals import QUIT
from dqn import DQN
from model import StateParser, World
from player import Player
from ball import Ball
from soccersim.strategies import auto_goalkeeper
from soccersim.settings import width, height
from soccersim.match import Match


class SoccerStateParser(StateParser):

    def __init__(self, *args, **kwargs):
        super(SoccerStateParser, self).__init__(*args, **kwargs)

    def load(self, n):
        return {
            "red_team": [Player(n[0], n[1]), Player(n[2], n[3])],
            "blue_team": [Player(n[4], n[5]), Player(n[6], n[7])],
            "ball": Ball(n[8], n[9]),
            "tic": n[10],
        }

    def dump(self, state):
        ret = []
        for player in state["red_team"] + state["blue_team"]:
            ret += player.pos
        ret += state["ball"].pos
        ret.append(state["tic"])
        return ret

    def state_size(self):
        return 11


class SoccerWorld(World):

    def __init__(self, graphics=False, *args, **kwargs):
        self.graphics = graphics
        if not graphics:
            os.environ["SDL_VIDEODRIVER"] = "dummy"
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Soccer")
        self.match = Match(
            2, 2,
            red_strategy=None,
            blue_strategy=None,
        )
        super(SoccerWorld, self).__init__(*args, **kwargs)

    def exe_action(self, state, action):
        self.match.set_state(state)

        def dqn_player(team, opp, ball, side=0, tic=0):
            auto_goalkeeper(team, 0, opp, ball, side, tic)
            team[1].move_dir(action["move"])
            team[1].walk_kick(ball)

        self.match.blue_strategy = dqn_player
        self.match.run()

        if self.graphics:
            self.match.draw(self.screen, draw_to_img=False, fancy=True)

            # listen to close event
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()

        reward = self.match.last_blue_score
        return self.match.get_state(), reward

    def isterminal(self, state):
        self.match.set_state(state)
        if self.match.any_team_scored:
            return True
        # if last kick was 1000 tics ago
        if self.match.tic - self.match.blue_kicked_at_tic > 1000:
            return True

    def gen_random_state(self):
        self.match = Match(
            2, 2,
            red_strategy=None,
            blue_strategy=None,
        )
        return self.match.get_state()


if __name__ == "__main__":
    actions = [
        {"move": "none", "kick": False},
        {"move": "top", "kick": False},
        {"move": "left", "kick": False},
        {"move": "right", "kick": False},
        {"move": "bottom", "kick": False},
        {"move": "topleft", "kick": False},
        {"move": "topright", "kick": False},
        {"move": "bottomleft", "kick": False},
        {"move": "bottomright", "kick": False},
        {"move": "none", "kick": True},
        {"move": "top", "kick": True},
        {"move": "left", "kick": True},
        {"move": "right", "kick": True},
        {"move": "bottom", "kick": True},
        {"move": "topleft", "kick": True},
        {"move": "topright", "kick": True},
        {"move": "bottomleft", "kick": True},
        {"move": "bottomright", "kick": True},
    ]

    DIM = 13

    rl = DQN("soccerdata/qmlp.pkl",
             SoccerWorld(graphics=True, actions=actions,
                         state_parser=SoccerStateParser()))
    rl.random_prob = 0.75
    rl.buffer_size = 10
    rl.batch_size = 3
    rl.clone_network_steps = 50
    rl.train_info_steps = 1
    rl.show_progress = False

    try:
        rl.train(100)
    finally:
        print "SAVING FILES...",
        rl.save_data("soccerdata/")
        print "DONE"
