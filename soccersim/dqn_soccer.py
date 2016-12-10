import numpy as np
import os
import sys
import pygame
from pygame.locals import K_DOWN, K_UP, K_LEFT, K_RIGHT, QUIT
from dqn import DQN
from model import StateParser, World
# from player import Player
# from ball import Ball
from soccersim.strategies import StrategyBase
from soccersim.settings import width, height
from soccersim.match import Match


class SoccerStateParser(StateParser):

    def __init__(self, *args, **kwargs):
        super(SoccerStateParser, self).__init__(*args, **kwargs)

    def dump(self, state):
        ret = []
        for player in state["red_team"] + state["blue_team"]:
            ret += player.pos
        ret += state["ball"].pos
        return ret

    def state_size(self):
        return 10


class DoNothingStrategy(StrategyBase):

    def run(self, team, opp, ball, side=0, tic=0):
        pass


class DQNStrategy(StrategyBase):

    def set_action(self, dir):
        self.dir = dir

    def run(self, team, opp, ball, side=0, tic=0):
        self.auto_goalkeeper(team, 0, opp, ball, side, tic)
        team[1].move_dir(self.dir)
        team[1].walk_kick(ball)


class SoccerWorld(World):

    def __init__(self, graphics=False, *args, **kwargs):
        self.graphics = graphics
        if not graphics:
            os.environ["SDL_VIDEODRIVER"] = "dummy"
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Soccer")

        self.dqn_strategy = DQNStrategy()
        self.match = Match(
            2, 2,
            red_strategy=DoNothingStrategy(),
            blue_strategy=self.dqn_strategy,
        )
        super(SoccerWorld, self).__init__(*args, **kwargs)

    def exe_action(self, action):
        self.dqn_strategy.set_action(action)
        self.match.run()

        if self.graphics:
            self.match.draw(self.screen, draw_to_img=False, fancy=True)

            # listen to close event
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()

        reward = self.match.last_blue_score
        return self.match.get_state(), reward

    def isterminal(self):
        if self.match.is_finished():
            return True

    def gen_random_state(self):
        self.match = Match(
            2, 2,
            red_strategy=DoNothingStrategy(),
            blue_strategy=self.dqn_strategy,
        )
        return self.match.get_state()


class SoccerDQN(DQN):

    def __init__(self, human_teacher=False, *args, **kwargs):
        super(SoccerDQN, self).__init__(*args, **kwargs)
        self.human_teacher = human_teacher
        self.final_scores = []
        self.match_gols = []

    def choose_action(self, state):
        if self.human_teacher:
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
            try:
                return self.world.actions.index(mv)
            except ValueError:
                return 0
        else:
            return super(DQN, self).choose_action(state)

    def train_episode(self, i):
        super(SoccerDQN, self).train_episode(i)
        self.final_scores.append(self.world.match.blue_score)
        self.match_gols.append(self.world.match.blue_gd())

    def save_data(self, name="soccer_rl"):
        super(SoccerDQN, self).save_data(name)
        fhandle = open(name + "_" + "final_scores.csv", "a")
        np.savetxt(fhandle, self.final_scores, delimiter=",")
        self.final_scores = []
        fhandle = open(name + "_" + "goles.csv", "a")
        np.savetxt(fhandle, self.match_gols, delimiter=",")
        self.match_gols = []


if __name__ == "__main__":
    actions = [
        "none",
        "top",
        "left",
        "right",
        "bottom",
        "topleft",
        "topright",
        "bottomleft",
        "bottomright",
    ]

    DIM = 13

    # TODO, construct world inside rl
    rl = SoccerDQN(
        human_teacher=False,
        network_name="soccerdata/qmlp",
        data_filename="soccerdata/",
        world=SoccerWorld(graphics=True, actions=actions,
                          state_parser=SoccerStateParser()),
        hidden_units=500,
        add_more_experience=False,
        make_net_learn=True,
    )

    rl.random_prob = 0
    rl.min_random_prob = 0
    rl.random_prob_decay = 0.999  # Reach 0.1 random_prob in 2000 episodes

    rl.train_info_steps = 1
    rl.show_progress = False

    rl.buffer_size = 100000
    rl.batch_size = 20
    rl.clone_network_steps = 10000
    rl.save_network_steps = 10000
    rl.backup_network_episodes = 100

    try:
        rl.train(5000)
    finally:
        print "SAVING FILES...",
        rl.save_data("soccerdata/")
        print "DONE"
