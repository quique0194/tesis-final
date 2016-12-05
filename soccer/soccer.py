#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Módulos
import time
import sys
import pygame
from pygame.locals import (
    QUIT,
)
from settings import width, height
from match import Match
from strategies import auto_strategy, manual_strategy


def main():
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Soccer")
    match = Match(
        2, 2,
        red_strategy=auto_strategy,
        blue_strategy=auto_strategy,
    )

    while True:
        time.sleep(0.01)
        match.run()
        match.draw(screen, draw_to_img=True)
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()


if __name__ == '__main__':
    pygame.init()
    main()
